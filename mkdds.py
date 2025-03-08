from wand import image
import sys

with image.Image(filename=sys.argv[1]) as img:
    img.compression = 'dxt5'
    img.save(filename='output.dds')

