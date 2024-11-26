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
        def centerVerticy(plane):
            a = [0, 0, 0]
            for x, y, z in plane:
                a[0] += x
                a[1] += y
                a[2] += y
            a[0] /= len(plane)
            a[0] /= len(plane)
            a[0] /= len(plane)
            return a

        self.planes.sort(
            key=lambda x: getDistance(centerVerticy(x), position), reverse=True
        )

    def getDistanceBy(self, point):
        return getDistance(self.position, point)


# https://en.wikipedia.org/wiki/Cohen%E2%80%93Sutherland_algorithm
# Define region codes
INSIDE = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000


def compute_region_code(x, y, x_min, y_min, x_max, y_max):
    code = INSIDE
    if x < x_min:  # To the left of the rectangle
        code |= LEFT
    elif x > x_max:  # To the right of the rectangle
        code |= RIGHT
    if y < y_min:  # Below the rectangle
        code |= BOTTOM
    elif y > y_max:  # Above the rectangle
        code |= TOP
    return code


def sortPlanesToCamera(planes, position):
    def closestVerticy(plane):
        a = copy.copy(plane)
        a.sort(key=lambda x: getDistance(x, position), reverse=True)
        return a[0]

    planes.sort(key=lambda x: getDistance(closestVerticy(x), position), reverse=True)


def cohenSutherlandClip(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    # Compute region codes for both endpoints
    code1 = compute_region_code(x1, y1, x_min, y_min, x_max, y_max)
    code2 = compute_region_code(x2, y2, x_min, y_min, x_max, y_max)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            # Both points are inside; trivially accept the line
            accept = True
            break
        elif code1 & code2 != 0:
            # Both points share an outside region; trivially reject the line
            break
        else:
            # The line is partially inside; clip it
            # Choose an endpoint outside the clipping rectangle
            code_out = code1 if code1 != 0 else code2

            # Find intersection point based on region code
            if code_out & TOP:  # Point is above the rectangle
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:  # Point is below the rectangle
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:  # Point is to the right of the rectangle
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:  # Point is to the left of the rectangle
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            # Replace endpoint outside the rectangle with intersection point
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_region_code(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = x, y
                code2 = compute_region_code(x2, y2, x_min, y_min, x_max, y_max)

    if accept:
        return rounded(x1), rounded(y1), rounded(x2), rounded(y2)
    else:
        return None


def getDistance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** (1 / 2)


WIDTH, HEIGHT = 1020, 800
MAXRES = max(WIDTH, HEIGHT)


def onAppStart(app):
    app.setMaxShapeCount(100000)
    app.RES = app.WIDTH, app.HEIGHT = WIDTH, HEIGHT
    app.camera = Camera()
    app.dragStartingPosition = None
    app.world = World()

    for i in range(-7, 8):
        for j in range(-7, 8):
            app.world.createBlock((i, j, 0), "green")
    app.world.createBlock((0, 0, 1), "brown")
    app.world.createBlock((0, 0, 2), "brown")
    app.world.createBlock((0, 0, 3), "brown")
    app.world.createBlock((0, 0, 4), "brown")
    app.world.createBlock((0, 0, 5), "brown")
    app.world.createBlock((0, 0, 6), "brown")
    for i in range(-2, 3):
        for j in range(-2, 3):
            for l in range(2):
                app.world.createBlock((i, j, 3 + l), "brown")
    for i in range(-1, 2):
        for j in range(-1, 2):
            app.world.createBlock((i, j, 5), "brown")

    app.world.createBlock((-1, 0, 6), "brown")
    app.world.createBlock((1, 0, 6), "brown")
    app.world.createBlock((0, -1, 6), "brown")
    app.world.createBlock((0, 1, 6), "brown")

    pass


def getPositionOnScreen(app, pos):
    x, y, z = pos
    COx, COy, COz = app.camera.orientation
    Cx, Cy, Cz = app.camera.position

    # Calculate differences between point and camera position
    difX = x - Cx
    difY = y - Cy
    difZ = z - Cz

    # Calculate sine and cosine of orientation angles
    Sx = math.sin(COx)
    Sy = math.sin(COy)
    Sz = math.sin(COz)
    Cx = math.cos(COx)
    Cy = math.cos(COy)
    Cz = math.cos(COz)

    # Transform world coordinates into camera space
    X = Cy * (Sz * difY + Cz * difX) - Sy * difZ
    Y = Sx * (Cy * difZ + Sy * (Sz * difY + Cz * difX)) + Cx * (Cz * difY - Sz * difX)
    Z = Cx * (Cy * difZ + Sy * (Sz * difY + Cz * difX)) - Sx * (Cz * difY - Sz * difX)

    # Discard points behind the camera or outside clipping planes
    near_plane = 0.1
    far_plane = 1000
    if Z >= 0 or Z < -far_plane or Z > -near_plane:
        return None

    # Perspective divide to map to normalized device coordinates (-1 to 1)
    py = Y / -Z
    px = X / -Z

    # Adjust for aspect ratio
    aspect_ratio = app.WIDTH / app.HEIGHT
    px /= aspect_ratio

    # Map normalized device coordinates to screen space
    py_map = (1 + py) / 2
    px_map = (1 + px) / 2

    posOnScreenY = int(py_map * app.HEIGHT)
    posOnScreenX = int(px_map * app.WIDTH)

    return posOnScreenY, posOnScreenX


def getPlanesFromBlocks(blocks):
    planes = dict()
    for block in blocks:
        for plane in block.planes:
            planeStr = ""
            i = 0
            for v in plane:
                if i == 0:
                    planeStr += f"{v[0]},{v[1]},{v[2]}"
                else:
                    planeStr += f";{v[0]},{v[1]},{v[2]}"
                i += 1
            planes[planeStr] = planes.get(planeStr, 0)
            planes[planeStr] += 1
    planesArr = []
    for planeStr in planes:
        if planes[planeStr] == 1:
            a = planeStr.split(";")
            b = []
            for aa in a:
                x, y, z = aa.split(",")
                b.append((int(x), int(y), int(z)))
            planesArr.append(b)
    return planesArr


def drawPlane(plane, app, color):
    points = []
    for point in plane:
        p = getPositionOnScreen(app, point)
        if p:
            x, y = p
            points += [(x, y)]
    newPoints = []
    for i in range(-1, len(points) - 1):
        point1 = points[i]
        point2 = points[i + 1]
        clippedLine = cohenSutherlandClip(
            point1[0], point1[1], point2[0], point2[1], 0, 0, WIDTH, HEIGHT
        )
        if clippedLine:
            newPoints += [clippedLine[0], clippedLine[1]]
            newPoints += [clippedLine[2], clippedLine[3]]
    drawPolygon(*newPoints, fill=color, border="black", borderWidth=0.4)


def redrawAll(app):
    blocks = app.world.getAllBlocks()
    if len(blocks) == 0:
        return
    planes = getPlanesFromBlocks(blocks)
    sortPlanesToCamera(planes, app.camera.position)
    for plane in planes:
        drawPlane(plane, app, "green")


def onKeyHold(app, keys):
    if "down" in keys:
        app.camera.changePositionX(app.camera.position[0] + 1)
    if "up" in keys:
        app.camera.changePositionX(app.camera.position[0] - 1)

    if "right" in keys:
        app.camera.changePositionY(app.camera.position[1] + 1)

    if "left" in keys:
        app.camera.changePositionY(app.camera.position[1] - 1)

    if "," in keys:
        app.camera.changePositionZ(app.camera.position[2] + 1)

    if "." in keys:
        app.camera.changePositionZ(app.camera.position[2] - 1)

    if "w" in keys:
        x, y, z = app.camera.orientation
        app.camera.changePositionX(app.camera.position[0] - 0.4 * math.cos(z))
        app.camera.changePositionY(app.camera.position[1] - 0.4 * math.sin(z))
        app.camera.changePositionZ(app.camera.position[2] - 0.4 * math.cos(y))
    if "s" in keys:
        x, y, z = app.camera.orientation
        app.camera.changePositionX(app.camera.position[0] + 0.4 * math.cos(z))
        app.camera.changePositionY(app.camera.position[1] + 0.4 * math.sin(z))
        app.camera.changePositionZ(app.camera.position[2] + 0.4 * math.cos(y))
    if "a" in keys:
        x, y, z = app.camera.orientation
        app.camera.changePositionX(
            app.camera.position[0] - 0.4 * math.cos(z + math.pi / 2)
        )
        app.camera.changePositionY(
            app.camera.position[1] - 0.4 * math.sin(z + math.pi / 2)
        )
        # app.camera.changePositionZ(app.camera.position[2] - 1/3 * math.cos(y))
    if "d" in keys:
        x, y, z = app.camera.orientation
        app.camera.changePositionX(
            app.camera.position[0] + 0.4 * math.cos(z + math.pi / 2)
        )
        app.camera.changePositionY(
            app.camera.position[1] + 0.4 * math.sin(z + math.pi / 2)
        )
        # app.camera.changePositionZ(app.camera.position[2] + 1/3 * math.cos(y))

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
