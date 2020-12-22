#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    mFileSystem/tests/fileLibTest.py [ FILE   ] - Unit test module.
## @package mFileSystem.tests.fileLibTest    [ MODULE ] - Unit test module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import unittest
import shutil

import mFileSystem.fileLib
import mFileSystem.exceptionLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
class FileTest(unittest.TestCase):

    def setUp(self):

        self._tempDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                             '..',
                                                             '..',
                                                             '..',
                                                             'test',
                                                             'file'))
        if not os.path.isdir(self._tempDirectory):
            os.makedirs(self._tempDirectory)

        self._fileBaseName  = 'testFile'
        self._fileExtension = 'txt'
        self._fileName      = '{}.{}'.format(self._fileBaseName, self._fileExtension)
        self._file          = os.path.join(self._tempDirectory, self._fileName)

        self._destinationDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                  '..',
                                                                  '..',
                                                                  '..',
                                                                  'test',
                                                                  'file',
                                                                  'destination'))
        if not os.path.isdir(self._destinationDirectory):
            os.makedirs(self._destinationDirectory)

        #
        # self._destinationFile = os.path.join(self._destinationDirectory, self._fileA)

    def tearDown(self):

        if os.path.isdir(self._tempDirectory):
            shutil.rmtree(self._tempDirectory)

    def test_attributes(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        self.assertEqual(_file.directory(), self._tempDirectory)
        self.assertEqual(_file.baseName() , self._fileBaseName)
        self.assertEqual(_file.extension(), self._fileExtension)
        self.assertEqual(_file.size()     , 0)

        os.remove(self._file)

    def test_setFile(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        self.assertTrue(_file.setFile(self._file))

        os.remove(self._file)

        self.assertFalse(_file.setFile(self._file))

    def test_update(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        self.assertTrue(_file.update())

        os.remove(self._file)

        self.assertFalse(_file.update())

    def test_exists(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        self.assertTrue(_file.exists())

        os.remove(self._file)

        self.assertFalse(_file.exists())

    def test_rename(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        self.assertTrue(_file.rename('newName.txt'))

        os.remove(_file.file())

    def test_copy(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        destinationFile = os.path.join(self._destinationDirectory, 'newFile.txt')

        self.assertEqual(_file.copy(destinationFile), destinationFile)

        self.assertRaises(mFileSystem.exceptionLib.FileAlreadyExists, _file.copy, destinationFile, False)

        os.remove(self._file)
        os.remove(destinationFile)

    def test_copyToPath(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        destinationFile = os.path.join(self._destinationDirectory, self._fileName)

        self.assertEqual(_file.copyToPath(self._destinationDirectory, True), destinationFile)

        self.assertRaises(mFileSystem.exceptionLib.FileAlreadyExists, _file.copyToPath, self._destinationDirectory, False)

        os.remove(self._file)
        os.remove(destinationFile)

    def test_remove(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        self.assertTrue(_file.remove())

    def test_write(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        _file.write('-' * 100)
        _file.update()

        self.assertEqual(_file.size(), 100)

        self.assertTrue(_file.remove())

    def test_writeLines(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        lineList = []
        for i in range(100):
            lineList.append('-')

        _file.writeLines(lineList)
        _file.update()

        self.assertEqual(_file.size(), 100)

        self.assertTrue(_file.remove())

    def test_read(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        _file.write('-' * 100)
        _file.update()

        self.assertEqual(_file.read(), '-' * 100)

        self.assertTrue(_file.remove())

    def test_readLines(self):

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        lineList = []
        for i in range(100):
            lineList.append('-\n')

        _file.writeLines(lineList)
        _file.update()

        self.assertEqual(_file.readLines(), lineList)

        self.assertTrue(_file.remove())

    def test_fileExists(self):

        self.assertFalse(mFileSystem.fileLib.File.fileExists(self._file))

        _file = mFileSystem.fileLib.File.create(self._file, overwrite=False)

        self.assertTrue(mFileSystem.fileLib.File.fileExists(self._file))

        self.assertTrue(_file.remove())

    def test_create(self):

        self.assertEqual(isinstance(mFileSystem.fileLib.File.create(self._file, overwrite=True), mFileSystem.fileLib.File), True)

        self.assertRaises(IOError, mFileSystem.fileLib.File.create, self._file, False)

        os.remove(self._file)

#
#-----------------------------------------------------------------------------------------------------
# INVOKE
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    unittest.main()
