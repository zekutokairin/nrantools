import os
from PIL import Image

TEMPLATE_PATH = os.path.join("resources","art_templates","FrontTemplate.png")
TEMPLATE_SIZE = 512,120

image_path = os.path.join("tests","spnlbrk.jpg")
template = Image.open(TEMPLATE_PATH).convert('RGBA')
marquee = Image.open(image_path).convert('RGBA')

romdir = os.getenv("NRAN_ROMDIR")
basedir = os.getenv("NRAN_BASEDIR")

def make_cabinetart(basename):
    # TODO: Given romset base name, look in marquee directory and make 
    

if __name__ == "__main__":
    marquee.thumbnail(TEMPLATE_SIZE , Image.Resampling.LANCZOS)
    offset = int((512-marquee.size[0])/2)

    # Insert into template image at coordinates 0,51:
    template.paste(marquee,(offset,51),marquee)
