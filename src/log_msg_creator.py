import pathlib

from logging import Logger
from resources import file_up_to_date, file_has_been_updated, directory_copied_to_replica, \
    directory_deleted_from_replica, file_deleted_from_replica, file_copied_to_replica


class LogMsgCreator:
    def __init__(self, logger: Logger):
        self._logger = logger

    def log_file_up_to_date(self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path):
        log_msg = file_up_to_date.format(
            source_item_path.name, str(source_item_path.parent.absolute()), str(replica_item_path.parent.absolute())
        )
        self._logger.info(log_msg)

    def log_copy_file_to_replica(self, source_item_path: pathlib, replica_item_path: pathlib.Path):
        log_msg = file_copied_to_replica.format(
            source_item_path.name, str(source_item_path.parent.absolute()), str(replica_item_path.parent.absolute())
        )
        self._logger.info(log_msg)

    def log_copy_directory_to_replica(self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path):
        log_msg = directory_copied_to_replica.format(
            str(source_item_path.absolute()), str(replica_item_path.parent.absolute())
        )
        self._logger.info(log_msg)

    def log_deleted_directory_from_replica(self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path):
        log_msg = directory_deleted_from_replica.format(
            str(replica_item_path.absolute()), str(source_item_path.absolute()))
        self._logger.info(log_msg)

    def log_deleted_file_from_replica(self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path):
        log_msg = file_deleted_from_replica.format(
            str(replica_item_path.name), str(replica_item_path.parent.absolute()), str(source_item_path.absolute()))
        self._logger.info(log_msg)

    def log_updated_file_in_replica(self, source_item_path: pathlib.Path, replica_item_path: pathlib.Path):
        log_msg = file_has_been_updated.format(
            str(source_item_path.name),
            str(source_item_path.parent.absolute()),
            str(replica_item_path.parent.absolute())
        )
        self._logger.info(log_msg)

    def log_terminated_manually(self):
        self._logger.info('Terminated manually!')

    def log_error(self, error_message):
        self._logger.error(error_message)
