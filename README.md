Folders Synchronizer.
Program that one-way synchronizes two folders.
Synchronization performs periodically, make changes(copy, remove, update) in folders, displayed and written to a log file.


Usage example:

	python main.py source_folder_dest replica_folder_dest --log-file log_file_dest --time-period period_to_sync_folders

1) source: Path to the source folder to be synchronized (required)
2) replica: Path to the replica folder to be synchonized (requerd)
3) --log-file: Path to the log-file (default: log.txt)
4) --time-period: Period for synchonization in seconds (default: 5)
