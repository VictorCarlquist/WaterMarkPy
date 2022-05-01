# The MIT License (MIT)

# Copyright (c) 2016 Victor Carlquist

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from re import A
from PIL import Image
import glob, os, sys


class WMImage:
    def __init__(self, im_main, im_watermark):
        self.im_main_filename = im_main.filename
        self.im_watermark_filename = im_watermark.filename
        self.im_main = im_main.convert("RGB")
        self.im_watermark = im_watermark.convert("RGBA")

    @staticmethod
    def _centerWatermark(mainImg, wmImg, ratioSize=100):
        wmImg = WMImage._resizeRelativeGlobalWatermark(mainImg, wmImg, ratioSize)
        wmain, hmain = mainImg.size
        wwater, hwater = wmImg.size

        # calculate new watermark's position
        px = wmain / 2 - wwater / 2
        py = hmain / 2 - hwater / 2

        watermark = wmImg.resize((wwater, hwater), Image.Resampling.LANCZOS)
        return {"wm": watermark, "pos": (px, py)}

    @staticmethod
    def _resizeRelativeGlobalWatermark(mainImg, wmImg, ratioSize):
        wmain, hmain = mainImg.size
        wwater, hwater = wmImg.size

        ratio = (
            min(wmain / float(wwater), hmain / float(hwater)) * float(ratioSize) / 100
        )
        wwater = int(ratio * wwater)
        hwater = int(ratio * hwater)

        watermark = wmImg.resize((wwater, hwater), Image.Resampling.LANCZOS)
        return watermark

    @staticmethod
    def _mergeImgs(mainImg, wmImg, position, alpha=255):
        newImg = mainImg.copy()
        x, y = position
        wmImg.putalpha(alpha)
        newImg.paste(wmImg, (int(x), int(y)), wmImg)
        return newImg

    @staticmethod
    def _mergeImgsNegativeGray(mainImg, wmImg, position, alpha):
        newImg = mainImg.copy()
        wmImg = wmImg.copy()
        wmin, hmin = position
        waux, haux = wmImg.size
        wmax = wmin + waux
        hmax = hmin + haux

        mainW, mainH = newImg.size

        avgP = 0
        for y in range(int(hmin), int(hmax)):
            for x in range(int(wmin), int(wmax)):
                if x < mainW and y < mainH:
                    rgb = newImg.getpixel((x, y))
                    # Calculate AVG Luminance
                    avgP = avgP + rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722

        avgP = avgP / ((hmax - hmin) * (wmax - wmin))
        avgP = max(1, avgP)
        if avgP > 128:
            ratio = 128 / avgP * 0.7
        else:
            ratio = 128 / avgP * 1.3

        for y in range(int(hmin), int(hmax)):
            for x in range(int(wmin), int(wmax)):
                r, g, b, a = wmImg.getpixel((x - wmin, y - hmin))
                r = int(r * ratio)
                g = int(g * ratio)
                b = int(b * ratio)
                wmImg.putpixel((int(x - wmin), int(y - hmin)), (r, g, b, a))

        newImg = WMImage._mergeImgs(mainImg, wmImg, position, alpha)
        return newImg

    @staticmethod
    def _marginWatermark(mainImg, marginRatioTop, marginRatioLeft):
        wmain, hmain = mainImg.size
        px = int(wmain * float(marginRatioLeft) / 100.0)
        py = int(hmain * float(marginRatioTop) / 100.0)
        return px, py

    @staticmethod
    def _saveImg(img, filename="", prefix=""):
        dirname = os.path.dirname(filename)
        if dirname:
            dirname += "/"
        nname = dirname + prefix + os.path.basename(filename).split(".")[0] + ".jpg"
        img.save(nname, "JPEG")

    @staticmethod
    def batchWMImageCenter(
        pathImgs, pathWM, prefix, ratioSize=100, alpha=255, adjustColor=False
    ):
        images = []
        for ext in (
            "*.bmp",
            "*.BMP",
            "*.jpg",
            "*.JPG",
            "*.jpeg",
            "*.JPEG",
            "*.gif",
            "*.GIF",
            "*.png",
            "*.PNG",
        ):
            for path in glob.glob(pathImgs + ext):
                with Image.open(path) as main, Image.open(pathWM) as watermark:
                    vm_obj = WMImage(main, watermark)
                    WMImageCentered = WMImage._centerWatermark(
                        vm_obj.im_main, vm_obj.im_watermark, ratioSize
                    )
                    if adjustColor:
                        main = WMImage._mergeImgsNegativeGray(
                            vm_obj.im_main,
                            WMImageCentered["wm"],
                            WMImageCentered["pos"],
                            alpha,
                        )
                    else:
                        main = WMImage._mergeImgs(
                            vm_obj.im_main,
                            WMImageCentered["wm"],
                            WMImageCentered["pos"],
                            alpha,
                        )
                    images.append((main, vm_obj.im_main_filename, prefix))
        return images

    @staticmethod
    def batchWMImage(
        pathImgs,
        pathWM,
        marginTop,
        marginLeft,
        prefix,
        ratioSize=100,
        alpha=255,
        adjustColor=False,
    ):
        images = []
        for ext in (
            "*.bmp",
            "*.BMP",
            "*.jpg",
            "*.JPG",
            "*.jpeg",
            "*.JPEG",
            "*.gif",
            "*.GIF",
            "*.png",
            "*.PNG",
        ):
            for path in glob.glob(pathImgs + ext):
                with Image.open(path) as main, Image.open(pathWM) as watermark:
                    vm_obj = WMImage(main, watermark)
                    im_wm = WMImage._resizeRelativeGlobalWatermark(
                        vm_obj.im_main, vm_obj.im_watermark, ratioSize
                    )
                    px, py = WMImage._marginWatermark(
                        vm_obj.im_main, marginTop, marginLeft
                    )
                    if adjustColor:
                        main = WMImage._mergeImgsNegativeGray(
                            vm_obj.im_main, im_wm, (px, py), alpha
                        )
                    else:
                        main = WMImage._mergeImgs(
                            vm_obj.im_main, im_wm, (px, py), alpha
                        )
                    images.append((main, path, prefix))
        return images

    def createWMCenter(self, ratioSize=100, alpha=255, adjustColor=False):
        main = self.im_main
        watermark = self.im_watermark
        WMImageCentered = WMImage._centerWatermark(main, watermark, ratioSize)
        if adjustColor:
            main = WMImage._mergeImgsNegativeGray(
                main, WMImageCentered["wm"], WMImageCentered["pos"], alpha
            )
        else:
            main = WMImage._mergeImgs(
                main, WMImageCentered["wm"], WMImageCentered["pos"], alpha
            )
        return main

    def createWMCustom(
        self, marginTop, marginLeft, ratioSize=100, alpha=255, adjustColor=False
    ):
        main = self.im_main
        watermark = self.im_watermark

        im_wm = WMImage._resizeRelativeGlobalWatermark(main, watermark, ratioSize)
        px, py = WMImage._marginWatermark(main, marginTop, marginLeft)
        if adjustColor:
            main = WMImage._mergeImgsNegativeGray(main, im_wm, (px, py), alpha)
        else:
            main = WMImage._mergeImgs(main, im_wm, (px, py), alpha)
        return main


def help():
    print("### WaterMarkPy allows to add watermark in images ###")
    print
    print("To add a watermark in the center of one image, run:")
    print
    print("> python main.py -i nameMain.bmp -w nameWM.png -o name_output")
    print
    print("To add a watermark in the center of multiples images in a folder, run:")
    print
    print("> python main.py -d imgs/ -w nomeWM.png")
    print
    print(
        "To scale (resize) the watermark image and define a relative position in one image, run:"
    )
    print
    print(
        "> python main.py -i imgs/name.bmp -w nameWM.png -s 10 -mt 25 -ml 25 -o nomeSaida"
    )
    print
    print(
        "To scale (resize) the watermark image and define a relative position in multiples image in a folder, run:"
    )
    print
    print("> python main.py -d imgs/ -w nameWM.png -s 30 -mt 25 -ml 25")
    print
    print
    print("\tParameters: ")
    print("\t-i path to image.                          ex: -i img/img.bmp")
    print("\t-w path to watermark image.                ex: -i img/wm.bmp")
    print("\t-d path to folder with images.             ex: -d img/")
    print("\t-s scale/resize (in %) watermark           ex: -s 30")
    print("\t proportional of the main image.")
    print("\t-mt margin TOP in %.                       ex: -mt 20")
    print("\t-ml margem LEFT in %.                      ex: -ml 20")
    print("\t-negative invert colors of the watermark   ex: -negative")
    print("\t considering bg color of the main image")
    print("\t-p Add a prefix in the name of output      ex: -p water")
    print("\t image in a batch operation.")
    print


def main():
    mainImg = None
    outputName = None
    dirImgs = None
    prefix = ""
    watermarkPath = None
    scale = None
    mt = None
    ml = None
    adjust = False
    alpha = 255
    index = 1
    while index < len(sys.argv):
        arg = sys.argv[index]
        if arg == "-i":
            index = index + 1
            mainImg = sys.argv[index]
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
            negative = True
        index = index + 1

    # batch images to center water (-d -w)
    if dirImgs and watermarkPath and not scale:
        images = WMImage.batchWMImageCenter(
            dirImgs, watermarkPath, prefix, alpha, adjust
        )
        for img, path, prefix in images:
            WMImage._saveImg(img, path, prefix)

    # (-d -w -s -mt -ml)
    elif dirImgs and watermarkPath and scale and mt and ml:
        images = WMImage.batchWMImage(
            dirImgs, watermarkPath, mt, ml, prefix, scale, alpha, adjust
        )
        for img, path, prefix in images:
            WMImage._saveImg(img, path, prefix)

    # (-i -w -s -o)
    elif mainImg and watermarkPath and outputName and scale and not mt and not ml:
        with Image.open(mainImg) as main, Image.open(watermarkPath) as wm:
            main = Image.open(mainImg)
            wm_obj = WMImage(main, wm)
            img = wm_obj.createWMCenter(scale, alpha, adjust)
            WMImage._saveImg(img, outputName)

    # (-i -w -o -s -mt -ml)
    elif mainImg and watermarkPath and outputName and scale and mt and ml:
        with Image.open(mainImg) as main, Image.open(watermarkPath) as wm:
            wm_obj = WMImage(main, wm)
            img = wm_obj.createWMCustom(mt, ml, scale, alpha, adjust)
            WMImage._saveImg(img, outputName)
    else:
        help()


if __name__ == "__main__":
    main()
