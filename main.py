#The MIT License (MIT)

#Copyright (c) 2016 Victor Carlquist

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

from PIL import Image, ImageDraw
import glob, os, sys

def CenterWatermark(mainImg, wmImg):
    wmain, hmain = mainImg.size
    wwater, hwater = wmImg.size

    ratio = min(wmain/float(wwater), hmain/float(hwater))

    wwater = int(ratio * wwater) 
    hwater = int(ratio * hwater)

    # calculate new watermark's position
    px = wmain / 2 - wwater / 2
    py = hmain / 2 - hwater / 2

    watermark = wmImg.resize((wwater, hwater), Image.ANTIALIAS)
    return {'wm': watermark, 'pos':(px, py)}


def ResizeRelativeGlobalWatermark(mainImg, wmImg, ratioSize):
    wmain, hmain = mainImg.size
    wwater, hwater = wmImg.size

    ratio = min(wmain/float(wwater), hmain/float(hwater)) * float(ratioSize)/100
    wwater = int(ratio * wwater) 
    hwater = int(ratio * hwater)
    
    watermark = wmImg.resize((wwater, hwater), Image.ANTIALIAS)
    return watermark


def MergeImgs(mainImg, wmImg, position):
    newImg = mainImg
    newImg.paste(wmImg, position, wmImg)
    return newImg

def MergeImgsNegativeGray(mainImg, wmImg, position):
    newImg = mainImg
    wmImg = wmImg.convert("RGBA")
    wmin, hmin = position 
    wmax, hmax = position
    waux, haux =  wmImg.size
    wmax = wmax + waux
    hmax = hmax + haux

    wWm, hWm  = wmImg.size

    avgP = 0
    for y in range(hmin, hmax):
        for x in range(wmin, wmax):
            rgb = newImg.getpixel((x, y))
            # Calculate AVG Luminance
            avgP = avgP + rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    
    avgP = avgP / ((hmax - hmin) * (wmax - wmin))
    if avgP > 128:
        ratio = 128/avgP * 0.7
    else:
        ratio = 128/avgP * 1.3

    for y in range(hmin, hmax):
        for x in range(wmin, wmax):
            r, g, b, a = wmImg.getpixel((x - wmin, y - hmin))
            r = int(r * ratio)
            g = int(g * ratio)
            b = int(b * ratio)
            wmImg.putpixel((x - wmin, y - hmin), (r, g, b, a))

    newImg = MergeImgs(mainImg, wmImg, position)
    return newImg

def MarginWatermark(mainImg, marginRatioTop, marginRatioLeft):
    wmain, hmain = mainImg.size
    px = int(wmain * float(marginRatioLeft)/100.0)
    py = int(hmain * float(marginRatioTop)/100.0)
    return px, py

def SaveImg(img, pathImg, prefix):
    nname = prefix + os.path.basename(pathImg).split('.')[0] + ".jpg"
    directory = os.path.dirname(pathImg) + "/"
    if len(directory) == 1:
        img.save(nname, "JPEG")
    else:
        directory = os.path.dirname(pathImg) + "/watermarked/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        img.save(directory + nname, "JPEG")

    print "Saving " + nname


## PUBLIC
def BatchImgCenter(pathImgs, pathWM, prefix, isNegative):
    for ext in ("*.bmp", "*.BMP", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.gif", "*.GIF", "*.png", "*.PNG"):
        for file in glob.glob(pathImgs + ext):
            print(file.split('.')[0])
            main = Image.open(file)
            watermark = Image.open(pathWM)
            
            imgCentered = CenterWatermark(main, watermark)
            if isNegative:
                main = MergeImgsNegativeGray(main, imgCentered['wm'], imgCentered['pos'])
            else:
                main = MergeImgs(main, imgCentered['wm'], imgCentered['pos'])
            SaveImg(main, file, prefix)


def BatchImgCustom(pathImgs, pathWM, ratioSize, marginTop, marginLeft, prefix, isNegative):
    for ext in ("*.bmp", "*.BMP", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.gif", "*.GIF", "*.png", "*.PNG"):
        for file in glob.glob(pathImgs + ext):
            print(file.split('.')[0])
            main = Image.open(file)
            watermark = Image.open(pathWM)
            
            imgCustom = ResizeRelativeGlobalWatermark(main, watermark, ratioSize)
            px, py = MarginWatermark(main, marginTop, marginLeft)
            if isNegative:
                main = MergeImgsNegativeGray(main, imgCustom, (px, py))
            else:
                main = MergeImgs(main, imgCustom, (px, py))

            SaveImg(main, file, prefix)

def ImgCenter(pathImg, pathWM, outputName, isNegative):
    main = Image.open(pathImg)
    watermark = Image.open(pathWM)
    imgCentered = CenterWatermark(main, watermark)
    if isNegative:
        main = MergeImgsNegativeGray(main, imgCentered['wm'], imgCentered['pos'])
    else:
        main = MergeImgs(main, imgCentered['wm'], imgCentered['pos'])
    SaveImg(main, outputName, "")


def ImgCustom(pathImg, pathWM, ratioSize, marginTop, marginLeft, outputName):
    main = Image.open(pathImg)
    watermark = Image.open(pathWM)
    
    imgCustom = ResizeRelativeGlobalWatermark(main, watermark, ratioSize)
    px, py = MarginWatermark(main, marginTop, marginLeft)
    if isNegative:
        main = MergeImgsNegativeGray(main, imgCustom, (px, py))
    else:
        main = MergeImgs(main, imgCustom, (px, py))
    SaveImg(main, outputName, "")


def help():
    print "### WaterMarkPy permite adicionar marcas daguas em imagens ###"
    print
    print "Para adicionar a marca no centro de UMA imagem, execute: "
    print
    print "> python main.py -i nomeImagem.bmp -w nomeWM.png -o nomeSaida"
    print
    print "Para adicionar a marca no centro de diversas imagens em um diretorio, execute: "
    print
    print "> python main.py -d imgs/ -w nomeWM.png"
    print
    print "Para alterar o tamanho da marca (escala (em %)) e definir a margem TOP (em %) e LEFT(em %) do local da marca em UMA imagem, execute: "
    print
    print "> python main.py -i imgs/nomeImagem.bmp -w nomeWM.png -s 10 -mt 25 -ml 25 -o nomeSaida"
    print
    print "Para alterar o tamanho da marca (escala (%)) e definir a margem TOP (%) e LEFT (%) do local da marca em varias imagens em um diretorio, execute: "
    print
    print "> python main.py -d imgs/ -w nomeWM.png -s 30 -mt 25 -ml 25"
    print
    print
    print "\tParametros: "
    print "\t-i Nome da imagem principal.               ex: -i imagem/img.bmp"
    print "\t-w Nome da imagem da watermark.            ex: -i imagem/wm.bmp"
    print "\t-d Diretorio com imagens sem a marca.      ex: -d imagem/"
    print "\t-s scale (em %) da marca em relacao ao     ex: -s 30"
    print "\t tamanho da imagem principal."
    print "\t-mt Margem TOP em %.                       ex: -mt 20"
    print "\t-ml Margem LEFT em %.                      ex: -ml 20"
    print "\t-negative Realca a marca dagua,            ex: -negative"
    print "\t escurecendo a imagem em fundo claro e"
    print "\t clareando em fundo escuro."
    print "\t-p Adicionar um prefixo no nome da imagem. ex: -p water"
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
    negative = False

    index = 1
    while index < len(sys.argv):
        arg = sys.argv[index]
        if arg == '-i':
            index = index + 1
            mainImg = sys.argv[index]
        elif arg == '-o':        
            index = index + 1
            outputName = sys.argv[index]
        elif arg == '-d':
            index = index + 1
            dirImgs = sys.argv[index]
        elif arg == '-p':
            index = index + 1
            prefix = sys.argv[index]
        elif arg == '-w':
            index = index + 1
            watermarkPath = sys.argv[index]
        elif arg == '-s':
            index = index + 1
            scale = sys.argv[index]
        elif arg == '-mt':
            index = index + 1
            mt = sys.argv[index]
        elif arg == '-ml':
            index = index + 1
            ml = sys.argv[index]
        elif arg == '-negative':
            negative = True 
        index = index + 1

    # batch images to center water (-d -w)
    if dirImgs and watermarkPath and not scale:
        BatchImgCenter(dirImgs, watermarkPath, prefix, negative)
    
    # (-d -w -s -mt -ml)
    elif dirImgs and watermarkPath and scale and mt and ml:
        BatchImgCustom(dirImgs, watermarkPath, scale, mt, ml, prefix, negative)
    
    # (-i -w -o)
    elif mainImg and watermarkPath and outputName and not scale:
        ImgCenter(mainImg, watermarkPath, outputName, negative)

    # (-i -w -o -s -mt -ml)
    elif mainImg and watermarkPath and outputName and scale and mt and ml:
        ImgCustom(mainImg, watermarkPath, scale, mt, ml, outputName, negative)
    else:
        help()

if __name__ == '__main__':
    main()
