
import maya.cmds as cmds
import aligerTool.mayalib.nodeLib as nodeLib
reload(nodeLib)
import aligerTool.mayalib.animLib as animLib
reload(animLib)

class SpaceController():
    def __init__(self, driven, constrained, parentWidget):
        self.drivenNode = driven
        self.constrainedNode = constrained
        self.parentWidget = parentWidget

        self.__constraint = None
        self.__targetList = []
        self.__weightAliasList = []
        self.__currentSpace = 'None'

        #Key: Object Value: menuItem
        self.__spaceDict = {}

        self.CreateUI()
        self.InitSpaces()

    def CreateUI(self):
        """ Create UI"""
        if self.parentWidget:
            cmds.setParent(self.parentWidget)

        self.frameLayout = cmds.frameLayout('Space %s' % self.drivenNode, marginHeight=5, marginWidth=5,
                                            backgroundShade=True)
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2)
        cmds.text(label='Driven: ')
        cmds.textField(text=self.drivenNode, editable=False)   # Driven Node
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2, parent=self.frameLayout)
        cmds.text(label='Constraint: ')
        cmds.textField(text=self.constrainedNode, editable=False)  # Constraint Node

        cmds.rowLayout(numberOfColumns=3, parent=self.frameLayout, adjustableColumn=1)
        cmds.text('')
        cmds.button('Add Space', backgroundColor=[0, 0.5, 0], command=self.AddSpace)
        cmds.button('Del Space', backgroundColor=[0.5, 0, 0], command=self.RemoveSpace)

        cmds.rowLayout(numberOfColumns=4, parent=self.frameLayout, adjustableColumn=1)
        self.spaceOptionMenu = cmds.optionMenu(label='Space: ', changeCommand=self.SwitchSpace)
        cmds.menuItem(label='None')
        cmds.button('Spa', backgroundColor=[0.5, 0, 0], command=self.AddKeySpace)
        cmds.button('Pos', backgroundColor=[0.5, 0, 0], command=self.AddKeyPos)
        cmds.button('Rot', backgroundColor=[0.5, 0, 0], command=self.AddKeyRot)

    def DeleteUI(self):
        """ """
        cmds.deleteUI(self.frameLayout)

    def InitSpaces(self):
        """ """
        self.__UpdateConstraintInfo()
        for spaceObject in self.__targetList:
            self.__spaceDict[spaceObject] = cmds.menuItem(label=spaceObject, parent=self.spaceOptionMenu)
        self.__currentSpace = self.GetCurrentSpace()
        cmds.optionMenu(self.spaceOptionMenu, edit=True, value=self.__currentSpace)

    def __UpdateConstraintInfo(self):
        self.__constraint = nodeLib.GetConstraint(self.constrainedNode)
        if self.__constraint:
            self.__targetList, self.__weightAliasList = nodeLib.GetConstraintData(self.__constraint)
        else:
            self.__targetList = []
            self.__weightAliasList = []

    def GetCurrentSpace(self):
        """ """
        if self.__constraint:
            for index, space in enumerate(self.__targetList):
                weight = cmds.getAttr('%s.%s' % (self.__constraint, self.__weightAliasList[index]))
                if weight > 0.5:
                    return space
        return 'None'



    def AddSpace(self, *args):
        """ """
        selection = cmds.ls(sl=1)
        if not selection:
            cmds.warning('Seleccione un objeto para configurar el Space')
            return
        if len(selection) > 1:
            cmds.warning('Seleccione un objeto para configurar el Space')
            return
        spaceObject = selection[0]
        if spaceObject in self.__spaceDict.keys():
            cmds.warning('Objeto %s ya es un Space configurado' % spaceObject)
            return

        self.__spaceDict[spaceObject] = cmds.menuItem(label=spaceObject, parent=self.spaceOptionMenu)
        cmds.parentConstraint(spaceObject, self.constrainedNode, mo=True, weight=0.0)

        self.__UpdateConstraintInfo()

    def RemoveSpace(self, *args):
        """ """
        space = cmds.optionMenu(self.spaceOptionMenu, query=1, value=True)
        if space == 'None':
            return

        cmds.deleteUI(self.__spaceDict[space])
        cmds.parentConstraint(space, self.constrainedNode, e=1, remove=1)
        del self.__spaceDict[space]

        self.__UpdateConstraintInfo()

        self.__currentSpace = self.GetCurrentSpace()
        cmds.optionMenu(self.spaceOptionMenu, edit=1, value=self.__currentSpace)

    def SwitchSpace(self, space):
        """ """
        if self.__currentSpace == space:
            return

        matrix = cmds.xform(self.drivenNode, query=True, matrix=True, worldSpace=True)

        for index, attr in enumerate(self.__weightAliasList):
            w = 0.0
            if self.__targetList[index] == space:
                w = 1.0
            cmds.setAttr('%s.%s' % (self.__constraint, attr), w)

        cmds.xform(self.drivenNode, matrix=matrix, worldSpace=True)
        self.__currentSpace = space

    def AddKeySpace(self, *args):
        """ """
        time = cmds.currentTime(query=True)
        for weightAlias in self.__weightAliasList:
            weight = cmds.getAttr('%s.%s' % (self.__constraint, weightAlias))
            animLib.SetKeyframe(self.__constraint, weightAlias, weight, time, animLib.TAN_LINEAR, animLib.TAN_LINEAR)

    def AddKeyPos(self, *args):
        """ """
        animLib.SetCurrentPosKey(self.drivenNode, animLib.TAN_LINEAR, animLib.TAN_LINEAR)

    def AddKeyRot(self, *args):
        """ """
        animLib.SetCurrentRotKey(self.drivenNode, animLib.TAN_LINEAR, animLib.TAN_LINEAR)