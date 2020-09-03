
import maya.cmds as cmds

import aligerTool.mayalib.alignLib as alingLib

WINDOW_NAME = 'AlignWindow'
WINDOW_TITLE = 'Align Window'
WIDTH = 300
HEIGHT = 150

widgets = {}

def UI():

    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME)

    # Window
    window = cmds.window(WINDOW_NAME, title=WINDOW_TITLE, width=WIDTH, height=HEIGHT,
                         sizeable=False, minimizeButton=False, maximizeButton=False)
    cmds.window(window, edit=True, width=WIDTH, height=HEIGHT)
    widgets['window'] = window

    # Main Layout
    mainLayout = cmds.columnLayout('mainLayout', width=WIDTH, rowSpacing=5)
    widgets['mainLayout'] = mainLayout

    cmds.separator(height=10)
    cmds.text('Seleciona target y uno o varios objetos a alinear', width=WIDTH, align='center')
    cmds.separator(height=5)

    # Row Layout
    cmds.frameLayout(label='Opciones de alineacion', width=WIDTH, collapsable=False)
    cmds.separator(height=1)
    w = WIDTH/3
    cmds.rowLayout('checkLayout', numberOfColumns=3, columnWidth=[(1, w), (2, w), (3, w)])
    widgets['checkPosition'] = cmds.checkBox(label='Position')
    widgets['checkRotation'] = cmds.checkBox(label='Rotation')
    widgets['checkScale'] = cmds.checkBox(label='Scale')

    cmds.setParent(mainLayout)
    cmds.separator(height=10)
    cmds.columnLayout(width=WIDTH, columnWidth=WIDTH, columnAttach=('both', 100))
    cmds.button(label='Align', height=40, backgroundColor=(0, 0.75, 0), command=HandleAlignButton)

    cmds.showWindow(window)


def HandleAlignButton(*args):

    selection = cmds.ls(sl=1)
    print selection
    if len(selection) < 2:
        cmds.error('Seleciona target y uno o varios objetos a alinear')
        return

    position = cmds.checkBox(widgets['checkPosition'], query=True, value=True)
    rotation = cmds.checkBox(widgets['checkRotation'], query=True, value=True)
    scale = cmds.checkBox(widgets['checkScale'], query=True, value=True)

    target = selection[0]
    for index in range(1, len(selection)):
        alingLib.AlinearObjetos(target, selection[index], posicion=position, rotacion=rotation, escala=scale)