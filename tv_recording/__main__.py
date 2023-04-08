from .cli import CLI
from .parser import get_args, get_logger


def main():
    """
    Main entry point
    """
    # Parse command line arguments
    args = get_args()

    # Create logger
    logger = get_logger(args.log_level)

    # Create a new instance of the app
    cli = CLI(args, logger)

    # Run the app
    cli.run()
