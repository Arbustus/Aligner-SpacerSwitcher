"""

"""

import maya.cmds as cmds

TAN_AUTO = 'auto'
TAN_CLAMPED = 'clamped'
TAN_FAST = 'fast'
TAN_FLAT = 'flat'
TAN_LINEAR = 'linear'
TAN_PLATEAU = 'plateau'
TAN_SLOW = 'slow'
TAN_SPLINE = 'spline'
TAN_STEP = 'step'
TAN_STEPNEXT = 'stepnext'


def SetKeyframe(node, attr, value, time, inTangent=TAN_LINEAR, outTangent=TAN_LINEAR):
    """ Set a keyframe"""
    cmds.setKeyframe(node, attribute=attr, t=time, value=value, inTangentType=inTangent, outTangentType=outTangent)

def SetPosKeyframe(node, value, time, inTangent=TAN_LINEAR, outTangent=TAN_LINEAR):
    """ Set a position keyframe"""
    SetKeyframe(node, 'translateX', float(value[0]), time, inTangent, outTangent)
    SetKeyframe(node, 'translateY', float(value[1]), time, inTangent, outTangent)
    SetKeyframe(node, 'translateZ', float(value[2]), time, inTangent, outTangent)


def SetRotKeyframe(node, value, time, inTangent=TAN_LINEAR, outTangent=TAN_LINEAR):
    """ Set a rotation keyframe"""
    SetKeyframe(node, 'rotateX', float(value[0]), time, inTangent, outTangent)
    SetKeyframe(node, 'rotateY', float(value[1]), time, inTangent, outTangent)
    SetKeyframe(node, 'rotateZ', float(value[2]), time, inTangent, outTangent)


def SetCurrentPosKey(node, inTangent=TAN_LINEAR, outTangent=TAN_LINEAR):
    """ Set position keyframe with current value and current time """
    position = cmds.getAttr('%s.translate' % node)[0]
    time = cmds.currentTime(query=True)
    SetPosKeyframe(node, position, time, inTangent, outTangent)

def SetCurrentRotKey(node, inTangent=TAN_LINEAR, outTangent=TAN_LINEAR):
    """ Set rotation keyframe with current value and current time """
    rotation = cmds.getAttr('%s.rotate' % node)[0]
    time = cmds.currentTime(query=True)
    SetRotKeyframe(node, rotation, time, inTangent, outTangent)