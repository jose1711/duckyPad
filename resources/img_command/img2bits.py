#!/usr/bin/env python
'''
Convert image file to a monochromatic 1-bit per pixel file for use
with DuckyPad (v3). Note that input image dimensions may not exceed
the resolution of OLED display (128x64).

Usage:

    img2bits.py [-d] [-h] [-o OUTPUT_FILE] image

positional arguments:
  image           Image file to convert

options:
  -h, --help      show this help message and exit
  -o OUTPUT_FILE  Output file (defaults to input file without extension)
  -d              Debug mode

Example:

    img2bits.py -o some_image some_image.png

'''

from math import ceil
from PIL import Image
import argparse
import logging
import os
import sys


def image_to_bits(image_file, output_file):
    image = Image.open(image_file).convert('RGB')

    width, height = image.size
    if display_width < width or display_height < height:
        raise Exception(f'Image dimensions exceed size of OLED display ({width}x{height} vs {display_width}x{display_height}')

    with open(output_file, 'wb') as f:
        logging.debug(f'{f} was opened')
        # the first byte is image width
        logging.debug(f'Detected image width: {image.width}')
        f.write(bytes([ceil(image.width/8)*8]))
        for y in range(height):
            for x in range(0, width, 8):
                byte = 0
                for i in range(8):
                    try:
                        curr_pixel = image.getpixel((x+i, y))
                        logging.debug(f'Current pixel: {curr_pixel}')
                        pixel_value = sum(curr_pixel) != 0
                    except IndexError:
                        pixel_value = 0
                    logging.debug(f'Interpreting as {"white" if pixel_value else "black"}')
                    byte |= (pixel_value << (7 - i))
                f.write(bytes([byte]))


display_width = 128
display_height = 64

parser = argparse.ArgumentParser(description='Convert image for duckyPad')
parser.add_argument('-o', nargs=1, metavar='OUTPUT_FILE', dest='outfile',
                    help='Output file (defaults to input file without extension)')
parser.add_argument('-d', action='store_true', help='Debug mode')
parser.add_argument('image',
                    help='Image file to convert')
args = parser.parse_args()

if args.d:
    logging.basicConfig(level=logging.DEBUG)

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
