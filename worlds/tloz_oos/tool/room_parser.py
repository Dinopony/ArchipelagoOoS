import os

from settings import get_settings
from worlds.tloz_oos.common.patching.RomData import RomData
from worlds.tloz_oos.common.patching.rooms.decoding import decompress_rooms
from worlds.tloz_oos.common.patching.rooms.tools import dump_rooms_to_txt

if __name__ == "__main__":
    if not os.path.isdir("output"):
        os.mkdir("output")
    file_name = get_settings()["tloz_oos_options"]["rom_file"]
    rom = RomData(bytes(open(file_name, "rb").read()))
    rooms = decompress_rooms(rom, seasons=True)
    dump_rooms_to_txt(rooms, "output")