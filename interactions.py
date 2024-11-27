#################################################
#                                               #
#            Interaction Functions              #
#                                               #
#################################################


import copy
import math
from cmu_graphics import *
from utils import *


def onKeyHold(app, keys):
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
        app.camera.changePositionX(app.camera.position[0] - stepX)
        app.camera.changePositionY(app.camera.position[1] - stepY)
        app.camera.changePositionZ(app.camera.position[2] - stepZ)
    if "s" in keys:
        app.camera.changePositionX(app.camera.position[0] + stepX)
        app.camera.changePositionY(app.camera.position[1] + stepY)
        app.camera.changePositionZ(app.camera.position[2] + stepZ)
    if "a" in keys:
        stepY = math.sin(app.camera.orientation[2] - math.pi / 2)
        stepX = math.cos(app.camera.orientation[2] - math.pi / 2)
        app.camera.changePositionX(app.camera.position[0] + stepX)
        app.camera.changePositionY(app.camera.position[1] + stepY)
    if "d" in keys:
        stepY = math.sin(app.camera.orientation[2] + math.pi / 2)
        stepX = math.cos(app.camera.orientation[2] + math.pi / 2)
        app.camera.changePositionX(app.camera.position[0] + stepX)
        app.camera.changePositionY(app.camera.position[1] + stepY)
    app.selectedBlockPosition = None


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
    app.selectedBlockPosition = None


def onMouseRelease(app, mouseX, mouseY, button):
    app.dragStartingPosition = None
    app.selectedBlockPosition = None


def onMousePress(app, mouseX, mouseY, label):
    if label == 2:
        if app.selectedBlockPosition:
            app.world.deleteBlock(app.selectedBlockPosition)
