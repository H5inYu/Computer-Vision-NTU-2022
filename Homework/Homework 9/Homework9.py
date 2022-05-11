import numpy as np
from PIL import Image
import math
import random
import statistics

def Robert_operator(image, threshold) -> Image:
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    mask1 = np.array([
        [-1, 0],
        [0, 1]
    ])
    mask2 = np.array([
        [0, -1],
        [1, 0]
    ])
    padding_image = padding(image, "Robert")
    Robert_image = Image.new("L", image.size)

    width, height = padding_image.size
    r1, r2 = 0, 0
    for y in range(1, height-1):
        for x in range(1, width-1):
            r1 = padding_image.getpixel((x,y)) * -1 + padding_image.getpixel((x+1,y+1)) * 1
            r2 = padding_image.getpixel((x+1,y)) * -1 + padding_image.getpixel((x,y+1)) * 1
            magnitude = (r1**2 + r2**2) **0.5
            if magnitude >= threshold:
                Robert_image.putpixel((x-1, y-1), 0)
            else:
                Robert_image.putpixel((x-1, y-1), 255)
    return Robert_image

def Prewitt_operator(image, threshold) -> Image:
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    padding_image = padding(image, "Prewitt")
    Prewitt_image = Image.new("L", image.size)
    width, height = padding_image.size
    p1, p2 = 0, 0
    for x in range(1, width-1):
        for y in range(1, height-1):
            p1 = (padding_image.getpixel((x+1,y+1))+padding_image.getpixel((x,y+1))+padding_image.getpixel((x-1,y+1))) \
                - (padding_image.getpixel((x+1,y-1))+padding_image.getpixel((x,y-1))+padding_image.getpixel((x-1,y-1)))
            p2 = -(padding_image.getpixel((x-1,y-1))+padding_image.getpixel((x-1,y))+padding_image.getpixel((x-1,y+1))) \
                + (padding_image.getpixel((x+1,y-1))+padding_image.getpixel((x+1,y))+padding_image.getpixel((x+1,y+1)))
            magnitude = (p1**2 + p2**2)**0.5
            if magnitude >= threshold:
                Prewitt_image.putpixel((x-1, y-1), 0)
            else:
                Prewitt_image.putpixel((x-1, y-1), 255)
    return Prewitt_image

def Sobel_operator(image, threshold) -> Image:
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    padding_image = padding(image, "Prewitt")
    Sobel_image = Image.new("L", image.size)
    width, height = padding_image.size
    p1, p2 = 0, 0
    for x in range(1, width-1):
        for y in range(1, height-1):
            p1 = (padding_image.getpixel((x+1,y+1))+2*padding_image.getpixel((x,y+1))+padding_image.getpixel((x-1,y+1))) \
                - (padding_image.getpixel((x+1,y-1))+2*padding_image.getpixel((x,y-1))+padding_image.getpixel((x-1,y-1)))
            p2 = -(padding_image.getpixel((x-1,y-1))+2*padding_image.getpixel((x-1,y))+padding_image.getpixel((x-1,y+1))) \
                + (padding_image.getpixel((x+1,y-1))+2*padding_image.getpixel((x+1,y))+padding_image.getpixel((x+1,y+1)))
            magnitude = (p1**2 + p2**2)**0.5
            if magnitude >= threshold:
                Sobel_image.putpixel((x-1, y-1), 0)
            else:
                Sobel_image.putpixel((x-1, y-1), 255)
    return Sobel_image

def Frei_and_Chen_operator(image, threshold) -> Image:
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    padding_image = padding(image, "Prewitt")
    Frei_and_Chen_image = Image.new("L", image.size)
    width, height = padding_image.size
    p1, p2 = 0, 0
    for x in range(1, width-1):
        for y in range(1, height-1):
            p1 = (padding_image.getpixel((x+1,y+1))+2**0.5*padding_image.getpixel((x,y+1))+padding_image.getpixel((x-1,y+1))) \
                - (padding_image.getpixel((x+1,y-1))+2**0.5*padding_image.getpixel((x,y-1))+padding_image.getpixel((x-1,y-1)))
            p2 = -(padding_image.getpixel((x-1,y-1))+2**0.5*padding_image.getpixel((x-1,y))+padding_image.getpixel((x-1,y+1))) \
                + (padding_image.getpixel((x+1,y-1))+2**0.5*padding_image.getpixel((x+1,y))+padding_image.getpixel((x+1,y+1)))
            magnitude = (p1**2 + p2**2)**0.5
            if magnitude >= threshold:
                Frei_and_Chen_image.putpixel((x-1, y-1), 0)
            else:
                Frei_and_Chen_image.putpixel((x-1, y-1), 255)
    return Frei_and_Chen_image
    
def Kirschs_operator(image, threshold) -> Image:
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    k0 = np.array([
        [-3,-3, 5],
        [-3, 0, 5],
        [-3, -3, 5]
    ])
    k1 = np.array([
        [-3, 5, 5],
        [-3, 0, 5],
        [-3, -3, -3]
    ])
    k2 = np.array([
        [5, 5, 5],
        [-3, 0, -3],
        [-3, -3, -3]
    ])
    k3 = np.array([
        [5, 5, -3],
        [5, 0, -3],
        [-3, -3, -3]
    ])
    k4 = np.array([
        [5, -3, -3],
        [5, 0, -3],
        [5, -3, -3]
    ])
    k5 = np.array([
        [-3, -3, -3],
        [5, 0, -3],
        [5, 5, -3]
    ])
    k6 = np.array([
        [-3, -3, -3],
        [-3, 0, -3],
        [5, 5, 5]
    ])
    k7 = np.array([
        [-3, -3, -3],
        [-3, 0, 5],
        [-3, 5, 5]
    ])
    K = [k0, k1, k2, k3, k4, k5, k6, k7]
    padding_image = padding(image, "Prewitt")
    width, height = padding_image.size
    Kirsch_array = np.zeros((height-2, width-2))
    padding_image_array = np.array(padding_image)
    for r in range(1, height-1):
        for c in range(1, width-1):
            process_array = padding_image_array[r-1:r+2, c-1:c+2]
            magnitude = 0
            for i in K:
                magnitude = max(magnitude, np.sum(process_array*i))
            if magnitude >= threshold:
                Kirsch_array[r-1, c-1] = 0
            else:
                Kirsch_array[r-1, c-1] = 255
            
    Kirsch_image = Image.fromarray(Kirsch_array)
    return Kirsch_image

def Robinson_operator(image, threshold) -> Image:
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    r0 = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    r1 = np.array([
        [0, 1, 2],
        [-1, 0, 1],
        [-2, -1, 0]
    ])
    r2 = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])
    r3 = np.array([
        [2, 1, 0],
        [1, 0, -1],
        [0, -1, -2]
    ])
    r4 = np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]
    ])
    r5 = np.array([
        [0, -1, -2],
        [1, 0, -1],
        [2, 1, 0]
    ])
    r6 = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])
    r7 = np.array([
        [-2,-1,0],
        [-1,0,1],
        [0,1,2]
    ])
    R = [r0, r1, r2, r3, r4, r5, r6, r7]
    padding_image = padding(image, "Prewitt")
    width, height = padding_image.size
    Robinson_array = np.zeros((height-2, width-2))
    padding_image_array = np.array(padding_image)
    for r in range(1, height-1):
        for c in range(1, width-1):
            process_array = padding_image_array[r-1:r+2, c-1:c+2]
            magnitude = 0
            for i in R:
                magnitude = max(magnitude, np.sum(process_array*i))
            if magnitude >= threshold:
                Robinson_array[r-1, c-1] = 0
            else:
                Robinson_array[r-1, c-1] = 255
            
    Robinson_image = Image.fromarray(Robinson_array)
    return Robinson_image

def Nevatia_Babu_5x5_operator(image, threshold) -> Image:
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    '''
    :param image: Image from PIL
    :param threshold: Integer for operation 
    '''
    ang0 = np.array([
        [100, 100, 100, 100, 100],
        [100, 100, 100, 100, 100],
        [0, 0, 0, 0, 0],
        [-100, -100, -100, -100, -100],
        [-100, -100, -100, -100, -100]
    ])
    ang30 = np.array([
        [100, 100, 100, 100, 100],
        [100, 100, 100, 78, -32],
        [100, 92, 0, -92, -100],
        [32, -78, -100, -100, -100], 
        [-100, -100, -100, -100, -100]
    ])
    ang60 = np.array([
        [100, 100, 100, 32, -100],
        [100, 100, 92, -78, -100],
        [100, 100, 0, -100, -100],
        [100, 78, -92, -100, -100],
        [100, -32, -100, -100, -100],
    ])
    ang_90 = np.array([
        [-100, -100, 0, 100, 100],
        [-100, -100, 0, 100, 100],
        [-100, -100, 0, 100, 100],
        [-100, -100, 0, 100, 100],
        [-100, -100, 0, 100, 100]
    ])
    ang_60 = np.array([
        [-100, 32, 100, 100, 100],
        [-100, -78, 92, 100, 100],
        [-100, -100, 0, 100, 100],
        [-100, -100, -92, 78, 100],
        [-100, -100, -100, -32, 100]
    ])
    ang_30 = np.array([
        [100, 100, 100, 100, 100],
        [-32, 78, 100, 100, 100],
        [-100, -92, 0, 92, 100],
        [-100, -100, -100, -78, 32],
        [-100, -100, -100, -100, -100]
    ])
    
    R = [ang0,ang30,ang60,ang_90,ang_60,ang_30]
    padding_image = padding(image, "Prewitt")
    padding_image = padding(padding_image, "Prewitt")
    width, height = padding_image.size
    Nevatia_Babu_array = np.zeros((height-2, width-2))
    padding_image_array = np.array(padding_image)
    for r in range(2, height-2):
        for c in range(2, width-2):
            process_array = padding_image_array[r-2:r+3, c-2:c+3]
            magnitude = 0
            for i in R:
                magnitude = max(magnitude, np.sum(process_array*i))
            if magnitude >= threshold:
                Nevatia_Babu_array[r-2, c-2] = 0
            else:
                Nevatia_Babu_array[r-2, c-2] = 255
            
    Nevatia_Babu_image = Image.fromarray(Nevatia_Babu_array)
    return Nevatia_Babu_image

def padding(image, type) -> Image:
    padding_image = Image.new("L", (image.size[0] +2, image.size[1]+2))
    width, height = padding_image.size
    if type == "Robert":
        for x in range(width):
            for y in range(height):
                if(x == 0 or x == width-1 or y == 0 or y == height -1):
                    padding_image.putpixel((x,y), 0)
                else:
                    padding_image.putpixel((x,y), image.getpixel((x-1,y-1)))
    elif type == "Prewitt":
        padding_image.putpixel((0,0), image.getpixel((0, 0)))
        padding_image.putpixel((0,height-1), image.getpixel((0, height-3)))
        padding_image.putpixel((width-1, 0), image.getpixel((width-3, 0)))
        padding_image.putpixel((width-1,height-1), image.getpixel((width-3, height -3)))
        for x in range(width):
            for y in range(height):
                if (x==0 or x==width-1) and (y==0 or y==height-1):
                    continue
                elif x==0:
                    padding_image.putpixel((x,y), image.getpixel((x, y-1)))
                elif x==width-1:
                    padding_image.putpixel((x,y), image.getpixel((x-2, y-1)))
                elif y==0:
                    padding_image.putpixel((x,y), image.getpixel((x-1, y)))
                elif y == height-1:
                    padding_image.putpixel((x,y), image.getpixel((x-1, y-2)))
                else:
                    padding_image.putpixel((x,y), image.getpixel((x-1,y-1)))

    
    return padding_image
    



if __name__ == "__main__":
    image = Image.open("lena.bmp")
    Robert_image = Robert_operator(image, 35)
    Robert_image.save("./picure on report/Robert_threshold_35.bmp")
    # Robert_image.show()

    Prewitt_image = Prewitt_operator(image, 30)
    Prewitt_image.save("./picure on report/Prewitt_threshold_30.bmp")
    # Prewitt_image.show()

    Sobel_image = Sobel_operator(image, 50)
    Sobel_image.save("./picure on report/Sobel_threshold_50.bmp")
    # Sobel_image.show()

    Frei_and_Chen_image = Frei_and_Chen_operator(image, 40)
    Frei_and_Chen_image.save("./picure on report/Frei_and_Chen_threshold_40.bmp")
    # Frei_and_Chen_image.show()

    Kirsch_image = Kirschs_operator(image, 150)
    # Kirsch_image.show()
    Kirsch_image = Kirsch_image.convert("L")
    Kirsch_image.save("./picure on report/Kirsch_threshold_150.bmp")
    
    Robinson_image = Robinson_operator(image, 60)
    # Robinson_image.show()
    Robinson_image = Robinson_image.convert("L")
    Robinson_image.save("./picure on report/Robinson_threshold_60.bmp")

    Nevatia_Babu_image = Nevatia_Babu_5x5_operator(image, 13000)
    # Nevatia_Babu_image.show()
    Nevatia_Babu_image = Nevatia_Babu_image.convert("L")
    Nevatia_Babu_image.save("./picure on report/Nevatia_Babu_threshold_13000.bmp")
    pass