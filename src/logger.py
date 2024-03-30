import logging


class Logger:
    def __init__(self, file_name: str) -> None:
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)
        self._configure_logger(file_name)

    def _configure_logger(self, file_name: str) -> None:
        formatter = self._create_formatter()
        file_handler = self._create_file_handler(file_name, formatter)
        stream_handler = self._create_stream_handler(formatter)
        self._add_handlers(file_handler, stream_handler)

    @staticmethod
    def _create_formatter() -> logging.Formatter:
        format_log = '%(asctime)s [%(levelname)s]: %(message)s'
        formatter = logging.Formatter(format_log)
        return formatter

    @staticmethod
    def _create_file_handler(file_name: str, formatter: logging.Formatter) -> logging.FileHandler:
        file_handler = logging.FileHandler(file_name, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        return file_handler

    @staticmethod
    def _create_stream_handler(formatter: logging.Formatter) -> logging.StreamHandler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        return stream_handler

    def _add_handlers(self, *handlers) -> None:
        for handler in handlers:
            self._logger.addHandler(handler)

    def log(self, message: str) -> None:
        log_msg = f'- {message}'
        self._logger.info(log_msg)
