import os, sys
from PIL import Image
import numpy as np
 
def load_image(infilename):
    img = Image.open(infilename)
    print('format:', img.format, "%dx%d" % img.size, img.mode)
    return img
 
def save_image(data, outfilename):
    data.save(outfilename)
    print(outfilename + ' file saved')
 
def show_image(imagefilename):
    img = Image.open(imagefilename)
    img.show()
 
def roberts_cross(infilename):
    image = load_image(infilename)
    image = image.convert('L')
    image.save('GS'+infilename)
    print('converted '+ infilename +' to greyscale')
    imagesize = image.size
    print(imagesize)
    r = np.zeros((imagesize[0], imagesize[1]))
    s = np.zeros((imagesize[0], imagesize[1]))
    #wprowadzanie aktualnej wartosci piksela do tablicy'''
    for x in range (imagesize[0]):
        for y in range (imagesize[1]):
            r[x, y] = image.getpixel((x, y))
    #krzyz bertsa
    tmp_x = np.zeros((imagesize[0], imagesize[1]))
    tmp_y = np.zeros((imagesize[0], imagesize[1]))
 
    g = np.zeros((imagesize[0], imagesize[1]), dtype = np.float)
    for x in range(imagesize[0]-1):
        for y in range(imagesize[1]-1):
            tmp_x[x, y] = r[x, y] - r[x+1, y+1]
            tmp_y[x, y] = r[x+1, y] - r[x, y+1]
    g = np.sqrt(np.power(tmp_x, 2)+np.power(tmp_y, 2))
 
    #threshold
    for i in range(imagesize[0]-1):
        for j in range(imagesize[1]-1):
            if (g[i,j]<11):
                s[i,j] = 0
            else:
                s[i,j] = 255
 
 
    for i in range (imagesize[0]):
        for j in range (imagesize[1]):
            image.putpixel((i, j), s[i, j])
    save_image(image, 'RC'+infilename)
    show_image('RC'+infilename)
 
 
roberts_cross('image.jpg')