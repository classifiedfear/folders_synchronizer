import pathlib
import time
import typing

from configuration import Configuration
from log_msg_creator import LogMsgCreator
from logger_factory import LoggerFactory
from folder_synchonizer import FolderSynchronizer


class Application:
    @staticmethod
    def run():
        configuration = Configuration()
        errors = configuration.get_errors_if_exists()
        try:
            logger_factory = LoggerFactory(configuration.log_file)
        except FileNotFoundError:
            raise ValueError(errors)

        log_msg_creator = LogMsgCreator(logger_factory.get_logger())
        Application._check_on_errors(errors, log_msg_creator)

        folder_synchronizer = FolderSynchronizer(log_msg_creator)
        log_msg_creator.log_start_sync(
            configuration.source, configuration.replica, configuration.log_file, configuration.time_period
        )
        Application._main(configuration, folder_synchronizer, log_msg_creator)

    @staticmethod
    def _main(configuration: Configuration, folder_synchronizer: FolderSynchronizer, log_msg_creator: LogMsgCreator):
        while True:
            try:
                errors = configuration.get_errors_if_exists()
                Application._check_on_errors(errors, log_msg_creator)
                start = time.time()
                folder_synchronizer.synchronize(pathlib.Path(configuration.source), pathlib.Path(configuration.replica))
                wait = start + configuration.time_period - time.time()
                if wait > 0:
                    time.sleep(wait)
            except KeyboardInterrupt:
                log_msg_creator.log_terminated_manually()
                raise SystemExit

    @staticmethod
    def _check_on_errors(errors: typing.List[str], log_msg_creator: LogMsgCreator):
        if errors:
            for error in errors:
                log_msg_creator.log_error(error)
            raise ValueError(errors)


if __name__ == '__main__':
    Application.run()
