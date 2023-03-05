import pygame
import random


def board(x, y):
    board = [[0 for _ in range(x)] for _ in range(y)]
    card_images = []
    for i in range(4):
        card_images.append(pygame.image.load("images/card{}cop.jpg".format(i+1)))

    for i in range(4, 8):
        card_images.append(pygame.image.load("images/card{}cop.png".format(i+1)))

    return board, card_images


def shuffling():
    cards = []
    for i in range(8):
        cards.append(i + 1)
        cards.append(i + 1)

    random.shuffle(cards)
    return cards