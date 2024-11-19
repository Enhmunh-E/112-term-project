#################################################
# app.py
#
# Your name: Enkhmunkh Enkhbayar
# Your andrew id: eenkhbay
#################################################


from cmu_graphics import *
import math
import copy


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
        newY = self.orientation[1] + y
        if newY > math.pi:
            newY = math.pi
        elif newY < 0:
            newY = 0
        self.orientation = (
            self.orientation[0] + x,
            newY,
            self.orientation[2] + z,
        )


class Camera(Object):
    pass


class World:
    def __init__(self):
        self.blocks = []

    def createBlock(self, position=(0, 0, 0), color=None):
        newBlock = Block(position, color)
        self.blocks.append(newBlock)

    def getAllBlocks(self):
        return self.blocks


class Block(Object):
    def __init__(self, position=(0, 0, 0), color=None):
        self.position = position
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
        self.colors = [color] * 6

    def __str__(self):
        return f"Block: {self.vertices}"

    def sortPlanes(self, position):
        def closestVerticy(plane):
            a = copy.copy(plane)
            a.sort(key=lambda x: getDistance(x, position), reverse=True)
            return a[0]

        self.planes.sort(
            key=lambda x: getDistance(closestVerticy(x), position), reverse=True
        )

    def draw(self, app):
        index = 0
        for plane in self.planes:
            points = []
            for point in plane:
                x, y = getPositionOnScreen(app, point)
                points += [x, y]
            drawPolygon(
                *points, fill=self.colors[index], border="black", borderWidth=0.4
            )
            index += 1

    def getDistanceBy(self, point):
        return getDistance(self.position, point)


def getDistance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** (1 / 2)


WIDTH, HEIGHT = 1020, 800
MAXRES = max(WIDTH, HEIGHT)


def onAppStart(app):
    app.RES = app.WIDTH, app.HEIGHT = WIDTH, HEIGHT
    app.camera = Camera()
    app.dragStartingPosition = None
    app.world = World()
    app.world.createBlock((0, 0, 0), "saddleBrown")
    app.world.createBlock((0, 0, 1), "saddleBrown")
    app.world.createBlock((0, 0, 2), "saddleBrown")
    app.world.createBlock((0, 0, 3), "saddleBrown")
    app.world.createBlock((0, 0, 4), "saddleBrown")
    for i in range(-2, 3):
        for j in range(-2, 3):
            for l in range(2):
                app.world.createBlock((0 + i, 0 + j, 2 + l), "oliveDrab")
    for i in range(-1, 2):
        for j in range(-1, 2):
            app.world.createBlock((0 + i, 0 + j, 4), "oliveDrab")
    app.world.createBlock((0, 0, 5), "oliveDrab")
    app.world.createBlock((0, 1, 5), "oliveDrab")
    app.world.createBlock((0, -1, 5), "oliveDrab")
    app.world.createBlock((1, 0, 5), "oliveDrab")
    app.world.createBlock((-1, 0, 5), "oliveDrab")
    pass


def getPositionOnScreen(app, pos):
    x, y, z = pos
    COx, COy, COz = app.camera.orientation
    Cx, Cy, Cz = app.camera.position
    difX = x - Cx
    difY = y - Cy
    difZ = z - Cz
    Sx = math.sin(COx)
    Sy = math.sin(COy)
    Sz = math.sin(COz)
    Cx = math.cos(COx)
    Cy = math.cos(COy)
    Cz = math.cos(COz)
    X = Cy * (Sz * difY + Cz * difX) - Sy * difZ
    Y = Sx * (Cy * difZ + Sy * (Sz * difY + Cz * difX)) + Cx * (Cz * difY - Sz * difX)
    Z = Cx * (Cy * difZ + Sy * (Sz * difY + Cz * difX)) - Sx * (Cz * difY - Sz * difX)
    if Z == 0:
        py = 0
        px = 0
    else:
        py = Y / -Z
        px = X / -Z
    py_map = (1 + py) / 2
    px_map = (1 + px) / 2
    return int(py_map * MAXRES), int(px_map * MAXRES)


def redrawAll(app):
    blocks = app.world.getAllBlocks()
    blocks.sort(key=lambda x: x.getDistanceBy(app.camera.position), reverse=True)
    for block in app.world.getAllBlocks():
        block.sortPlanes(app.camera.position)
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
        x, y, z = app.camera.orientation
        app.camera.changePositionX(app.camera.position[0] - 1 / 5 * math.cos(z))
        app.camera.changePositionY(app.camera.position[1] - 1 / 5 * math.sin(z))
        app.camera.changePositionZ(app.camera.position[2] - 1 / 5 * math.cos(y))
    if "s" in keys:
        x, y, z = app.camera.orientation
        app.camera.changePositionX(app.camera.position[0] + 1 / 5 * math.cos(z))
        app.camera.changePositionY(app.camera.position[1] + 1 / 5 * math.sin(z))
        app.camera.changePositionZ(app.camera.position[2] + 1 / 5 * math.cos(y))
    if "a" in keys:
        x, y, z = app.camera.orientation
        app.camera.changePositionX(
            app.camera.position[0] - 1 / 5 * math.cos(z + math.pi / 2)
        )
        app.camera.changePositionY(
            app.camera.position[1] - 1 / 5 * math.sin(z + math.pi / 2)
        )
        # app.camera.changePositionZ(app.camera.position[2] - 1 / 5 * math.cos(y))
    if "d" in keys:
        x, y, z = app.camera.orientation
        app.camera.changePositionX(
            app.camera.position[0] + 1 / 5 * math.cos(z + math.pi / 2)
        )
        app.camera.changePositionY(
            app.camera.position[1] + 1 / 5 * math.sin(z + math.pi / 2)
        )
        # app.camera.changePositionZ(app.camera.position[2] + 1 / 5 * math.cos(y))

    pass


def onMouseDrag(app, mouseX, mouseY):
    # if button == 2:
    # Right Click
    if app.dragStartingPosition:
        # Meaning it has already started dragging
        disX = app.dragStartingPosition[0] - mouseX
        disY = app.dragStartingPosition[1] - mouseY
        app.camera.changeOrientation(
            0, math.pi / 180 * disY / 10, math.pi / 180 * disX / 10
        )
    app.dragStartingPosition = (mouseX, mouseY)


def onMouseRelease(app, mouseX, mouseY, button):
    app.dragStartingPosition = None


def onStep(app):
    pass


def main():
    runApp(WIDTH, HEIGHT)


main()
