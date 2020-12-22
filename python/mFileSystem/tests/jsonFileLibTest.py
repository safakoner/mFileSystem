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
## @file    mFileSystem/tests/jsonFileLibTest.py [ FILE   ] - Unit test module.
## @package mFileSystem.tests.jsonFileLibTest    [ MODULE ] - Unit test module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import unittest
import shutil

import mFileSystem.jsonFileLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
class JSONFileTest(unittest.TestCase):

    def setUp(self):

        self._tempDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                           '..',
                                                           '..',
                                                           '..',
                                                           'test',
                                                           'jsonFile'))
        if not os.path.isdir(self._tempDirectory):
            os.makedirs(self._tempDirectory)

        self._fileBaseName  = 'testFile'
        self._fileExtension = 'json'
        self._fileName      = '{}.{}'.format(self._fileBaseName, self._fileExtension)
        self._file          = os.path.join(self._tempDirectory, self._fileName)

    def tearDown(self):

        if os.path.isdir(self._tempDirectory):
            shutil.rmtree(self._tempDirectory)

    def test_setFile(self):

        _file = mFileSystem.jsonFileLib.JSONFile.create(self._file, overwrite=False)

        self.assertTrue(_file.setFile(self._file))

        os.remove(self._file)

        self.assertFalse(_file.setFile(self._file))

    def test_write(self):

        _file = mFileSystem.jsonFileLib.JSONFile.create(self._file, overwrite=False)

        data = [{'attr':'value'}]

        _file.setContent(data)

        _file.write()

        os.remove(self._file)

    def test_read(self):

        _file = mFileSystem.jsonFileLib.JSONFile.create(self._file, overwrite=False)

        data = [{'attr':'value'}]

        _file.setContent(data)
        _file.write()

        self.assertEqual(_file.read(), data)

        os.remove(self._file)

#
#-----------------------------------------------------------------------------------------------------
# INVOKE
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    unittest.main()
