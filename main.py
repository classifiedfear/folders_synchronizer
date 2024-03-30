import asyncio
import os


from src.configuration import Configuration
from src.file_logger import FileLogger
from src.logger import Logger
from src.folder_synchonizer import FolderSynchronizer


class Application:
    @staticmethod
    async def run():
        configuration = Configuration()
        Application._check_folders_exist(configuration.source, configuration.replica)
        logger = Logger(configuration.log_file)
        file_logger = FileLogger(logger)
        folder_synchronizer = FolderSynchronizer(file_logger)

        while True:
            try:
                await folder_synchronizer.synchronize(configuration.source, configuration.replica)
                await asyncio.sleep(configuration.time_period)
            except KeyboardInterrupt:
                logger.log('Terminated manually!')
                raise SystemExit

    @staticmethod
    def _check_folders_exist(source_folder: str, replica_folder: str):
        if not os.path.isdir(source_folder):
            os.makedirs(source_folder)
        if not os.path.isdir(replica_folder):
            os.makedirs(replica_folder)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(Application.run())


