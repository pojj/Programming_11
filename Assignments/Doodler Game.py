# by william

import simplegui


class Shape:
    def __init__(self,size,colour,pos,type):
        self.size = size
        self.col = colour
        self.pos = pos
        self.type = type
        
    def draw_dot(self, canvas):
        canvas.draw_circle(self.pos, self.size, 1, self.col, self.col)
        
    def draw_triangle(self, canvas):
        canvas.draw_polygon([[self.pos[0],self.pos[1]-self.size],
                             [self.pos[0]+self.size,self.pos[1]+self.size],
                             [self.pos[0]-self.size,self.pos[1]+self.size]], 1, self.col, self.col)
        
    def draw_square(self, canvas):
        canvas.draw_polygon([[self.pos[0]-self.size,self.pos[1]-self.size],
                             [self.pos[0]+self.size,self.pos[1]-self.size],
                             [self.pos[0]+self.size,self.pos[1]+self.size],
                             [self.pos[0]-self.size,self.pos[1]+self.size]], 1, self.col, self.col)
        
    def draw_unicorn(self, canvas):
        canvas.draw_image(IMAGE, (IMG_WIDTH / 2, IMG_HEIGHT / 2),
                          (IMG_WIDTH, IMG_HEIGHT),
                          self.pos, (self.size*2, self.size*2))
    

def clear():
    global dots
    dots = []

def input_handler(text_input):
    global colour
    colour = text_input 
    
def increase():
    global size
    size += 3
    label.set_text("Brush size: " + str(size))
       
def decrease():
    global size
    if size > 3:
        size -= 3
    label.set_text("Brush size: " + str(size))

def next_shape():
    global current_shape
    current_shape = shapes[(shapes.index(current_shape)+1) % 4]
    label2.set_text("Brush type: " + current_shape)
        

def mouse_handler(position):
    new_dot = Shape(size, colour, position, current_shape)
    dots.append(new_dot)
        
def draw(canvas):
    canvas.draw_image(BKG_IMG, (BKG_WIDTH / 2, BKG_HEIGHT / 2),
                      (BKG_WIDTH, BKG_HEIGHT),
                      (WIDTH/2, HEIGHT/2),
                      (WIDTH, HEIGHT))
    
    for pixel in dots:
        if pixel.type == "Dot":
            pixel.draw_dot(canvas)
        if pixel.type == "Triangle":
            pixel.draw_triangle(canvas)
        if pixel.type == "Square":
            pixel.draw_square(canvas)
        if pixel.type == "Unicorn":
            pixel.draw_unicorn(canvas)

dots = []
shapes = ["Dot", "Triangle", "Square", "Unicorn"]
current_shape = "Dot"
colour = "black"
size = 10

WIDTH = 800
HEIGHT = 600

BKG_IMG = simplegui.load_image('https://cdn.mos.cms.futurecdn.net/42E9as7NaTaAi4A6JcuFwG.jpg')
BKG_WIDTH = 700
BKG_HEIGHT = 467

IMAGE = simplegui.load_image('https://media.istockphoto.com/vectors/cartoon-unicorn-head-vector-id1127169576')
IMG_WIDTH = 1024
IMG_HEIGHT = 1024

frame = simplegui.create_frame("Draw", WIDTH, HEIGHT)

frame.add_button("Clear", clear)

frame.add_input("Colour", input_handler, 50)

frame.add_button("Increase Thicc", increase)
frame.add_button("Decrease Thicc", decrease)
label = frame.add_label("Brush size: " + str(size))

frame.add_button("Change Shape", next_shape)
label2 = frame.add_label("Brush type: " + current_shape)

frame.set_mouseclick_handler(mouse_handler)
frame.set_mousedrag_handler(mouse_handler)

frame.set_draw_handler(draw)
frame.start()

