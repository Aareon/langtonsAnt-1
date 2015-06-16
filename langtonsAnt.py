#!/usr/bin/python
# -*- coding: utf-8 -*-

##############################################################################
# #
# By cadian42
# #
##############################################################################

import pyglet
from pyglet import window
from pyglet import clock
import random
from argparse import ArgumentParser

class Grid(pyglet.window.Window):
    
    def __init__(self, windowHeight, windowWidth, cellSize):
        #création de la fenêtre
        window.Window.__init__(self, windowWidth, windowHeight)

        self.columns = windowWidth/cellSize
        self.rows = windowHeight/cellSize
        self.cellSize = cellSize
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        #initialisation de la grille : False=Black, True=White
        self.cells = []
        for i in range(self.rows):
            self.cells.append([])
            for j in range(self.columns):
                self.cells[i].append(False)

        self.ant = Ant(int(random.random()*self.columns), int(random.random()*self.rows), 0, self.rows, self.columns)
    
    #choisit aléatoirement la couleur des cellules sur la grille
    def randomizeGrid(self):
        for i in range(self.rows):
            self.cells.append([])
            for j in range(self.columns):
                if random.random() > 0.5:
                    self.cells[i][j] = True
                else:
                    self.cells[i][j] = False

    #affiche tout ce qu'il y a à afficher
    def draw(self):
        self.clear()
        self.drawCells()
        self.drawAnt(self.ant.x, self.ant.y)
        self.drawGrid()

    #affiche le quadrillage
    def drawGrid(self):
        #couleur du quadrillage = gris
        pyglet.gl.glColor4f(0.5, 0.5, 0.5, 1.0)
        #on dessine les lignes
        for r in range(self.rows):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (0, r*self.cellSize, self.windowWidth, r*self.cellSize)))
        #on dessine les colonnes
        for c in range(self.columns):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (c*self.cellSize, 0, c*self.cellSize, self.windowHeight)))

    #affiche les cases de la grille
    def drawCells(self):
        #on ne dessine que les cellules blanches car le fond est déja noir
        pyglet.gl.glColor4f(1., 1., 1., 1.)
        for i in range(len(self.cells)):
            currentRow = self.cells[i]
            for j in range(len(currentRow)):
                if currentRow[j]:
                    self.rectangle(j*self.cellSize, i*self.cellSize, (j+1)*self.cellSize, (i+1)*self.cellSize)

    #affiche la fourmi
    def drawAnt(self, x, y):
        #couleur = rouge
        pyglet.gl.glColor4f(1., 0., 0., 1.)
        self.rectangle(x*self.cellSize, y*self.cellSize, (x+1)*self.cellSize, (y+1)*self.cellSize)

    #affiche un rectangle
    def rectangle(self, x1, y1, x2, y2):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

    #lance l'automate
    def loop(self):
        #limite les fps pour éviter de planter l'ordi :o
        clock.set_fps_limit(60)
        #variable pour compter les étapes
        steps = 0
        #on fait évoluer l'automate tant que l'user n'a pas cliqué sur la croix (exit)
        while not self.has_exit:
            self.dispatch_events()

            #on fait bouger la fourmi et on met a jour sa case
            self.cells[self.ant.y][self.ant.x] = not self.cells[self.ant.y][self.ant.x]
            self.ant.move(not self.cells[self.ant.y][self.ant.x])
            
            self.draw()
            #update la fenêtre
            self.flip()
            #update l'horloge
            clock.tick()
            #update le nombre d'étape + affichage
            steps += 1
            print steps


class Ant(object):
    
    def __init__(self, x, y, dir, rows, columns):
        self.rows = rows
        self.columns = columns
        self.x = x
        self.y = y
        #direction : 0=Nord, 1=Est, 2=Sud, 3=West
        self.dir = dir

    def move(self, currentCell):
        #on met a jour la direction (case blanche = 90° droite, case noire = 90° gauche)
        if currentCell:
            self.dir = (self.dir + 1) % 4
        else:
            self.dir = self.dir -1
            if self.dir == -1:
                self.dir = 3

        #on avance d'une case
        if (self.dir == 0):
            self.y = (self.y + 1) % self.rows
        elif (self.dir == 1):
            self.x = (self.x + 1) % self.columns
        elif (self.dir == 2):
            self.y = (self.y - 1) % self.rows
        else:
            self.x = (self.x - 1) % self.columns


def main():
    parser = ArgumentParser()

    parser.add_argument("-wh", action="store", dest="windowHeight", default=600)
    parser.add_argument("-ww", action="store", dest="windowWidth", default=800)
    parser.add_argument("-s", action="store", dest="cellSize", default=10)
    parser.add_argument("-r", action="store_true", dest="randomize", default=False)

    args = parser.parse_args()

    myGrid = Grid(int(args.windowHeight), int(args.windowWidth), int(args.cellSize))
    if args.randomize:
        myGrid.randomizeGrid()
    myGrid.loop()

if __name__ == '__main__':
    main()

