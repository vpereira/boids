#!/usr/bin/env python
# Boid runner

import pygame
import random
import sys
sys.path.append("../lib")
from boid import Boid, Predator

size = width, height = 800, 600
black = 0, 0, 0

maxVelocity = 10
numBoids = 100
boids = []

pygame.init()

screen = pygame.display.set_mode(size)

prey = pygame.image.load("../lib/ball.png")
predator = pygame.image.load("../lib/gray-ball.png")

preyrect = prey.get_rect()

predatorect = predator.get_rect()



predators = [ Predator(random.randint(0, width),
    random.randint(0, height),1, screen) for i in xrange(0,numBoids/50)]


# create boids at random positions
for i in range(numBoids):
    boids.append(Boid(random.randint(0, width),
        random.randint(0, height),random.randint(1,2),screen))

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for pred in predators:
        pred.keepOnScreen()
        pred.setSpeed()
        pred.move()
        # predators are killing
        boids = [ boid for boid in boids if boid.distance(pred) >= 10 ]



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
        boid.keepOnScreen()

        boid.move()

    screen.fill(black)

    for pred in predators:
        pred.doScreen()

    for boid in boids:
        boid.doScreen()

    pygame.display.flip()
    pygame.time.delay(10)
