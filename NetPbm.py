import sys
from enum import Enum

import qimage2ndarray
from PyQt5.QtGui import QImage
import numpy as np
import os.path
import chardet


class NetPbmReaderResult(Enum):
    OK = 0
    UnsupportedFormatVersion = 1
    CorruptedFile = 2
    FileDoesNotExists = 3
    UnknownError = 4


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


def netPbmFileTypeEnumToMagic(input: NetPbmFileType):
    return "P" + str(input.value)


def readerResultToString(result: NetPbmReaderResult) -> str:
    if result == NetPbmReaderResult.OK:
        return "All OK"
    if result == NetPbmReaderResult.UnsupportedFormatVersion:
        return "Following version of the format is not supported"
    if result == NetPbmReaderResult.CorruptedFile:
        return "File is corrupted"
    if result == NetPbmReaderResult.FileDoesNotExists:
        return "File doesn't exists"
    if result == NetPbmReaderResult.UnknownError:
        return "Unknown Reader Error"
    return "Undefined Error"


def writerResultToString(result: NetPbmWriterResult) -> str:
    if result == NetPbmWriterResult.OK:
        return "All OK"
    if result == NetPbmReaderResult.NetPbmWriterResult:
        return "Following version of the format is not supported"
    return "Undefined Error"


class NetPbmReader:
    image = None

    def fromFile(self, fileName: str):
        if not os.path.exists(fileName):
            return NetPbmReaderResult.FileDoesNotExists

        ## TODO: Might break if encoding is different but since non-ascii characters are forbidden it shouldn't be problem
        fileInitRead = open(fileName, "r", encoding="Latin-1")
        magic = fileInitRead.read(2)
        fileInitRead.close()
        if magic == netPbmFileTypeEnumToMagic(NetPbmFileType.PortablePixMapAscii):
            return self.readAsciiStream(fileName)
        elif magic == netPbmFileTypeEnumToMagic(NetPbmFileType.PortablePixMapBinary):
            return self.readBinaryStream(fileName)
        else:
            return NetPbmReaderResult.UnsupportedFormatVersion

    def readBinaryStream(self, fileName: str):
        file = open(fileName, "r", encoding="Latin-1")
        data = file.readlines()
        tokens = self.__tokenize(data)
        normailize = False
        _ = next(tokens)
        width, height = (int(next(tokens)) for i in range(2))
        maxColorValueText = next(tokens)
        maxColorValue = int(maxColorValueText)
        _ = next(tokens)

        if maxColorValue != 255:
            normailize = True
        arr = np.zeros((height, width, 3))
        file.close()

        fileBin = open(fileName, "rb")
        # read header that we don't need
        _ = fileBin.read(self.currPos)

        try:
            readArr = np.frombuffer(fileBin.read(), dtype='uint8')
        except ValueError as e:
            return NetPbmReaderResult.CorruptedFile  # TODO: IDK what are the exception types for numpy so we return that its corrupted
        except Exception as e:
            print(e)
            return NetPbmReaderResult.UnknownError

        if len(readArr) != width * height * 3:
            return NetPbmReaderResult.CorruptedFile

        arr = readArr.reshape(height, width, 3)
        copy = arr.copy()
        if normailize:
            for h in range(height):
                for w in range(0, width):
                    r, g, b = arr[h][w]
                    copy[h][w] = np.array([self.normalize(r, maxColorValue), self.normalize(g, maxColorValue),
                                            self.normalize(b, maxColorValue)])

        self.image = qimage2ndarray.array2qimage(copy, False)

        return NetPbmReaderResult.OK

    def readAsciiStream(self, fileName: str):
        file = open(fileName, "r", encoding="Latin-1")
        data = file.readlines()
        tokens = self.__tokenize(data)
        normailize = False
        _ = next(tokens)
        width, height, maxColorValue = (int(next(tokens)) for i in range(3))

        if maxColorValue != 255:
            normailize = True

        arr = np.zeros((height, width, 3))

        try:
            for h in range(height):
                for w in range(0, width):
                    r, g, b = (int(next(tokens)) for i in range(3))
                    if normailize:
                        r = self.normalize(r, maxColorValue)
                        g = self.normalize(g, maxColorValue)
                        b = self.normalize(b, maxColorValue)
                    arr[h][w] = np.array([r, g, b])
        except RuntimeError as e:
            if e.__cause__ == "StopIteration":  # We can't get next set, file corrupted.
                return NetPbmReaderResult.CorruptedFile
            else:
                return NetPbmReaderResult.UnknownError

        self.image = qimage2ndarray.array2qimage(arr)

        return NetPbmReaderResult.OK

    def normalize(self, val: int, max: int) -> int:
        return int((val * 255) / max)

    def getDecoded(self) -> QImage:
        return self.image

    def __tokenize(self, data):
        self.currPos = 0
        for line in data:
            if line[0] != '#':
                for t in line.split():
                    if '#' in t:
                        # comment in middle, skip the rest of the line
                        break
                    else:
                        yield t

            self.currPos += len(line)


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
