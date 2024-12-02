#################################################
# app.py
#
# Your name: Enkhmunkh Enkhbayar
# Your andrew id: eenkhbay
#################################################

#################################################
#                                               #
#               Graphics Functions              #
#                                               #
#################################################

import math
import time
import json


from cmu_graphics import *
from classes import *
from utils import *
from interactions import *


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

    # Menu and Start
    app.mouseX = 0
    app.mouseY = 0
    app.selectedWorld = 0
    app.deleteSound = Sound("./assets/break.mp3")
    app.placeSound = Sound("./assets/place.mp3")

    # for i in range(-7, 8):
    #     for j in range(-7, 8):
    #         app.world.createBlock((i, j, 0), "green")
    # app.world.createBlock((0, 0, 1), "brown")
    # app.world.createBlock((0, 0, 2), "brown")
    # app.world.createBlock((0, 0, 6), "brown")
    # for i in range(-2, 3):
    #     for j in range(-2, 3):
    #         for l in range(2):
    #             app.world.createBlock((i, j, 3 + l), "brown")
    # for i in range(-1, 2):
    #     for j in range(-1, 2):
    #         app.world.createBlock((i, j, 5), "brown")

    # app.world.createBlock((-1, 0, 6), "brown")
    # app.world.createBlock((1, 0, 6), "brown")
    # app.world.createBlock((0, -1, 6), "brown")
    # app.world.createBlock((0, 1, 6), "brown")


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


def game_redrawAll(app):
    for plane in app.planePointsOnScreen:
        drawPlane(plane[0], plane[1], plane[2])

    # Draws center pointer
    drawRect(WIDTH / 2, HEIGHT / 2, 2, 8, align="center", fill="black")
    drawRect(WIDTH / 2, HEIGHT / 2, 8, 2, align="center", fill="black")
    drawLabel(f"{app.fps} FPS", 5, 5, fill="black", align="left-top")

    drawInventory(app)


def game_onStep(app):
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


# Main Screen


def start_redrawAll(app):
    drawImage("./assets/main.png", 0, 0)
    drawButton(app, "Play", 175, 55, WIDTH / 2, 500)


def drawButton(app, label, width, height, x, y, size=32):
    drawRect(x, y, width, height, align="center", fill=rgb(204, 204, 204))
    drawRect(x + 1, y + 1, width - 2, height - 2, align="center", fill=rgb(87, 87, 87))
    if checkMouseHoveringButton(app.mouseX, app.mouseY, x, y, width, height):
        drawRect(x, y, width - 2, height - 2, align="center", fill=rgb(87, 87, 87))
    else:
        drawRect(x, y, width - 2, height - 2, align="center", fill=rgb(111, 111, 111))
    drawLabel(label, x, y, size=size, fill="white", font="monospace", bold=True)


# Worlds Screen


def menu_onScreenActivate(app):
    with open("main.json", "r") as file:
        app.worlds = json.load(file)


def menu_redrawAll(app):
    drawImage("./assets/menu.png", 0, 0)
    drawLabel("Worlds:", WIDTH / 2, 100)
    for worldIndex in range(len(app.worlds)):
        drawRect(
            50,
            250
            + 25 * worldIndex
            + 100 * worldIndex
            - (125 * (app.selectedWorld - 2) if app.selectedWorld > 2 else 0),
            700,
            100,
            border="white" if worldIndex == app.selectedWorld else None,
            borderWidth=2,
            fill=None,
        )
        drawLabel(
            app.worlds[worldIndex]["name"],
            70,
            280
            + 25 * worldIndex
            + 100 * worldIndex
            - (125 * (app.selectedWorld - 2) if app.selectedWorld > 2 else 0),
            fill="white",
            align="left",
            bold=True,
            size=24,
            font="monospace",
        )
        drawLabel(
            "Last saved: " + app.worlds[worldIndex]["updatedAt"],
            70,
            320
            + 25 * worldIndex
            + 100 * worldIndex
            - (125 * (app.selectedWorld - 2) if app.selectedWorld > 2 else 0),
            fill=rgb(184, 182, 181),
            align="left",
            size=24,
            bold=True,
            font="monospace",
        )
    drawImage("./assets/menuTop.png", 0, 0)
    drawImage("./assets/menuBottom.png", 0, 695)
    drawButton(app, "Create New World", 275, 55, 187.5, 747.5, 24)
    drawButton(app, "Delete", 105, 55, 387.5, 747.5, 24)
    drawButton(app, "Play Selected World", 300, 55, 600, 747.5, 24)


def initializeGame(app):
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


def menu_onMousePress(app, mouseX, mouseY, label):
    if 187.5 - 275 / 2 < mouseX < 187.5 + 275 / 2:
        if 747.5 - 55 / 2 < mouseY < 747.5 + 55 / 2:
            print("Create New World")
            createWorld(app)
    if 387.5 - 105 / 2 < mouseX < 387.5 + 105 / 2:
        if 747.5 - 55 / 2 < mouseY < 747.5 + 55 / 2:
            if len(app.worlds) > app.selectedWorld:
                deleteWorld(app.worlds[app.selectedWorld]["name"])
    if 600 - 300 / 2 < mouseX < 600 + 300 / 2:
        if 747.5 - 55 / 2 < mouseY < 747.5 + 55 / 2:
            if len(app.worlds) > app.selectedWorld:
                initializeGame(app)
                loadWorld(app, app.worlds[app.selectedWorld]["name"])
                print("Play Selected World")
                setActiveScreen("game")


def main():
    runAppWithScreens(initialScreen="start", width=WIDTH, height=HEIGHT)


main()
