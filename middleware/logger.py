import logging

# Formatter: timestamp, level, and message
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler only
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Logger setup
logger = logging.getLogger("SmanCortexLogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

# Prevent log duplication
logger.propagate = False
