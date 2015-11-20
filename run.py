#!/usr/bin/env python
# Boid runner

import pygame
import random
import sys
from boid import Boid

size = width, height = 800,600
black = 0, 0, 0

maxVelocity = 10
numBoids = 50
boids = []

pygame.init()

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
ballrect = ball.get_rect()

# create boids at random positions
for i in range(numBoids):
    boids.append(Boid(random.randint(0, width), random.randint(0, height)))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for boid in boids:
        closeBoids = []
        for otherBoid in boids:
            if otherBoid == boid: continue
            distance = boid.distance(otherBoid)
            if distance < 200:
                closeBoids.append(otherBoid)


        boid.moveCloser(closeBoids)
        boid.moveWith(closeBoids)
        boid.moveAway(closeBoids, 25)

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        border = 25
        if boid.x < border and boid.velocityX < 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.x > width - border and boid.velocityX > 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.y < border and boid.velocityY < 0:
            boid.velocityY = -boid.velocityY * random.random()
        if boid.y > height - border and boid.velocityY > 0:
            boid.velocityY = -boid.velocityY * random.random()

        boid.move()

    screen.fill(black)
    for boid in boids:
        boidRect = pygame.Rect(ballrect)
        boidRect.x = boid.x
        boidRect.y = boid.y
        screen.blit(ball, boidRect)
    pygame.display.flip()
    pygame.time.delay(10)
