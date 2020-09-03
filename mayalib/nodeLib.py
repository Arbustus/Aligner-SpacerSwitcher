"""

"""

import maya.cmds as cmds

def CreateRootGroup(node, name='', suffix='_root', zero_group=True):
    ''' '''
    groupName = name
    if not groupName: # groupName == None or len(groupName) == 0
        groupName = node
    groupName += suffix
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    group = cmds.group(name=groupName, empty=True, world=True)
    if parent:
        group = cmds.parent(group, parent)[0]
    if zero_group:
        matrix = cmds.xform(node, q=1, matrix=1, worldSpace=1)
        cmds.xform(group, matrix = matrix, worldSpace=1)
    cmds.parent(node, group)
    return group

def GetConstraint(node, constraintType='parentConstraint'):
    """ """
    constraintList = cmds.listRelatives(node, children=True, type=constraintType)
    if constraintList:
        return constraintList[0]
    return None


def GetConstraintData(constraint):
    """Given a constraint, returns the drivers and weightAlias of the constraint as a Tuple"""
    allowed_constraint_types = ['parentConstraint', 'orientConstraint', 'scaleConstraint']
    if cmds.objExists(constraint) == False:
        cmds.warning('GetConstraintData Constraint %s does not exist' % constraint)
        return None, None
    constraintType = cmds.objectType(constraint)
    if constraintType not in allowed_constraint_types:
        cmds.warning('Constraint type %s not supported' % constraintType)
        return None, None
    if constraintType == 'parentConstraint':
        targetList = cmds.parentConstraint(constraint, q=1, targetList=1) or []
        weightAliasList = cmds.parentConstraint(constraint, q=1, weightAliasList=1) or []
    elif constraintType == 'orientConstraint':
        targetList = cmds.orientConstraint(constraint, q=1, targetList=1) or []
        weightAliasList = cmds.orientConstraint(constraint, q=1, weightAliasList=1) or []
    else:
        targetList = cmds.scaleConstraint(constraint, q=1, targetList=1) or []
        weightAliasList = cmds.scaleConstraint(constraint, q=1, weightAliasList=1) or []

    return targetList, weightAliasList