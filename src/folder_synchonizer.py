import os
import hashlib
import shutil
import pathlib
import typing

from .folder_data_dto import FolderDataDTO
from .log_msg_creator import LogMsgCreator


class FolderSynchronizer:
    def __init__(self, log_msg_creator: LogMsgCreator):
        self._log_msg_creator = log_msg_creator

    def synchronize(self, source_folder: pathlib.Path, replica_folder: pathlib.Path) -> None:
        self._check_folders_exist(source_folder, replica_folder)
        source = FolderDataDTO(pathlib.Path(source_folder), self._get_set_items_from_folder(source_folder))
        replica = FolderDataDTO(pathlib.Path(replica_folder), self._get_set_items_from_folder(replica_folder))
        self._sync_source_items_to_replica_folder(source, replica)
        self._sync_replica_items_to_source_folder(replica, source)

    def _check_folders_exist(self, source_folder: pathlib.Path, replica_folder: pathlib.Path):
        if not os.path.isdir(source_folder):
            os.makedirs(source_folder)
            self._log_msg_creator.log_create_directory(source_folder)

        if not os.path.isdir(replica_folder):
            os.makedirs(replica_folder)
            self._log_msg_creator.log_create_directory(replica_folder)

    @staticmethod
    def _get_set_items_from_folder(folder: str | pathlib.Path) -> typing.Set[pathlib.Path]:
        return set(pathlib.Path(os.path.join(folder, item)) for item in os.listdir(folder))

    def _sync_source_items_to_replica_folder(self, source: FolderDataDTO, replica: FolderDataDTO) -> None:
        for source_item in source.internal_items:
            self._sync_source_item_to_replica_folder(source_item, replica)

    def _sync_source_item_to_replica_folder(
            self, source_item: pathlib.Path, replica: FolderDataDTO
    ) -> None:
        replica_item_path = pathlib.Path(replica.folder_path, source_item.name)
        if replica_item_path in replica.internal_items:
            self._work_with_items_which_exist_in_both_folders(source_item, replica_item_path)
        else:
            self._work_with_items_which_not_exist_in_replica_folder(source_item, replica_item_path)

    def _work_with_items_which_exist_in_both_folders(
            self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path
    ) -> None:
        if source_item_path.is_dir():
            self.synchronize(source_item_path, replica_item_path)
        elif self._check_if_two_files_equal(source_item_path, replica_item_path):
            self._log_msg_creator.log_file_up_to_date(source_item_path, replica_item_path)
        else:
            self._update_file_in_replica(source_item_path, replica_item_path)

    @staticmethod
    def _check_if_two_files_equal(file_name_1: pathlib.Path, file_name_2: pathlib.Path) -> bool:
        if os.path.getsize(file_name_1) != os.path.getsize(file_name_2):
            return False
        with file_name_1.open(mode='rb') as file_1, file_name_2.open(mode='rb') as file_2:
            compare_1 = hashlib.md5(file_1.read()).hexdigest()
            compare_2 = hashlib.md5(file_2.read()).hexdigest()
            return compare_1 == compare_2

    def _update_file_in_replica(self, source_item_path: pathlib.Path, replica_item_data: pathlib) -> None:
        shutil.copy2(source_item_path, replica_item_data)
        self._log_msg_creator.log_updated_file_in_replica(source_item_path, replica_item_data)

    def _work_with_items_which_not_exist_in_replica_folder(
            self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path
    ) -> None:
        if source_item_path.is_dir():
            self._copy_directory_to_replica(source_item_path, replica_item_path)
        else:
            self._copy_file_to_replica(source_item_path, replica_item_path)

    def _copy_directory_to_replica(self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path) -> None:
        shutil.copytree(source_item_path, replica_item_path)
        self._log_msg_creator.log_copy_directory_to_replica(source_item_path, replica_item_path)

    def _copy_file_to_replica(self, source_item_path: pathlib.Path, replica_item_data: pathlib.Path) -> None:
        shutil.copy2(source_item_path, replica_item_data)
        self._log_msg_creator.log_copy_file_to_replica(source_item_path, replica_item_data)

    def _sync_replica_items_to_source_folder(
            self, replica_folder_data: FolderDataDTO, source_folder_data: FolderDataDTO
    ) -> None:
        for replica_item in replica_folder_data.internal_items:
            source_item_path = pathlib.Path(os.path.join(source_folder_data.folder_path, replica_item.name))
            if source_item_path not in source_folder_data.internal_items:
                self._work_with_item_which_not_exists_in_source(replica_item, source_folder_data)

    def _work_with_item_which_not_exists_in_source(
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
        self._log_msg_creator.log_deleted_directory_from_replica(source_folder_data.folder_path, replica_item_path)

    def _remove_file_that_not_exists_in_source(
            self, replica_item_path: pathlib.Path, source_folder_data: FolderDataDTO
    ) -> None:
        os.remove(replica_item_path)
        self._log_msg_creator.log_deleted_file_from_replica(source_folder_data.folder_path, replica_item_path)




