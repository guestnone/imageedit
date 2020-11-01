from PyQt5 import QtCore
from PyQt5.Qt3DCore import QTransform, QEntity
from PyQt5.Qt3DExtras import QPhongMaterial, QOrbitCameraController, Qt3DWindow, QTorusMesh, QSphereMesh, QCuboidMesh, \
    QTextureMaterial, QSkyboxEntity
from PyQt5 import Qt3DRender
from PyQt5.Qt3DRender import QTechnique, QRenderPass, QMaterial, QEffect, QShaderProgram
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, QPropertyAnimation, QRect, QByteArray
from PyQt5.QtGui import QMatrix4x4, QVector3D, QQuaternion, QPainter, QOpenGLShader, QOpenGLShaderProgram
from PyQt5.QtWidgets import QWidget, QDialog
import numpy as np


class OrbitTransformController(QObject):
    def __init__(self, parent):
        super(OrbitTransformController, self).__init__(parent)
        self.m_target = QTransform()
        self.m_matrix = QMatrix4x4()
        self.m_radius = 1.0
        self.m_angle = 0

    def getTarget(self):
        return self.m_target

    def setTarget(self, target):
        if self.m_target != target:
            self.m_target = target
            self.targetChanged.emit()

    def getRadius(self):
        return self.m_radius

    def setRadius(self, radius):
        if not QtCore.qFuzzyCompare(self.m_radius, radius):
            self.m_radius = radius
            self.updateMatrix()
            self.radiusChanged.emit()

    def getAngle(self):
        return self.m_angle

    def setAngle(self, angle):
        if not QtCore.qFuzzyCompare(angle, self.m_angle):
            self.m_angle = angle
            self.updateMatrix()
            self.angleChanged.emit()

    def updateMatrix(self):
        self.m_matrix.setToIdentity()
        self.m_matrix.rotate(self.m_angle, QVector3D(0, 1, 0))
        self.m_matrix.translate(self.m_radius, 0, 0)
        self.m_target.setMatrix(self.m_matrix)

    # QSignal
    targetChanged = pyqtSignal()
    radiusChanged = pyqtSignal()
    angleChanged = pyqtSignal()

    # Qt properties
    target = pyqtProperty(QTransform, fget=getTarget, fset=setTarget)
    radius = pyqtProperty(float, fget=getRadius, fset=setRadius)
    angle = pyqtProperty(float, fget=getAngle, fset=setAngle)


def generateRgbTexture():
    input = np.zeros(256, 256)

def getRgbCubeMaterial(entity):
    vertexShaderInput = """
     varying vec4 position; 
           // this is a varying variable in the vertex shader
         
        void main()
        {
            position = 0.5 * (gl_Vertex + vec4(1.0, 1.0, 1.0, 0.0));
               // Here the vertex shader writes output(!) to the 
               // varying variable. We add 1.0 to the x, y, and z 
               // coordinates and multiply by 0.5, because the 
               // coordinates of the cube are between -1.0 and 1.0 
               // but we need them between 0.0 and 1.0 
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
         }
    """

    fragmentShaderInput = """
     varying vec4 position; 
            // this is a varying variable in the fragment shader
         
         void main()
         {
            gl_FragColor = position;
               // Here the fragment shader reads intput(!) from the 
               // varying variable. The red, gree, blue, and alpha 
               // component of the fragment color are set to the 
               // values in the varying variable. (The alpha 
               // component of the fragment doesn't matter here.) 
         }
    """

    vertexShader = QOpenGLShader(QOpenGLShader.Vertex)
    vertexShader.compileSourceCode(vertexShaderInput)

    fragmentShader = QOpenGLShader(QOpenGLShader.Fragment)
    fragmentShader.compileSourceCode(fragmentShaderInput)

    program = QShaderProgram()
    program.setShaderCode(QShaderProgram.Vertex, QByteArray(bytes(vertexShaderInput, "UTF-8")))
    program.setShaderCode(QShaderProgram.Fragment, QByteArray(bytes(fragmentShaderInput, "UTF-8")))
    print(program.log())

    renderPass = QRenderPass()
    renderPass.setShaderProgram(program)
    technique = QTechnique()
    technique.addRenderPass(renderPass)
    effect = QEffect()
    effect.addTechnique(technique)
    material = QMaterial(entity)
    material.setEffect(effect)
    return material



class ThreeDeeCubeWindow(Qt3DWindow):
    def __init__(self):
        super().__init__()
        self.scene = self.createScene()

        # camera
        camera = self.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000)
        camera.setPosition(QVector3D(0, 0, 40))
        camera.setViewCenter(QVector3D(0, 0, 0))

        # for camera control
        self.camController = QOrbitCameraController(self.scene)
        self.camController.setLinearSpeed(50.0)
        self.camController.setLookSpeed(180.0)
        self.camController.setCamera(camera)

        self.setRootEntity(self.scene)
        self.show()

    def createScene(self):
        # root
        rootEntity = QSkyboxEntity()
        material = QPhongMaterial(rootEntity)
        #skybox = QSkyboxEntity(rootEntity)

        # torus
        cubeEntity = QEntity(rootEntity)
        cubeMesh = QCuboidMesh()
        cubeTransform = QTransform()
        #cubeMaterial = getRgbCubeMaterial(cubeEntity)
        cubeMaterial = QPhongMaterial(cubeEntity)
        cubeTransform.setTranslation(QVector3D(5.0, -4.0, 0.0))
        cubeTransform.setScale(4.0)
        cubeTransform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(1, 0, 0), 45))

        cubeEntity.addComponent(cubeMesh)
        cubeEntity.addComponent(cubeTransform)
        cubeEntity.addComponent(cubeMaterial)

        return rootEntity
