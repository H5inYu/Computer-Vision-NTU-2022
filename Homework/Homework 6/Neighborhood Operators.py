# Neighborhood Operators

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



def downSampling(image, rate):
    '''
    image: Image from PIL\n
    rate: (int) down-sampling rate.
    '''
    width, height = image.size
    new_width = width//rate
    new_height = height//rate
    new_image = Image.new("L", (new_width,new_height))
   
    for x in range(new_width):
        for y in range(new_height):
            new_image.putpixel((x,y), image.getpixel((x*rate,y*rate)))
    
    return new_image

def Yokoi(origin_image):
    '''
    image: Image from PIL
    '''
    width, height = origin_image.size
    newList = [[" " for i in range(width)] for j in range(height)]
    for c in range(width):
        for r in range(height):
            if origin_image.getpixel((c,r)) != 0:

                a1 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c+1,r)), 
                                    myGetPixel(origin_image,(c+1,r-1)), myGetPixel(origin_image,(c,r-1)))

                a2 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c,r-1)), 
                                    myGetPixel(origin_image,(c-1,r-1)), myGetPixel(origin_image,(c-1,r)))

                a3 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c-1,r)), 
                                    myGetPixel(origin_image,(c-1,r+1)), myGetPixel(origin_image,(c,r+1)))

                a4 = Yokoi_h_function(myGetPixel(origin_image,(c,r)), myGetPixel(origin_image,(c,r+1)), 
                                    myGetPixel(origin_image,(c+1,r+1)), myGetPixel(origin_image,(c+1,r)))
                newList[r][c] = Yokoi_f_function(a1,a2,a3,a4)
               
    return newList
    
def myGetPixel(image, position):
    x, y = position
    width, height = image.size
    if(0 <= x < width and  0 <= y < height):
        return image.getpixel(position)
    else:
        return 0

if __name__ == "__main__":
    from PIL import Image
    import numpy as np
    
    originalImage = Image.open('binary.bmp')
    downSamplingImage = downSampling(originalImage, 8)
    output_list = Yokoi(downSamplingImage)
    with open("Yokoi_connectivity.txt","w") as output_file:
        for i in output_list:
            for j in i:
                output_file.write(str(j))
            output_file.write('\n')