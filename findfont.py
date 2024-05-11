import pygame, sys

pygame.init()
pygame.mixer.init()
winWidth = 800
winHeight = 600
display_surface = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Geometry War")

# Print all system fonts
fonts = pygame.font.get_fonts()

i = 0
target_font = pygame.font.SysFont(None, 50)
target_text = target_font.render("GEOMETRY WARS", True, (255, 255, 255))
taregt_rect = target_text.get_rect(center=(winWidth//2, winHeight//4 * 3))

current_font = pygame.font.SysFont(fonts[i], 50)
current_text = current_font.render("GEOMETRY WARS", True, (255, 255, 255))
current_rect = current_text.get_rect(center=(winWidth//2, winHeight//4))

print(fonts[i])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                i -= 1
                current_font = pygame.font.SysFont(fonts[i], 50)
                current_text = current_font.render("GEOMETRY WARS", True, (255, 255, 255))
                current_rect = current_text.get_rect(center=(winWidth//2, winHeight//4))
                print(fonts[i])

            if event.key == pygame.K_RIGHT:
                i += 1
                current_font = pygame.font.SysFont(fonts[i], 50)
                current_text = current_font.render("GEOMETRY WARS", True, (255, 255, 255))
                current_rect = current_text.get_rect(center=(winWidth//2, winHeight//4))
                print(fonts[i])


    display_surface.fill((0, 0, 0))
    display_surface.blit(current_text, current_rect)
    display_surface.blit(target_text, taregt_rect)
    pygame.display.update()