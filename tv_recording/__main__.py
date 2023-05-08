from .cli import CLI
from .parser import get_logger, get_parser_and_args


def main():
    """
    Main entry point
    """
    # Parse command line arguments
    args, parser = get_parser_and_args()

    # Create logger
    logger = get_logger(args.log_level)

    # Create a new instance of the app
    cli = CLI(args, parser, logger)

    # Run the app
    cli.execute()
