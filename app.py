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

colors = [
    "black",
    "darkBlue",
    "darkGreen",
    "darkCyan",
    "darkRed",
    "indigo",
    "goldenrod",
    "lightGray",
    "darkGray",
    "blue",
]


def onAppStart(app):
    # app.setMaxShapeCount(100000)
    app.RES = app.WIDTH, app.HEIGHT = WIDTH, HEIGHT
    app.camera = Camera((0, 0, 0), [], (0, math.pi / 2, 0))
    app.dragStartingPosition = None
    app.world = World()
    app.selectedBlockPosition = None
    app.selectedBlockFace = None

    app.stepsPerSecond = 60
    app.start_time = time.perf_counter()
    app.frame_count = 0
    app.fps = 0

    app.planesToShow = []
    app.planePointsOnScreen = []

    app.colors = colors
    app.selectedColorIndex = 0

    for i in range(-7, 8):
        for j in range(-7, 8):
            app.world.createBlock((i, j, 0), "green")
    app.world.createBlock((0, 0, 1), "brown")
    app.world.createBlock((0, 0, 2), "brown")
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


def drawPlane(plane, selected, color):
    drawPolygon(
        *plane,
        fill=color,
        border="red" if selected == True else "black",
        borderWidth=2 if selected == True else 0.4,
    )


def drawInventory(app):

    startingX = (WIDTH - len(colors) * 24) / 2
    startingY = HEIGHT - 24
    for i in range(len(colors)):
        drawRect(
            startingX + i * 24,
            startingY,
            24,
            24,
            fill=colors[i],
            border="white" if app.selectedColorIndex != i else "grey",
        )


def redrawAll(app):
    for plane in app.planePointsOnScreen:
        drawPlane(plane[0], plane[1], plane[2])

    # Draws center pointer
    drawRect(WIDTH / 2, HEIGHT / 2, 2, 8, align="center", fill="black")
    drawRect(WIDTH / 2, HEIGHT / 2, 8, 2, align="center", fill="black")
    drawLabel(f"{app.fps} FPS", 5, 5, fill="black", align="left-top")

    drawInventory(app)


def onStep(app):
    updatePlanesToShow(app)
    findSelectedBlockPosition(app)
    updatePlanePointsOnScreen(app)
    app.frame_count += 1
    current_time = time.perf_counter()
    elapsed_time = current_time - app.start_time

    # Calculate and display FPS every second
    if elapsed_time > 1.0:
        app.fps = math.ceil(app.frame_count / elapsed_time)
        # Reset counters
        app.start_time = current_time
        app.frame_count = 0


def main():
    runApp(WIDTH, HEIGHT)


main()
