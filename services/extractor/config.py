GENERAL = {
    "cycle_sleep_time": 3,
    "max_process": 3,
    "extracted_path": "data/work/extracted/",
}

DATASOURCES = {
    "ftp_ds": {
        "type": "ftp",
        "url": "ftp_files_ds",
        "path": "/",
        "username": "username",
        "password": "mypass",
        "local_path": "data/work/download/"
    }
}

MESSAGE_BROKER = {
    "broker_url": "rabbitmq",
    "broker_queue": "extracted",
    "broker_routing_key": "extracted"
}

ERROR_HANDLER = {
    "max_general_errors": 5,
    "general_errors_retry_timeout": 3
}

CACHE = {
    "host": "redis",
    "port": 6379,
    "db": 0,
    "download_cache_prefix":  "download-",
    "extracted_cache_prefix": "extracted-"
}
