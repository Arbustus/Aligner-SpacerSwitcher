
import maya.cmds as cmds

class BaseWindow(object):

    WINDOW_NAME = 'BaseWindow'
    WINDOW_TITLE = 'Base Window with PlanetaCG'
    WIDTH = 300
    HEIGHT = 600
    SCROLLABLE = True

    def __init__(self):
        """ """
        self.CreateUI()

    def CreateUI(self):
        """ """
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME)

        # Window
        self.window = cmds.window(self.WINDOW_NAME, title=self.WINDOW_TITLE, width=self.WIDTH, height=self.HEIGHT,
                             sizeable=False, minimizeButton=False, maximizeButton=False)
        cmds.window(self.window, edit=True, width=self.WIDTH, height=self.HEIGHT)

        self.mainLayout = cmds.columnLayout('mainLayout', width=self.WIDTH)

        self.contentLayout = self.mainLayout

        if self.SCROLLABLE:
            self.scrollLayout = cmds.scrollLayout('scrollLayout', width=self.WIDTH, height=self.HEIGHT, parent=self.mainLayout)
            self.contentLayout = cmds.columnLayout('contentLayout', width=self.WIDTH - 16, parent=self.scrollLayout)

        self.CreateCustomUI()

        cmds.showWindow(self.window)

    def CreateCustomUI(self):
        """ """
        print 'BaseWindow.CreateCustomUI Override this fuction in child classes'