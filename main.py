import PIL.Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog

displayImageLabels = []
displayImageButtons = []
images = []
displayImages =[]

def openfile():
    infolabel.config(text = "opening files...")
    images.clear()
    displayImages.clear()
    filepaths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    print(filepaths)


    for f in filepaths:
        newImage = PIL.Image.open(f)
        newImage = newImage.resize((120, 150))
        displayImages.append(newImage)
        images.append(PIL.Image.open(f))

    placeImages()
    
    
def placeImages():
#some calculations to display images in center, next to each otehr
    
    for l in displayImageLabels:
        l.destroy()

    for b in displayImageButtons:
        b.destroy()


    
    imageWidth = 120
    totalWidth = imageWidth * len(displayImages)
    xStart = (window.winfo_width() - totalWidth) /2

    for index, i in enumerate(displayImages):
        img = ImageTk.PhotoImage(i)
        labl = Label(image = img)
        labl.config(image = img)
        labl.photoimage = img
        labl.place(relx = xStart/window.winfo_width() + (index*imageWidth)/window.winfo_width(), rely = 0.3)
        
        #place some buttons under
        left_button = Button(text="<", command=lambda
        index=index:move_image_left(index))
        left_button.bindtags(("left_button_{}", format(index),) + left_button.bindtags())
        right_button = Button(text=">", command=lambda
        index=index:move_image_right(index))
        right_button.bindtags(("right_button_{}", format(index),) + right_button.bindtags())
        
        left_button.place(relx = xStart/window.winfo_width() + (index*imageWidth)/window.winfo_width()+ 0.05, rely = 0.65)
        right_button.place(relx = xStart/window.winfo_width() + (index*imageWidth)/window.winfo_width() + 0.1, rely = 0.65)

        displayImageLabels.append(labl)
        displayImageButtons.append(left_button)
        displayImageButtons.append(right_button)

    infolabel.config(text = "Waiting...")

def move_image_left(image_index):
    if image_index > 0:
        displayImages[image_index - 1], displayImages[image_index] = displayImages[image_index], displayImages[image_index-1]
        images[image_index - 1], images[image_index] = images[image_index], images[image_index-1]
    placeImages()

def move_image_right(image_index):
    if image_index < len(displayImages) -1:
        displayImages[image_index + 1], displayImages[image_index] = displayImages[image_index], displayImages[image_index+1]
        images[image_index + 1], images[image_index] = images[image_index], images[image_index+1]
    placeImages()

def saveFile():
    infolabel.config(text = "saving...")
    images[0].save(
        filedialog.asksaveasfilename(defaultextension=".pdf"), "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )
    print("file saved.")
    infolabel.config(text = "File Saved.")

window = Tk()
window.geometry("700x500")
label = Label(text = "Welcome to Image to PDF Generator")
label.place(relx = 0.5, rely=0.1, anchor = CENTER)
label.pack()
label2 = Label(text = "Choose the files you want to combine to a PDF")
label2.place(relx = 0.5, rely=0.2, anchor = CENTER)
label2.pack()
button = Button(text = "Open", command = openfile)
button.place(relx = 0.5, rely=0.3, anchor = CENTER)
button.pack()
button2 = Button(text = "Save", command = saveFile)
button2.place(relx = 0.5, rely=0.8, anchor = CENTER)
infolabel = Label(text = "Waiting...")
infolabel.place(relx = 0.5, rely= 0.9, anchor = CENTER)


window.mainloop()
