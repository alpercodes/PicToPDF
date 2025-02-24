import PIL.Image 
from PIL import ImageTk
from tkinter import filedialog, Button, Label, Checkbutton, Tk, CENTER, IntVar
import ocrmypdf

displayImageLabels = []
displayImageButtons = []
images = []
displayImages =[]

def openfile(): #function when pressing "open" button ... loads chosen images
    infolabel.config(text = "opening files...")
    images.clear()
    displayImages.clear()
    try:
        filepaths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])

        for f in filepaths:
            newImage = PIL.Image.open(f)
            newImage = newImage.resize((120, 150))
            displayImages.append(newImage)
            images.append(PIL.Image.open(f))

        placeImages()
    except:
        infolabel.config(text = "ERROR while uploading files.")
    
    
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

def move_image_left(image_index): #function when pressing "left-button" under an image.. moves it to the left
    if image_index > 0:
        displayImages[image_index - 1], displayImages[image_index] = displayImages[image_index], displayImages[image_index-1]
        images[image_index - 1], images[image_index] = images[image_index], images[image_index-1]
    placeImages()

def move_image_right(image_index): #function when pressing "right-button" under an image.. moves it to the right
    if image_index < len(displayImages) -1:
        displayImages[image_index + 1], displayImages[image_index] = displayImages[image_index], displayImages[image_index+1]
        images[image_index + 1], images[image_index] = images[image_index], images[image_index+1]
    placeImages()

def saveFile(): #Save Images in order as PDF
    if len(images) == 0:
        infolabel.config(text = "No Images selected...")
    else:
        infolabel.config(text = "saving...")
        target_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        images[0].save(target_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
        print("file saved.")
        print(ocr_checked.get())
        if ocr_checked.get() == 1:
            print("trying ocr....")
            ocrmypdf.ocr(target_path, target_path, deskew=True)
        infolabel.config(text = "File Saved.")

window = Tk()
ocr_checked = IntVar()
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
checkbox = Checkbutton(window, text='OCR Enabled',variable=ocr_checked, onvalue=1, offvalue=0)
checkbox.place(relx=0.5, rely=0.75, anchor = CENTER)
button2 = Button(text = "Save", command = saveFile)
button2.place(relx = 0.5, rely=0.85, anchor = CENTER)
infolabel = Label(text = "Waiting...")
infolabel.place(relx = 0.5, rely= 0.95, anchor = CENTER)


window.mainloop()
