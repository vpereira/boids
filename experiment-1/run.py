#!/usr/bin/env python
# Boid runner

import pygame
import random
import sys
sys.path.append("..")
from boids.boid import Boid, Predator
from boids.boid_constants import BoidConstants

size = width, height = BoidConstants.MAP_SIZE

maxVelocity = 10
numBoids = 400
boids = []

pygame.init()

screen = pygame.display.set_mode(size)

predators = [ Predator(random.randint(0, width),
    random.randint(0, height),1, screen) for i in xrange(0,5)]


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
        pred.moveCloser(boids)

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
        # trx to stick together
        boid.moveAway(closeBoids, 25)
        # try to move away from predators
        boid.moveAway(predators, random.randint(0,25))

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        boid.keepOnScreen()

        boid.move()

    screen.fill(BoidConstants.BACKGROUND_COLOR)

    for el in predators + boids:
        el.doScreen()

    pygame.display.flip()
    pygame.time.delay(BoidConstants.DEFAULT_DELAY)
