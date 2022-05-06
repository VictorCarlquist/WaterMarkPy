import sys

from watermarkpy.watermark import WMImage
from PIL import Image


def helpMessages():
    print("### WaterMarkPy allows to add watermark in images ###")
    print()
    print("To add a watermark in the center of one image, run:")
    print()
    print("> watermarkpy-image -i nameMain.bmp -w nameWM.png -o name_output")
    print()
    print("To add a watermark in the center of multiples images in a folder, run:")
    print()
    print("> watermarkpy-image -d imgs/ -w nomeWM.png")
    print()
    print(
        "To scale (resize) the watermark image and define a relative position in one image, run:"
    )
    print()
    print(
        "> watermarkpy-image -i imgs/name.bmp -w nameWM.png -s 10 -mt 25 -ml 25 -o nomeSaida"
    )
    print()
    print(
        "To scale (resize) the watermark image and define a"
        "relative position in multiples image in a folder, run:"
    )
    print()
    print("> watermarkpy-image -d imgs/ -w nameWM.png -s 30 -mt 25 -ml 25")
    print()
    print()
    print("\tParameters: ")
    print("\t-i path to image.                          ex: -i img/img.bmp")
    print("\t-w path to watermark image.                ex: -i img/wm.bmp")
    print("\t-d path to folder with images.             ex: -d img/")
    print("\t-s scale/resize (in %) watermark           ex: -s 30")
    print("\t proportional of the main image.")
    print("\t-mt margin TOP in %.                       ex: -mt 20")
    print("\t-ml margem LEFT in %.                      ex: -ml 20")
    print("\t-adjust color of the watermark             ex: -adjust")
    print("\t considering bg color of the main image")
    print("\t-p Add a prefix in the name of output      ex: -p water")
    print("\t image in a batch operation.")
    print()


def main():
    main_img = None
    outputName = None
    dirImgs = None
    prefix = ""
    watermarkPath = None
    scale = 100
    mt = None
    ml = None
    adjust = False
    alpha = 255
    index = 1
    while index < len(sys.argv):
        arg = sys.argv[index]
        if arg == "-i":
            index = index + 1
            main_img = sys.argv[index]
        elif arg == "-o":
            index = index + 1
            outputName = sys.argv[index]
        elif arg == "-d":
            index = index + 1
            dirImgs = sys.argv[index]
        elif arg == "-p":
            index = index + 1
            prefix = sys.argv[index]
        elif arg == "-w":
            index = index + 1
            watermarkPath = sys.argv[index]
        elif arg == "-s":
            index = index + 1
            scale = sys.argv[index]
        elif arg == "-mt":
            index = index + 1
            mt = sys.argv[index]
        elif arg == "-ml":
            index = index + 1
            ml = sys.argv[index]
        elif arg == "-a":
            index = index + 1
            alpha = int(sys.argv[index])
        elif arg == "-adjust":
            adjust = True
        index = index + 1

    # batch images to center water (-d -w)
    if dirImgs and watermarkPath and not scale:
        images = WMImage.batchWMImageCenter(
            dirImgs, watermarkPath, prefix, alpha, adjust
        )
        for img, path, prefix in images:
            WMImage.saveImg(img, path, prefix)

    # (-d -w -s -mt -ml)
    elif dirImgs and watermarkPath and scale and mt and ml:
        images = WMImage.batchWMImage(
            dirImgs, watermarkPath, mt, ml, prefix, scale, alpha, adjust
        )
        for img, path, prefix in images:
            WMImage.saveImg(img, path, prefix)

    # (-i -w -o)
    elif main_img and watermarkPath and outputName and not mt and not ml:
        with Image.open(main_img) as main, Image.open(watermarkPath) as wm:
            main = Image.open(main_img)
            wm_obj = WMImage(main, wm)
            img = wm_obj.createWMCenter(scale, alpha, adjust)
            WMImage.saveImg(img, outputName)

    # (-i -w -o -s -mt -ml)
    elif main_img and watermarkPath and outputName and scale and mt and ml:
        with Image.open(main_img) as main, Image.open(watermarkPath) as wm:
            wm_obj = WMImage(main, wm)
            img = wm_obj.createWMCustom(mt, ml, scale, alpha, adjust)
            WMImage.saveImg(img, outputName)
    else:
        helpMessages()


if __name__ == "__main__":
    main()
