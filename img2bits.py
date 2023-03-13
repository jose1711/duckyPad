#!/usr/bin/env python
'''
convert image file to a monochromatic 1-bit per pixel file for use
with DuckyPad (v3).
'''
from PIL import Image
from math import ceil
import argparse
import os
import sys


def image_to_bits(image_file, output_file):
    image = Image.open(image_file)

    width, height = image.size
    if display_width < width or display_height < height:
        raise Exception(f'Image dimensions exceed size of OLED display ({width}x{height} vs {display_width}x{display_height}')

    with open(output_file, 'wb') as f:
        # the first byte is image width
        f.write(bytes([ceil(image.width/8)*8]))
        for y in range(height):
            for x in range(0, width, 8):
                byte = 0
                for i in range(8):
                    try:
                        if isinstance(image.getpixel((x+i, y)), tuple):
                            pixel_value = sum(image.getpixel((x+i, y))) != 0
                        else:
                            pixel_value = image.getpixel((x+i, y)) != 0
                    except IndexError:
                        pixel_value = 0

                    byte |= (pixel_value << (7 - i))
                f.write(bytes([byte]))


display_width = 128
display_height = 64

parser = argparse.ArgumentParser(description='Convert image for duckyPad')
parser.add_argument('-o', nargs=1, metavar='OUTPUT_FILE', dest='outfile',
                    help='Output file (defaults to input file without extension)')
parser.add_argument('image',
                    help='Image file to convert')
args = parser.parse_args()

if not os.path.splitext(args.image)[1]:
    raise ValueError('input file must have an extension!')

if not args.outfile:
    outfile = os.path.splitext(args.image)[0]
else:
    outfile = args.outfile[0]

if os.path.exists(outfile):
    print(f'Output file {outfile} already exists!')
    sys.exit(1)

image_to_bits(args.image, outfile)
