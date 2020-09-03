"""

"""

import maya.cmds as cmds

import aligerTool.mayalib.nodeLib as nodeLib
import aligerTool.mayalib.attrLib as attrLib
from aligerTool.mayalib.ui_cmds.baseWindow import BaseWindow

import spaceController
reload(spaceController)
from spaceController import SpaceController

class SpaceSwitcher(BaseWindow):
    WINDOW_NAME = 'SpaceSwitcher'
    WINDOW_TITLE = 'Space Switcher'
    WIDTH = 300
    HEIGHT = 700
    SCROLLABLE = False

    CONSTRAINT_NODE_SUFFIX = '_SpaceSwitcher'
    DRIVEN_OB_ATTR = 'drivenObject'

    def __init__(self):
        super(SpaceSwitcher, self).__init__()
        # Key: Objeto Value: Instancia SpaceController
        self.__spaceControllers = {}

    def CreateCustomUI(self):
        """

        Returns:

        """
        cmds.frameLayout(label='Dynamic Spaces', width=self.WIDTH, marginHeight=5, marginWidth=5, collapsable=False)

        cmds.separator()
        self.searchSpaceButton = cmds.button('Search Dynamic Spaces', command=self.SearchSpaceControllers)
        self.addSpaceButton = cmds.button('Add Dynamic Space', backgroundColor=[0, 0.5, 0],
                                          command=self.AddSpaceController )

        self.spaceScroll = cmds.scrollLayout(width=self.WIDTH, height=self.HEIGHT - 100, parent=self.contentLayout)
        self.spaceContent = cmds.columnLayout(width=self.WIDTH - 20, adjustableColumn=True, parent=self.spaceScroll)

    def SearchSpaceControllers(self, *args):

        for spaceController in self.__spaceControllers.values():
            spaceController.DeleteUI()
        self.__spaceControllers.clear()

        nodeList = cmds.ls('*%s' % self.CONSTRAINT_NODE_SUFFIX)
        for node in nodeList:
            if attrLib.ExistAttr(node, self.DRIVEN_OB_ATTR):
                drivenNode = cmds.getAttr('%s.%s' % (node, self.DRIVEN_OB_ATTR))
                if drivenNode in self.__spaceControllers.keys():
                    cmds.warning('Objeto %s ya configurado con SpaceSwitcher' % drivenNode)
                    continue
                self.__spaceControllers[drivenNode] = SpaceController(drivenNode, node, self.spaceContent)

    def AddSpaceController(self, *arg):

        selection = cmds.ls(sl=True)
        if not selection or len(selection) == 0:
            cmds.warning('Seleccione un objeto para configurar SpaceSwitcher')
            return
        drivenNode = selection[0]
        if drivenNode in self.__spaceControllers.keys():
            cmds.warning('Objeto %s ya configurado con SpaceSwitcher' % drivenNode)
            return
        constraintNode = self.GetConstraintNode(drivenNode)
        if not constraintNode:
            constraintNode = nodeLib.CreateRootGroup(drivenNode, suffix=self.CONSTRAINT_NODE_SUFFIX)
            attrLib.AddAttrStr(constraintNode, self.DRIVEN_OB_ATTR, value=drivenNode) # Generamos atributo
        self.__spaceControllers[drivenNode] = SpaceController(drivenNode, constraintNode, self.spaceContent)



    def GetConstraintNode(self, node):
        """ """
        expected_name = node + self.CONSTRAINT_NODE_SUFFIX
        parent = cmds.listRelatives(node, parent=True)
        if parent and parent[0] == expected_name and attrLib.ExistAttr(parent, self.DRIVEN_OB_ATTR):
            return parent[0]
        return None
