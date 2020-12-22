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
## @file    mFileSystem/simpleWatcherLib.py @brief [ FILE   ] - Watch for file changes.
## @package mFileSystem.simpleWatcherLib    @brief [ MODULE ] - Watch for file changes.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os

from   threading import Timer

import mFileSystem.directoryLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to watch file changes.
#
# @code
#import sys
#import mFileSystem.simpleWatcherLib
#
#def created(fileList):
#    sys.stdout.write('created')
#    sys.stdout.write(fileList)
#
#def edited(fileList):
#    sys.stdout.write('edited')
#    sys.stdout.write(fileList)
#
#def deleted(fileList):
#    sys.stdout.write('deleted')
#    sys.stdout.write(fileList)
#
#def changed(fileList):
#    sys.stdout.write('changed')
#    sys.stdout.write(fileList)
#
# _watcher = mFileSystem.simpleWatcherLib.SimpleWatcher(path='absolutePath',
#                                                       recursive=False,
#                                                       extension='py',
#                                                       createdCallback=created,
#                                                       editedCallback=edited,
#                                                       deletedCallback=deleted,
#                                                       callback=changed)
#                                                       )
# _watcher.start()
#
# #_watcher.stop()
#
# @endcode
class SimpleWatcher(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param path            [ str      | None  | in  ] - Absolute directory to be watched.
    #  @param recursive       [ bool     | False | in  ] - Whether to watch recursively.
    #  @param extension       [ str      | None  | in  ] - Extension of the files to be watched.
    #  @param createdCallback [ function | None  | in  ] - Created callback.
    #  @param editedCallback  [ function | None  | in  ] - Edited callback.
    #  @param deletedCallback [ function | None  | in  ] - Deleted callback.
    #  @param callback        [ function | None  | in  ] - Callback.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self,
                 path,
                 recursive=False,
                 extension=None,
                 createdCallback=None,
                 editedCallback=None,
                 deletedCallback=None,
                 callback=None):

        ## [ str ] - Absolute directory to be watched.
        self._path              = path

        ## [ bool ] - Whether to watch recursively.
        self._recursive         = recursive

        ## [ str ] - Extension of the files to be watched.
        self._extension         = extension

        ## [ function ] - Created callback.
        self._createdCallback   = createdCallback

        ## [ function ] - Edited callback.
        self._editedCallback    = editedCallback

        ## [ function ] - Deleted callback.
        self._deletedCallback   = deletedCallback


        ## [ function ] - Callback.
        self._callback          = callback


        ## [ dict ] - Data of the files that being watched.
        self._entryData         = {}

        ## [ list ] - Created files list.
        self._createdFiles      = []

        ## [ list ] - Edited files list.
        self._editedFiles       = []

        ## [ list ] - Deleted files list.
        self._deletedFiles      = []

        ## [ float ] - Watch interval.
        self._interval          = 1.0

        ## [ mFileSystem.directoryLib.Directory ] - Directory class instance.
        self._directory         = mFileSystem.directoryLib.Directory(directory=absPath)

        ## [ threading.Timer ] - Timer class instance.
        self._thread            = Timer(self._interval, self._detectChanges)

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Detect file changes.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _detectChanges(self):

        # Clear files
        self._createdFiles[:] = []
        self._editedFiles[:]  = []
        self._deletedFiles[:] = []

        # List files
        entryList = []

        if not self._recursive:
            entryList = self._directory.listFilesWithAbsolutePath(extension=self._extension)
        else:
            entryList = self._directory.listFilesRecursively(extension=self._extension)

        if not entryList and not self._entryData:
            return

        # Detect deleted files
        if self._entryData:
            for k, v in self._entryData.items():
                if not k in entryList:
                    self._deletedFiles.append(k)
                    del self._entryData[k]

        for f in entryList:

            if self._entryData.get(f):
                # File is already listed previously
                # so check the file for changes
                timeStamp = os.stat(f).st_mtime
                if self._entryData[f] != timeStamp:
                    self._entryData[f] = timeStamp
                    self._editedFiles.append(f)
            else:
                # File has been created so add it
                self._entryData[f] = os.stat(f).st_mtime
                self._createdFiles.append(f)

        # Invoke callbacks
        if self._callback:

            fileList = []

            if self._createdFiles:
                fileList.extend(self._createdFiles)

            if self._editedFiles:
                fileList.extend(self._editedFiles)

            if self._deletedFiles:
                fileList.extend(self._deletedFiles)

            if fileList:
                self._callback(fileList)

        else:

            if self._createdCallback and self._createdFiles:
                self._createdCallback(self._createdFiles)

            if self._editedCallback and self._editedFiles:
                self._editedCallback(self._editedFiles)

            if self._deletedCallback and self._deletedFiles:
                self._deletedCallback(self._deletedFiles)

        # Repeat the process
        self._thread = Timer(self._interval, self._detectChanges)
        self._thread.start()

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Start watcher.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def start(self):

        self._thread.start()

    #
    ## @brief Stop watcher.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def stop(self):

        self._thread.cancel()


