import numpy as np
from PIL import Image


def paddingArray(array) -> np.ndarray:
    '''
    :param array: np.ndarray
    '''
    row,column = array.shape
    padding_array = np.zeros((row+2, column+2))
    row, column = padding_array.shape
    padding_array[0,0] = array[0,0]
    padding_array[row-1, 0] = array[row-3, 0]
    padding_array[0, column-1] = array[0, column-3]
    padding_array[row-1, column-1] = array[row-3, column-3]
    for c in range(column):
        for r in range(row):
            if (c==0 or c==column-1) and (r==0 or r==row-1):
                continue
            elif c==0:
                padding_array[r,c] = array[r-1, c]
            elif c==column-1:
                padding_array[r,c] = array[r-1, c-2]
            elif r==0:
                padding_array[r,c] = array[r, c-1]
            elif r == row-1:
                padding_array[r,c] = array[r-2, c-1]
            else:
                padding_array[r,c] = array[r-1, c-1]
    return padding_array

def Laplacian(image, kernel, threshold) -> np.ndarray:
    '''
    :param image: PIL Image
    :param kernel: numpy ndarray
    :param threshold: integer
    '''
    padding_array = np.array(image)
    print(padding_array.shape)
    size = kernel.shape[0]//2
    print("size = ", size)
    for i in range(size):
        padding_array = paddingArray(padding_array)

    Laplacian_mask = np.zeros(image.size, dtype = int)
    row, column = padding_array.shape
    for r in range(size, row-size):
        for c in range(size, column-size):
            neighborhood_array = padding_array[r-size:r+size+1, c-size:c+size+1] * kernel
            if np.sum(neighborhood_array) >= threshold:
                Laplacian_mask[r-size,c-size] = 1
            elif np.sum(neighborhood_array) <= -threshold:
                Laplacian_mask[r-size,c-size] = -1
            else:
                Laplacian_mask[r-size,c-size] = 0
    return Laplacian_mask


def zero_crossing(array, threshold, kernel) -> Image:
    size = kernel.shape[0]//2
    padding_array = array
    for i in range(size):
        padding_array = paddingArray(padding_array)
    new_image = Image.new("1", array.shape)
    row, column = padding_array.shape
    for r in range(size, row-size):
        for c in range(size, column-size):
            if (padding_array[r,c] >= threshold and np.sum(padding_array[r-size:r+size+1, c-size:c+size+1] <= -threshold) >= 1):
                new_image.putpixel((c-size, r-size), 0)
            else:
                new_image.putpixel((c-size, r-size), 1)

    return new_image

if __name__ == "__main__":
    laplace_mask1 = np.array([
        [0, 1, 0],
        [1, -4, 1],
        [0, 1, 0]
    ])
    laplace_mask2 = np.array([
        [1, 1, 1],
        [1, -8, 1],
        [1, 1, 1]
    ])/3

    minimum_variance = np.array([
        [2, -1, 2],
        [-1, -4, -1],
        [2, -1, 2]
    ])/3
    Laplacian_of_Gaussian = np.array([
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
        [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
        [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
        [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
        [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
        [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
    ])
    difference_of_gaussian = np.array([
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
        [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
        [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
        [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
        [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
        [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
        [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]
    ])

    origin_image = Image.open("lena.bmp")

    # Laplacian_mask1_array_15 = Laplacian(origin_image, laplace_mask1, 20)
    # Laplacian_mask1_15_image = zero_crossing(Laplacian_mask1_array_15, 1, laplace_mask1)
    # Laplacian_mask1_15_image.save("Laplacian_mask1_20_image.bmp")

    # Laplacian_mask2_array_15 = Laplacian(origin_image, laplace_mask2, 20)
    # Laplacian_mask2_15_image = zero_crossing(Laplacian_mask2_array_15, 1, laplace_mask2)
    # Laplacian_mask2_15_image.save("Laplacian_mask2_20_image.bmp")

    minimum_variance_array_20 = Laplacian(origin_image, minimum_variance, 15)
    minimum_variance_20_image = zero_crossing(minimum_variance_array_20, 1, minimum_variance)
    minimum_variance_20_image.save("minimum_variance_15_image.bmp")
    minimum_variance_20_image.show()

    # Laplacian_of_Gaussian_array_3000 = Laplacian(origin_image, Laplacian_of_Gaussian, 5000)
    # Laplacian_of_Gaussian_3000_image = zero_crossing(Laplacian_of_Gaussian_array_3000, 1, laplace_mask2)
    # Laplacian_of_Gaussian_3000_image.save("Laplacian_of_Gaussian_5000_image.bmp")
    # Laplacian_of_Gaussian_3000_image.show()

    # difference_of_gaussian_array_1 = Laplacian(origin_image, difference_of_gaussian, 4)
    # difference_of_gaussian_1_image = zero_crossing(difference_of_gaussian_array_1, 1, laplace_mask2)
    # difference_of_gaussian_1_image.save("difference_of_gaussian_4_image.bmp")
    # difference_of_gaussian_1_image.show()



    