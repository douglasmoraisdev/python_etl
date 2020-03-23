GENERAL = {
    "cycle_sleep_time": 3,
    "max_process": 5,
    "transformed_path": "data/work/transformed/",
}

GOOGLE_MAPS = {
    "geocode_api_url": "https://maps.googleapis.com/maps/api/geocode/json",
    "api_key": "<your_api_key>"
}

MESSAGE_BROKER = {
    "broker_url": "rabbitmq",
    "broker_queue": "transformed",
    "broker_routing_key": "transformed"
}

DATABASE = {
    "db_host": "mysql",
    "database": "etl4all",
    "username": "root",
    "password": "example",
}

LOOKUP_DB = {
    "db_host": "mongo",
    "db_port": 27017,
    "database": "etl4all_lookup",
    "username": "root",
    "password": "example",
}

ERROR_HANDLER = {
    "max_general_errors": 5,
    "general_errors_retry_timeout": 3
}
