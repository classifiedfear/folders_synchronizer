
import os
import time

from src.configuration import Configuration
from src.file_logger import FileLogger
from src.folder_synchonizer import FolderSynchronizer


class Application:
    @staticmethod
    def run():
        configuration = Configuration()
        Application._check_folders_exist(configuration.source, configuration.replica)
        file_logger = FileLogger(configuration.log_file)
        folder_synchronizer = FolderSynchronizer(file_logger)

        while True:
            try:
                folder_synchronizer.synchronize(configuration.source, configuration.replica)
                time.sleep(configuration.time_period)
            except KeyboardInterrupt:
                file_logger.log('Terminated manually!')
                raise SystemExit

    @staticmethod
    def _check_folders_exist(source_folder: str, replica_folder: str):
        if not os.path.isdir(source_folder):
            os.makedirs(source_folder)
        if not os.path.isdir(replica_folder):
            os.makedirs(replica_folder)


if __name__ == '__main__':
    Application.run()


