import argparse
import logging
import logging.config
import os

from app.utils.exceptions import InvalidError


class TreeLogger:
    _logger = None
    _initialized = False

    def __init__(self, name="root"):
        TreeLogger.build()
        TreeLogger._logger = logging.getLogger(name=name)

    @staticmethod
    def build(filename=None):
        if not TreeLogger._initialized:
            if filename is None:
                parser = argparse.ArgumentParser(__name__)
                parser.add_argument('--logging', type=str,
                                    help='Logging file path', default=None)
                args, unknown = parser.parse_known_args()
                if args.logging is None:
                    # Adjust this path to point to the project root logging.ini
                    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
                    filename = os.path.join(base_dir, "logging.ini")
                else:
                    filename = args.logging

            if not os.path.exists(filename):
                raise InvalidError(f"Logging config file not found at: {filename}")

            logging.config.fileConfig(fname=filename)
            TreeLogger._initialized = True
            logging.debug("Logging config file loaded from: {}".format(os.path.abspath(filename)))

    @property
    def get_logger(self):
        return TreeLogger._logger

    @staticmethod
    def _get_debug_msg(debug):
        return "debug: {}".format(debug).rstrip("\n")

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls._logger.info(msg, *args, **kwargs)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls._logger.debug(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls._logger.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls._logger.error(msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg, *args, exc_info=True, **kwargs):
        cls._logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        cls._logger.critical(msg, *args, **kwargs)


def get_logger(name="root"):
    """
    Get a logger instance with the specified name.
    :param name: The name of the logger.
    :return: Logger instance.
    """
    return TreeLogger(name=name)
