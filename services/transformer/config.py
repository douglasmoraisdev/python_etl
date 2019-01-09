GENERAL = {
    "cycle_sleep_time": 3,
    "max_process": 4,
    "extracted_path": "data/work/extracted/",
    "transformed_path": "data/work/transformed/",
}

GOOGLE_MAPS = {
    "geocode_api_url": "https://maps.googleapis.com/maps/api/geocode/json",
    "api_key": "AIzaSyAPqlDhdKGmxjaWWxj1EcpmbPV5LNhwW7c"
}

MESSAGE_BROKER = {
    "broker_url": "rabbitmq",
    "extracted_queue": "extracted",
    "transformed_queue": "transformed",
}

ERROR_HANDLER = {
    "max_general_errors": 5,
    "general_errors_retry_timeout": 3
}
