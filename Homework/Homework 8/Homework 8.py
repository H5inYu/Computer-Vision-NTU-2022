import numpy as np
from PIL import Image
import math
import random
import statistics

def generate_gaussian_noise(image, amplitude) -> Image:
    '''
    This function uses to generate gaussian noise for a image
    :param image: Image from PIL.
    :param amplitude: An integer. Indicate the amplitude of noise
    '''
    gaussian_noise_image = Image.new('L', image.size)

    width, height = image.size
    for x in range(width):
        for y in range(height):
            noise_pixel = int(image.getpixel((x,y)) + amplitude*random.gauss(0,1))
            if noise_pixel > 255:
                noise_pixel = 255
            gaussian_noise_image.putpixel((x,y), noise_pixel)
    gaussian_noise_image.save("gaussian_noise_image_{}.bmp".format(amplitude))     
    return gaussian_noise_image
    
def generate_salt_and_pepper(image, threshold) -> Image:
    '''
    This function uses to generate salt_and_pepper noise for a image
    :param image: Image from PIL.
    :param threshold: Threshold determines signal-to-noise ratio
    '''
    salt_and_pepper_image = Image.new('L', image.size)
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if (random.uniform(0, 1) < threshold):
                salt_and_pepper_image.putpixel((x,y), 0)
            elif (random.uniform(0, 1) > 1 - threshold):
                salt_and_pepper_image.putpixel((x,y), 255)
            else:
                salt_and_pepper_image.putpixel((x,y), image.getpixel((x,y)))
    salt_and_pepper_image.save("salt_and_pepper_image_{}.bmp".format(threshold))
    return salt_and_pepper_image

def box_filter(image, box_size) -> Image:
    '''
    :param image: Image from PIL.
    :param box_size: tuple or list. It means the size of the box filter.
    '''
    box_filter_image = Image.new('L', image.size)
    offset_x, offset_y = box_size
    offset_x, offset_y = offset_x//2, offset_y//2
    width, height = image.size
    for x in range(width):
        for y in range(height):
            pixel_list = []
            for i in range(x - offset_x, x + offset_x + 1):
                for j in range(y - offset_y, y + offset_y + 1):
                    if (0 <= i < width and 0 <= j < height):
                        pixel_list.append(image.getpixel((i, j)))
            new_pixel = int(sum(pixel_list)/len(pixel_list))
            box_filter_image.putpixel((x,y), new_pixel)
    return box_filter_image

def median_filter(image, median_size) -> Image:
    '''
    :param image: Image from PIL.
    :param median_size: tuple or list. It means the size of the median filter.
    '''
    median_filter_image = Image.new('L', image.size)
    offset_x, offset_y = median_size
    offset_x, offset_y = offset_x//2, offset_y//2
    width, height = image.size
    for x in range(width):
        for y in range(height):
            pixel_list = []
            for i in range(x - offset_x, x + offset_x + 1):
                for j in range(y - offset_y, y + offset_y + 1):
                    if (0 <= i < width and 0 <= j < height):
                        pixel_list.append(image.getpixel((i, j)))
            median_filter_image.putpixel((x,y), int(statistics.median(pixel_list)))
    return median_filter_image

def Dilation(image, kernel, kernelCenter) ->Image:
    '''
    :param image: Image (from PIL)
    :param kernel: np.array (from numpy)
    :param kernelCenter: tuple(r, c) r = row, c = column
    '''
    width, height = image.size
    gs_DilationImage = Image.new('L', image.size)
    for c in range(width):
        for r in range(height):
            newPixel = image.getpixel((c, r))
            for x in range(-kernelCenter[1], kernelCenter[1] + 1):
                for y in range(-kernelCenter[0], kernelCenter[0] + 1):
                    if (0 <= c+x < width and 0 <= r+y < height and kernel[kernelCenter[0]+y, kernelCenter[1]+x] == 0):
                        newPixel = max(newPixel, image.getpixel((c+x, r+y)))
            gs_DilationImage.putpixel((c, r), newPixel)

    return gs_DilationImage

def Erosion(image, kernel, kernelCenter) -> Image:
    '''
    :param image: Image (from PIL)
    :param kernel: np.array (from numpy)
    :param kernelCenter: tuple(r, c) r = row, c = column
    '''
    width, height = image.size
    gs_ErosionImage = Image.new('L', image.size)
    for c in range(width):
        for r in range(height):
            newPixel = image.getpixel((c, r))
            for x in range(-kernelCenter[1], kernelCenter[1] + 1):
                for y in range(-kernelCenter[0], kernelCenter[0] + 1):
                    if (0 <= c+x < width and 0 <= r+y < height and kernel[kernelCenter[0]+y, kernelCenter[1]+x] == 0):
                        newPixel = min(newPixel, image.getpixel((c+x, r+y)))
            gs_ErosionImage.putpixel((c, r), newPixel)

    return gs_ErosionImage

def Opening(image, kernel, kernelCenter) -> Image:
    return Dilation(Erosion(image, kernel, kernelCenter), kernel, kernelCenter)

def Closing(image, kernel, kernelCenter) -> Image:
    return Erosion(Dilation(image, kernel, kernelCenter), kernel, kernelCenter)


def signal_to_noise_ratio(original_image, image_noise) -> float:
    '''
    This function compares the level of a desired signal to the level of background noise. 
    :param origin_image: Image from PIL
    :param image_noise: Image from PIL
    '''
    # calculate the mean of image 
    width, height = original_image.size
    mu, mu_n = 0, 0
    for y in range(height):
        for x in range(width):
            mu += original_image.getpixel((x,y))/255
            mu_n += image_noise.getpixel((x,y))/255- original_image.getpixel((x,y))/255
    mu = mu / (width * height)
    mu_n = mu_n / (width * height)
    
    VS, VN = 0, 0
    for y in range(height):
        for x in range(width):
            VS += (original_image.getpixel((x,y))/255 - mu)**2
            VN += (image_noise.getpixel((x,y))/255- original_image.getpixel((x,y))/255 - mu_n)**2
    VS = VS / (width * height)
    VN = VN / (width * height)
    SNR = 20 * math.log10(VS**0.5/VN**0.5)
    return SNR

if __name__ == "__main__":
    original_image = Image.open("lena.bmp")
    # gaussin_image_10 = generate_gaussian_noise(original_image, 10)
    # gaussin_image_30 = generate_gaussian_noise(original_image, 30)
    # salt_and_pepper_image_01 = generate_salt_and_pepper(original_image, 0.1)
    # salt_and_pepper_image_005 = generate_salt_and_pepper(original_image, 0.05)
    gaussin_image_10 = Image.open("gaussian_noise_image_10.bmp")
    gaussin_image_30 = Image.open("gaussian_noise_image_30.bmp")
    salt_and_pepper_image_01 = Image.open("salt_and_pepper_image_0.1.bmp")
    salt_and_pepper_image_005 = Image.open("salt_and_pepper_image_0.05.bmp")
    
    # print(signal_to_noise_ratio(original_image, gaussin_image_10))
    # print(signal_to_noise_ratio(original_image, gaussin_image_30))
    # print(signal_to_noise_ratio(original_image, salt_and_pepper_image_01))
    # print(signal_to_noise_ratio(original_image, salt_and_pepper_image_005))


    image_list = [gaussin_image_10, gaussin_image_30, salt_and_pepper_image_01, salt_and_pepper_image_005]

    # box filter 3x3 to each image
    # for i in range(0, len(image_list)):
    #     box_filter_3x3_image = box_filter(image_list[i], (3,3))
    #     box_filter_3x3_image.save("./Box Folder_3x3/{}_box_filter_3x3_image.bmp".format(i))
    
    # box filter 5x5 to each image
    # for i in range(0, len(image_list)):
    #     box_filter_5x5_image = box_filter(image_list[i], (5,5))
    #     box_filter_5x5_image.save("./Box Folder_5x5/{}_box_filter_5x5_image.bmp".format(i))
    
    # median filter 3x3 to each image
    # for i in range(0, len(image_list)): 
    #     median_filter_3x3_image = median_filter(image_list[i], (3,3))
    #     median_filter_3x3_image.save("./Median Folder_3x3/{}_median_filter_3x3_image.bmp".format(i))

    # median filter 5x5 to each image
    # for i in range(0, len(image_list)):
    #     median_filter_5x5_image = median_filter(image_list[i], (5,5))
    #     median_filter_5x5_image.save("./Median Folder_5x5/{}_median_filter_5x5_image.bmp".format(i))
    
    kernel = np.array([
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1]])
    kernelCenter = (2, 2)
    # opening then closing to each image
    for i in range(0, 4):
        opening_then_closing_image = Opening(image_list[i], kernel, kernelCenter)
        opening_then_closing_image = Closing(opening_then_closing_image, kernel, kernelCenter)
        # opening_then_closing_image.show()
        opening_then_closing_image.save("./Open_Close/{}_opening_then_closing_image.bmp".format(i))
    
    # closing then opening tot each image
    for i in range(0, 4):
        closing_then_opening_image = Closing(image_list[i], kernel, kernelCenter)
        closing_then_opening_image = Opening(closing_then_opening_image, kernel, kernelCenter)
        # closing_then_opening_image.show()
        closing_then_opening_image.save("./Close_Open/{}_closing_then_opening_image.bmp".format(i))

    # calculate snr

    # with open("./Box Folder_3x3/box_3x3_SNR.txt", "w") as SNR_file:
    #     for i in range(4):
    #         noise_image = Image.open("./Box Folder_3x3/{}_box_filter_3x3_image.bmp".format(i))
    #         snr = signal_to_noise_ratio(original_image, noise_image)
    #         SNR_file.write("SNR of {}_box_filter_3x3_image = {}\n".format(i, snr))
    
    # with open("./Box Folder_5x5/box_5x5_SNR.txt", "w") as SNR_file:
    #     for i in range(4):
    #         noise_image = Image.open("./Box Folder_5x5/{}_box_filter_5x5_image.bmp".format(i))
    #         snr = signal_to_noise_ratio(original_image, noise_image)
    #         SNR_file.write("SNR of {}_box_filter_5x5_image = {}\n".format(i, snr))

    # with open("./Median Folder_3x3/median_3x3_SNR.txt", "w") as SNR_file:
    #     for i in range(4):
    #         noise_image = Image.open("./Median Folder_3x3/{}_median_filter_3x3_image.bmp".format(i))
    #         snr = signal_to_noise_ratio(original_image, noise_image)
    #         SNR_file.write("SNR of {}_median_filter_3x3_image = {}\n".format(i, snr))

    # with open("./Median Folder_5x5/median_5x5_SNR.txt", "w") as SNR_file:
    #     for i in range(4):
    #         noise_image = Image.open("./Median Folder_5x5/{}_median_filter_5x5_image.bmp".format(i))
    #         snr = signal_to_noise_ratio(original_image, noise_image)
    #         SNR_file.write("SNR of {}_median_filter_5x5_image = {}\n".format(i, snr))

    # with open("./Open_Close/Open_Close_SNR.txt", "w") as SNR_file:
    #     for i in range(4):
    #         noise_image = Image.open("./Open_Close/{}_opening_then_closing_image.bmp".format(i))
    #         snr = signal_to_noise_ratio(original_image, noise_image)
    #         SNR_file.write("SNR of {}_opening_then_closing_image = {}\n".format(i, snr))

    # with open("./Close_Open/Close_Open_SNR.txt", "w") as SNR_file:
    #     for i in range(4):
    #         noise_image = Image.open("./Close_Open/{}_closing_then_opening_image.bmp".format(i))
    #         snr = signal_to_noise_ratio(original_image, noise_image)
    #         SNR_file.write("SNR of {}_closing_then_opening_image = {}\n".format(i, snr))  