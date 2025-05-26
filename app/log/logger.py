import logging
import sys

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Evita duplicados
if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Log a archivo
    file_handler = logging.FileHandler("./app/log/app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log a consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
