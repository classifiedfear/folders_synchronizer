Folders Synchronizer.
Program that one-way synchronizes two folders.
Synchronization performs periodically, make changes(copy, remove, update) in folders, displayed and written to a log file.


Usage example:
	source: Path to the source folder to be synchronized (required)
 	replica: Path to the replica folder to be synchonized (requerd)
	--log-file: Path to the log-file (default: log.txt)
	--time-period: Period for synchonization in seconds (default: 5)
	python main.py source_folder_dest replica_folder_dest --log-file log_file_dest --time-period period_to_sync_folders
