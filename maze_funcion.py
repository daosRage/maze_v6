import pygame
from data import *

pygame.init()

#ствирили батьківський клас спрайт
class Sprite(pygame.Rect):
    def __init__(self, x, y, width, height, color=(120,120,120), image= None, speed= 5):
        super().__init__(x, y, width, height)
        self.COLOR = color
        self.IMAGE_LIST = image         #список картинок
        #фото яке будемо або демонструвати на екран або змінювати(розвертати в напрямку руху). 
        # Спочатку призначаємо малюнок, в якому персонаж НЕ РУХАЄТЬСЯ
        self.IMAGE = self.IMAGE_LIST[1] 
        self.IMAGE_COUNT = 0            #лічильник для зміни зображень
        self.IMAGE_NOW = self.IMAGE     #зображення, яке буде демонструватись на екрані
        self.SPEED = speed
    
    def move_image(self):
        #функція для зміни фотографій(створення анімації)
        self.IMAGE_COUNT += 1
        if self.IMAGE_COUNT == len(self.IMAGE_LIST) * 10 - 1:
            self.IMAGE_COUNT = 0
        if self.IMAGE_COUNT % 10 == 0:
            self.IMAGE = self.IMAGE_LIST[self.IMAGE_COUNT // 10]

class Hero(Sprite):
    def __init__(self, x, y, width, height, color=(120,120,120), image= None, speed= 5):
        super().__init__(x, y, width, height, color, image, speed)
        #словник для визначення направлення руху
        self.MOVE = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
        self.DIRECTION = False          #властивість, яка визначає в яку сторону потрібно "дивитись" герою при русі вправо/вліво

    def move(self, window):
        #функція руху
        if self.MOVE["UP"] and self.y > 0:
            self.y -= self.SPEED
            if self.collidelist(wall_list) != -1:
                self.y += self.SPEED
        elif self.MOVE["DOWN"] and self.y < setting_win["HEIGHT"] - self.height:
            self.y += self.SPEED
            if self.collidelist(wall_list) != -1:
                self.y -= self.SPEED
        if self.MOVE["LEFT"] and self.x > 0:
            self.x -= self.SPEED
            if self.collidelist(wall_list) != -1:
                self.x += self.SPEED
            self.DIRECTION = False      #потрібно дивись вліво
        elif self.MOVE["RIGHT"] and self.x < setting_win["WIDTH"] - self.width:
            self.x += self.SPEED
            if self.collidelist(wall_list) != -1:
                self.x -= self.SPEED
            self.DIRECTION = True       #потрібно дивитись вправо

        #якщо персонаж рухується, то потрібно змінювати картинки, інакше ставимо картинку героя, де він стоїть на місці
        if self.MOVE["UP"] or self.MOVE["DOWN"] or self.MOVE['LEFT'] or self.MOVE["RIGHT"]:
            self.move_image()
        else:
            self.IMAGE = self.IMAGE_LIST[1]
        #якщо властивість визначення сторони повороту - тру, то ми маємо ровернути картинку вправо
        #інакше просто перепризначаємо картинку
        if self.DIRECTION:
            self.IMAGE_NOW = pygame.transform.flip(self.IMAGE, True, False)
        else:
            self.IMAGE_NOW = self.IMAGE
        #демонструємо картинку на екран
        window.blit(self.IMAGE_NOW, (self.x, self.y))

class Bot(Sprite):
    def __init__(self, x, y, width, height, color=(120,120,120), image= None, speed= 5, orientation= None):
        super().__init__(x, y, width, height, color, image, speed)
        self.ORIENTATION = orientation
    
    def move(self, window):
        if self.ORIENTATION.lower() == "horizontal":
            self.x += self.SPEED
            if self.collidelist(wall_list) != -1 or self.x <= 0 or self.x + self.width >= setting_win["WIDTH"]:
                self.SPEED *= -1
        elif self.ORIENTATION.lower() == "vertical":
            self.y += self.SPEED
            if self.collidelist(wall_list) != -1 or self.y <= 0 or self.y + self.height >= setting_win["HEIGHT"]:
                self.SPEED *= -1
        self.move_image()
        window.blit(self.IMAGE, (self.x, self.y))


def create_wall(key):
    #функція для створення стін
    x, y = 0, 0             #змінні для визначення координат побудови стін
    index_x, index_y = 0, 0 #змінні для роботи зі списком та строками і визначення індексів
    width = 20              #ширина стіни

    for string in maps[key]:        #проходимо по списку строк
        for elem in string:         #проходимо по елементам строки
            if elem == "1":         #якщо елемент строки дорівнює 1, то це означає що з цього місця у вікні має будуватись вертикальна стіна
            #проходимо в циклі по списку чисел, від індекса строки(index_y) де була знайдена 1, до довжини списка строк(len(maps[key])), 
            #зберігаючи індекс елемента в самій строці(index_x), для того, щоб рухатись вертикально вниз і знайти 2, яка означає завершення стіни
                for index in range(index_y, len(maps[key])):    
                    if maps[key][index][index_x] == "2":#якщо елемент строки в списку строк дорівнює 2, то в цьому місці має закінчитись стіна
                        #додаємо стіну в список строк(стіною є звичайний прямокутник - Rect об'єкт)
                        wall_list.append(pygame.Rect(x, y, width, (index - index_y) * width + width))
                        break   #як тільки нашли 2, то виходимо з циклу
            if elem == "3":         #якщо елемент строки дорівнює 3, то це означає що з цього місця у вікні має будуватись горизонтальна стіна
    #проходимо в циклі по списку чисел, від індекса елемента в строці(index_x), де була знайдена 3, до довжини самої строки(len(maps[key][index_y]))
    #зберігаючи індекс строки(index_y), для того, щоб рухатись горизонатльно вправо і знайти 2, яка означає завершення стіни
                for index in range(index_x, len(maps[key][index_y])):
                    if maps[key][index_y][index] == "2":#якщо елемент строки дорівнює 2, то в цьому місці має закінчитись стіна
                        #додаємо стіну в список строк(стіною є звичайний прямокутник - Rect об'єкт)
                        wall_list.append(pygame.Rect(x, y, (index - index_x) * width + width, width))
                        break   #як тільки нашли 2, то виходимо з циклу
            x += width  #при проході по елементам строки, змінюємо х на ширину стіни
            index_x += 1#при проході по елементам строки, змінюємо index_x на 1
        x = 0           #при переході на нову строку, оновлюємо х на 0
        index_x = 0     #при переході на нову строку, оновлюємо index_x на 0
        y += width      #при переході на нову строку, змінюємо у на ширину стіни
        index_y += 1    #при переході на нову строку, змінюємо index_y на 1

create_wall("MAP1")
