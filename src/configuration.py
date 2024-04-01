import argparse
import pathlib
import typing

from resources import error_existence_source, error_same_folders, error_existence_replica, error_time_period, \
    error_log_file_folder


class Configuration:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Folder synchronization application')
        parser.add_argument('source', type=str, help='Source folder path')
        parser.add_argument('replica', type=str, help='Replica folder path')
        parser.add_argument('--log-file', type=str, default='log.txt', help='Log file path')
        parser.add_argument(
            '--time-period', type=int, default=5, help='Time period for synchronization in seconds'
        )
        self._args = parser.parse_args()

    @property
    def source(self):
        return pathlib.Path(self._args.source)

    @property
    def replica(self):
        return pathlib.Path(self._args.replica)

    @property
    def log_file(self):
        return pathlib.Path(self._args.log_file)

    @property
    def time_period(self):
        return self._args.time_period

    def get_errors_if_exists(self) -> typing.List[str]:
        errors = []

        if not (self.log_file.parent.exists() or self._try_create_dir(self.log_file.parent)):
            errors.append(error_log_file_folder.format(self.log_file.parent, self.log_file.name))

        if not self.source.exists():
            errors.append(error_existence_source.format(self.source))

        if self.source.absolute() == self.replica.absolute():
            errors.append(error_same_folders)

        if not (self.replica.exists() or self._try_create_dir(self.replica)):
            errors.append(error_existence_replica.format(self.replica))

        if self.time_period < 1:
            errors.append(error_time_period.format(self.time_period))

        return errors

    @staticmethod
    def _try_create_dir(path: pathlib.Path) -> bool:
        try:
            path.mkdir()
            return True
        except OSError:
            return False
