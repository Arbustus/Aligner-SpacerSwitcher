
import maya.cmds as cmds

def AlinearObjetos(target, object, posicion = False, rotacion = False, escala = False):
    """
    Alinea dos objetos en posicion, rotacion o escala
    target: nombre del objeto usado como referencia
    object: nombre del objeto a alinear
    posicion: True para alinear en posicion
    rotacion: True para alinear en rotacion
    escala: True para alinear en escala
    return: True si la operacion se ha ejecutado correctamente, False en caso contrario
    """
    
    #Asi sabemos que los dos objetos existen
    if cmds.objExists(target) == False:
        cmds.warning("Target %s no existe" % target)
        return False
        
    if cmds.objExists(object) == False:
        cmds.warning("Object %s no existe" % object)
        return False
        
    
    #Ejecutamos los constraint
    
    if posicion == True:
        constraint = cmds.pointConstraint(target, object, mo = 0)
        cmds.delete(constraint)
        
    if rotacion == True:
        constraint = cmds.orientConstraint(target, object, mo = 0)
        cmds.delete(constraint)
        
    if escala == True:
        constraint = cmds.scaleConstraint(target, object, mo = 0)
        cmds.delete(constraint)
        
    return True