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
## @file    mFileSystem/templateFileLib.py @brief [ FILE   ] - Operate on template files.
## @package mFileSystem.templateFileLib    @brief [ MODULE ] - Operate on template files.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os

import mCore.pythonUtilsLib
import mCore.pythonVersionLib

import mFileSystem.fileLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on template files.
#
#  This class allows you to read a template file and replace its content and write the changed content
#  out into a file.
class TemplateFile(mFileSystem.fileLib.File):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self):

        mFileSystem.fileLib.File.__dict__['__init__'](self)

        ## [ dict ] - Replace data.
        self._replaceData     = None

        ## [ str ] - Replaced content.
        self._replacedContent = None

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Replace data.
    #
    #  @exception N/A
    #
    #  @return str - Replace data.
    def replaceData(self):

        return self._replaceData

    #
    ## @brief Replaced content.
    #
    #  @exception N/A
    #
    #  @return str - Replaced content.
    def replacedContent(self):

        return self._replacedContent

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # REIMPLEMENTED PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set template file.
    #
    #  @param absFile [ str | None | in  ] - Absolute path of a template file.
    #
    #  @exception N/A
    #
    #  @return bool - Result, returns `False` is the file doesn't exist, `True` otherwise.
    def setFile(self, absFile):

        result = mFileSystem.fileLib.File.__dict__['setFile'](self, absFile)
        if not result:
            return False

        mFileSystem.fileLib.File.__dict__['read'](self)

        return True

    #
    ## @brief Write replaced content into the output file.
    #
    #  @param absFile   [ str  | None  | in  ] - Absolute path of the output file.
    #  @param overwrite [ bool | False | in  ] - Whether existing `absFile` file will be overwritten.
    #
    #  @exception IOError - If `absFile` exists and overwrite argument provided False.
    #
    #  @return bool - Result.
    def write(self, absFile, overwrite=False):

        if os.path.isfile(absFile) and not overwrite:
            raise IOError('File already exists, could not be created: {}'.format(absFile))

        path = os.path.dirname(absFile)
        if not os.path.isdir(path):
            os.makedirs(path)
        
        _file = open(absFile, 'w')
        _file.write(self._replacedContent)
        _file.close()

        return True

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Replace what needs to be replaced in the template file.
    #
    #  @param replaceData [ dict | None | in  ] - Data, which will be used to replace whats in the template file.
    #
    #  @exception N/A
    #
    #  @return str - File info
    def replace(self, replaceData):

        self._replaceData       = replaceData
        self._replacedContent   = self._content

        items = None
        if mCore.pythonVersionLib.isPython3():
            items = self._replaceData.items()
        else:
            items = self._replaceData.iteritems()

        for key, value in items:
            self._replacedContent = self._replacedContent.replace(key, value)

        return self._replacedContent

    #
    ## @brief Replace what needs to be replaced in the template file by a custom function.
    #
    #  Function must expect a string argument, which is the content of the template file and return edited content.
    #
    #  @param function [ object | None | in  ] - A function object.
    #
    #  @exception RuntimeError - If provided `function` is not a callable.
    #
    #  @return str - Replaced content.
    def replaceByFunction(self, function):

        if not callable(function):
            raise RuntimeError('Provided function is not callable.')

        self._replacedContent = function(self._content)

        return self._replacedContent
