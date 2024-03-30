import asyncio
import os
import pathlib
import time

from src.configuration import Configuration
from src.log_msg_creator import LogMsgCreator
from src.logger import Logger
from src.folder_synchonizer import FolderSynchronizer


class Application:
    @staticmethod
    def run():
        configuration = Configuration()
        logger = Logger(configuration.log_file)
        file_logger = LogMsgCreator(logger)
        folder_synchronizer = FolderSynchronizer(file_logger)

        while True:
            try:
                start = time.time()
                folder_synchronizer.synchronize(pathlib.Path(configuration.source), pathlib.Path(configuration.replica))
                before_next_sync = start + configuration.time_period - time.time()
                if before_next_sync > 0:
                    time.sleep(before_next_sync)
            except KeyboardInterrupt:
                logger.log('Terminated manually!')
                raise SystemExit


if __name__ == '__main__':
    Application.run()


