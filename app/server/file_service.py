"""Module providing file service."""

import os
import shutil


def create_directory(directory_path: str):
    """
    Create a directory if it does not exist.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def copy_file(source_path: str, destination_path: str):
    """
    Copy a file from source to destination.
    """
    shutil.copy(source_path, destination_path)


def remove_directory(directory_path: str):
    """
    Remove a directory and all its contents.
    """
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
