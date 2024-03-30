import asyncio
import os
import hashlib
import shutil
import pathlib
from asyncio.tasks import Task

from .folder_data_dto import FolderDataDTO
from .file_logger import FileLogger


class FolderSynchronizer:
    def __init__(self, file_logger: FileLogger):
        self._file_logger = file_logger

    async def synchronize(self, source_folder: str | pathlib.Path, replica_folder: str | pathlib.Path) -> None:
        source = FolderDataDTO(pathlib.Path(source_folder), os.listdir(source_folder))
        replica = FolderDataDTO(pathlib.Path(replica_folder), os.listdir(replica_folder))
        await asyncio.gather(
            self._compare_source_items_to_replica(source, replica),
            self._compare_replica_to_source(replica, source)
        )

    async def _compare_source_items_to_replica(self, source: FolderDataDTO, replica: FolderDataDTO) -> None:
        tasks = []
        for source_item in source.internal_items:
            task = self._get_task_to_compare_source_item_to_replica(source_item, source, replica)
            tasks.append(task)
        await asyncio.gather(*tasks)

    def _get_task_to_compare_source_item_to_replica(
            self, source_item: str, source: FolderDataDTO, replica: FolderDataDTO
    ) -> Task:
        source_item_path = pathlib.Path(os.path.join(source.folder_path, source_item))
        replica_item_path = pathlib.Path(os.path.join(replica.folder_path, source_item))
        if source_item in replica.internal_items:
            task = asyncio.create_task(
                self._work_with_items_which_exist_in_both_folders(source_item_path, replica_item_path)
            )
        else:
            task = asyncio.create_task(
                self._work_with_items_which_not_exist_in_both_folders(source_item_path, replica_item_path)
            )
        return task

    async def _work_with_items_which_exist_in_both_folders(
            self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path
    ) -> None:
        if source_item_path.is_dir():
            await self.synchronize(source_item_path, replica_item_path)
        elif self._check_if_two_files_equal(source_item_path, replica_item_path):
            self._file_logger.log_file_up_to_date(source_item_path, replica_item_path)
        else:
            self._update_file_in_replica(source_item_path, replica_item_path)

    @staticmethod
    def _check_if_two_files_equal(file_name_1: pathlib.Path, file_name_2: pathlib.Path) -> bool:
        with file_name_1.open(mode='rb') as file_1, file_name_2.open(mode='rb') as file_2:
            compare_1 = hashlib.md5(file_1.read()).hexdigest()
            compare_2 = hashlib.md5(file_2.read()).hexdigest()
            return compare_1 == compare_2

    def _update_file_in_replica(self, source_item_path: pathlib.Path, replica_item_data: pathlib) -> None:
        shutil.copy2(source_item_path, replica_item_data)
        self._file_logger.log_updated_file_in_replica(source_item_path, replica_item_data)

    async def _work_with_items_which_not_exist_in_both_folders(
            self, source_item_data: pathlib.Path, replica_item_data: pathlib.Path
    ) -> None:
        if source_item_data.is_dir():
            self._copy_directory_to_replica(source_item_data, replica_item_data)
        else:
            self._copy_file_to_replica(source_item_data, replica_item_data)

    def _copy_directory_to_replica(self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path) -> None:
        shutil.copytree(source_item_path, replica_item_path)
        self._file_logger.log_copy_directory_to_replica(source_item_path, replica_item_path)

    def _copy_file_to_replica(self, source_item_path: pathlib.Path, replica_item_data: pathlib.Path) -> None:
        shutil.copy2(source_item_path, replica_item_data)
        self._file_logger.log_copy_file_to_replica(source_item_path, replica_item_data)

    async def _compare_replica_to_source(self, replica_folder_data: FolderDataDTO, source_folder_data: FolderDataDTO) -> None:
        tasks = []
        for replica_item in replica_folder_data.internal_items:
            replica_item_data = pathlib.Path(os.path.join(replica_folder_data.folder_path, replica_item))
            if replica_item not in source_folder_data.internal_items:
                task = asyncio.create_task(
                    self._work_with_item_which_not_exists_in_source(replica_item_data, source_folder_data)
                )
                tasks.append(task)
        await asyncio.gather(*tasks)

    async def _work_with_item_which_not_exists_in_source(
            self, replica_item_path: pathlib.Path, source_folder_data: FolderDataDTO
    ) -> None:
        if replica_item_path.is_dir():
            self._remove_directory_that_not_exist_in_source(replica_item_path, source_folder_data)
        else:
            self._remove_file_that_not_exists_in_source(replica_item_path, source_folder_data)

    def _remove_directory_that_not_exist_in_source(
            self, replica_item_path: pathlib.Path, source_folder_data: FolderDataDTO
    ) -> None:
        shutil.rmtree(replica_item_path)
        self._file_logger.log_deleted_directory_from_replica(source_folder_data.folder_path, replica_item_path)

    def _remove_file_that_not_exists_in_source(
            self, replica_item_path: pathlib.Path, source_folder_data: FolderDataDTO
    ) -> None:
        os.remove(replica_item_path)
        self._file_logger.log_deleted_file_from_replica(source_folder_data.folder_path, replica_item_path)




