import os

from settings import get_settings
from worlds.tloz_oos.common.patching.RomData import RomData
from worlds.tloz_oos.common.patching.rooms.decoding import decompress_rooms
from worlds.tloz_oos.common.patching.rooms.encoding import write_room_data
from worlds.tloz_oos.common.patching.rooms.tools import dump_rooms_to_txt

if __name__ == "__main__":
    if not os.path.isdir("output"):
        os.mkdir("output")
    file_name = get_settings()["tloz_oos_options"]["rom_file"]
    rom = RomData(bytes(open(file_name, "rb").read()))
    rooms = decompress_rooms(rom, True)
    dump_rooms_to_txt(rooms, "output")
    write_room_data(rom, rooms, True)
    rooms2 = decompress_rooms(rom, True)

    for room_id in range(len(rooms)):
        assert rooms[room_id] == rooms2[room_id], f"Room {hex(room_id)} was parsed wrong"
