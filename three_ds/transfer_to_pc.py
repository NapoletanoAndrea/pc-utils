from .common.helpers import move_contents
from .common.data import get_full_paths


def transfer_to_pc():
    paths = get_full_paths()

    for name, paths in paths.items():
        print(f"Transferring {name} to PC...")
        move_contents(paths["console"], paths["pc"])

    print("Transfer complete!")
