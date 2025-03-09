from wand import image
import sys
import os.path

def convert(imgpath, output_dir):
    # Takes a path to an image, converts to DDS and writes to the given directory
    with image.Image(filename=imgpath) as img:
        import code
        imgfile = os.path.basename(imgpath)
        targetfile = os.path.splitext(imgfile)[0]+".dds"
        targetpath = os.path.join(output_dir, targetfile)
        print(targetpath)
        #code.interact(local=locals())
        img.compression = 'dxt5'
        img.save(filename=targetpath)

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
