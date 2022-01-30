# make 3 functions box volume, triangle area, box surface
# by william

def box_volume(length, width, height):
    return length*width*height

def triangle_area(base, height):
    return base*height/2

def box_surface(length, width, height):
    return ((length*width)+(length*height)+(width*height))*2




print (box_volume(3.0, 4.0, 5.0)) # should print 60.0

print (triangle_area(8.0, 5.0)) # should print 20.0 

print (box_surface(3.0, 4.0, 5.0)) # should print 94.0 