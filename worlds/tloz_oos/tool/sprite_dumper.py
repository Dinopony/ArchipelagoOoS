import os

from settings import get_settings
from worlds.tloz_oos.common.patching.RomData import RomData
from worlds.tloz_oos.common.spriter.microbmp import MicroBMP
from worlds.tloz_oos.common.spriter.sprite import bw_palette, green_palette
from worlds.tloz_oos.common.spriter.sprite.decoding import load_link_data, load_link_sprite
from worlds.tloz_oos.common.spriter.sprite.encoding import encode_sprite, remap_sprite

if __name__ == "__main__":
    if not os.path.isdir("output"):
        os.mkdir("output")
    file_name = get_settings().tloz_oos_options.rom_file
    rom = RomData(bytes(open(file_name, "rb").read()))
    sprite_data = load_link_data(rom)
    image = load_link_sprite(sprite_data, True)
    image.palette = bw_palette
    image.save("output/link_bw.bmp")
    image.palette = green_palette
    image.save("output/link_g.bmp")

    # Test encoder
    encoded = encode_sprite(image)
    image = load_link_sprite(encoded, True)
    image.palette = bw_palette
    image.save("output/link_bw_2.bmp")

    # Test remapping
    image = MicroBMP().load("output/link_bw.bmp")
    remap_sprite(image)
    image.save("output/link_bw3.bmp")
    image = MicroBMP().load("output/link_g.bmp")
    remap_sprite(image)
    image.save("output/link_g3.bmp")
