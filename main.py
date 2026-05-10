import argparse
from three_ds.main import main as main_3ds

parser = argparse.ArgumentParser()
parser.add_argument("command", help="Name of the command")

args = parser.parse_args()
if args.command == "3ds":
    main_3ds()
