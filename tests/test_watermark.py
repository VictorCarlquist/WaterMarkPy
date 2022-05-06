import sys

from watermarkpy.watermark import WMImage
from watermarkpy.watermark import main

from PIL import Image
import pytest


@pytest.mark.parametrize(
    ("p_main", "p_wm"),
    [
        ("img/ship.jpg", "img/shipwm.jpg"),
    ],
)
def test_one_image_center(p_main, p_wm):
    with Image.open(p_main) as main, Image.open(p_wm) as wm:
        wm_obj = WMImage(main, wm)
        img = wm_obj.createWMCenter()


@pytest.mark.parametrize(
    ("p_main", "p_wm", "scale", "alpha", "adjust"),
    [
        ("img/ship.jpg", "img/shipwm.jpg", 10, 160, True),
        ("img/ship.jpg", "img/shipwm.jpg", 10, 160, False),
    ],
)
def test_one_image_center_param(p_main, p_wm, scale, alpha, adjust):
    with Image.open(p_main) as main, Image.open(p_wm) as wm:
        wm_obj = WMImage(main, wm)
        img = wm_obj.createWMCenter(scale, alpha, adjust)


@pytest.mark.parametrize(
    ("p_main", "p_wm", "mt", "ml", "scale", "alpha", "adjust"),
    [
        ("img/ship.jpg", "img/shipwm.jpg", 20, 30, 10, 160, True),
        ("img/ship.jpg", "img/shipwm.jpg", 20, 30, 10, 160, False),
        ("img/ship.jpg", "img/shipwm.jpg", 20, 100, 10, 160, False),
        ("img/ship.jpg", "img/shipwm.jpg", 20, 100, 10, 160, True),
    ],
)
def test_one_image_custom(p_main, p_wm, mt, ml, scale, alpha, adjust):
    with Image.open(p_main) as main, Image.open(p_wm) as wm:
        wm_obj = WMImage(main, wm)
        img = wm_obj.createWMCustom(mt, ml, scale, alpha, adjust)


@pytest.mark.parametrize(
    ("dir_path", "p_wm", "prefix", "scale", "alpha", "adjust"),
    [
        ("img/", "img/shipwm.jpg", "", 10, 160, True),
        ("img/", "img/shipwm.jpg", "a", 10, 160, False),
        ("img/", "img/shipwm.jpg", "", 10, 160, False),
        ("img/", "img/shipwm.jpg", "a", 10, 160, True),
    ],
)
def test_batch_center(dir_path, p_wm, prefix, scale, alpha, adjust):
    images = WMImage.batchWMImageCenter(dir_path, p_wm, prefix, scale, alpha, adjust)
    assert len(images) > 0


@pytest.mark.parametrize(
    ("dir_path", "p_wm", "mt", "ml", "prefix", "scale", "alpha", "adjust"),
    [
        ("img/", "img/shipwm.jpg", 10, 10, "", 10, 160, True),
        ("img/", "img/shipwm.jpg", 10, 10, "a", 10, 160, False),
        ("img/", "img/shipwm.jpg", 100, 10, "", 10, 160, False),
        ("img/", "img/shipwm.jpg", 10, 100, "a", 10, 160, True),
    ],
)
def test_batch(dir_path, p_wm, mt, ml, prefix, scale, alpha, adjust):
    images = WMImage.batchWMImage(dir_path, p_wm, mt, ml, prefix, scale, alpha, adjust)
    assert len(images) > 0


@pytest.mark.parametrize(
    ("param"),
    [
        (
            (
                "command",
                "-i",
                "img/ship.jpg",
                "-w",
                "img/shipwm.jpg",
                "-mt",
                10,
                "-ml",
                10,
                "-s",
                10,
                "-a",
                100,
                "-adjust",
                "-o",
                "new",
            )
        ),
        (
            (
                "command",
                "-i",
                "img/ship.jpg",
                "-w",
                "img/shipwm.jpg",
                "-s",
                10,
                "-a",
                100,
                "-adjust",
                "-o",
                "new",
            )
        ),
        (("command", "-i", "img/ship.jpg", "-w", "img/shipwm.jpg", "-h")),
    ],
)
def test_run_module(param):
    sys.argv = param
    main()
