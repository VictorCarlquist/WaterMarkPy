"""System module."""
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

import glob
import os
import sys

from re import A
from PIL import Image


class WMImage:
    def __init__(self, im_main, im_watermark):
        self.im_main_filename = im_main.filename
        self.im_watermark_filename = im_watermark.filename
        self.im_main = im_main.convert("RGB")
        self.im_watermark = im_watermark.convert("RGBA")

    @staticmethod
    def _centerWatermark(main_img, wm_img, scale=100):
        wm_img = WMImage._resizeRelativeGlobalWatermark(main_img, wm_img, scale)
        wmain, hmain = main_img.size
        wwater, hwater = wm_img.size

        # calculate new watermark's position
        px = wmain / 2 - wwater / 2
        py = hmain / 2 - hwater / 2

        watermark = wm_img.resize((wwater, hwater), Image.Resampling.LANCZOS)
        return {"wm": watermark, "pos": (px, py)}

    @staticmethod
    def _resizeRelativeGlobalWatermark(main_img, wm_img, scale):
        wmain, hmain = main_img.size
        wwater, hwater = wm_img.size

        ratio = min(wmain / float(wwater), hmain / float(hwater)) * float(scale) / 100
        wwater = int(ratio * wwater)
        hwater = int(ratio * hwater)

        watermark = wm_img.resize((wwater, hwater), Image.Resampling.LANCZOS)
        return watermark

    @staticmethod
    def _mergeImgs(main_img, wm_img, position, alpha=255):
        new_img = main_img.copy()
        x, y = position
        wm_img.putalpha(alpha)
        new_img.paste(wm_img, (int(x), int(y)), wm_img)
        return new_img

    @staticmethod
    def _mergeImgsNegativeGray(main_img, wm_img, position, alpha):
        new_img = main_img.copy()
        wm_img = wm_img.copy()
        wmin, hmin = position
        waux, haux = wm_img.size
        wmax = wmin + waux
        hmax = hmin + haux

        mainW, mainH = new_img.size

        avgP = 0
        for y in range(int(hmin), int(hmax)):
            for x in range(int(wmin), int(wmax)):
                if x < mainW and y < mainH:
                    rgb = new_img.getpixel((x, y))
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
                r, g, b, a = wm_img.getpixel((x - wmin, y - hmin))
                r = int(r * ratio)
                g = int(g * ratio)
                b = int(b * ratio)
                wm_img.putpixel((int(x - wmin), int(y - hmin)), (r, g, b, a))

        new_img = WMImage._mergeImgs(main_img, wm_img, position, alpha)
        return new_img

    @staticmethod
    def _marginWatermark(main_img, margin_ratio_top, margin_ratio_left):
        wmain, hmain = main_img.size
        px = int(wmain * float(margin_ratio_left) / 100.0)
        py = int(hmain * float(margin_ratio_top) / 100.0)
        return px, py

    @staticmethod
    def saveImg(img, filename="", prefix=""):
        dirname = os.path.dirname(filename)
        if dirname:
            dirname += "/"
        nname = dirname + prefix + os.path.basename(filename).split(".")[0] + ".jpg"
        img.save(nname, "JPEG")

    @staticmethod
    def batchWMImageCenter(
        path_imgs, path_wm, prefix, scale=100, alpha=255, adjust_color=False
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
            for path in glob.glob(path_imgs + ext):
                with Image.open(path) as main, Image.open(path_wm) as watermark:
                    vm_obj = WMImage(main, watermark)
                    wm_image_centered = WMImage._centerWatermark(
                        vm_obj.im_main, vm_obj.im_watermark, scale
                    )
                    if adjust_color:
                        main = WMImage._mergeImgsNegativeGray(
                            vm_obj.im_main,
                            wm_image_centered["wm"],
                            wm_image_centered["pos"],
                            alpha,
                        )
                    else:
                        main = WMImage._mergeImgs(
                            vm_obj.im_main,
                            wm_image_centered["wm"],
                            wm_image_centered["pos"],
                            alpha,
                        )
                    images.append((main, vm_obj.im_main_filename, prefix))
        return images

    @staticmethod
    def batchWMImage(
        path_imgs,
        path_wm,
        marginTop,
        marginLeft,
        prefix,
        scale=100,
        alpha=255,
        adjust_color=False,
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
            for path in glob.glob(path_imgs + ext):
                with Image.open(path) as main, Image.open(path_wm) as watermark:
                    vm_obj = WMImage(main, watermark)
                    im_wm = WMImage._resizeRelativeGlobalWatermark(
                        vm_obj.im_main, vm_obj.im_watermark, scale
                    )
                    px, py = WMImage._marginWatermark(
                        vm_obj.im_main, marginTop, marginLeft
                    )
                    if adjust_color:
                        main = WMImage._mergeImgsNegativeGray(
                            vm_obj.im_main, im_wm, (px, py), alpha
                        )
                    else:
                        main = WMImage._mergeImgs(
                            vm_obj.im_main, im_wm, (px, py), alpha
                        )
                    images.append((main, path, prefix))
        return images

    def createWMCenter(self, scale=100, alpha=255, adjust_color=False):
        main = self.im_main
        watermark = self.im_watermark
        wm_image_centered = WMImage._centerWatermark(main, watermark, scale)
        if adjust_color:
            main = WMImage._mergeImgsNegativeGray(
                main, wm_image_centered["wm"], wm_image_centered["pos"], alpha
            )
        else:
            main = WMImage._mergeImgs(
                main, wm_image_centered["wm"], wm_image_centered["pos"], alpha
            )
        return main

    def createWMCustom(
        self, marginTop, marginLeft, scale=100, alpha=255, adjust_color=False
    ):
        main = self.im_main
        watermark = self.im_watermark

        im_wm = WMImage._resizeRelativeGlobalWatermark(main, watermark, scale)
        px, py = WMImage._marginWatermark(main, marginTop, marginLeft)
        if adjust_color:
            main = WMImage._mergeImgsNegativeGray(main, im_wm, (px, py), alpha)
        else:
            main = WMImage._mergeImgs(main, im_wm, (px, py), alpha)
        return main


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
