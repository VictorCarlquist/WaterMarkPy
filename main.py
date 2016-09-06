# Author: Victor Carlquist
# Year: 2016

from PIL import Image, ImageDraw
import glob, os

pathImgs = raw_input("Digite o caminho da pasta com as imagens para adicionar a marca dagua (ex:imgs/): ")
pathWM = raw_input("Digite o caminho e o nome da imagem da marca dagua (marca.png): ")

for ext in ("*.bmp", "*.BMP", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.gif", "*.GIF", "*.png", "*.PNG"):
    for file in glob.glob(pathImgs + ext):
        print(file.split('.')[0])
        main = Image.open(file)
        watermark = Image.open(pathWM)

        wmain, hmain = main.size
        wwater, hwater = watermark.size

        ratio = min(wmain/float(wwater), hmain/float(hwater))

        wwater = int(ratio * wwater) 
        hwater = int(ratio * hwater)

        px = wmain / 2 - wwater / 2
        py = hmain / 2 - hwater / 2

        watermark = watermark.resize((wwater, hwater), Image.ANTIALIAS)
        main.paste(watermark, (px,py), watermark)
        main.save(os.path.dirname(file) + "/w" + os.path.basename(file).split('.')[0] + ".jpg", "JPEG")
