from planefinder import logging
from pathlib import Path


def test_logging_setup():
    log_file = Path(__file__).parent.joinpath("logging-test.log")
    logging.setup_applevel_logger(file_name=log_file)
    log = logging.get_logger(__file__)
    log.debug("Logging debug")
