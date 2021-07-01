import os
import shutil
import stat
from typing import List, Optional


class FilesUtil:
    @staticmethod
    def copy_dir_files(
        src_directory: str,
        destination_dir: str,
        except_list: Optional[List[str]] = None,
    ):
        for file in {
            file for file in os.listdir(src_directory) if file not in except_list
        }:
            shutil.copyfile(
                os.path.join(src_directory, file), os.path.join(destination_dir, file)
            )

    @staticmethod
    def change_dir_files_permissions(
        directory: str, except_list: Optional[List[str]] = None
    ):
        for file in {file for file in os.listdir(directory) if file not in except_list}:
            os.chmod(os.path.join(directory, file), stat.S_IRUSR)

    @staticmethod
    def remove_dir_files(directory: str, except_list: Optional[List[str]] = None):
        for file in {file for file in os.listdir(directory) if file not in except_list}:
            os.remove(os.path.join(directory, file))
