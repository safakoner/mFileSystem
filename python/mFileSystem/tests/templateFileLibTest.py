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
## @file    mFileSystem/tests/templateFileLibTest.py [ FILE   ] - Unit test module.
## @package mFileSystem.tests.templateFileLibTest    [ MODULE ] - Unit test module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import unittest

import mCore.pythonUtilsLib
import mCore.pythonVersionLib

import mFileSystem.templateFileLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
EXPECTED_CONTENT = '''What is REPLACED_LOREM REPLACED_IPSUM?
REPLACED_LOREM REPLACED_IPSUM is simply dummy text of the printing and typesetting industry.
REPLACED_LOREM REPLACED_IPSUM has been the industry's standard dummy text ever since the 1500s,
when an unknown printer took a galley of type and scrambled it to make a type
specimen book. It has survived not only five centuries, but also the leap into
electronic typesetting, remaining essentially unchanged. It was popularised in
the 1960s with the release of REPLACED_LETRASET sheets containing REPLACED_LOREM REPLACED_IPSUM passages,
and more recently with desktop publishing software like Aldus PageMaker
including versions of REPLACED_LOREM REPLACED_IPSUM.'''

def replaceByFunction(content):

    data = {'Ipsum':'REPLACED_IPSUM',
            'Letraset':'REPLACED_LETRASET',
            'Lorem':'REPLACED_LOREM'}

    items = None
    if mCore.pythonVersionLib.isPython3():
        items = data.items()
    else:
        items = data.iteritems()

    for key, value in items:
        content = content.replace(key, value)

    return content

class TemplateFileTest(unittest.TestCase):

    def setUp(self):

        self._tempDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                             '..',
                                                             '..',
                                                             '..',
                                                             'test',
                                                             'mFileSystem',
                                                             'templateFile'))

        self._templateFilePath = os.path.join(self._tempDirectory, 'template.txt')
        self._outputFilePath   = os.path.join(self._tempDirectory, 'output.txt')

    def test_replace(self):

        _templateFile = mFileSystem.templateFileLib.TemplateFile()
        _templateFile.setFile(self._templateFilePath)
        _templateFile.replace({'Ipsum':'REPLACED_IPSUM',
                               'Letraset':'REPLACED_LETRASET',
                               'Lorem':'REPLACED_LOREM'})
        _templateFile.write(self._outputFilePath)

        self.assertEqual(_templateFile.replacedContent(), EXPECTED_CONTENT)

        _file = open(self._outputFilePath, 'r')
        content = _file.read()
        _file.close()
        self.assertEqual(content, EXPECTED_CONTENT)

        self.assertRaises(IOError, _templateFile.write, self._outputFilePath)

        os.remove(self._outputFilePath)

    def test_replaceByFunction(self):

        _templateFile = mFileSystem.templateFileLib.TemplateFile()
        _templateFile.setFile(self._templateFilePath)
        _templateFile.replaceByFunction(replaceByFunction)
        _templateFile.write(self._outputFilePath)

        self.assertEqual(_templateFile.replacedContent(), EXPECTED_CONTENT)

        _file = open(self._outputFilePath, 'r')
        content = _file.read()
        _file.close()
        self.assertEqual(content, EXPECTED_CONTENT)

        self.assertRaises(IOError, _templateFile.write, self._outputFilePath)

        os.remove(self._outputFilePath)

#
#-----------------------------------------------------------------------------------------------------
# INVOKE
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    unittest.main()