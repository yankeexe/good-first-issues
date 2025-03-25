import argparse
import logging
import sys
from datetime import datetime

# Configure argument parser
parser = argparse.ArgumentParser(description="A script with logging capabilities.")
parser.add_argument("--log", action="store_true", help="Enable logging for debugging.")

# Parse arguments
args = parser.parse_args()

# Configure logging
if args.log:
    log_filename = f"logs/debug_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    print(f"Logging enabled. Logs will be saved in: {log_filename}")

    # Log script start
    logging.info("Script started.")


# Example script functionality
def main():
    try:
        logging.info("Executing main function.")
        # Simulating an event
        print("Hello, World!")
        logging.info("Execution successful.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
