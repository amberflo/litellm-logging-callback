import unittest
import logging

from amberflo.logging import get_logger


# TODO actually assert on the contents of stderr


class TestLogging(unittest.TestCase):
    def test_debug_json(self):
        logger = get_logger("logger1", level=logging.DEBUG, json_logs=True)
        logger.debug("hello1")

    def test_info_normal(self):
        logger = get_logger("logger2", level=logging.INFO, json_logs=False)
        logger.info("hello2")

    def test_exception_normal(self):
        logger = get_logger("logger3", level=logging.INFO, json_logs=False)

        try:
            raise Exception("boom!")
        except Exception:
            logger.exception("hello3")

    def test_exception_json(self):
        logger = get_logger("logger4", level=logging.INFO, json_logs=True)

        try:
            raise Exception("boom!")
        except Exception:
            logger.exception("hello4")
