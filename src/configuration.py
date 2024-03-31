import argparse
import os
import typing


class Configuration:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Folder synchronization application')
        parser.add_argument('source', type=str, help='Source folder path')
        parser.add_argument('replica', type=str, help='Replica folder path')
        parser.add_argument('--log-file', type=str, default='log.txt', help='Log file path')
        parser.add_argument('--time-period', type=int, default=5, help='Time period for synchronization')
        self._args = parser.parse_args()

    @property
    def source(self):
        return self._args.source

    @property
    def replica(self):
        return self._args.replica

    @property
    def log_file(self):
        return self._args.log_file

    @property
    def time_period(self):
        return self._args.time_period

    def get_errors_if_exists(self) -> typing.List[str]:
        errors = []

        if not os.path.isdir(self.source):
            errors.append(f"Source folder {self.source!r} does not exist")

        if os.path.abspath(self.source) == os.path.abspath(self.replica):
            errors.append("Replica folder can not be the same as the source folder")
        if not (os.path.isdir(self.replica) or self._try_create_dir(self.replica)):
            errors.append(f"Replica folder {self.replica!r} does not exist and could not be created")

        if self.time_period < 1:
            errors.append(f"Seconds between sync must be greater than zero, current value is {self.time_period!r}")

        return errors

    @staticmethod
    def _try_create_dir(path: str) -> bool:
        try:
            os.mkdir(path)
            return True
        except OSError:
            return False
