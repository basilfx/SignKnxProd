from xml2pdb.utils import VerboseAction, PathAction, NewPathAction
from xml2pdb import converter

import argparse
import logging
import sys

# Logger instance.
logger = logging.getLogger(__name__)


def parse_arguments():
    """
    Parse commandline arguments.
    """

    parser = argparse.ArgumentParser()

    # Add positional arguments.
    parser.add_argument(
        "master", action=PathAction, help="path to the master file")
    parser.add_argument(
        "source", action=PathAction, help="path to source template to convert")
    parser.add_argument(
        "destination", action=NewPathAction, default=None,
        help="path to destination folder (will be created)")

    # Add other arguments.
    parser.add_argument(
        "-d", "--define", action="append", type=str,
        help="define key=value for the pre-processing stage")
    parser.add_argument(
        "-v", "--verbose", nargs="?", action=VerboseAction, default=0,
        help="toggle verbose mode (-vv, -vvv for more)")
    parser.add_argument(
        "-l", "--log-file", action=NewPathAction, help="log file")

    # Parse command line.
    return parser.parse_args(), parser


def setup_logging(console=True, log_file=None, verbose=False):
    """
    Setup logging.

    :param bool console: If True, log to console.
    :param str log_file: If set, log to a file (append) as specified.
    :param bool verbose: Enable debug logging if True.
    """

    # Configure logging
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    level = logging.DEBUG if verbose else logging.INFO

    # Add console output handler
    if console:
        console_log_handler = logging.StreamHandler()
        console_log_handler.setLevel(level)
        console_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_log_handler)

    # Add file output handler
    if log_file:
        file_log_handler = logging.FileHandler(log_file)
        file_log_handler.setLevel(level)
        file_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_log_handler)

    logging.getLogger().setLevel(level)
    logger.info("Verbose level is %d", verbose)


def main():
    """
    Main entry point. Parses arguments and starts the converter.
    """

    # Parse arguments and setup logging.
    arguments, parser = parse_arguments()

    setup_logging(True, arguments.log_file, arguments.verbose)

    # Run application.
    context = {}

    converter.run(
        arguments.master, arguments.source, arguments.destination, context)


# E.g. `python Xml2PDb.py master.xml source.xml`.
if __name__ == "__main__":
    sys.exit(main())
