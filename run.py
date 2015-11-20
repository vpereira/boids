#!/usr/bin/env python
# Boid runner

import pygame
import random
import sys
from boid import Boid, Predator

size = width, height = 800, 600
black = 0, 0, 0

maxVelocity = 10
numBoids = 20
boids = []

pygame.init()

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
predator = pygame.image.load("gray-ball.png")

ballrect = ball.get_rect()

predatorect = predator.get_rect()

boid_predator = Predator(random.randint(0, width),
    random.randint(0, height),random.randint(1,2))


# create boids at random positions
for i in range(numBoids):
    boids.append(Boid(random.randint(0, width),
        random.randint(0, height),random.randint(1,2)))

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    boid_predator.keep_on_screen()
    boid_predator.move()

    print len(boids)

    # predator is killing
    boids = [ boid for boid in boids if boid.distance(boid_predator) >= 10 ]

    print len(boids)
    for boid in boids:
        closeBoids = []
        for otherBoid in boids:
            if otherBoid == boid:
                continue
            distance = boid.distance(otherBoid)
            if distance < 200:
                closeBoids.append(otherBoid)
            if distance <= 1:
                baby = boid.procreate(otherBoid)
                if baby:
                    boids.append(baby)
                else:
                    pass

        boid.moveCloser(closeBoids)
        boid.moveWith(closeBoids)
        boid.moveAway(closeBoids, 25)

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        boid.keep_on_screen()

        boid.move()

    screen.fill(black)

    predatoRect = pygame.Rect(predatorect)
    predatoRect.x = boid_predator.x
    predatoRect.y = boid_predator.y
    screen.blit(predator, predatoRect)

    for boid in boids:
        boidRect = pygame.Rect(ballrect)
        boidRect.x = boid.x
        boidRect.y = boid.y
        screen.blit(ball, boidRect)
    pygame.display.flip()
    pygame.time.delay(10)
