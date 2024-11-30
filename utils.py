#################################################
#                                               #
#               Helper Functions                #
#                                               #
#################################################

import copy
import math
from cmu_graphics import *
import numpy as np

WIDTH, HEIGHT = 800, 800
MAXRES = max(WIDTH, HEIGHT)

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
        a = copy.copy(plane[0])
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


def getPositionOnScreen(app, pos):
    x, y, z = pos
    COx, COy, COz = app.camera.orientation
    Cpx, Cpy, Cpz = app.camera.position

    # Differences between point and camera position
    difX = x - Cpx
    difY = y - Cpy
    difZ = z - Cpz

    # Sine and cosine of orientation angles
    SinX = math.sin(COx)
    SinY = math.sin(COy)
    SinZ = math.sin(COz)
    CosX = math.cos(COx)
    CosY = math.cos(COy)
    CosZ = math.cos(COz)

    # Transform world coordinates into camera space (verify correctness)
    X = CosY * (SinZ * difY + CosZ * difX) - SinY * difZ
    Y = SinX * (CosY * difZ + SinY * (SinZ * difY + CosZ * difX)) + CosX * (
        CosZ * difY - SinZ * difX
    )
    Z = CosX * (CosY * difZ + SinY * (SinZ * difY + CosZ * difX)) - SinX * (
        CosZ * difY - SinZ * difX
    )

    # Discard points behind the camera or outside clipping planes
    near_plane = 0.1
    far_plane = 1000
    if Z >= 0 or Z < -far_plane or Z > -near_plane:
        return None

    # Perspective divide and aspect ratio adjustment
    py = Y / -Z
    px = X / -Z
    aspect_ratio = app.WIDTH / app.HEIGHT
    px /= aspect_ratio

    # Map to screen space
    py_map = (1 + py) / 2
    px_map = (1 + px) / 2

    posOnScreenY = int(py_map * app.HEIGHT)
    posOnScreenX = int(px_map * app.WIDTH)

    return posOnScreenY, posOnScreenX


def getDirLengths(orientation):
    Y = math.sin(orientation[2]) * math.cos(math.pi / 2 - orientation[1])
    X = math.cos(orientation[2]) * math.cos(math.pi / 2 - orientation[1])
    Z = math.sin(math.pi / 2 - orientation[1])
    return X, Y, Z


def getPlanesFromBlocks(app, blocks):
    planes = dict()
    for block in blocks:
        for plane in block.planes:
            planeStr = ";".join(f"{v[0]},{v[1]},{v[2]}" for v in plane)

            if planeStr not in planes:
                planes[planeStr] = {
                    "count": 0,
                    "selected": block.position == app.selectedBlockPosition,
                    "color": block.color,
                }
            planes[planeStr]["count"] += 1

    planesArr = []
    for planeStr, data in planes.items():
        # Only include visible (non-shared) planes
        if data["count"] == 1:
            vertices = [
                tuple(map(float, vertex.split(","))) for vertex in planeStr.split(";")
            ]
            planesArr.append((vertices, data["selected"], data["color"]))

    return planesArr


def findSelectedBlockPosition(app):
    camX, camY, camZ = copy.copy(app.camera.position)
    stepX, stepY, stepZ = getDirLengths(app.camera.orientation)
    for i in range(0, 100):
        X = camX - stepX / 10 * i
        Y = camY - stepY / 10 * i
        Z = camZ - stepZ / 10 * i
        if (
            f"{rounded(X)},{rounded(Y)},{rounded(Z)}"
            in app.world.blockPositionsStringSet
        ):
            app.selectedBlockPosition = (
                rounded(X),
                rounded(Y),
                rounded(Z),
            )
            return
    app.selectedBlockPosition = None


def isPointInPolygon(polygon, test_point):
    x, y = test_point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def getBlockPositionFromPlane(blocks, plane):
    for block in blocks:
        if plane in block.planes:
            return block


def findPlacingBlockPosition(blockPosition, blockFace):
    if blockPosition == None:
        return None
    if blockFace == 0:
        return (blockPosition[0], blockPosition[1], blockPosition[2] - 1)
    if blockFace == 1:
        return (blockPosition[0], blockPosition[1], blockPosition[2] + 1)
    if blockFace == 2:
        return (blockPosition[0], blockPosition[1] - 1, blockPosition[2])
    if blockFace == 3:
        return (blockPosition[0], blockPosition[1] + 1, blockPosition[2])
    if blockFace == 4:
        return (blockPosition[0] - 1, blockPosition[1], blockPosition[2])
    if blockFace == 5:
        return (blockPosition[0] + 1, blockPosition[1], blockPosition[2])


def updatePlanesToShow(app):
    blocks = app.world.getAllBlocks()

    if len(blocks) == 0:
        return

    planes = getPlanesFromBlocks(app, blocks)

    sortPlanesToCamera(planes, app.camera.position)

    app.planesToShow = planes


def updatePlanePointsOnScreen(app):
    newPlanePointsOnScreen = []
    for plane in app.planesToShow:
        points = []
        for point in plane[0]:
            p = getPositionOnScreen(app, point)
            if p:
                x, y = p
                points += [(x, y)]
        newPoints = []
        newPointsDifArr = []
        for i in range(-1, len(points) - 1):
            point1 = points[i]
            point2 = points[i + 1]
            clippedLine = cohenSutherlandClip(
                point1[0], point1[1], point2[0], point2[1], 0, 0, WIDTH, HEIGHT
            )
            if clippedLine:
                newPoints += [clippedLine[0], clippedLine[1]]
                newPoints += [clippedLine[2], clippedLine[3]]
                newPointsDifArr.append([clippedLine[0], clippedLine[1]])
                newPointsDifArr.append([clippedLine[2], clippedLine[3]])
        if len(newPoints) > 0:
            if plane[1] == True:
                if isPointInPolygon(newPointsDifArr, [WIDTH / 2, HEIGHT / 2]):
                    block = getBlockPositionFromPlane(
                        app.world.getAllBlocks(), plane[0]
                    )
                    app.selectedBlockFace = block.planes.index(plane[0])
            newPlanePointsOnScreen.append((newPoints, plane[1], plane[2]))
    app.planePointsOnScreen = newPlanePointsOnScreen
