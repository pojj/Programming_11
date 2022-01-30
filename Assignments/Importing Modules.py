#find area of circle from inputed radius using math
#then rounds up and down and then to the nearest whole number
#generates length, width and height of cube then gives volume
#to the nearest 10, and the nearest 100 using the round function
#written by William

import math
import random

radius = int(input("Enter radius of circle"))
area = radius ** 2 * math.pi

print("A circle with an radius of",radius,"has an area of",area)
print(area,"is between",int(math.floor(area)),"and",int(math.ceil(area)))
print(area,"is closer to",int(round(area)))


print()
print("Generates a random length, width and height of cube")

length = random.randint(1, 10)
width = random.randint(1, 10)
height = random.randint(1, 10)
volume = length*width*height

print("A cube with side lengths of",str(length)+",",str(width)+",",str(height),"has an volume of",volume)
print("Volume rounded to the nearest 10 is",round(volume, -1))
print("Volume rounded to the nearest 100 is",round(volume, -2))