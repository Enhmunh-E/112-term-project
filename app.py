#################################################
# app.py
#
# Your name: Enkhmunkh Enkhbayar
# Your andrew id: eenkhbay
#################################################


import math
import time

from cmu_graphics import *
from classes import *
from utils import *
from interactions import *


#################################################
#                                               #
#               Graphics Functions              #
#                                               #
#################################################

WIDTH, HEIGHT = 800, 800
MAXRES = max(WIDTH, HEIGHT)


def onAppStart(app):
    # app.setMaxShapeCount(100000)
    app.RES = app.WIDTH, app.HEIGHT = WIDTH, HEIGHT
    app.camera = Camera((0, 0, 0), [], (0, math.pi / 2, 0))
    app.dragStartingPosition = None
    app.world = World()
    app.selectedBlockPosition = None

    app.stepsPerSecond = 60
    app.start_time = time.perf_counter()
    app.frame_count = 0
    app.fps = 0

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


def drawPlane(plane, app, color):
    points = []
    for point in plane[0]:
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
    drawPolygon(
        *newPoints,
        fill=color,
        border="red" if plane[1] == True else "black",
        borderWidth=2 if plane[1] == True else 0.4,
    )


def redrawAll(app):
    blocks = app.world.getAllBlocks()

    if len(blocks) == 0:
        return

    planes = getPlanesFromBlocks(app, blocks)

    sortPlanesToCamera(planes, app.camera.position)

    for plane in planes:
        drawPlane(plane, app, "green")

    # Draws center pointer
    drawRect(WIDTH / 2, HEIGHT / 2, 2, 8, align="center", fill="black")
    drawRect(WIDTH / 2, HEIGHT / 2, 8, 2, align="center", fill="black")
    drawLabel(f"{app.fps} FPS", 5, 5, fill="black", align="left-top")


def onStep(app):
    app.frame_count += 1
    current_time = time.perf_counter()
    elapsed_time = current_time - app.start_time

    # Calculate and display FPS every second
    if elapsed_time > 1.0:
        app.fps = math.ceil(app.frame_count / elapsed_time)
        # Reset counters
        app.start_time = current_time
        app.frame_count = 0

    findSelectedBlockPosition(app)
    pass


def main():
    runApp(WIDTH, HEIGHT)


main()
