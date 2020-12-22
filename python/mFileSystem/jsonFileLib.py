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
## @file    mFileSystem/jsonFileLib.py @brief [ FILE   ] - Operate on JSON files.
## @package mFileSystem.jsonFileLib    @brief [ MODULE ] - Operate on JSON files.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import json

import mFileSystem.fileLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on JSON files.
class JSONFile(mFileSystem.fileLib.File):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param path [ str | None | in  ] - Absolute path of a file.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, path=None):

        mFileSystem.fileLib.File.__dict__['__init__'](self, path)

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Set JSON content.
    #
    #  @param content [ variant | None | in  ] - Value to be set.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setContent(self, content):

        ## [ str ] - Content of the file.
        self._content = content

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # REIMPLEMENTED PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set file.
    #
    #  @param path [ str | None | in  ] - Absolute path of a file.
    #
    #  @exception N/A
    #
    #  @return bool - Result, returns `False` is the file doesn't exist, `True` otherwise.
    def setFile(self, path):

        if mFileSystem.fileLib.File.__dict__['setFile'](self, path):
            return True

        return False

    ## @name CONTENT

    ## @{
    #
    ## @brief Write the content into the file.
    #
    #  @param indent [ int | None | in  ] - Indentation.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def write(self, indent=None):

        with open(self._file, 'w') as outFile:
            json.dump(self._content, outFile, indent=indent)

        return True

    #
    ## @brief Read the content of the file and store it in content member.
    #
    #  @exception N/A
    #
    #  @return variant - Content.
    def read(self):

        with open(self._file) as inFile:
            self._content = json.load(inFile,
                                      cls=None,
                                      object_hook=None,
                                      parse_float=None,
                                      parse_int=None,
                                      parse_constant=None,
                                      object_pairs_hook=None)

        return self._content

    #
    ## @}