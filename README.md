![example workflow](https://github.com/VictorCarlquist/WaterMarkPy/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/VictorCarlquist/WaterMarkPy/branch/master/graph/badge.svg?token=3H4HQ9CEHN)](https://codecov.io/gh/VictorCarlquist/WaterMarkPy)


# WaterMarkPy

---

WaterMarkPy is a simple free open-source library to add watermark in images. The WaterMarkPy keeps the watermark with the same locate and with the same size in the image despite of the image resolution, because the WaterMarkPy uses percent (\%) unit to position the watermark.

You can find the source code at: [https://github.com/VictorCarlquist/WaterMarkPy/](https://github.com/VictorCarlquist/WaterMarkPy/),

Install
---

```
pip install watermarkpy-image
```

---
To add a watermark in the center of one image, run:

```python
from watermarkpy.watermark import WMImage

main_image = "img/ship.jpg"
watermark = "img/shipwm.jpg"

with Image.open(main_image) as main, Image.open(watermark) as wm:
    wm = WMImage(main, wm)
    img = wm.createWMCenter()
    img.save("new.jpg", "JPEG")
```

---

To add a watermark in the center of one image with a different scale and alpha, run:

```python
from watermarkpy.watermark import WMImage

main_image = "img/ship.jpg"
watermark = "img/shipwm.jpg"

with Image.open(main_image) as main, Image.open(watermark) as wm:
    wm = WMImage(main, wm)
    img = wm.createWMCenter(scale=25, alpha=120)
    img.save("new.jpg", "JPEG")
```
Parameters:
```
scale = [0% - 100%]
alpha = [0 - 255]
```

To add a watermark in a diffente position, run:

```python
from watermarkpy.watermark import WMImage

main_image = "img/ship.jpg"
watermark = "img/shipwm.jpg"

with Image.open(main_image) as main, Image.open(watermark) as wm:
    wm = WMImage(main, wm)
    img = wm.createWMCustom(marginTop=70 marginLeft=60, scale=25, alpha=120)
    img.save("new.jpg", "JPEG")
```
Parameters:
```
marginTop = [0% - 100%]
marginLeft = [0% - 100%]
scale = [0% - 100%]
alpha = [0 - 255]
```

To add a watermark and improve the brightness based in the brightness of the background region, run:
```python
from watermarkpy.watermark import WMImage

main_image = "img/ship.jpg"
watermark = "img/shipwm.jpg"

with Image.open(main_image) as main, Image.open(watermark) as wm:
    wm = WMImage(main, wm)
    img = wm.createWMCustom(marginTop=70 marginLeft=60, adjust_color=True)
    img.save("new.jpg", "JPEG")
```

Parameters:
```
marginTop = [0% - 100%]
marginLeft = [0% - 100%]
adjust_color = [True, False]
```
---

To add a watermark in the center of one image, run:

> watermarkpy-image -i name.bmp -w nameWM.png -o name_output
```
* -i: path to image
* -w: path to watermark image
* -o: name of the output image
```

To add a watermark in the center of multiples images in a folder, run:

> watermarkpy-image -d imgs/ -w nameWM.png
```
* -d: path to folder
* -w: path to watermark image
```

To scale (resize) the watermark image and define a relative position in one image, run:

> watermarkpy-image -i imgs/name.bmp -w nomeWM.png -s 10 -mt 25 -ml 25 -o name_output
```
* -i: path to image
* -w: path to watermark image
* -s: % scale size to watermark image
* -mt: position in % from TOP margin
* -ml: position in % from LEFT margin
* -o: name of the output image
```

To scale (resize) the watermark image and define a relative position in multiples image in a folder, run:

> watermarkpy-image -d imgs/ -w nomeWM.png -s 30 -mt 25 -ml 25
```
* -d: path to folder
* -w: path to watermark image
* -s: % scale size to watermark image
* -mt: position in % from TOP margin
* -ml: position in % from LEFT margin
```

Parameters:
```
> -i path to image
>> ex: -i img/img.bmp

> -w path to watermark image
>> ex: -i img/wm.bmp

> -d path to folder with image
>> ex: -d img/

> -s scale/resize (in %) watermark considering the dimensions of the main image
>> ex: -s 30

> -mt Margin TOP in %.
>> ex: -mt 20

> -ml Margin LEFT in %.
>> ex: -ml 20

> -negative invert colors of the watermark considering bg color of the main image
>> ex: -negative

> -p Add a prefix in the name of output image in a batch operation.
>> ex: -p water
```
