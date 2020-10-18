import sys
from enum import Enum

import qimage2ndarray
from PyQt5.QtGui import QImage
import numpy as np
import os.path


class NetPbmReaderResult(Enum):
    OK = 0
    UnsupportedFormatVersion = 1
    CorruptedFile = 2


class NetPbmWriterResult(Enum):
    OK = 0
    UnsupportedFormatVersion = 1


class NetPbmFileType(Enum):
    Unknown = 0
    PortableBitMapAscii = 1
    PortableGrayMapAscii = 2
    PortablePixMapAscii = 3
    PortableBitMapBinary = 4
    PortableGrayMapBinary = 5
    PortablePixMapBinary = 6


# def netPbmMagicTagToFileTypeEnum(input: str):

def netPbmFileTypeEnumToMagic(input: NetPbmFileType):
    return "P" + str(input.value)


class NetPbmReader:
    def fromFile(self, fileName: str):
        return 0

    def read(self, stream):
        return NetPbmReaderResult.OK

    def readBinaryStream(self):
        return 0

    def readAsciiStream(self):
        return 0

    def __tokenize(self):
        return 0


class NetPbmWriter:

    def save(self, image: QImage, path: str, type: NetPbmFileType):
        if type == NetPbmFileType.PortablePixMapAscii:
            return self.saveAsciiFileFromQImage(image, path)
        if type == NetPbmFileType.PortablePixMapBinary:
            return self.saveBinaryFileFromQImage(image, path)

        return NetPbmWriterResult.UnsupportedFormatVersion

    def saveAsciiFileFromQImage(self, image: QImage, path: str):
        # RGB positioning is for Big Endian platforms, so we get ndarray of that endiannes
        rgbData = qimage2ndarray.rgb_view(image, 'big')
        magic = netPbmFileTypeEnumToMagic(NetPbmFileType.PortablePixMapAscii)
        width = image.width()
        height = image.height()
        infoComment = "Saved with NetPbm utility class by P.Recko (guest_none) (PixMap ASCII). " \
                      "https://www.youtube.com/watch?v=b1CIdU_r0ak"
        maxColorValue = 255

        # open the file for write-only, Python opens them in ascii mode by default
        fileOut = open(path, 'w')

        fileOut.write("%s\n" % (magic))
        fileOut.write("#%s\n" % infoComment)
        fileOut.write("%d %d\n" % (width, height))
        fileOut.write("%d\n" % maxColorValue)

        for w in rgbData:
            for val in w:
                fileOut.write("%d %d %d  " % (val[0], val[1], val[2]))
            fileOut.write("\n")

        fileOut.close()

        return NetPbmWriterResult.OK

    def saveBinaryFileFromQImage(self, image: QImage, path: str):
        # We use BGR image, since we can't save the array directly when using write (throws ndarray is not C-contiguous)
        rgbData = qimage2ndarray.rgb_view(image, 'little')
        magic = netPbmFileTypeEnumToMagic(NetPbmFileType.PortablePixMapBinary)
        width = image.width()
        height = image.height()
        infoComment = "Saved with NetPbm utility class by P.Recko (guest_none) (PixMap Binary). " \
                      "https://www.youtube.com/watch?v=WWdJ_scLLkI"
        maxColorValue = 255

        fileOut = open(path, 'wb')

        fileOut.write(bytes("%s\n" % magic, sys.stdin.encoding))
        fileOut.write(bytes("#%s\n" % infoComment, sys.stdin.encoding))
        fileOut.write(bytes("%d %d\n" % (width, height), sys.stdin.encoding))
        fileOut.write(bytes("%d\n" % maxColorValue, sys.stdin.encoding))
        for w in rgbData:
            for val in w:
                # Convert BGR (little-endian) pixel value to RGB (big-endian) value
                formed = np.array([val[2], val[1], val[0]])
                fileOut.write(formed.tobytes())

        fileOut.close()

        return NetPbmWriterResult.OK
