

import maya.cmds as cmds

def ExistAttr(node, attrName):
    """ True if an attribute exists, False otherwise """
    attrListLong = cmds.listAttr(node, string=attrName) or []
    attrListShort = cmds.listAttr(node, shortNames=True, string=attrName) or []
    attrList = attrListLong + attrListShort
    if attrList is None or len(attrList) == 0:
        return False
    return True

def AddAttrStr(node, attrName, niceName=None, value=None):
    """ Adds an string attribute to a node """
    if ExistAttr(node, attrName):
        return False
    if niceName == None:
        niceName = attrName
    cmds.addAttr(node, longName=attrName, niceName=niceName, dataType='string')
    if value:
        cmds.setAttr('%s.%s' % (node, attrName), value, type='string')