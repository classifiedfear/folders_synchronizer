import argparse


class Configuration:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Folder synchronization application')
        parser.add_argument('--source', type=str, default='source', help='Source folder path')
        parser.add_argument('--replica', type=str, default='replica', help='Replica folder path')
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
