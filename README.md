# WaterMarkPy
Add watermark in multiple images at once.

##WaterMarkPy permite adicionar marcas d'águas em imagens

To add a watermark in the center of one image, run:
> python main.py -i nomeImagem.bmp -w nomeWM.png -o nomeSaida

* -i: path to image
* -w: path to watermark image
* -o: name of the output image

To add a watermark in the center of multiples images in a folder, run:
> python main.py -d imgs/ -w nomeWM.png

* -d: path to folder
* -w: path to watermark image

To scale (resize) the watermark image and define a relative position in one image, run:

> python main.py -i imgs/nomeImagem.bmp -w nomeWM.png -s 10 -mt 25 -ml 25 -o nomeSaida

* -i: path to image
* -w: path to watermark image
* -s: % scale size to watermark image
* -mt: position in % from TOP margin
* -ml: position in % from LEFT margin
* -o: name of the output image

To scale (resize) the watermark image and define a relative position in multiples image in a folder, run:

> python main.py -d imgs/ -w nomeWM.png -s 30 -mt 25 -ml 25

* -d: path to folder
* -w: path to watermark image
* -s: % scale size to watermark image
* -mt: position in % from TOP margin
* -ml: position in % from LEFT margin


Parameters:

> -i path to image
>> ex: -i imagem/img.bmp

> -w path to watermark image
>> ex: -i imagem/wm.bmp

> -d path to folder with image
>> ex: -d imagem/

> -s scale/resize (in %) watermark considering the dimensions of the main image
>> ex: -s 30

> -mt Margin TOP in %.
>> ex: -mt 20

> -ml Margin LEFT in %.
>> ex: -ml 20

> -p Add a prefix in the name of output image in a batch operation.
>> ex: -p water
