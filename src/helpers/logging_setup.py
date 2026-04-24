import logging


def logging_setup(level: int = logging.INFO, log_file: str = "app.log") -> None:
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    has_stream = any(h.__class__ is logging.StreamHandler for h in logger.handlers)
    has_file = any(isinstance(h, logging.FileHandler) for h in logger.handlers)

    if not has_stream:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if not has_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
