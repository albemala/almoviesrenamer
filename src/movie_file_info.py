import os

__author__ = "Alberto Malagoli"


class MovieFileInfo:
    def __init__(self):
        # file path (only directory)
        self._directory_path = ""
        # original movie title, before renaming
        self._original_file_name = ""
        # file extension
        self._file_extension = ""
        # movie new title (after renaming)
        self._renamed_file_name = ""

    def get_original_file_name(self):
        return self._original_file_name

    def get_renamed_file_name(self):
        return self._renamed_file_name

    def get_absolute_original_file_path(self):
        return os.path.join(self._directory_path, self._original_file_name + self._file_extension)

    def get_absolute_renamed_file_path(self):
        return os.path.join(self._directory_path, self._renamed_file_name + self._file_extension)

    def get_directory_path(self):
        return self._directory_path

    def fill_with_absolute_file_path(self, absolute_file_path):
        path, name = os.path.split(absolute_file_path)
        name, extension = os.path.splitext(name)
        self._directory_path = os.path.normpath(path)
        self._original_file_name = name
        self._file_extension = extension
