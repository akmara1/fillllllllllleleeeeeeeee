from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Canvas, Toplevel, simpledialog, messagebox
from tkinter.filedialog import askopenfilename
import basic_functions
from export import export
from tkinter import Frame

# Defining some global variables
img = None
img_copy = None
app_title = "Simple Immage Editor"
root = None
tk_im = None
color = (255,255,255,255)
filepath = ""

# Function to get the image using a Tkinter file dialog
def show_image():
    global filepath
    Tk().withdraw()
    filepath = askopenfilename()
    img = Image.open(filepath)
    tk_im = ImageTk.PhotoImage(img)
    return img, tk_im

# This function is called whenever the image display needs to be updated (when changes are made to the image)
def displayImage(im, canvas):

    global tk_im
    global image_window
    image_window.geometry(str(im.size[0])+"x"+str(im.size[1]))
    canvas.pack(side="top",fill="both",expand="yes")
    canvas.create_image(im.size[0]/2, im.size[1]/2, image=tk_im)

# This function is called as soon as the user starts making a change to the image
def makeCopy():
    global img
    global img_copy
    img_copy = img

def drawMode():
    global canvas
    canvas.bind("<Button 1>", drawPoint)
    canvas.bind("<B1-Motion>", drawCurve)
    

def drawCurve(event):
    global img
    makeCopy()
    if (event.x <= img.size[0] and event.y <= img.size[1]):
        drawPoint(event)

def textMode():
    global canvas
    canvas.bind("<Button 1>", addText)

def colorPicker():
    global canvas
    canvas.bind("<Button 1>", pickColor)

def drawPoint(event):
    global tk_im
    global img
    global canvas
    global color
    makeCopy()
    img = basic_functions.draw_point(img, event.x, event.y, color)
    tk_im = ImageTk.PhotoImage(img)
    canvas.delete("all")
    displayImage(img, canvas)

def addText(event):
    global tk_im
    global img
    global canvas
    global color
    makeCopy()
    content = simpledialog.askstring(title=app_title, prompt="Enter text: ")
    try:
        img = basic_functions.add_text(img, event.x, event.y, content,color)
    except TypeError:
        pass
    tk_im = ImageTk.PhotoImage(img)
    canvas.delete("all")
    displayImage(img, canvas)



    

# Set the global color variable to the RGBA value
def pickColor(event):
    global tk_im
    global img 
    global canvas
    global color

    color = basic_functions.pick_color(img, event.x, event.y)
    messagebox.showinfo(title=app_title, message=str("Selected RGBA color is: "+str(color)))
    canvas.unbind("<Button-1>")

def grayScale():

    global tk_im
    global img
    global canvas
    makeCopy()
    img = basic_functions.grayscale(img)
    tk_im = ImageTk.PhotoImage(img)
    canvas.delete("all")
    displayImage(img, canvas)

# Resize the image to dimensions given by user through Tkinter dialog
def resizing():
    global tk_im
    global img
    global canvas
    makeCopy()
    x = simpledialog.askinteger(title=app_title, prompt="Enter new X size:")
    if x != None:
        y = simpledialog.askinteger(title=app_title, prompt="Enter new Y size:")
        try:
            img = basic_functions.resize(img, x, y)
        except TypeError:
            pass
    tk_im = ImageTk.PhotoImage(img)
    canvas.delete("all")
    displayImage(img, canvas)


# Invert every pixel's color
def invertColors():

    global tk_im
    global img
    global canvas
    makeCopy()
    img = basic_functions.invertColors(img)
    tk_im = ImageTk.PhotoImage(img)
    canvas.delete("all")
    displayImage(img, canvas)

# All pixels with a color corresponding to the global color variable become transparent


# Undo the most recent action and display the copy made before the changes
def undo():
    global img
    global img_copy
    global canvas
    global tk_im
    img = img_copy
    tk_im = ImageTk.PhotoImage(img)
    canvas.delete("all")
    displayImage(img, canvas)


# Elements for the menu
root = Tk()
root.geometry("500x500")
root.title(app_title)

button = Button(master=root, command=grayScale, text="Grayscale")
button.pack()
button = Button(master=root, command=resizing, text="Resize")
button.pack()
button = Button(master=root, command=invertColors, text="Color inversion")
button.pack()
button = Button(master=root, command= lambda: export(img), text="Save")
button.pack()
button = Button(master=root, command=drawMode, text="Draw")
button.pack()
button = Button(master=root, command=textMode, text="Text")
button.pack()
button = Button(master=root, command=colorPicker, text="Color picker")
button.pack()
button = Button(master=root, command=undo, text="Undo")
button.pack()

frame = Frame(root, width=50, height=50)
frame.pack()
frame.place(x=5, y=5)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("alatoo.png"))
label = Label(frame, image = img)
label.pack()


# Image display GUI initialization + getting the image using get_image()
try:
    img,tk_im = show_image()
    makeCopy()

    image_window = Toplevel()
    image_window.title(filepath)
    image_window.geometry(str(img.size[0])+"x"+str(img.size[1]))
    image_window.resizable(False, False)
    canvas = Canvas(master=image_window)
    displayImage(img, canvas)

    root.mainloop()
except AttributeError:
    pass