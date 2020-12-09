from enum import Enum

import cv2
import numpy as np
import qimage2ndarray
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QWidget

from Binarization import OtsuBinarize
from HistogramUtility import BeforeAfterHistogramDialog
from MorphOpsDialog import Ui_MorphOpsDialog


############################################
#  DILATION, EROSION, OPENING AND CLOSING  #
############################################

def getMaxTypeValue(type='uint8'):
    if type == 'uint8':
        return 255
    if type == 'binary':
        return 1
    if type == 'int32':
        return 2147483647
    return 1


def negate(inputImage):
    return (getImageLimits(inputImage)[0] + getImageLimits(inputImage)[1] - inputImage).astype(inputImage.dtype)


def binaryToGrayScale(inputImage, dtype="uint8"):
    maxPixelValue = getMaxTypeValue(dtype)
    if dtype == 'uint8':
        return np.array(np.clip(inputImage * maxPixelValue, 0, 255), np.uint8)
    else:
        return toInt32(inputImage * maxPixelValue) - toInt32(negate(inputImage) * getMaxTypeValue(dtype))


def getImageLimits(inputImage):
    if inputImage.dtype == np.bool:
        return np.array([0, 1])
    if inputImage.dtype == np.uint8:
        return np.array([0, 255])
    if inputImage.dtype == np.int32:
        return np.array([-2147483647, 2147483647])


def isBinary(inputImage):
    return inputImage.dtype == bool


def createImageIntersection(first, second):
    return np.minimum(first, second).astype(first.dtype)


def matrixToSet(matrixImage):
    if len(matrixImage.shape) == 1:
        matrixImage = matrixImage[np.newaxis, :]
    offsets = np.nonzero(np.ravel(matrixImage) - getImageLimits(matrixImage)[0])[0]
    if len(offsets) == 0:
        return [], []
    height, width = matrixImage.shape
    outCoords = [0, 1]
    outCoords[0] = offsets // width - (height - 1) // 2
    outCoords[1] = offsets % width - (width - 1) // 2
    outCoords = np.transpose(outCoords)
    outValues = np.take(np.ravel(matrixImage), offsets)
    return outCoords, outValues


def toInt32(value):
    return np.asanyarray(value).astype(np.int32)


def setToMatrix(inputSet):
    coords, values = inputSet
    values = np.asarray(values)
    maxHeight, maxWidth = abs(coords).max(0)
    height, width = (2 * maxHeight) + 1, (2 * maxWidth) + 1
    output = np.ones((height, width), np.int32) * getImageLimits(values)[0]
    offset = coords[:, 0] * width + coords[:, 1] + (maxHeight * width + maxWidth)
    np.put(output, offset, values)
    return output.astype(values.dtype)


def binary(inputImage, value=1):
    return np.asanyarray(inputImage) >= value


def getDefaultStructuringElement():
    return binary([[0, 1, 0],
                   [1, 1, 1],
                   [0, 1, 0]])


def dilationAddition(inputImage, value):
    if not value:
        return inputImage
    y = np.asarray(inputImage, np.float64) + value
    limitMin, limitMax = getImageLimits(inputImage)
    y = ((inputImage == limitMin) * limitMin) + ((inputImage != limitMin) * y)
    return np.maximum(np.minimum(y, limitMax), limitMin).astype(inputImage.dtype)


def performErosion(inputImage, structurizingElement=None):
    if structurizingElement is None:
        structurizingElement = getDefaultStructuringElement()

    structurizingElement = structurizingElement != 0
    height, width = inputImage.shape
    coords, values = matrixToSet(structurizingElement)

    if isBinary(values):
        values = createImageIntersection(binaryToGrayScale(values, 'int32'), 0)
    maxHeight, maxWidth = max(abs(coords)[:, 0]), max(abs(coords)[:, 1])
    y = (np.ones((height + 2 * maxHeight, width + 2 * maxWidth), np.int32) * getImageLimits(inputImage)[0]).astype(
        inputImage.dtype)
    for i in range(coords.shape[0]):
        if values[i] > -2147483647:
            y[maxHeight + coords[i, 0]:maxHeight + coords[i, 0] + height,
            maxWidth + coords[i, 1]:maxWidth + coords[i, 1] + width] = np.maximum(
                y[maxHeight + coords[i, 0]:maxHeight + coords[i, 0] + height,
                maxWidth + coords[i, 1]:maxWidth + coords[i, 1] + width], dilationAddition(inputImage, values[i]))

    return y[maxHeight:maxHeight + height, maxWidth:maxWidth + width]


def performDilation(inputImage, structurizingElement=None):
    if structurizingElement is None:
        structurizingElement = getDefaultStructuringElement()
    # Use erosion to perform dilation by doing some tricks related to negating
    return negate(performErosion(negate(inputImage), structurizingElement[::-1, ::-1]))


def performClosing(inputImage):
    structurizingElement = getDefaultStructuringElement()
    return performErosion(performDilation(inputImage, structurizingElement), structurizingElement)


def performOpening(inputImage):
    structurizingElement = getDefaultStructuringElement()
    return performDilation(performErosion(inputImage, structurizingElement), structurizingElement)


##########################
#  HIT OR MISS THINNING  #
##########################

def createHitOrMissTemplate(leftExtermity, complementOfRightExtermity):
    return leftExtermity, complementOfRightExtermity


def rotateStructuralElement(element, theta=45):
    theta = np.pi * theta / 180.
    coords, values = matrixToSet(element)
    if len(coords) == 0:
        return binary([0])
    x0 = coords[:, 1] * np.cos(theta) - coords[:, 0] * np.sin(theta)
    x1 = coords[:, 1] * np.sin(theta) + coords[:, 0] * np.cos(theta)
    x0 = toInt32((x0 + 0.5) * (x0 >= 0) + (x0 - 0.5) * (x0 < 0))
    x1 = toInt32((x1 + 0.5) * (x1 >= 0) + (x1 - 0.5) * (x1 < 0))
    x = np.transpose(np.array([np.transpose(x1), np.transpose(x0)]))
    return setToMatrix((x, values))


def rotateInterval(interval, theta=45):
    leftExtermity, complRightExtermity = interval
    return createHitOrMissTemplate(rotateStructuralElement(leftExtermity, theta),
                                   rotateStructuralElement(complRightExtermity, theta))


def isEqual(first, second):
    if first.shape != second.shape:
        return False
    return np.all(first == second)


def performThinning(inputImage):
    theta = 90 # 45 gives better result but presentation says so...
    interval = createHitOrMissTemplate(binary([[0, 0, 0],
                                               [0, 1, 0],
                                               [1, 1, 1]]),

                                       binary([[1, 1, 1],
                                               [0, 0, 0],
                                               [0, 0, 0]]))

    n = np.product(inputImage.shape)

    # all subsequent operations are done on copy, without any reference to original (since we're using it for histogram)
    copyForModification = inputImage.copy()
    zero = createImageIntersection(copyForModification, 0)
    for i in range(n):
        aux = zero
        for t in range(0, 360, theta):
            # Generate Sup for hit-miss
            leftExtermity, complRightExtermity = rotateInterval(interval, t)
            sup = createImageIntersection(performDilation(copyForModification, leftExtermity),
                                          performDilation(negate(copyForModification),
                                                          complRightExtermity))
            aux = np.maximum(aux, sup).astype(aux.dtype)
            # Subtract union image
            bottom, top = getImageLimits(copyForModification)
            copyForModification = np.clip(copyForModification.astype('d') - sup, bottom, top).astype(
                copyForModification.dtype)
        if isEqual(aux, zero):
            break
    return copyForModification


def performThickening(inputImage):
    theta = 90 # 45 gives better result but presentation says so...
    interval = createHitOrMissTemplate(binary([[1, 1, 1],
                                               [0, 0, 0],
                                               [0, 0, 0]]),

                                       binary([[0, 0, 0],
                                               [0, 1, 0],
                                               [1, 1, 1]]))

    n = np.product(inputImage.shape)

    # all subsequent operations are done on copy, without any reference to original (since we're using it for histogram)
    copyForModification = inputImage.copy()
    zero = createImageIntersection(copyForModification, 0)
    for i in range(n):
        aux = zero
        for t in range(0, 360, theta):
            # Generate Sup for hit-miss
            leftExtermity, complRightExtermity = rotateInterval(interval, t)
            sup = createImageIntersection(performDilation(copyForModification, leftExtermity),
                                          performDilation(negate(copyForModification),
                                                          complRightExtermity))
            aux = np.maximum(aux, sup).astype(aux.dtype)

            # apply generated sub to image
            copyForModification = np.maximum(copyForModification, sup).astype(copyForModification.dtype)
        if isEqual(aux, zero):
            break
    return copyForModification


class MorphOpType(Enum):
    Dilation = 0
    Erosion = 1
    Opening = 2
    Closing = 3
    HitOrMissThinning = 4
    HitOrMissThickening = 5
    Unknown = -1


class MorphOpsDialogImpl(QDialog):
    def __init__(self):
        QWidget.__init__(self)
        self.isChange = False
        self.ui = Ui_MorphOpsDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.handleOK)
        self.ui.buttonBox.rejected.connect(self.handleCancel)

    @pyqtSlot()
    def handleOK(self):
        self.isChange = True

    @pyqtSlot()
    def handleCancel(self):
        self.isChange = False

    def getDoIt(self):
        return self.isChange

    def getOpType(self):
        if self.ui.dilationRadioButton.isChecked():
            return MorphOpType.Dilation

        if self.ui.erosionRadioButton.isChecked():
            return MorphOpType.Erosion

        if self.ui.openingRadioButton.isChecked():
            return MorphOpType.Opening

        if self.ui.closingRadioButton.isChecked():
            return MorphOpType.Closing

        if self.ui.thinningRadioButton.isChecked():
            return MorphOpType.HitOrMissThinning

        if self.ui.thickeningRadioButton.isChecked():
            return MorphOpType.HitOrMissThickening

        return MorphOpType.Unknown


class MorphologicalOperations:
    def __init__(self, image):
        self.dialog = MorphOpsDialogImpl()
        self.dialog.setModal(True)
        self.dialog.exec_()
        if self.dialog.getDoIt():
            print("GOWNO")
            self.process(image, self.dialog.getOpType())
            showInput = cv2.cvtColor(self.binarizedGrayScale, cv2.COLOR_GRAY2BGR)
            self.dialog = BeforeAfterHistogramDialog(qimage2ndarray.array2qimage(showInput), self.afterImage)
            self.dialog.setModal(True)
            self.dialog.exec_()

    def getAfterQImage(self):
        return qimage2ndarray.array2qimage(self.afterImage)

    def isChanged(self):
        return self.dialog.isChange

    def process(self, image, type):
        # Convert to gray scale
        input = qimage2ndarray.rgb_view(image, 'little')
        grayImage = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

        # using Otsu binarization, convert to binary
        self.binarizedGrayScale = OtsuBinarize(grayImage)
        trueBinarized = binary(self.binarizedGrayScale, 255)

        if type == MorphOpType.Dilation:
            processed = performDilation(trueBinarized)
            self.afterImage = binaryToGrayScale(processed)
        elif type == MorphOpType.Erosion:
            processed = performErosion(trueBinarized)
            self.afterImage = binaryToGrayScale(processed)
        elif type == MorphOpType.Opening:
            processed = performOpening(trueBinarized)
            self.afterImage = binaryToGrayScale(processed)
        elif type == MorphOpType.Closing:
            processed = performClosing(trueBinarized)
            self.afterImage = binaryToGrayScale(processed)
        elif type == MorphOpType.HitOrMissThinning:
            processed = performThinning(trueBinarized)
            self.afterImage = binaryToGrayScale(processed)
        elif type == MorphOpType.HitOrMissThickening:
            processed = performThickening(trueBinarized)
            self.afterImage = binaryToGrayScale(processed)
        else:
            print("Unknown")
            self.afterImage = binaryToGrayScale(trueBinarized)
