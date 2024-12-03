#################################################
#                                               #
#            Interaction Functions              #
#                                               #
#################################################


import math
from cmu_graphics import *
from utils import *


def game_onKeyHold(app, keys):
    if "down" in keys:
        app.camera.changePositionX(app.camera.position[0] + 0.4)
    if "up" in keys:
        app.camera.changePositionX(app.camera.position[0] - 0.4)
    if "right" in keys:
        app.camera.changePositionY(app.camera.position[1] + 0.4)
    if "left" in keys:
        app.camera.changePositionY(app.camera.position[1] - 0.4)
    if "," in keys:
        app.camera.changePositionZ(app.camera.position[2] + 0.4)
    if "." in keys:
        app.camera.changePositionZ(app.camera.position[2] - 0.4)
    stepX, stepY, stepZ = getDirLengths(app.camera.orientation)
    if "w" in keys:
        app.camera.changePositionX(app.camera.position[0] - stepX * 0.4)
        app.camera.changePositionY(app.camera.position[1] - stepY * 0.4)
        app.camera.changePositionZ(app.camera.position[2] - stepZ * 0.4)
    if "s" in keys:
        app.camera.changePositionX(app.camera.position[0] + stepX * 0.4)
        app.camera.changePositionY(app.camera.position[1] + stepY * 0.4)
        app.camera.changePositionZ(app.camera.position[2] + stepZ * 0.4)
    if "a" in keys:
        stepY = math.sin(app.camera.orientation[2] - math.pi / 2)
        stepX = math.cos(app.camera.orientation[2] - math.pi / 2)
        app.camera.changePositionX(app.camera.position[0] + stepX * 0.4)
        app.camera.changePositionY(app.camera.position[1] + stepY * 0.4)
    if "d" in keys:
        stepY = math.sin(app.camera.orientation[2] + math.pi / 2)
        stepX = math.cos(app.camera.orientation[2] + math.pi / 2)
        app.camera.changePositionX(app.camera.position[0] + stepX * 0.4)
        app.camera.changePositionY(app.camera.position[1] + stepY * 0.4)
    app.selectedBlockPosition = None


def game_onMouseDrag(app, mouseX, mouseY):
    if app.dragStartingPosition:
        # Meaning it has already started dragging
        disX = app.dragStartingPosition[0] - mouseX
        disY = app.dragStartingPosition[1] - mouseY
        app.camera.changeOrientation(
            0, math.pi / 180 * disY / 10, math.pi / 180 * disX / 10
        )
    app.dragStartingPosition = (mouseX, mouseY)
    app.selectedBlockPosition = None


def game_onMouseRelease(app, mouseX, mouseY):
    app.dragStartingPosition = None
    app.selectedBlockPosition = None


def game_onMousePress(app, posX, posY, label):
    if label == 2:
        if app.selectedBlockPosition:
            if len(app.world.getAllBlocks()) > 1:
                app.world.deleteBlock(app.selectedBlockPosition)
    pass


def game_onKeyPress(app, key):
    if key == "f":
        position = findPlacingBlockPosition(
            app.selectedBlockPosition, app.selectedBlockFace
        )
        if position:
            if (
                f"{position[0]},{position[1]},{position[2]}"
                not in app.world.blockPositionsStringSet
            ):
                app.placeSound.play(restart=True)
                app.world.createBlock(position, app.colors[app.selectedColorIndex])
    if key in "0123456789":
        keyNum = int(key)
        if key == "0":
            app.selectedColorIndex = 9
        else:
            app.selectedColorIndex = keyNum - 1
    if key == "escape":
        app.clickSound.play(restart=True)
        saveWorld(app)
        setActiveScreen("menu")


# Main Screen


def start_onMousePress(app, mouseX, mouseY, label):
    if (
        400 + 175 / 2 >= mouseX >= 400 - 175 / 2
        and 520 - 55 / 2 <= mouseY <= 520 + 55 / 2
    ):
        app.clickSound.play(restart=True)
        setActiveScreen("menu")


def start_onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY


# def start_onKeyPress(app, key):
#     if key == "escape":
#         exit()


# Menu


def menu_onKeyPress(app, key):
    if key == "up":
        if app.selectedWorld != 0:
            app.clickSound.play(restart=True)
            app.selectedWorld -= 1
    if key == "down":
        if app.selectedWorld < len(app.worlds) - 1:
            app.clickSound.play(restart=True)
            app.selectedWorld += 1
    if key == "escape":
        app.clickSound.play(restart=True)
        setActiveScreen("start")


def menu_onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY
