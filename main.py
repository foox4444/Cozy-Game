import pygame, sys

pygame.init()
pygame.display.set_caption('Cozy Game')

#Variables
screen = pygame.display.set_mode((1200, 720))
font = pygame.font.Font(None, 20)
clock = pygame.time.Clock()
total = 0
profit = 10
click = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    global click
    while True:
        
        screen.fill("midnightblue")
        draw_text('Main Menu', font, (255, 255, 255), screen, 20, 20)
        
        mx, my = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(50, 100, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.button == 1:
                        if button_1.collidepoint(event.pos):
                            game()

        pygame.display.update()
        clock.tick(60)

def game():
    global click
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.fill("yellow")
        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        
        mx, my = pygame.mouse.get_pos()
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_2.collidepoint((mx, my)):
            if click:
                shop_menu()
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.button == 1:
                        if button_2.collidepoint(event.pos):
                            shop_menu()

        pygame.display.update()
        clock.tick(60)

def shop_menu():
    global click
    click = False
    running = True
    while running:
        screen.fill("teal")
        draw_text('Shop', font, (255, 255, 255), screen, 20, 20)
        mx, my = pygame.mouse.get_pos()
        
        buy_button = pygame.Rect(50, 100, 200, 50)
        back_button = pygame.Rect(50, 170, 200, 50)
        
        pygame.draw.rect(screen, (0, 205, 0), buy_button)
        pygame.draw.rect(screen, (205, 0, 0), back_button)
        
        draw_text('Buy BETTER Machine', font, (255, 255, 255), screen, 60, 115)
        draw_text('Back', font, (255, 255, 255), screen, 60, 185)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buy_button.collidepoint(event.pos):
                        print("Purchased!")
                    if back_button.collidepoint(event.pos):
                        return

        pygame.display.update()
        clock.tick(60)

main_menu()