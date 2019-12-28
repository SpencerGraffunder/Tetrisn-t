import pygame

def draw_text(screen, text_str, pt_size, pos, col, font = 'freesansbold.ttf'):
	text_font        = pygame.font.Font(font, pt_size)
	text             = text_font.render(text_str, True, (col[0],col[1],col[2]))
	text_rect        = text.get_rect()
	text_rect.center = (int(pos[0]), int(pos[1]))
	screen.blit(text, text_rect)