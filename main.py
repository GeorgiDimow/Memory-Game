import pygame

from game_board import board, shuffling
from collections import deque


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
VIOLET_BLUE = (158, 161, 240)
BLUE = (58, 161, 240)

background = pygame.image.load("images/background.png")
WIDTH = 450
HEIGHT = 700
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BOARD_WIDTH = 4
BOARD_HEIGHT = 4
CARD_SIZE = 100
CARD_SPACING = 10


def main_loop():
    select_card = None
    game_over = False
    curr_score = 0
    board_start, card_images = board(BOARD_WIDTH, BOARD_HEIGHT)
    cards = deque(shuffling())
    shown_pics = 0

    button_show = pygame.Surface((100, 100))
    button_show.fill(BLUE)
    screen.blit(button_show, (100, 100))
    is_showing = False
    count = 0

    while True:
        if game_over:
            end_screen(curr_score)
            pygame.quit()
            break

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEWHEEL:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and count < 1:
                x = pos[0] // 100
                y = pos[1] // 100
                if x == 2 and y == 5:
                    is_showing = True
            else:
                is_showing = False

            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x = pos[0] // (CARD_SIZE + CARD_SPACING)
                y = pos[1] // (CARD_SIZE + CARD_SPACING)

                try:
                    if board_start[y][x] == 0:
                        board_start[y][x] = cards[y * BOARD_WIDTH + x]
                        shown_pics += 1

                    if select_card is None:
                        select_card = (x, y)

                    else:
                        if board_start[y][x] == board_start[select_card[1]][select_card[0]]:
                            curr_score += 1

                            board_start[y][x] = -cards[y * BOARD_WIDTH + x]
                            board_start[select_card[1]][select_card[0]] = -cards[y * BOARD_WIDTH + x]

                            select_card = None
                        else:
                            select_card = (x, y)

                except IndexError:
                    pass

        screen.blit(background, (0, 0))
        screen.blit(button_show, (175, 500))
        font = pygame.font.Font(None, 36)
        text = font.render("Show", True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (225, 550)
        screen.blit(text, text_rect)
        card = pygame.image.load("images/card.png")

        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                card_value = board_start[y][x]

                if card_value < 0:
                    screen.blit(card_images[abs(card_value) - 1], (
                        (CARD_SIZE + CARD_SPACING) * x + CARD_SPACING, (CARD_SIZE + CARD_SPACING) * y + CARD_SPACING))

                    s = pygame.Surface((CARD_SIZE, CARD_SIZE))
                    s.set_alpha(128)
                    s.fill(GRAY)
                    screen.blit(s, ((CARD_SIZE + CARD_SPACING) * x + CARD_SPACING, (CARD_SIZE + CARD_SPACING) * y +
                                    CARD_SPACING))

                elif card_value != 0:
                    screen.blit(card_images[card_value - 1], (
                        (CARD_SIZE + CARD_SPACING) * x + CARD_SPACING, (CARD_SIZE + CARD_SPACING) * y + CARD_SPACING))

                else:
                    if is_showing:
                        cards_copy = cards.copy()
                        while cards_copy:
                            for y1 in range(BOARD_HEIGHT):
                                for x1 in range(BOARD_WIDTH):
                                    curr_card = cards_copy.popleft()

                                    screen.blit(card_images[curr_card - 1], (
                                        (CARD_SIZE + CARD_SPACING) * x1 + CARD_SPACING,
                                        (CARD_SIZE + CARD_SPACING) * y1 + CARD_SPACING))

                        button_show.fill(GRAY)
                        count += 1

                    else:
                        screen.blit(card, (
                            (CARD_SIZE + CARD_SPACING) * x + CARD_SPACING,
                            (CARD_SIZE + CARD_SPACING) * y + CARD_SPACING,
                            CARD_SIZE,
                            CARD_SIZE))

        pygame.display.flip()
        clock.tick(60)

        if curr_score == 8:
            game_over = True

        if shown_pics == BOARD_WIDTH * BOARD_HEIGHT:
            game_over = True


def end_screen(score):
    game_over = False
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Game over! Score: {}".format(score), True, VIOLET_BLUE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2 - 20)
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 24)
    text = font.render("Press SPACE to play again, or ESCAPE to quit", True, VIOLET_BLUE)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2 + 20)
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_loop()
                elif event.key == pygame.K_ESCAPE:
                    game_over = True

        if game_over:
            break


if __name__ == '__main__':
    main_loop()
