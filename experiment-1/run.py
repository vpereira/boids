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
numBoids = 90
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
        pred.keep_on_screen()
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
        boid.keep_on_screen()

        boid.move()

    screen.fill(black)

    for pred in predators:
        pred.do_screen()

    for boid in boids:
        boid.do_screen()

    pygame.display.flip()
    pygame.time.delay(10)
