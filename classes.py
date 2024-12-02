#################################################
#                                               #
#               Necessary Classes               #
#                                               #
#################################################

from utils import *


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
        # if newY > math.pi:
        #     print(newY, "fix", math.pi)
        #     newY = math.pi
        # if newY < 0:
        #     newY = 0
        self.orientation = (
            self.orientation[0] + x,
            newY,
            self.orientation[2] + z,
        )

    def changeOrientationFully(self, x, y, z):
        self.orientation = (
            x,
            y,
            z,
        )


class Camera(Object):
    pass


class World:
    def __init__(self):
        self.blocks = []
        self.blockPositionsStringSet = []

    def createBlock(self, position=(0, 0, 0), color=None):
        newBlock = Block(position, color)
        self.blocks.append(newBlock)
        self.blockPositionsStringSet.append(
            f"{position[0]},{position[1]},{position[2]}"
        )

    def deleteBlock(self, position):
        if f"{position[0]},{position[1]},{position[2]}" in self.blockPositionsStringSet:
            self.blockPositionsStringSet.remove(
                f"{position[0]},{position[1]},{position[2]}"
            )
        self.blocks = [block for block in self.blocks if block.position != position]

    def getAllBlocks(self):
        return self.blocks


class Block(Object):
    def __init__(self, position=(0, 0, 0), color=None):
        self.position = position
        x, y, z = position
        self.vertices = [
            (x - 0.5, y - 0.5, z - 0.5),
            (x + 0.5, y - 0.5, z - 0.5),
            (x + 0.5, y + 0.5, z - 0.5),
            (x - 0.5, y + 0.5, z - 0.5),
            (x - 0.5, y - 0.5, z + 0.5),
            (x + 0.5, y - 0.5, z + 0.5),
            (x + 0.5, y + 0.5, z + 0.5),
            (x - 0.5, y + 0.5, z + 0.5),
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
        # self.colors = [color] * 6
        self.color = color if color else "green"

    def __str__(self):
        return f"Block: {self.vertices}"

    def sortPlanes(self, position):
        def centerVerticy(plane):
            a = [0, 0, 0]
            for x, y, z in plane:
                a[0] += x
                a[1] += y
                a[2] += y
            a[0] /= len(plane)
            a[1] /= len(plane)
            a[2] /= len(plane)
            return a

        self.planes.sort(
            key=lambda x: getDistance(centerVerticy(x), position), reverse=True
        )

    def getDistanceBy(self, point):
        return getDistance(self.position, point)
