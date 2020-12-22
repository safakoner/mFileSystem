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
## @file    mFileSystem/tests/directoryLibTest.py [ FILE   ] - Unit test module.
## @package mFileSystem.tests.directoryLibTest    [ MODULE ] - Unit test module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import shutil
import unittest

import mCore.platformLib

import mFileSystem.directoryLib
import mFileSystem.fileLib
import mFileSystem.versionLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
class DirectoryTest(unittest.TestCase):

    def setUp(self):

        self._tempDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                           '..',
                                                           '..',
                                                           '..',
                                                           'test',
                                                           'mFileSystem',
                                                           'directory'))

        self._testDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                           '..',
                                                           '..',
                                                           '..',
                                                           'test',
                                                           'mFileSystem'))

        if not os.path.isdir(self._tempDirectory):
            os.makedirs(self._tempDirectory)

    def tearDown(self):

        if os.path.isdir(self._tempDirectory):
            shutil.rmtree(self._tempDirectory)

    def test_constructor(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

    def test_exists(self):

        customDir = os.path.join(self._tempDirectory, 'custom')
        os.makedirs(customDir)

        _dir = mFileSystem.directoryLib.Directory(customDir)

        self.assertTrue(_dir.exists())

        shutil.rmtree(customDir)

        self.assertFalse(_dir.exists())

    def test_rename(self):

        customDir = os.path.join(self._tempDirectory, 'custom')
        os.makedirs(customDir)

        newCustomDir = os.path.join(self._tempDirectory, 'newCustom')

        _dir = mFileSystem.directoryLib.Directory(customDir)

        self.assertTrue(_dir.rename('newCustom'))

        shutil.rmtree(newCustomDir)

    def test_remove(self):

        customDir = os.path.join(self._tempDirectory, 'custom')
        os.makedirs(customDir)

        _dir = mFileSystem.directoryLib.Directory(customDir)

        self.assertTrue(_dir.remove())

    def test_createFolder(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

        self.assertTrue(_dir.createFolder('newCustom'))

        newCustomDir = os.path.join(self._tempDirectory, 'newCustom')

        shutil.rmtree(newCustomDir)

    def test_getBaseName(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

        self.assertEqual(_dir.getBaseName(), 'directory')

        self.assertNotEqual(_dir.getBaseName(), 'dir2')

    def test_listFolders(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

        _dir.createFolder('new1', False)
        _dir.createFolder('new2', False)
        _dir.createFolder('new3', False)

        self.assertEqual(_dir.listFolders(), ['new1', 'new2', 'new3'])

        self.assertNotEqual(_dir.listFolders(), ['new2', 'new2', 'new2'])

    def test_listDirectories(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

        _dir.createFolder('new1', False)
        _dir.createFolder('new2', False)
        _dir.createFolder('new3', True)
        _dir.createFolder('new4', False)

        _dir.setDirectory(self._tempDirectory)

        _dir.listDirectoriesRecursively()

        self.assertEqual(_dir.listDirectoriesRecursively(), [os.path.join(self._tempDirectory, 'new1'),
                                                              os.path.join(self._tempDirectory, 'new2'),
                                                              os.path.join(self._tempDirectory, 'new3'),
                                                              os.path.join(self._tempDirectory, 'new3', 'new4')])


        self.assertNotEqual(_dir.listDirectoriesRecursively(), [os.path.join(self._tempDirectory, 'new1'),
                                                                os.path.join(self._tempDirectory, 'new2'),
                                                                os.path.join(self._tempDirectory, 'new3'),
                                                                os.path.join(self._tempDirectory, 'new3', 'new5')])

        shutil.rmtree(os.path.join(self._tempDirectory, 'new1'))
        shutil.rmtree(os.path.join(self._tempDirectory, 'new2'))
        shutil.rmtree(os.path.join(self._tempDirectory, 'new3'))

    def test_listFiles(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

        file1 = os.path.join(self._tempDirectory, 'file1.txt')
        file2 = os.path.join(self._tempDirectory, 'file2.txt')

        mFileSystem.fileLib.File.create(file1, overwrite=False)
        mFileSystem.fileLib.File.create(file2, overwrite=False)

        self.assertEqual(_dir.listFiles(), ['file1.txt', 'file2.txt'])

        self.assertNotEqual(_dir.listFolders(), ['file2.txt', 'file2.txt'])

    def test_listFilesWithAbsolutePath(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

        file1 = os.path.join(self._tempDirectory, 'file1.txt')
        file2 = os.path.join(self._tempDirectory, 'file2.txt')
        file3 = os.path.join(self._tempDirectory, 'file3.txt')

        mFileSystem.fileLib.File.create(file1, overwrite=False)
        mFileSystem.fileLib.File.create(file2, overwrite=False)
        mFileSystem.fileLib.File.create(file3, overwrite=False)

        _dir.setDirectory(self._tempDirectory)

        self.assertEqual(_dir.listFilesWithAbsolutePath(), [file1,
                                                             file2,
                                                             file3])

        self.assertNotEqual(_dir.listFilesWithAbsolutePath(), [file1,
                                                               file2,
                                                               file2])

        shutil.rmtree(self._tempDirectory)

    def test_listFilesRecursively(self):

        _dir = mFileSystem.directoryLib.Directory(self._tempDirectory)

        _dir.createFolder('f1', False)
        _dir.createFolder('f2', True)
        _dir.createFolder('f3', True)

        file1 = os.path.join(self._tempDirectory, 'f1', 'file1.txt')
        file2 = os.path.join(self._tempDirectory, 'f2', 'file2.txt')
        file3 = os.path.join(self._tempDirectory, 'f2', 'f3', 'file3.txt')

        mFileSystem.fileLib.File.create(file1, overwrite=True)
        mFileSystem.fileLib.File.create(file2, overwrite=True)
        mFileSystem.fileLib.File.create(file3, overwrite=True)

        _dir.setDirectory(self._tempDirectory)

        self.assertEqual(_dir.listFilesRecursively(), [file1,
                                                       file3,
                                                       file2])

        self.assertNotEqual(_dir.listFilesRecursively(), [file1,
                                                          file1,
                                                          file1])

        shutil.rmtree(self._tempDirectory)

    def test_navigateUp(self):

        if mCore.platformLib.Platform.isWindows():
            return

        path = '/somePath/with/someOther/folder'

        self.assertEqual(mFileSystem.directoryLib.Directory.navigateUp(path, 2), '/somePath/with')

    def test_directoryExists(self):

        self.assertTrue(mFileSystem.directoryLib.Directory.directoryExists(self._tempDirectory))

    def test_listVersionedFolders(self):

        versionFolderDirectory = os.path.join(self._testDirectory, 'versionedFolders')

        self.assertEqual(['1.0.0', '2.0.0', '3.0.0', '10.0.0'],
                          mFileSystem.directoryLib.Directory.listVersionedFolders(directory=versionFolderDirectory,
                                                                                  absolutePath=False,
                                                                                  version=mFileSystem.versionLib.Version.kAll,
                                                                                  semanticOnly=True,
                                                                                  ignore=False,
                                                                                  createPath=False))

        self.assertEqual('10.0.0', mFileSystem.directoryLib.Directory.listVersionedFolders(directory=versionFolderDirectory,
                                                                                           absolutePath=False,
                                                                                           version=mFileSystem.versionLib.Version.kLatest,
                                                                                           semanticOnly=True,
                                                                                           ignore=False,
                                                                                           createPath=False))

        self.assertEqual('10.0.0', mFileSystem.directoryLib.Directory.listVersionedFolders(directory=versionFolderDirectory,
                                                                                           absolutePath=False,
                                                                                           version=mFileSystem.versionLib.Version.kCurrent,
                                                                                           semanticOnly=True,
                                                                                           ignore=False,
                                                                                           createPath=False))

        self.assertEqual('1.0.0', mFileSystem.directoryLib.Directory.listVersionedFolders(directory=versionFolderDirectory,
                                                                                          absolutePath=False,
                                                                                          version=mFileSystem.versionLib.Version.kFirst,
                                                                                          semanticOnly=True,
                                                                                          ignore=False,
                                                                                          createPath=False))

        self.assertEqual('10.0.0', mFileSystem.directoryLib.Directory.listVersionedFolders(directory=versionFolderDirectory,
                                                                                           absolutePath=False,
                                                                                           version=mFileSystem.versionLib.Version.kLast,
                                                                                           semanticOnly=True,
                                                                                           ignore=False,
                                                                                           createPath=False))

        self.assertEqual('3.0.0', mFileSystem.directoryLib.Directory.listVersionedFolders(directory=versionFolderDirectory,
                                                                                          absolutePath=False,
                                                                                          version=mFileSystem.versionLib.Version.kPrevious,
                                                                                          semanticOnly=True,
                                                                                          ignore=False,
                                                                                          createPath=False))

        self.assertEqual('1.0.0', mFileSystem.directoryLib.Directory.listVersionedFolders(directory=versionFolderDirectory,
                                                                                          absolutePath=False,
                                                                                          version='1.0.0',
                                                                                          semanticOnly=True,
                                                                                          ignore=False,
                                                                                          createPath=False))

    def test_listVersionedFiles(self):

        versionFileDirectory = os.path.join(self._testDirectory, 'versionedFiles')

        self.assertEqual(['file.v001.txt', 'file.v002.txt', 'file.v003.txt', 'file.v010.txt', 'file.v011.txt'],
                          mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                  absolutePath=False,
                                                                                  version=mFileSystem.versionLib.Version.kAll,
                                                                                  createPath=False))

        self.assertEqual('file.v011.txt', mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                                 absolutePath=False,
                                                                                                 version=mFileSystem.versionLib.Version.kLatest,
                                                                                                 createPath=False))

        self.assertEqual('file.v011.txt', mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                                 absolutePath=False,
                                                                                                 version=mFileSystem.versionLib.Version.kCurrent,
                                                                                                 createPath=False))

        self.assertEqual('file.v001.txt', mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                                 absolutePath=False,
                                                                                                 version=mFileSystem.versionLib.Version.kFirst,
                                                                                                 createPath=False))

        self.assertEqual('file.v011.txt', mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                                 absolutePath=False,
                                                                                                 version=mFileSystem.versionLib.Version.kLast,
                                                                                                 createPath=False))

        self.assertEqual('file.v010.txt', mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                                 absolutePath=False,
                                                                                                 version=mFileSystem.versionLib.Version.kPrevious,
                                                                                                 createPath=False))

        self.assertEqual('file.v001.txt', mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                                 absolutePath=False,
                                                                                                 version='1',
                                                                                                 createPath=False))

        self.assertEqual('file.v001.txt', mFileSystem.directoryLib.Directory.listVersionedFiles(directory=versionFileDirectory,
                                                                                                 absolutePath=False,
                                                                                                 version=1,
                                                                                                 createPath=False))

    def test_toNativeSeparators(self):

        path         = '/mnt/libs//external\\boost\\\\1.66'
        expectedPath = '/mnt/libs/external/boost/1.66'

        if mCore.platformLib.Platform.isWindows():
            expectedPath = 'W:\\mnt\\libs\\external\\boost\\1.66\\src\\v2'
            path = 'W:\\mnt\\libs\\external//boost\\1.66\\\\src/v2'

        self.assertEqual(mFileSystem.directoryLib.Directory.toNativeSeparators(path),
                         expectedPath)

#
#-----------------------------------------------------------------------------------------------------
# INVOKE
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    unittest.main()
