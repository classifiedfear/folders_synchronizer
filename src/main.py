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
        errors = configuration.get_errors_if_exists()
        try:
            logger_factory = LoggerFactory(configuration.log_file)
        except FileNotFoundError:
            raise ValueError(errors)

        log_msg_creator = LogMsgCreator(logger_factory.get_logger())
        if errors:
            for error in errors:
                log_msg_creator.log_error(error)
            raise ValueError(errors)

        folder_synchronizer = FolderSynchronizer(log_msg_creator)
        log_msg_creator.log_start_sync(
            configuration.source, configuration.replica, configuration.log_file, configuration.time_period
        )
        Application._main(configuration, folder_synchronizer, log_msg_creator)

    @staticmethod
    def _main(configuration: Configuration, folder_synchronizer: FolderSynchronizer, log_msg_creator: LogMsgCreator):
        while True:
            try:
                Application._create_folders_if_not_exists(configuration.source, configuration.replica, log_msg_creator)
                start = time.time()
                folder_synchronizer.synchronize(pathlib.Path(configuration.source), pathlib.Path(configuration.replica))
                wait = start + configuration.time_period - time.time()
                if wait > 0:
                    time.sleep(wait)
            except KeyboardInterrupt:
                log_msg_creator.log_terminated_manually()
                raise SystemExit

    @staticmethod
    def _create_folders_if_not_exists(
            source_folder: pathlib.Path, replica_folder: pathlib.Path, log_msg_creator: LogMsgCreator
    ) -> None:
        if not source_folder.exists():
            source_folder.mkdir()
            log_msg_creator.created_folder(source_folder)

        if not replica_folder.exists():
            replica_folder.mkdir()
            log_msg_creator.created_folder(replica_folder)


if __name__ == '__main__':
    Application.run()
