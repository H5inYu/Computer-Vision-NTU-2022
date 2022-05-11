# 2020, 1st semester computer
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def up_side_down(image):
    imageNpArray = np.array(image)[::-1]
    return Image.fromarray(imageNpArray)


def flip_right_left(image):
    imageNpArray = np.array(image)
    for i in range(width):
        imageNpArray[i] = imageNpArray[i][::-1]
    return Image.fromarray(imageNpArray)


def flip_diagonally(image):
    imageNpArray = np.array(image)
    for i in range(width):
        for j in range(i, height):
            imageNpArray[i][j], imageNpArray[j][i] = imageNpArray[j][i], imageNpArray[i][j]
    return Image.fromarray(imageNpArray)


def binary_with_threshold(image, threshold):
    binary_image = Image.new("L", image.size)
    binary_image_array = binary_image.load()
    for c in range(width):
        for r in range(height):
            if image.getpixel((c,r)) >= threshold:
                binary_image_array[c,r] = 255
            else:
                binary_image_array[c,r] = 0
    binary_image.save("Binary Image.bmp")
    binary_image.show()


def histogram(image, axis_range):
    x_axis = np.arange(axis_range)
    y_axis = np.zeros(axis_range)
    for c in range(width):
        for r in range(height):
            y_axis[image.getpixel((c,r))] += 1
    plt.bar(x_axis, y_axis)
    plt.show()


def histogram_equalization(image, axis_range):
    x_axis = np.arange(axis_range)
    totalNumberOfPixels = width * height
    s = np.zeros(256)
    ImageHis = np.zeros(256)

    # get original image histogram count
    for c in range(width):
        for r in range(height):
            ImageHis[image.getpixel((c,r))] += 1

    # calculate the equalization histogram
    for i in range(256):
        s[i] = np.sum(ImageHis[0:i+1]) * 255 / totalNumberOfPixels

    # make new equalizedImage 
    equalizedImage = Image.new("L", image.size)
    for c in range(width):
        for r in range(height):
            equalizedImage.putpixel((c,r), int(s[image.getpixel((c,r))]))
    equalizedImage.save("EqualizeedImage.bmp")
    equalizedImage.show()    

    # make the histogram of equalization image
    equalizedHis = np.zeros(256)
    for c in range(width):
        for r in range(height):
            equalizedHis[equalizedImage.getpixel((c,r))] += 1

    plt.bar(x_axis, equalizedHis)
    plt.show()

def compare(image, kernel):
    isMatch = flase
    for c in range(image.size[0]):
        for r in range(image.size[1]):


    if(isMatch):
        return True
    else:
        return False
def Dilation(image, kernel, center = [0,0]):
    imageArray = np.array(image)
    newImage = Image.new("L", image.size)
    newImageArray = newImage.load()
    # comapre image and kernel
    for c in range(width):
        for r in range(height):
            pass
            # compare and set
    newImage.show()
    return newImage
    pass
def Erosion():
    pass
def Opening():
    pass
def Closing():
    pass
def Hit_and_miss_transform():
    pass


if __name__ == "__main__":
    path = "DividedImage.bmp"
    with Image.open(path) as image:
        width, height = image.size
        histogram_equalization(image,256)
