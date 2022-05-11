# GS = gray scale morphology
from PIL import Image
import numpy as np

def Dilation(image, kernel, kernelCenter) -> Image:
    '''
    :param image: Image (from PIL)
    :param kernel: np.array (from numpy)
    :param kernelCenter: tuple(r, c) r = row, c = column
    '''
    width, height = image.size
    dilationImage = Image.new('L', image.size)
    # compare image with kernel
    for y in range(height): 
        for x in range(width):
            # dilate for white elements
            if image.getpixel((x, y)) == 255:
                for r in range(kernel.shape[0]):
                    for c in range(kernel.shape[1]):
                        if 0 <= y+r-kernelCenter[0] < width and 0 <= x+c-kernelCenter[1] < height and kernel[r, c] == 1:
                            dilationImage.putpixel(
                                (x+c-kernelCenter[1], y+r-kernelCenter[0]), 255)
    return dilationImage


def Erosion(image, kernel, kernelCenter) -> Image:
    '''
    :param image: Image (from PIL)
    :param kernel: np.array (from numpy)
    :param kernelCenter: tuple(r, c) r = row, c = column
    '''
    width, height = image.size
    erosionImage = Image.new('1', image.size)
    # compare image with kernel
    for y in range(height):
        for x in range(width):
            # erosion for white elements
            # if all match => put 1, not match => 0
            isMatch = True
            for r in range(kernel.shape[0]):
                for c in range(kernel.shape[1]):
                    # out of range case
                    if kernel[r, c] == 1:
                        if 0 <= x+c - kernelCenter[1] < width and 0 <= y+r - kernelCenter[0] < height:
                            if image.getpixel((x+c - kernelCenter[1], y+r - kernelCenter[0])) == 0:
                                isMatch = False
                                break
                        else:
                            isMatch = False
                            break
                if not isMatch:
                    break
            if isMatch:
                erosionImage.putpixel((x, y), 255)
    return erosionImage


def Opening(image, kernel, kernelCenter):
    return Dilation(Erosion(image, kernel, kernelCenter), kernel, kernelCenter)


def Closing(image, kernel, kernelCenter):
    return Erosion(Dilation(image, kernel, kernelCenter), kernel, kernelCenter)


def Complement(image):
    '''
    image: Image (from PIL)
    '''
    width, height = image.size
    complementImage = Image.new('L', image.size)
    for i in range(width):
        for j in range(height):
            if image.getpixel((i, j)) == 255:
                complementImage.putpixel((i, j), 0)
            else:
                complementImage.putpixel((i, j), 255)
    return complementImage


def Intersection(imageA, imageB):
    '''
    imageA: Image (from PIL)
    imageB: Image (from PIL)
    these two image must be the same size
    '''
    intersectionImage = Image.new('L', imageA.size)
    width, height = imageA.size
    for i in range(width):
        for j in range(height):
            if imageA.getpixel((i, j)) == 255 and imageB.getpixel((i, j)) == 255:
                intersectionImage.putpixel((i, j), 255)
            else:
                intersectionImage.putpixel((i, j), 0)
    return intersectionImage


def Hit_and_miss_transform(image, kernelJ, cneterJ, kernelK, centerK):
    return Intersection(Erosion(image, kernelJ, centerJ), Erosion(Complement(image), kernelK, centerK))


def gs_Dilation(image, kernel, kernelCenter):
    '''
    gs = gray scale
    image: Image (from PIL)
    kernel: np.array
    kernelCenter: 2D tuple
    '''
    width, height = image.size
    gs_DilationImage = Image.new('L', image.size)
    for c in range(width):
        for r in range(height):
            newPixel = image.getpixel((c, r))
            for x in range(-kernelCenter[0], kernelCenter[0] + 1):
                for y in range(-kernelCenter[0], kernelCenter[0] + 1):
                    if (0 <= c+x < width and 0 <= r+y < height and kernel[kernelCenter[0]+x, kernelCenter[1]+y] == 1):
                        newPixel = max(newPixel, image.getpixel((c+x, r+y)))
            gs_DilationImage.putpixel((c, r), newPixel)

    return gs_DilationImage


def gs_Erosion(image, kernel, kernelCenter):
    '''
    gs = gray scale
    image: Image (from PIL)
    kernel: np.array
    kernelCenter: 2D tuple
    '''
    width, height = image.size
    gs_ErosionImage = Image.new('L', image.size)
    for c in range(width):
        for r in range(height):
            newPixel = image.getpixel((c, r))
            for x in range(-kernelCenter[0], kernelCenter[0] + 1):
                for y in range(-kernelCenter[0], kernelCenter[0] + 1):
                    if (0 <= c+x < width and 0 <= r+y < height and kernel[kernelCenter[0]+x, kernelCenter[1]+y] == 1):
                        newPixel = min(newPixel, image.getpixel((c+x, r+y)))
            gs_ErosionImage.putpixel((c, r), newPixel)

    return gs_ErosionImage


def gs_Opening(image, kernel, kernelCenter):
    return gs_Dilation(gs_Erosion(image, kernel, kernelCenter), kernel, kernelCenter)


def gs_Closing(image, kernel, kernelCenter):
    return gs_Erosion(gs_Dilation(image, kernel, kernelCenter), kernel, kernelCenter)


if __name__ == "__main__":
    

    # define kernel 3-5-5-5-3
    kernel = np.array([
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0]])
    kernelCenter = (2, 2)

    # define kernel J
    kernelJ = np.array([
        [1, 1],
        [0, 1]])
    centerJ = (1, 0)

    # defien kernel K
    kernelK = np.array([
        [1, 1],
        [0, 1]])
    centerK = (0, 1)
    # load image
    originalImage = Image.open("lena.bmp")

    # Q1
    gs_dilationImage = gs_Dilation(originalImage, kernel, (2,2))
    gs_dilationImage.show()
    #gs_dilationImage.save("gs_dilationImage.bmp")

    # Q2
    gs_erosionImage = gs_Erosion(originalImage, kernel, (2, 2))
    gs_erosionImage.show()
    #gs_erosionImage.save("gs_erosionImage.bmp")

    # Q3
    # gs_openingImage = gs_Opening(originalImage, kernel, (2, 2))
    # gs_openingImage.show()
    #gs_openingImage.save("gs_openingImage.bmp")

    # Q4
    # gs_closingImage = gs_Closing(originalImage, kernel, (2, 2))
    # gs_closingImage.show()
    #gs_closingImage.save("gs_closingImage.bmp")