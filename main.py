from data import *
from maze_funcion import *

window = pygame.display.set_mode((setting_win["WIDTH"], setting_win["HEIGHT"]))
pygame.display.set_caption("Лабіринт")

def run():
    
    hero = Hero(50,50, setting_hero["WIDTH"], setting_hero["HEIGHT"], image= hero_list)
    bot1 = Bot(210, 100, 50, 50, image= bot1_list, orientation= "vertical")
    clock = pygame.time.Clock()

    game = True
    while game:
        window.fill((191, 230, 221))

        #малювання сітки, потрібно було для зручної побудови стін, зараз не потрібно, але залиште в коді
        #x,y = 20, 20
        #for i in range(50):
        #    pygame.draw.line(window, (255,255,255), (0, y), (1000, y))
        #    pygame.draw.line(window, (255,255,255), (x, 0), (x, 700))
        #    x += 20
        #    y += 20
        
        #WALL
        #запускаємо цикл для проходу по списку стін, і малюємо кожну стіну
        for wall in wall_list:
            pygame.draw.rect(window, (255,255,255), wall)

        #HERO
        hero.move(window)       #запускаємо функцію руху гравця

        bot1.move(window)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = True
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = True
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = True
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = False
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = False
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = False
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = False

        clock.tick(60)
        pygame.display.flip()

run()