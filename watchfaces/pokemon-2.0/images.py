from PIL import Image
import os.path
import math

ROOT_DIR = f"{os.path.dirname(__file__)}/pokemon-src/main-sprites/yellow"
FRONT_DIR = f"{ROOT_DIR}/gray"
BACK_DIR = f"{ROOT_DIR}/back/gray"

COUNT = 151

OUT_DIR = f"{os.path.dirname(__file__)}/pokemon-out"

D_DATA = [
    [
        [0]
    ],
    [
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ],
    [
        [1, 0],
        [0, 0]
    ],
    [
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 1]
    ],
    [
        [1, 0],
        [0, 1]
    ]
]

D_LEVELS = len(D_DATA) * 2 - 1

def make_dithering(i: int) -> Image.Image:
    im = Image.new("L", (68, 68), 'white')
    if i < len(D_DATA):
        d = D_DATA[i]
    else:
        d = D_DATA[D_LEVELS - i - 1]
    w = len(d[0])
    h = len(d)
    for x in range(68):
        for y in range(68):
            v = d[y % h][x % w]
            if i < len(D_DATA):
                im.putpixel((x, y), 256 if v else 0)
            else:
                im.putpixel((x, y), 0 if v else 256)
    return im

D_IM = [make_dithering(i) for i in range(D_LEVELS)]

def make_extent() -> Image.Image:
    im = Image.new("L", (12, 68), color=0)
    for x in range(12):
        for y in range(68):
            im.putpixel((x, y), 256)
    return im

EXTENT = make_extent()

def make_mask(im: Image.Image, i: int) -> Image.Image:
    return im.point(lambda p: 1 if p >= math.floor(i * 256 / D_LEVELS) and p < math.ceil((i + 1) * 256 / D_LEVELS) else 0, mode="1")

def convert(im: Image.Image) -> Image.Image:
    im = im.resize((68, 68))
    im0, im = im, Image.new(im.mode, (80, 68), color=1)
    for i in range(D_LEVELS):
        im.paste(D_IM[i], (0, 0), mask=make_mask(im0, i))
    im.paste(EXTENT, (68, 0))
    im = im.convert(mode="P")
    return im

def convert_front(im: Image.Image) -> Image.Image:
    w0, h0 = im_src.size
    im = Image.new(im_src.mode, (56, 56), 'white')
    im.paste(im_src, ((56 - w0) // 2, (56 - h0) // 2))
    return convert(im)

def convert_back(im_src: Image.Image) -> Image.Image:
    im = Image.new(im_src.mode, (28, 28), 'white')
    im.paste(im_src, (0, 0))
    return convert(im)

if __name__ == '__main__':
    for i in range(1, COUNT + 1):
        with Image.open(f"{FRONT_DIR}/{i}.png") as im_src:
            im_out = convert_front(im_src)
            im_out.save(f"{OUT_DIR}/front_{i}.bmp")
        
        with Image.open(f"{BACK_DIR}/{i}.png") as im_src:
            im_out = convert_back(im_src)
            im_out.save(f"{OUT_DIR}/back_{i}.bmp")