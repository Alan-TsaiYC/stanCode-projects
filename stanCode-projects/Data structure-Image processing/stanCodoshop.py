"""
File: stanCodoshop.py
----------------------------------------------
SC101_Assignment3
Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.

-----------------------------------------------
Name: Alan Tsai

TODO: Remove unexpected people(or something other) from photo by inputting multiple(3 or more) photos
"""

import os
import sys
from simpleimage import SimpleImage

import math
import time


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): color distance between red, green, and blue pixel values

    """
    dist = math.sqrt((red-pixel.red)**2+(green-pixel.green)**2+(blue-pixel.blue)**2)
    return dist


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    red, green, blue = 0, 0, 0      # to count r,g,b sum
    for pixel in pixels:
        red += pixel.red
        green += pixel.green
        blue += pixel.blue
    return [int(red/len(pixels)), int(green/len(pixels)), int(blue/len(pixels))]    # return r,g,b average


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """
    avg = get_average(pixels)
    dic = {}
    for pixel in pixels:
        dic[get_pixel_dist(pixel, avg[0], avg[1], avg[2])] = pixel  # dic of pixel dist, key:dist value:pixel
    dist = sorted(dic)                                              # get sorted key
    return dic[dist[0]]                                             # return pixel (key:lowest dist)


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)

    start_time = time.time()                                    # count time

    for y in range(height):                                     # loop in (x, y)
        for x in range(width):
            pixels = []                                         # build pixels list, to sent to best pixel function
            for img in images:
                pixels.append(img.get_pixel(x, y))
            best_pixel = get_best_pixel(pixels)
            result.get_pixel(x, y).red = best_pixel.red         # replace pixel to best pixel
            result.get_pixel(x, y).green = best_pixel.green
            result.get_pixel(x, y).blue = best_pixel.blue
    print(f'Used time:{round(time.time()-start_time, 2)}s')
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
