import os

azahar_saves_location = "C:/Users/Andrea/AppData/Roaming/Azahar/sdmc/Nintendo 3DS/00000000000000000000000000000000/00000000000000000000000000000000/title/00040000/"
console_saves_location = "ftp://192.168.1.16:5000/3ds/Checkpoint/saves/"

paths = {
    "tloz_a_link_between_worlds": {"pc": "000ec400/data/00000001/",
                                   "console": "0x00EC4 The Legend of Zelda/transferable/"}
}


def get_full_paths() -> dict[str, dict[str, str]]:
    full_paths = {}
    for game in paths:
        full_paths[game] = {"pc": os.path.join(azahar_saves_location, paths[game]["pc"]),
                            "console": os.path.join(console_saves_location, paths[game]["console"])}
    return full_paths
