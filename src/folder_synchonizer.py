import asyncio
import dataclasses
import os
import hashlib
import shutil
import typing
import pathlib

from src.file_logger import FileLogger
from src.resources import file_up_to_date, file_has_been_updated, file_deleted_from_replica, file_copied_to_replica

@dataclasses.dataclass
class FolderData:
    folder_path: str | pathlib.Path
    internals: typing.List[str]


class FolderSynchronizer:
    def __init__(self, file_logger: FileLogger):
        self._file_logger = file_logger

    def synchronize(self, source_folder: str | pathlib.Path, replica_folder: str | pathlib.Path):
        source = FolderData(pathlib.Path(source_folder), os.listdir(source_folder))
        replica = FolderData(pathlib.Path(replica_folder), os.listdir(replica_folder))
        self._compare_source_to_replica(source, replica)
        self._compare_replica_to_source(replica, source)
        #for source_file in source_files:
        #    source_file_path = pathlib.Path(os.path.join(source_folder, source_file))
        #    replica_file_path = pathlib.Path(os.path.join(replica_folder, source_file))
        #    if source_file in replica_files:
        #        if source_file_path.is_dir():
        #            self.synchronize(source_file_path, replica_file_path)
        #        elif self.compare_two_file(source_file_path, replica_file_path):
        #            self._file_logger.log(file_up_to_date.format(
        #                source_file_path.name, source_folder, replica_folder
        #            ))
        #        else:
        #            shutil.copy2(source_file_path, replica_file_path)
        #            self._file_logger.log(file_has_been_updated.format(
        #                source_file_path.name, source_folder, replica_folder
        #            ))
        #    else:
        #        if source_file_path.is_dir():
        #            shutil.copytree(source_file_path, replica_file_path)
        #        else:
        #            shutil.copy2(source_file_path, replica_file_path)
        #            self._file_logger.log(file_copied_to_replica.format(
        #                source_file_path.name, source_folder, replica_folder
        #            ))
        #for replica_file in replica_files:
        #    replica_file_path = pathlib.Path(os.path.join(replica_folder, replica_file))
        #    if replica_file not in source_files:
        #        if replica_file_path.is_dir():
        #            shutil.rmtree(replica_file_path)
        #        else:
        #            os.remove(os.path.join(replica_folder, replica_file))
        #            self._file_logger.log(file_deleted_from_replica.format(
        #                replica_file_path.name, replica_folder
        #            ))

    def _compare_source_to_replica(self, source: FolderData, replica: FolderData):
        for source_item in source.internals:
            source_file_path = pathlib.Path(os.path.join(source.folder_path, source_item))
            replica_file_path = pathlib.Path(os.path.join(replica.folder_path, source_item))
            if source_item in replica.internals:
                if source_file_path.is_dir():
                    self.synchronize(source_file_path, replica_file_path)
                elif self.compare_two_file(source_file_path, replica_file_path):
                    self._file_logger.log(file_up_to_date.format(
                        source_file_path.name, source.folder_path, replica.folder_path
                    ))
                else:
                    shutil.copy2(source_file_path, replica_file_path)
                    self._file_logger.log(file_has_been_updated.format(
                        source_file_path.name, source.folder_path, replica.folder_path
                    ))
            else:
                if source_file_path.is_dir():
                    shutil.copytree(source_file_path, replica_file_path)
                    self._file_logger.log(f'Directory {source.folder_path!r} was copied to {replica.folder_path}')
                else:
                    shutil.copy2(source_file_path, replica_file_path)
                    self._file_logger.log(file_copied_to_replica.format(
                        source_file_path.name, source.folder_path, replica.folder_path
                    ))


    def _compare_replica_to_source(self, replica: FolderData, source: FolderData):
        for replica_file in replica.internals:
            replica_file_path = pathlib.Path(os.path.join(replica.folder_path, replica_file))
            if replica_file not in source.internals:
                if replica_file_path.is_dir():
                    shutil.rmtree(replica_file_path)
                    self._file_logger.log(
                        f'Deleted directory that not exists {str(replica.folder_path)} in {str(source.folder_path)}'
                    )
                else:
                    os.remove(os.path.join(replica.folder_path, replica_file))
                    self._file_logger.log(file_deleted_from_replica.format(
                        replica_file_path.name, replica.folder_path
                    ))

    @staticmethod
    def compare_two_file(file_name_1: pathlib.Path, file_name_2: pathlib.Path) -> bool:
        with file_name_1.open(mode='rb') as file_1, file_name_2.open(mode='rb') as file_2:
            compare_1 = hashlib.md5(file_1.read()).hexdigest()
            compare_2 = hashlib.md5(file_2.read()).hexdigest()
            return compare_1 == compare_2



