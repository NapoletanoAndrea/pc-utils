from .transfer_to_3ds import transfer_to_3ds
from .transfer_to_pc import transfer_to_pc


def main():
    print("Scegli:\n")

    res = -1

    while (res == -1):
        res = int(input("1. Transfer to PC\n2. Transfer to 3ds\n"))

        if (res == 1):
            transfer_to_pc()
        elif (res == 2):
            transfer_to_3ds()
