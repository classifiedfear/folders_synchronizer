import pathlib
import time

from configuration import Configuration
from log_msg_creator import LogMsgCreator
from logger_factory import LoggerFactory
from folder_synchonizer import FolderSynchronizer


class Application:
    @staticmethod
    def run():
        configuration = Configuration()
        logger_factory = LoggerFactory(configuration.log_file)
        file_logger = LogMsgCreator(logger_factory.get_logger())
        errors = configuration.get_errors_if_exists()
        if errors:
            for error in errors:
                file_logger.log_error(error)
                raise ValueError(error)
        folder_synchronizer = FolderSynchronizer(file_logger)

        while True:
            try:
                start = time.time()
                folder_synchronizer.synchronize(pathlib.Path(configuration.source), pathlib.Path(configuration.replica))
                before_next_sync = start + configuration.time_period - time.time()
                if before_next_sync > 0:
                    time.sleep(before_next_sync)
            except KeyboardInterrupt:
                file_logger.log_terminated_manually()
                raise SystemExit


if __name__ == '__main__':
    Application.run()


