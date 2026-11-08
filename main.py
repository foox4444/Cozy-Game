import pygame
from sys import exit
import time, random, os, sys

pygame.init()
pygame.display.set_caption('Cozy Game')

def resource_path(relative_path):
    try:
        base_path = sys.MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

#Variables
screen = pygame.display.set_mode((1000, 720))
main_font = pygame.font.Font("ArbaneKnitted.ttf", 150)
font = pygame.font.SysFont('sans', 30)
button_font = pygame.font.Font("ArbaneKnitted.ttf", 75)
clock = pygame.time.Clock()
total = 0
profit = 10
click = False

# Images

#Background
main_menu_img = pygame.image.load("images/main_menu.jpg").convert_alpha()
main_bg = pygame.transform.scale(main_menu_img, (1000, 750))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    global click
    while True:
        
        screen.blit(main_bg, (0, 0))
        draw_text('Main Menu', main_font, (255, 219, 187), screen, 200, 50)
        
        button_1 = pygame.Rect(400, 300, 200, 90)
        button_3 = pygame.Rect(400, 500, 200, 90)
        
        mx, my = pygame.mouse.get_pos()
        b1_color = (180, 90, 0) if button_1.collidepoint((mx, my)) else (150, 75, 0)
        b3_color = (180, 90, 0) if button_3.collidepoint((mx, my)) else (150, 75, 0)
        
        pygame.draw.rect(screen, b1_color, button_1, border_radius=5)
        pygame.draw.rect(screen, b3_color, button_3, border_radius=5)
        
        draw_text('Play', button_font, (255, 219, 187), screen, 420, 310)
        draw_text('Quit', button_font, (255, 219, 187), screen, 420, 510)
        
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
                    if button_1.collidepoint(event.pos):
                        game()
                    if button_3.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(60)

def game():
    global click, total
    running = True
    
    MENU_WIDTH = 300
    menu_x = -MENU_WIDTH
    menu_target_x = -MENU_WIDTH
    slide_speed = 20
    shop_open = False
    
    coffee_tier = 0
    croissant_tier = 1
    coffee_upgrade_cost = 50
    croissant_upgrade_cost = 30
    
    error_message = ""
    error_timer = 0
    
    coffee_station = pygame.Rect(100, 250, 350, 150)
    pastry_station = pygame.Rect(100, 450, 350, 150)
    
    while running:
        mx, my = pygame.mouse.get_pos()
        
        screen.fill((245, 222, 179))
        draw_text(f'Coins: {total}', font, (0, 0, 0), screen, 40, 40)
        draw_text('Click stations to sell goods!', font, (120, 100, 80), screen, 40, 90)
        
        shop_toggle_bin = pygame.Rect(750, 40, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), shop_toggle_bin)
        draw_text('Open Shop', font, (255, 255, 255), screen, 60, 210)
        
        #Coffee and Croissant
        croissant_payout = croissant_tier * 5
        coffee_payout = coffee_tier * 10
        
        
        if coffee_tier == 0:
            coffee_color = (120, 60, 30)
            coffee_text = "Coffee Machine (Locked)"
            coffee_subtext = "Unlock in Shop"
        else:
            coffee_color = (120, 60, 30)
            coffee_text = f"Brew Coffee (Tier {coffee_tier})"
            coffee_subtext = f"Earns +${coffee_payout} per click"
        
        pygame.draw.rect(screen, coffee_color, coffee_station, border_radius=10)
        draw_text(coffee_text, font, (255, 255, 255), screen, coffee_station.x + 20, coffee_station.y + 40)
        draw_text(coffee_subtext, font, (230, 230, 230), screen, coffee_station.x + 20, coffee_station.y + 90)
        
        pygame.draw.rect(screen, (210, 105, 30), pastry_station, border_radius=10)
        draw_text(f"Bake Croissant (Tier {croissant_tier})", font, (255, 255, 255,), screen, pastry_station.x + 20, pastry_station.y + 40)
        draw_text(f"Earns +${croissant_payout} per click", font, (230, 230, 230), screen, pastry_station.x + 20, pastry_station.y + 90)
        
        if menu_x < menu_target_x:
            menu_x = min(menu_target_x, menu_x + slide_speed)
        elif menu_x > menu_target_x:
            menu_x = max(menu_target_x, menu_x - slide_speed)
        
        if menu_x > -MENU_WIDTH:
            shop_bg_rect = pygame.Rect(menu_x, 0, MENU_WIDTH, 720)
            pygame.draw.rect(screen, (0, 128, 128), shop_bg_rect)
            draw_text('Upgrade Shop', font, (255, 255, 255), screen, menu_x + 20, 30)
        
            croissant_label = f"Croissant T.{croissant_tier+1} (${croissant_upgrade_cost})"
            coffee_label = f"Unlock Coffee (${coffee_upgrade_cost})" if coffee_tier == 0 else f"Coffee T.{coffee_tier+1} (${coffee_upgrade_cost})"
        
            buy_croissant_btn = pygame.Rect(menu_x + 20, 120, 260, 60)
            buy_coffee_btn = pygame.Rect(menu_x + 20, 210, 260, 60)
            back_button = pygame.Rect(menu_x + 20, 320, 260, 50)
            
            pygame.draw.rect(screen, (0, 180, 0), buy_croissant_btn, border_radius=5)
            pygame.draw.rect(screen, (0, 180, 0), buy_coffee_btn, border_radius=5)
            pygame.draw.rect(screen, (205, 0, 0), back_button, border_radius=5)

            draw_text(croissant_label, font, (255, 255, 255), screen, menu_x + 30, 135)
            draw_text(coffee_label, font, (255, 255, 255), screen, menu_x + 30, 225)
            draw_text('Close Shop', font, (255, 255, 255), screen, menu_x + 30, 330)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if shop_open:
                        if buy_croissant_btn.collidepoint(event.pos):
                            if total >= croissant_upgrade_cost:
                                total -= croissant_upgrade_cost
                                croissant_tier += 1
                                croissant_upgrade_cost = int(croissant_upgrade_cost * 1.6)
                            else:
                                error_message = "Not enough coins!"
                                error_timer = pygame.time.get_ticks()
                        elif buy_coffee_btn.collidepoint(event.pos):
                            if total >= coffee_upgrade_cost:
                                total -= coffee_upgrade_cost
                                coffee_tier += 1
                                coffee_upgrade_cost = int(coffee_upgrade_cost * 1.8)
                            else:
                                error_message = "Not enough coins!"
                                error_timer = pygame.time.get_ticks()
                        elif back_button.collidepoint(event.pos):
                            shop_open = False
                            menu_target_x = -MENU_WIDTH
                    else:
                        if shop_toggle_bin.collidepoint(event.pos):
                            shop_open = True
                            menu_target_x = 0
                        elif pastry_station.collidepoint(event.pos):
                            total += croissant_payout
                        elif coffee_station.collidepoint(event.pos) and coffee_tier >= 0:
                            total += coffee_payout

        if error_message != "":
            if pygame.time.get_ticks() - error_timer > 1000:
                error_message = ""
            else:
                draw_text(error_message, font, (255, 0, 0), screen, 40, 140)

        pygame.display.update()
        clock.tick(60)

main_menu()