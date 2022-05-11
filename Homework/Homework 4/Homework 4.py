# morphology

def Dilation(image, kernel, kernelCenter):
    '''
    image: Image (from PIL)
    kernel: np.array (from numpy)
    kernelCenter: tuple(x, y)
    '''
    width, height = image.size
    dilationImage = Image.new('L', image.size)
    # compare image with kernel
    for c in range(width):
        for r in range(height):
            # dilate for white elements
            if image.getpixel((c,r)) == 255:
                for i in range(kernel.shape[0]):
                    for j in range(kernel.shape[1]):
                        if 0 <= c+i-kernelCenter[0] < width and 0 <= r+j-kernelCenter[1] < height and kernel[i, j] == 1:
                            dilationImage.putpixel((c+i-kernelCenter[0], r+j-kernelCenter[1]),255)
    return dilationImage


def Erosion(image, kernel, kernelCenter):
    '''
    image: Image (from PIL)
    kernel: np.array (from numpy)
    '''
    width, height = image.size
    erosionImage = Image.new('1', image.size)
    # compare image with kernel
    for c in range(width):
        for r in range(height):
            # erosion for white elements
            # if all match => put 1, not match => 0
            isMatch = True
            for i in range(kernel.shape[0]):
                for j in range(kernel.shape[1]):
                    # out of range case
                    if kernel[i, j] == 1:
                        if 0 <= c+i - kernelCenter[0] < width and 0 <= r+j - kernelCenter[1] < height:
                            if image.getpixel((c+i - kernelCenter[0], r+j - kernelCenter[1])) == 0:
                                isMatch = False
                                break
                        else:
                            isMatch = False
                            break
                if not isMatch:
                    break
            if isMatch:
                erosionImage.putpixel((c,r), 255)
    return erosionImage

def Opening(image, kernel,kernelCenter):
    return Dilation(Erosion(image,kernel, kernelCenter),kernel,kernelCenter)

def Closing(image, kernel,kernelCenter):
    return Erosion(Dilation(image, kernel,kernelCenter), kernel,kernelCenter)

def Complement(image):
    '''
    image: Image (from PIL)
    '''
    width, height = image.size
    complementImage = Image.new('L', image.size)
    for i in range(width):
        for j in range(height):
            if image.getpixel((i,j)) == 255:
                complementImage.putpixel((i,j), 0)
            else:
                complementImage.putpixel((i,j), 255)
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
            if imageA.getpixel((i,j)) == 255 and imageB.getpixel((i,j)) == 255:
                intersectionImage.putpixel((i,j), 255)
            else:
                intersectionImage.putpixel((i,j),0)
    return intersectionImage

def Hit_and_miss_transform(image, kernelJ, cneterJ, kernelK, centerK):
    return Intersection(Erosion(image, kernelJ, centerJ), Erosion(Complement(image), kernelK, centerK))

if __name__ == "__main__":
    from PIL import Image
    import numpy as np

    # define kernel 3-5-5-5-3
    kernel = np.array([
        [0,1,1,1,0],
        [1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,1,1,1],
        [0,1,1,1,0]])
    kernelCenter = (2,2)
    
    # define kernel J
    kernelJ = np.array([
        [1,1],
        [0,1]])
    centerJ = (1, 0)
    

    # defien kernel K
    kernelK = np.array([
        [1,1],
        [0,1]])
    centerK = (0, 1)
    # load image 
    originalImage = Image.open("Binary Image.bmp")

    # Q1
    dilationImage = Dilation(originalImage, kernel, (2,2))
    dilationImage.show()

    # Q2
    erosionImage = Erosion(originalImage, kernel, (2,2))
    erosionImage.show()
    
    # Q3
    openImage = Opening(originalImage, kernel, (2,2))
    openImage.show()

    # Q4
    closeImage = Closing(originalImage, kernel, (2,2))
    closeImage.show()

    # Q5
    hitMissImage = Hit_and_miss_transform(originalImage, kernelJ, centerJ, kernelK, centerK)
    hitMissImage.show()
    
    