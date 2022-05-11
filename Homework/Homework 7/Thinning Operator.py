# Thinning Operator
from PIL import Image
import numpy as np
def binary(image, threshold):
    '''
    image: PIL Image
    threshold: int
    return: PIL Image
    '''
    width, height = image.size
    binarizedImage = Image.new("1", image.size)
    for x in range(width):
        for y in range(height):
            if image.getpixel((x,y))>=threshold:
                binarizedImage.putpixel((x,y), 1)
            else:
                binarizedImage.putpixel((x,y), 0)
    return binarizedImage

def down_sample(image, factor):
    '''
    image: PIL Image
    factor: int
    return: PIL Image
    '''
    width, height = image.size
    new_width, new_height = width//factor, height//factor
    new_image = Image.new("1", (new_width, new_height))
    for x in range(new_width):
        for y in range(new_height):
            new_image.putpixel((x,y), image.getpixel((x*factor, y*factor)))
    return new_image

def Yokoi_h_function(b, c, d, e):
    
    if(b==c and (d!=b or e!=b)):
        return "q"
    elif b==c and (d==b and e==b):
        return "r"
    elif b!=c:
        return "s"

def Yokoi_f_function(a1, a2, a3, a4):
    if a1==a2==a3==a4=="r":
        return 5
    else:
        return [a1, a2, a3, a4].count("q")

def Yokoi(origin_image):
    '''
    image: Image from PIL
    return: np.array from PIL
    '''
    width, height = origin_image.size
    
    connectivity = np.full(origin_image.size, ' ')
    # newList = [[" " for i in range(width)] for j in range(height)]
    for r in range(height):
        for c in range(width):
            if origin_image.getpixel((c,r)) != 0:

                a1 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c+1,r)), 
                                    myGetPixel(origin_image,(c+1,r-1)), myGetPixel(origin_image,(c,r-1)))

                a2 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c,r-1)), 
                                    myGetPixel(origin_image,(c-1,r-1)), myGetPixel(origin_image,(c-1,r)))

                a3 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c-1,r)), 
                                    myGetPixel(origin_image,(c-1,r+1)), myGetPixel(origin_image,(c,r+1)))

                a4 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c,r+1)), 
                                    myGetPixel(origin_image,(c+1,r+1)), myGetPixel(origin_image,(c+1,r)))
                
                connectivity[r,c] = Yokoi_f_function(a1,a2,a3,a4)
               
    return connectivity
    
def myGetPixel(image, position):
    x, y = position
    width, height = image.size
    if(0 <= x < width and  0 <= y < height):
        return image.getpixel(position)
    else:
        return 0

def neighbor_pixel(position, Yokoi_connectivity):
    r, c = position
    width, height = np.size(Yokoi_connectivity,1), np.size(Yokoi_connectivity,0)
    neighbors = []
    if 0 <= c+1 < width:
        neighbors.append(Yokoi_connectivity[r,c+1])
    else:
        neighbors.append(' ')
    if 0 <= r-1 < height:
        neighbors.append(Yokoi_connectivity[r-1, c])
    else:
        neighbors.append(' ')
    if 0 <= c-1 < width:
        neighbors.append(Yokoi_connectivity[r, c-1])
    else:
        neighbors.append(' ')
    if 0 <= r+1 < height:
        neighbors.append(Yokoi_connectivity[r+1, c])
    else:
        neighbors.append(' ')
    return neighbors

def pair_operator_h_function(a, m):
    if a == m:
        return 1
    else:
        return 0

def pair_operator_output(x0, m, Yokoi_Array):
    counter = 0
    neighborPixels = neighbor_pixel(x0, Yokoi_Array)
    
    for i in neighborPixels:
        counter += pair_operator_h_function(i, m)
    if counter < 1 or Yokoi_Array[x0] != m:
        return "q"
    else:
        return "p"


def pair_operator(image, Yokoi_Array):
    Pair_Array = np.full(image.size, ' ')
    width, height = image.size
    for r in range(height):
        for c in range(width):
            if Yokoi_Array[r, c] != ' ':
                Pair_Array[r, c] = pair_operator_output((r,c), '1', Yokoi_Array)
    return Pair_Array


def Connected_Shrink_Operator(origin_image, Pair_Array):
    width, height = origin_image.size
    for r in range(height):
        for c in range(width):
            if Pair_Array[r, c] == 'p':
                a1 = CSO_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c+1,r)), 
                                    myGetPixel(origin_image,(c+1,r-1)), myGetPixel(origin_image,(c,r-1)))

                a2 = CSO_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c,r-1)), 
                                    myGetPixel(origin_image,(c-1,r-1)), myGetPixel(origin_image,(c-1,r)))

                a3 = CSO_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c-1,r)), 
                                    myGetPixel(origin_image,(c-1,r+1)), myGetPixel(origin_image,(c,r+1)))

                a4 = CSO_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c,r+1)), 
                                    myGetPixel(origin_image,(c+1,r+1)), myGetPixel(origin_image,(c+1,r)))
                origin_image.putpixel((c,r), CSO_f_function(a1, a2, a3, a4, origin_image.getpixel((c,r))))
            
    return origin_image


def CSO_h_function(b, c, d, e):
    if b== c and (d!=b or e!= b):
        return 1
    else:
        return 0
def CSO_f_function(a1, a2, a3, a4, x):
    if [a1, a2, a3, a4].count(1) == 1:
        return 0 # background
    else:
        return x
    


if __name__ == "__main__":
    origin_image = Image.open('lena.bmp')
    binary_image = binary(origin_image,128)
    down_sample_image = down_sample(binary_image, 8)
    
    for i in range(7):
        # thinning start
        Yokoi_Array = Yokoi(down_sample_image)
        Pair_Array = pair_operator(down_sample_image, Yokoi_Array)
        down_sample_image = Connected_Shrink_Operator(down_sample_image, Pair_Array)
        # thinning end
    down_sample_image.save("thinning.bmp")
    down_sample_image.show()
