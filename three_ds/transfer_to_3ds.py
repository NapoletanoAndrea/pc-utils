from .common.helpers import move_contents
from .common.data import get_full_paths


def transfer_to_3ds():
    paths = get_full_paths()

    for name, paths in paths.items():
        print(f"Transferring {name} to 3DS...")
        move_contents(paths["pc"], paths["console"])

    print("Transfer complete!")
