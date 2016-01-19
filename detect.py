import os, sys
from PIL import Image
import numpy as np
from scipy import ndimage

roberts_cross_x = np.array([[1, 0],
                            [0, -1]])

roberts_cross_y = np.array([[0, 1],
                            [-1, 0]])

sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

sobel_y = np.array([[-1, -2, -1],
                    [0, 0, 0],
                    [1, 2, 1]])

prewitt_x = np.array([[-1, 0, 1],
                      [-1, 0, 1],
                      [-1, 0, 1]])

prewitt_y = np.array([[-1, -1, -1],
                      [0, 0, 0],
                      [1, 1, 1]])

scharr_x = np.array([[3, 0, -3],
                    [10, 0, -10],
                    [3, 0, -3]])

scharr_y = np.array([[3, 10, 3],
                    [0, 0, 0],
                    [-3, -10, -3]])


def load_image(infilename):
    img = Image.open(infilename)
    print('format:', img.format, "%dx%d" % img.size, img.mode)
    img.load()
    img = img.convert('L');
    return np.asarray(img, dtype="int32")


def save_image(data, outfilename):
    img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "L")
    print(outfilename + ' file saved')
    img.save(outfilename)


def show_image(imagefilename):
    img = Image.open(imagefilename)
    img.show()


def roberts_cross(infilename, outfilename):
    image = load_image(infilename)
    vertical = ndimage.convolve(image, roberts_cross_x)
    horizontal = ndimage.convolve(image, roberts_cross_y)
    output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
    save_image(output_image, outfilename)


def sobel(infilename, outfilename):
    image = load_image(infilename)
    vertical = ndimage.convolve(image, sobel_x)
    horizontal = ndimage.convolve(image, sobel_y)
    output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
    save_image(output_image, outfilename)


def prewitt(infilename, outfilename):
    image = load_image(infilename)
    vertical = ndimage.convolve(image, prewitt_x)
    horizontal = ndimage.convolve(image, prewitt_y)
    output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
    save_image(output_image, outfilename)


def scharr(infilename, outfilename):
    image = load_image(infilename)
    vertical = ndimage.convolve(image, prewitt_x)
    horizontal = ndimage.convolve(image, prewitt_y)
    output_image = np.sqrt(np.square(horizontal) + np.square(vertical))
    save_image(output_image, outfilename)


# infilename = sys.argv[1]
# outfilename = sys.argv[2]

roberts_cross('image.jpg', 'RCimage.jpg')
sobel('image.jpg', 'SOBELimage.jpg')
prewitt('image.jpg', 'PREWITTimage.jpg')
scharr('image.jpg', 'SCHARRimage.jpg')
