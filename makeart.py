import os
from PIL import Image

TEMPLATE_PATH = os.path.join("resources","art_templates","FrontTemplate.png")

size = 512,120

image_path = os.path.join("tests","spnlbrk.jpg")
template = Image.open(TEMPLATE_PATH).convert('RGBA')
marquee = Image.open(image_path).convert('RGBA')

def cabinetart(basename):
    marquee.thumbnail(size, Image.Resampling.LANCZOS)
    # placement at (512-width of image)/2
    offset = int((512-marquee.size[0])/2)
    print(offset)

    # Insert into template image at coordinates 0,51:
    # FIXME: Maybe we need to remove alpha channel from template
    #           due to PIL weirdness??
    #template.paste(marquee,(51,offset), marquee.convert('RGBA'))
    template.paste(marquee,(offset,51),marquee)
    #template.paste(marquee,(51,60),marquee)

    #Image.Image.alpha_composite(template.convert('RGBA'), marquee.convert('RGBA'))
    #template.alpha_composite(marquee)
    #template.alpha_composite(marquee,(51,offset), marquee.convert('RGBA'))
    import code
    #code.interact(local=locals())
    template.save("output.png")


if __name__ == "__main__":
    cabinetart("spnlbrk")

