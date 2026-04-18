from worlds.tloz_oos.common.spriter.microbmp import MicroBMP
from worlds.tloz_oos.common.spriter.sprite import link_palette
from worlds.tloz_oos.common.spriter.sprite.encoding import remap_sprite

if __name__ == "__main__":
    # Test reader
    image = MicroBMP().load("output/link_bw.bmp")
    remap_sprite(image)
    image.save("output/link_bw3.bmp")
    image.palette = link_palette
    image.save("output/link_g2.bmp")
    image = MicroBMP().load("output/link_g.bmp")
    remap_sprite(image)
    image.save("output/link_g3.bmp")
