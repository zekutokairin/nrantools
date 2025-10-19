import os
from PIL import Image

TEMPLATE_PATH = os.path.join("resources","art_templates","FrontTemplate.png")
TEMPLATE_SIZE = 512,120

image_path = os.path.join("tests","spnlbrk.jpg")
template = Image.open(TEMPLATE_PATH).convert('RGBA')
marquee = Image.open(image_path).convert('RGBA')

romdir = os.getenv("NRAN_ROMDIR")
basedir = os.getenv("NRAN_BASEDIR")

def cabinetart(basename):
    marquee.thumbnail(size, Image.Resampling.LANCZOS)
    # placement at (512-width of image)/2
    # TODO: moa lot of these function should be 

if __name__ == "__main__":
    marquee.thumbnail(TEMPLATE_SIZE , Image.Resampling.LANCZOS)
>>>>>>> 226dd90ca3b79201f6404a2a4756420d116e3ee8
    offset = int((512-marquee.size[0])/2)

    # Insert into template image at coordinates 0,51:
    template.paste(marquee,(offset,51),marquee)
<<<<<<< HEAD
    #template.paste(marquee,(51,60),marquee)

    #Image.Image.alpha_composite(template.convert('RGBA'), marquee.convert('RGBA'))
    #template.alpha_composite(marquee)
    #template.alpha_composite(marquee,(51,offset), marquee.convert('RGBA'))
    import code
    #code.interact(local=locals())
    template.save("output.png")


if __name__ == "__main__":
    cabinetart("spnlbrk")

=======
>>>>>>> 226dd90ca3b79201f6404a2a4756420d116e3ee8
