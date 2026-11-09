import pygame
from sys import exit
import time, random, os, sys

pygame.init()
pygame.display.set_caption('Cozy Cafe')

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
coin_image = pygame.transform.scale(pygame.image.load(resource_path("images/coin.png")), (30, 30))
croissant_image = pygame.transform.scale(pygame.image.load(resource_path("images/croissant.png")), (80, 80))
help_image = pygame.transform.scale(pygame.image.load(resource_path("images/help.png")), (30, 50))
coffee_image = pygame.transform.scale(pygame.image.load(resource_path("images/coffee.png")), (120, 120))
tip_image = pygame.transform.scale(pygame.image.load(resource_path("images/tip_jar.png")), (100, 75))

#Background
main_menu_img = pygame.image.load("images/main_menu.jpg").convert_alpha()
main_bg = pygame.transform.scale(main_menu_img, (1000, 750))

game_menu_img = pygame.image.load("images/game_bg.png").convert_alpha()
game_bg = pygame.transform.scale(game_menu_img, (1000, 750))

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
        
        help_rect = pygame.Rect(930, 30, 30, 50)
        
        mx, my = pygame.mouse.get_pos()
        b1_color = (180, 90, 0) if button_1.collidepoint((mx, my)) else (150, 75, 0)
        b3_color = (180, 90, 0) if button_3.collidepoint((mx, my)) else (150, 75, 0)
        
        pygame.draw.rect(screen, b1_color, button_1, border_radius=5)
        pygame.draw.rect(screen, b3_color, button_3, border_radius=5)
        
        draw_text('Play', button_font, (255, 219, 187), screen, 420, 310)
        draw_text('Quit', button_font, (255, 219, 187), screen, 420, 510)
        
        screen.blit(help_image, (help_rect.x, help_rect.y))
        
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
                    if help_rect.collidepoint(event.pos):
                        instructions()
                    if button_3.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(60)

def instructions():
    running = True
    while running:
        screen.fill((100, 50, 20))
        draw_text('How To Play', button_font, (255, 219, 187), screen, 300, 50)

        draw_text('1. Click on the Croissant to earn coins.', font, (255, 219, 187), screen, 80, 200)
        draw_text('2. Open the Upgrade Shop to spend your coins and get better tiers.', font, (255, 219, 187), screen, 80, 270)
        draw_text('3. Unlock the coffee machine to get more money!', font, (255, 219, 187), screen, 80, 340)
        draw_text('3. Achieve better tiers to make the ultimate cafe!', font, (255, 219, 187), screen, 80, 410)

        back_btn = pygame.Rect(400, 550, 200, 80)
        mx, my = pygame.mouse.get_pos()
        btn_color = (180, 90, 0) if back_btn.collidepoint((mx, my)) else (150, 75, 0)
        pygame.draw.rect(screen, btn_color, back_btn, border_radius=5)
        draw_text('Back', button_font, (255, 219, 187), screen, 435, 555)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_btn.collidepoint(event.pos):
                        running = False
        
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
    
    coffee_pos = (200, 300)
    croissant_pos = (600, 320)
    
    #tip variables
    tip_jar_pos = (450, 310)
    tip_jar_rect = pygame.Rect(tip_jar_pos[0], tip_jar_pos[1], 100, 100)
    uncollected_tips = 0
    last_tip_time = time.time()
    tip_interval = 4.0
    
    coffee_hitbox = pygame.Rect(coffee_pos[0], coffee_pos[1], 120, 120)
    croissant_hitbox = pygame.Rect(croissant_pos[0], croissant_pos[1], 80, 80)
    
    while running:
        mx, my = pygame.mouse.get_pos()
        
        screen.blit(game_bg, (0, 0))
        
        coin_text_str = f'Coins: {total}'
        draw_text(coin_text_str, font, (0, 0, 0), screen, 40, 40)
        text_width, text_height = font.size(coin_text_str)
        screen.blit(coin_image, (40 + text_width + 10, 45))
        
        draw_text('Click stations to sell goods!', font, (120, 100, 80), screen, 40, 90)
        shop_toggle_bin = pygame.Rect(750, 40, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), shop_toggle_bin)
        draw_text('Open Shop', font, (255, 255, 255), screen, 790, 50)
        
        #Coffee and Croissant
        croissant_payout = croissant_tier * 5
        coffee_payout = coffee_tier * 10
        
        screen.blit(croissant_image, croissant_pos)
        draw_text(f"Croissant (Tier {croissant_tier})", font, (100, 50, 20), screen, croissant_pos[0] - 20, croissant_pos[1] + 90)
        draw_text(f"+${croissant_payout}/click", font, (139, 69, 19), screen, croissant_pos[0] - 10, croissant_pos[1] + 125)
        
        if coffee_tier == 0:
            locked_overlay = coffee_image.copy()
            locked_overlay.fill((50, 50, 50, 150), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(locked_overlay, coffee_pos)
            draw_text("Coffee (Locked)", font, (100, 100, 100), screen, coffee_pos[0] - 10, coffee_pos[1] + 130)
        else:
            screen.blit(coffee_image, coffee_pos)
            draw_text(f"Coffee (Tier {coffee_tier})", font, (100, 50, 20), screen, coffee_pos[0] - 10, coffee_pos[1] + 130)
            draw_text(f"+${coffee_payout}/click", font, (139, 69, 19), screen, coffee_pos[0] +5, coffee_pos[1] + 165)
        
        current_time = time.time()
        if current_time - last_tip_time > tip_interval:
            base_tip = random.randint(1, 5)
            tier_bonus = croissant_tier + coffee_tier
            uncollected_tips += base_tip + tier_bonus
            last_tip_time = current_time
        
        screen.blit(tip_image, tip_jar_pos)
        if uncollected_tips > 0:
            draw_text(f"+${uncollected_tips} waiting!", font, (0, 150, 0), screen, tip_jar_pos[0] - 20, tip_jar_pos[1] - 35)
        else:
            draw_text("Empty", font, (130, 130, 130), screen, tip_jar_pos[0] + 10, tip_jar_pos[1] - 35)
        
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
                        elif croissant_hitbox.collidepoint(event.pos):
                            total += croissant_payout
                        elif coffee_hitbox.collidepoint(event.pos) and coffee_tier >= 0:
                            total += coffee_payout
                        elif tip_jar_rect.collidepoint(event.pos) and uncollected_tips > 0:
                            total += uncollected_tips
                            uncollected_tips = 0

        if error_message != "":
            if pygame.time.get_ticks() - error_timer > 1000:
                error_message = ""
            else:
                draw_text(error_message, font, (255, 0, 0), screen, 40, 140)

        pygame.display.update()
        clock.tick(60)

main_menu()