
import maya.cmds as cmds

from baseWindow import BaseWindow

class ExampleWindow(BaseWindow):
    WINDOW_NAME = 'ExampleWindow'
    WINDOW_TITLE = 'Example Window by PlanetaCG'
    WIDTH = 300
    HEIGHT = 600
    SCROLLABLE = True

    def CreateCustomUI(self):
        """ """

        for i in xrange(100):
            cmds.button(i)