#################################################
# app.py
#
# Your name: Enkhmunkh Enkhbayar
# Your andrew id: eenkhbay
#################################################


from cmu_graphics import *
import random
import copy
import numpy as np
import math


def flatten(xss):
    return [x for xs in xss for x in xs]


class Object:
    def __init__(self, position=(0, 0, 0), vertices=[], orientation=(0, 0, 0)):
        self.position = position
        self.orientation = orientation
        self.vertices = vertices

    def changePosition(self, x, y, z):
        self.position = (x, y, z)

    def changePositionX(self, x):
        self.position = (x, self.position[1], self.position[2])

    def changePositionY(self, y):
        self.position = (self.position[0], y, self.position[2])

    def changePositionZ(self, z):
        self.position = (self.position[0], self.position[1], z)

    def changeOrientation(self, x, y, z):
        self.orientation = (
            self.orientation[0] + x,
            self.orientation[1] + y,
            self.orientation[2] + z,
        )


class Camera(Object):
    pass


class World:
    def __init__(self):
        self.blocks = []

    def createBlock(self, position=(0, 0, 0)):
        newBlock = Block(position)
        self.blocks.append(newBlock)

    def getAllBlocks(self):
        return self.blocks


class Block(Object):
    def __init__(self, position=(0, 0, 0)):
        x, y, z = position
        self.vertices = [
            (x, y, z),
            (x + 1, y, z),
            (x + 1, y + 1, z),
            (x, y + 1, z),
            (x, y, z + 1),
            (x + 1, y, z + 1),
            (x + 1, y + 1, z + 1),
            (x, y + 1, z + 1),
        ]
        self.planes = [
            [
                self.vertices[0],
                self.vertices[1],
                self.vertices[2],
                self.vertices[3],
            ],  # Bottom face
            [
                self.vertices[4],
                self.vertices[5],
                self.vertices[6],
                self.vertices[7],
            ],  # Top face
            [
                self.vertices[0],
                self.vertices[1],
                self.vertices[5],
                self.vertices[4],
            ],  # Front face
            [
                self.vertices[3],
                self.vertices[2],
                self.vertices[6],
                self.vertices[7],
            ],  # Back face
            [
                self.vertices[0],
                self.vertices[3],
                self.vertices[7],
                self.vertices[4],
            ],  # Left face
            [
                self.vertices[1],
                self.vertices[2],
                self.vertices[6],
                self.vertices[5],
            ],  # Right face
        ]
        self.colors = [
            None,
            "green",
            None,
            None,
            None,
            None,
        ]

    def __str__(self):
        return f"Block: {self.vertices}"

    def draw(self, app):
        index = 0
        for plane in self.planes:
            points = []
            for point in plane:
                x, y = getPositionOnScreen(app, point)
                points += [x, y]
            drawPolygon(*points, fill=self.colors[index], border="black")
            index += 1


WIDTH, HEIGHT = 800, 800
MAXRES = max(WIDTH, HEIGHT)


def onAppStart(app):
    app.RES = app.WIDTH, app.HEIGHT = 800, 800
    app.camera = Camera()
    app.world = World()
    app.world.createBlock((0, 0, 0))
    app.world.createBlock((0, 1, 0))
    app.world.createBlock((0, 0, 1))
    app.world.createBlock((1, 0, 0))
    pass


def getPositionOnScreen(app, pos):
    x, y, z = pos
    COx, COy, COz = app.camera.orientation
    Cx, Cy, Cz = app.camera.position
    a = (
        np.matrix(
            [
                [1, 0, 0],
                [0, math.cos(COx), math.sin(COx)],
                [0, -math.sin(COx), math.cos(COx)],
            ]
        )
        * np.matrix(
            [
                [math.cos(COy), 0, -math.sin(COy)],
                [0, 1, 0],
                [math.sin(COy), 0, math.cos(COy)],
            ]
        )
        * np.matrix(
            [
                [math.cos(COz), math.sin(COz), 0],
                [-math.sin(COz), math.cos(COz), 0],
                [0, 0, 1],
            ]
        )
        * (np.matrix([[x], [y], [z]]) - np.matrix([[Cx], [Cy], [Cz]]))
    )

    a = a.flatten().getA()[0]
    x, y, z = a
    if z == 0:
        py = 0
        px = 0
    else:
        py = y / -z
        px = x / -z
    py_map = (1 + py) / 2
    px_map = (1 + px) / 2
    return int(py_map * MAXRES), int(px_map * MAXRES)


def redrawAll(app):
    for block in app.world.getAllBlocks():
        block.draw(app)


def onKeyHold(app, keys):
    if "down" in keys:
        app.camera.changePositionX(app.camera.position[0] + 1 / 5)
    if "up" in keys:
        app.camera.changePositionX(app.camera.position[0] - 1 / 5)

    if "right" in keys:
        app.camera.changePositionY(app.camera.position[1] + 1 / 5)

    if "left" in keys:
        app.camera.changePositionY(app.camera.position[1] - 1 / 5)

    if "," in keys:
        app.camera.changePositionZ(app.camera.position[2] + 1 / 5)

    if "." in keys:
        app.camera.changePositionZ(app.camera.position[2] - 1 / 5)

    if "w" in keys:
        app.camera.changeOrientation(0, math.pi / 18 / 5, 0)
    if "s" in keys:
        app.camera.changeOrientation(0, -math.pi / 18 / 5, 0)
    if "d" in keys:
        app.camera.changeOrientation(0, 0, math.pi / 18 / 5)
    if "a" in keys:
        app.camera.changeOrientation(0, 0, -math.pi / 18 / 5)
    pass


def onStep(app):
    pass


def main():
    runApp(800, 800)


main()
