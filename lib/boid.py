#!/usr/bin/env python
# Boid implementation in Python using PyGame

import sys
import random
import math
import pygame


class BoidBase(pygame.sprite.Sprite):
    def __init__(self, x, y, gender, screen, maxVelocity=10):
        self.x = x
        self.y = y
        self.gender = gender
        self.screen = screen
        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0
        self.maxVelocity = maxVelocity

    "paint it in the screen"
    def do_screen(self):
        objRect = pygame.Rect(self.rect)
        objRect.x = self.x
        objRect.y = self.y
        self.screen.blit(self.image, objRect)

    "Perform actual movement based on our velocity"
    def move(self):
        if abs(self.velocityX) > self.maxVelocity or abs(self.velocityY) > self.maxVelocity:
            scaleFactor = self.maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.x += self.velocityX
        self.y += self.velocityY

    "keep on screen"
    def keepOnScreen(self,border=25, height=600,width=800):
        if self.x < border and self.velocityX < 0:
            self.velocityX = -self.velocityX * random.random()
        if self.x > width - border and self.velocityX > 0:
            self.velocityX = -self.velocityX * random.random()
        if self.y < border and self.velocityY < 0:
            self.velocityY = -self.velocityY * random.random()
        if self.y > height - border and self.velocityY > 0:
            self.velocityY = -self.velocityY * random.random()



class Boid(BoidBase):
    def __init__(self, x, y, gender, screen, maxVelocity=10):
        super(self.__class__, self).__init__(x,y,gender,screen,maxVelocity)
        pygame.sprite.Sprite.__init__(self)
        # TODO
        # fix the path
        self.image = pygame.image.load("../lib/ball.png")
        self.rect = self.image.get_rect()

    "Procreation"
    def procreate(self,boid):
        if self.gender != boid.gender:
            return Boid(random.randint(0, 100),
                random.randint(0, 100),random.randint(1,2),self.screen)

    "Return the distance from another boid"
    def distance(self, boid):
        distX = self.x - boid.x
        distY = self.y - boid.y
        return math.sqrt(distX * distX + distY * distY)

    "Move closer to a set of boids"
    def moveCloser(self, boids):
        if len(boids) < 1:
            return

        # calculate the average distances from the other boids
        avgX = 0
        avgY = 0
        for boid in boids:
            if boid.x == self.x and boid.y == self.y:
                continue

            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)

        avgX /= len(boids)
        avgY /= len(boids)

        # set our velocity towards the others
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0

        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)

    "Move with a set of boids"
    def moveWith(self, boids):
        if len(boids) < 1:
            return
        # calculate the average velocities of the other boids
        avgX = 0
        avgY = 0

        for boid in boids:
            avgX += boid.velocityX
            avgY += boid.velocityY

        avgX /= len(boids)
        avgY /= len(boids)

        # set our velocity towards the others
        self.velocityX += (avgX / 10)
        self.velocityY += (avgY / 10)

    "Move away from a set of boids. This avoids crowding"
    def moveAway(self, boids, minDistance):
        if len(boids) < 1:
            return

        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boids:
            distance = self.distance(boid)
            if distance < minDistance:
                numClose += 1
                xdiff = (self.x - boid.x)
                ydiff = (self.y - boid.y)

                if xdiff >= 0:
                    xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0:
                    xdiff = -math.sqrt(minDistance) - xdiff

                if ydiff >= 0:
                    ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0:
                    ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff
                distanceY += ydiff

        if numClose == 0:
            return

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5


class Predator(BoidBase):
    def __init__(self, x, y, gender, screen, maxVelocity=60):
        super(self.__class__, self).__init__(x,y,gender, screen,maxVelocity)
        pygame.sprite.Sprite.__init__(self)
        # TODO
        # fix the path
        self.image = pygame.image.load("../lib/gray-ball.png")
        self.rect = self.image.get_rect()
    def setSpeed(self):
        self.velocityX *= 1.01
        self.velocityY *= 1.01

    def move(self):
        if abs(self.velocityX) > self.maxVelocity or abs(self.velocityY) > self.maxVelocity:
            scaleFactor = self.maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor

        self.x += self.velocityX
        self.y += self.velocityY
