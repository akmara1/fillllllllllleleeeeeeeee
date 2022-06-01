from PIL import ImageFilter, Image, ImageDraw, ImageFont
# Basic features of the editor

def grayscale(im):
    im = im.convert("L")
    im = im.convert("RGBA")
    return im
def resize(im, x, y):
    im = im.resize((x,y))
    return im

def invertColors(im):
    current_pixel = []

    for x in range(im.size[0]):
        for y in range(im.size[1]):
            current_pixel = list(im.getpixel((x, y)))
            #Invert colors of the pixel
            current_pixel[0] = abs(255-current_pixel[0])
            current_pixel[1] = abs(255-current_pixel[1])
            current_pixel[2] = abs(255-current_pixel[2])
            im.putpixel((x,y), tuple(current_pixel))

    return im
            


def draw_point(im, x, y, color):

    for x_coord in range(x-3, x+3):
        for y_coord in range(y-3, y+3):
            im.putpixel((x_coord,y_coord), color)
    
    return im

def add_text(im, x, y, content, color):
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype("comic.ttf", 36)

    d.text((x,y), content, fill=color, font=font)

    return im



