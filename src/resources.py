file_up_to_date = '- {!r} file from source {!r} does not need change in replica {!r}.'
file_has_been_updated = '- {!r} file from source {!r} has been updated in replica {!r}.'
file_deleted_from_replica = """
- {!r} file has been deleted from source {!r}, because does not exist in replica {!r}.
"""
file_copied_to_replica = '- {!r} file from source {!r} has been copied in replica {!r}.'
directory_copied_to_replica = '- Folder from source {!r} was copied to replica {!r}.'
directory_deleted_from_replica = '- Deleted folder from replica {!r} that not exists in source {!r}.'
folder_created = '- {!r} was created.'
error_existence_source = '- Source folder {!r} does not exist.'
error_same_folders = '- Replica folder can not be the same as the source folder.'
error_existence_replica = '- Replica folder {!r} does not exist and could not be created.'
error_time_period = '- Seconds between sync must be greater than zero, current value is {!r}.'
error_log_file_folder = '- Folder {!r} for log-file {!r} can not be created.'
start_sync = """
- Starting synchronization with parameters:
    source - {!r};
    replica - {!r};
    log-file - {!r};
    time-period - {!r} sec.
        
Ctrl+C to exit.
"""
