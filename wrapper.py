import tkinter as tk
import os
import shutil
import webbrowser
import tkinter.messagebox
import requests
import json
    

HEIGHT = 500
WIDTH = 800
yvalue = .075
xvalue = .17
root = r"C:\Users\zachw\Desktop\361Parts"

window = tk.Tk()

# webbrowser.open(r"C:\Users\zachw\Desktop\361 project\readme.txt")

canvas = tk.Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(window, bg = 'green')
frame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

# window.iconbitmap(r"C:\Users\zachw\Desktop\361 project\car.ico")


# --------------------------------Functions----------------------------------------------

def soldClick():
    if(tkinter.messagebox.askokcancel("warning", "you're about to move a part in your inventory press ok to proceed")):
        moveToSold()

def moveToSold():
    partNum = soldPartNumberEntry.get()
    soldPrice = soldPriceEntry.get()
    partNumListed = partNum + ' LISTED'

    for dirpath, dirnames, filenames in os.walk(root):
        if partNumListed in dirnames:
            oldPathWithListed = dirpath  + '\\' + partNum + ' LISTED'
            newPath = dirpath + '\\' + partNum + " $%s" %(soldPrice)
            
    os.rename(oldPathWithListed, newPath)
    destination = r"C:\Users\zachw\Desktop\361Parts\sold"

    shutil.move(newPath, destination)
    webbrowser.open(r"C:\Users\zachw\Desktop\361 mvp\moved.txt")
    return

def makeDirectory(partNum, boxNum):
    boxPath = root + r"\box #" + boxNum

    if(os.path.isdir(boxPath)):
        partPath = boxPath + "\\" + partNum
        try: 
            os.mkdir(partPath)
            print("Directory " , partPath , " Created ")
            return True 
        except FileExistsError:
            tkinter.messagebox.showinfo('already exists', "This part is already in your files" )
            print("Directory " , partPath ,  " already exists")
            return False
    else:
        os.mkdir(boxPath)
        makeDirectory(partNum, boxNum)

def makeFile(grpNum, partNum, name, env, weight, box, manufacturer, notes, numItems):
    filePath = root + r"\box #" + box + "\\" + partNum + "\\description.txt"

    textFrag1 = "group Number: %s \nname: %s \nweight: %s \nenvelope size: %s" %(grpNum, name, weight, env)
    textFrag2 = "\nmanufacturer: %s \nnumber of items: %s \nbox number: %s \nnotes: %s \n" %(manufacturer, numItems, box, notes)

    text = textFrag1 + textFrag2
    f = open(filePath, "w")
    f.truncate(0)
    f.seek(0)
    f.write(text)
    f.close()

def addPart():
    grpNum = groupNumEntry.get()
    partNum = partNumEntry.get()
    boxNum = boxNumEntry.get()

    partName = partNameEntry.get()
    envelSize = envelopeSizeEntry.get()
    weight = weightEntry.get()
    manufacturer = manufacturerEntry.get()
    notes = notesEntry.get()
    numItems = numItemsEntry.get()

    partNumWithListed = partNum + ' LISTED'

    for dirpath, dirnames, filenames in os.walk(root):
        if partNum in dirnames or partNumWithListed in dirnames:
            tkinter.messagebox.showinfo('already exists', "This part is already in your files at %s" %(dirpath))
            return
            
    
    if (makeDirectory(partNum, boxNum)):
        makeFile(grpNum, partNum, partName, envelSize, weight, boxNum, manufacturer, notes, numItems)
        webbrowser.open(r"C:\Users\zachw\Desktop\361 project\added.txt")
    
    return

def shipping():
    weight = shipWeightEntry.get()
    zone = zoneEntry.get()

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"weight": %s, "zone": %s}' %(weight, zone)

    response = requests.post('https://password-server.herokuapp.com/shipping', headers=headers, data=data)

    jason = response.json()

    total = jason['shippingTotal']

    tkinter.messagebox.showinfo('shipping', "Shipping will cost $%s" %(total) )
    return

def findBox():
    partNum = partNumberBoxFindEntry.get()
    partNumWithListed = partNum + ' LISTED'

    for dirpath, dirnames, filenames in os.walk(root):
        if partNum in dirnames or partNumWithListed in dirnames:
            partBoxPath = os.path.basename(dirpath)
            displayBoxNum(partBoxPath)
    return

def displayBoxNum(partBoxPath):
    tkinter.messagebox.showinfo('Box', "your part is in %s" %(partBoxPath) )
    return

def addListed():
    partNum = partNumberAddListedEntry.get()

    alreadyTagged = root + '\\' + partNum + " LISTED"

    for dirpath, dirnames, filenames in os.walk(root):
        if alreadyTagged in dirnames:
            tkinter.messagebox.showinfo('listed', "The listed tag has already been added to this part" )
            break
        elif partNum in dirnames:
            partPath = dirpath + '\\' + partNum
            withListed = partPath + " LISTED"

    os.rename(partPath, withListed)
    tkinter.messagebox.showinfo('listed', "The listed tag has been added" )
    return

def moveClick():
    if(tkinter.messagebox.askokcancel("warning", "you're about to move a part in your inventory press ok to proceed")):
        movePart()

def movePart():
    partNum = partNumberMoveEntry.get()
    boxNum = boxNumMoveEntry.get()
    partNumWithListed = partNum + ' LISTED'

    for dirpath, dirnames, filenames in os.walk(root):
        if partNum in dirnames:
            partPath = dirpath + '\\' + partNum
        elif partNumWithListed in dirnames:
            partPath = dirpath + '\\' + partNumWithListed

    destination = root + '\\' + "box #%s" %(boxNum)
    print(partPath)
    print(destination)

    shutil.move(partPath, destination)
    webbrowser.open(r"C:\Users\zachw\Desktop\361 mvp\moved.txt")
    return

#-------------------------------------------Add part window------------------------------------------

def menuAddPart():
    global groupNumEntry, partNameEntry, partNumEntry, boxNumEntry, weightEntry, envelopeSizeEntry, imagesEntry
    global manufacturerEntry, notesEntry, numItemsEntry
    addPartWindow = tk.Toplevel(window)
    addPartWindow.geometry('800x800')

    HEIGHT = 500
    WIDTH = 800

    canvas = tk.Canvas(addPartWindow, height = HEIGHT, width = WIDTH)
    canvas.pack()

    addFrame = tk.Frame(addPartWindow, bg = 'green')
    addFrame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)
    
    groupNumLabel = tk.Label(addFrame, text = "Group Number: ")
    groupNumLabel.place(relx = 0, rely = 0)

    partNumLabel = tk.Label(addFrame, text = "Part Number: ")
    partNumLabel.place(relx = 0, rely = yvalue)

    partNameLabel = tk.Label(addFrame, text = "Part Name: ")
    partNameLabel.place(relx = 0, rely = 2 * yvalue)

    boxNumLabel = tk.Label(addFrame, text = "Box Number: ")
    boxNumLabel.place(relx = 0, rely = 3 * yvalue)

    weightLabel = tk.Label(addFrame, text = "Weight: ")
    weightLabel.place(relx = 0, rely = 4 * yvalue)

    envelopeSizeLabel = tk.Label(addFrame, text = "Envelope Size: ")
    envelopeSizeLabel.place(relx = 0, rely = 5 * yvalue)

    imagesLabel = tk.Label(addFrame, text = "Images: ")
    imagesLabel.place(relx = 0, rely = 6 * yvalue)

    manufacturerLabel = tk.Label(addFrame, text = "Manufacturer: ")
    manufacturerLabel.place(relx = 0, rely = 7 * yvalue)

    notesLabel = tk.Label(addFrame, text = "Notes: ")
    notesLabel.place(relx = 0, rely = 8 * yvalue)

    numItemsLabel = tk.Label(addFrame, text = "Number of Items: ")
    numItemsLabel.place(relx = 0, rely = 9 * yvalue)

    groupNumEntry = tk.Entry(addFrame)
    groupNumEntry.place(relx = xvalue, rely = 0)

    partNumEntry = tk.Entry(addFrame)
    partNumEntry.place(relx = xvalue, rely = yvalue)

    partNameEntry = tk.Entry(addFrame)
    partNameEntry.place(relx = xvalue, rely = 2* yvalue)

    boxNumEntry = tk.Entry(addFrame)
    boxNumEntry.place(relx = xvalue, rely = 3 * yvalue)

    weightEntry = tk.Entry(addFrame)
    weightEntry.place(relx = xvalue, rely = 4 * yvalue)

    envelopeSizeEntry = tk.Entry(addFrame)
    envelopeSizeEntry.place(relx = xvalue, rely = 5 * yvalue)

    imagesEntry = tk.Entry(addFrame)
    imagesEntry.place(relx = xvalue, rely = 6 * yvalue)

    manufacturerEntry = tk.Entry(addFrame)
    manufacturerEntry.place(relx = xvalue, rely = 7 * yvalue)

    notesEntry = tk.Entry(addFrame)
    notesEntry.place(relx = xvalue, rely = 8 * yvalue)

    numItemsEntry = tk.Entry(addFrame)
    numItemsEntry.place(relx = xvalue, rely = 9 * yvalue)

    add = tk.Button(addFrame, text = "Add Part", command = addPart)
    add.place(relx = .15, rely = .8)

    return

def menuMoveToSold():
    global soldPartNumberEntry, soldPriceEntry
    moveSoldWindow = tk.Toplevel(window)
    moveSoldWindow.geometry('500x400')

    window.eval(f'tk::PlaceWindow {str(moveSoldWindow)} center')

    HEIGHT = 500
    WIDTH = 800

    canvas = tk.Canvas(moveSoldWindow, height = HEIGHT, width = WIDTH)
    canvas.pack()

    moveSoldFrame = tk.Frame(moveSoldWindow, bg = 'green')
    moveSoldFrame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

    soldPartNumber = tk.Label(moveSoldFrame, text = "Part number: ")
    soldPartNumber.place(relx = 0, rely = 0)

    soldPrice = tk.Label(moveSoldFrame, text = "Sold for: ")
    soldPrice.place(relx = 0, rely = .08)

    soldPartNumberEntry = tk.Entry(moveSoldFrame)
    soldPartNumberEntry.place(relx = .27, rely = 0)

    soldPriceEntry = tk.Entry(moveSoldFrame)
    soldPriceEntry.place(relx = .27, rely = .08)

    add = tk.Button(moveSoldFrame, text = "Move to Sold", command = soldClick)
    add.place(relx = xvalue, rely = .2)
    return

def menuShippingCost():
    global shipWeightEntry, zoneEntry
    shippingWindow = tk.Toplevel(window)
    shippingWindow.geometry('500x400')

    window.eval(f'tk::PlaceWindow {str(shippingWindow)} center')

    HEIGHT = 500
    WIDTH = 800

    canvas = tk.Canvas(shippingWindow, height = HEIGHT, width = WIDTH)
    canvas.pack()

    shippingFrame = tk.Frame(shippingWindow, bg = 'green')
    shippingFrame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

    weight = tk.Label(shippingFrame, text = "weight: ")
    weight.place(relx = 0, rely = 0)

    zone = tk.Label(shippingFrame, text = "zone: ")
    zone.place(relx = 0, rely = .08)

    shipWeightEntry = tk.Entry(shippingFrame)
    shipWeightEntry.place(relx = .27, rely = 0)

    zoneEntry = tk.Entry(shippingFrame)
    zoneEntry.place(relx = .27, rely = .08)

    add = tk.Button(shippingFrame, text = "Shipping Cost", command = shipping)
    add.place(relx = .27, rely = .57)
    return

def menuFindBox():
    global partNumberBoxFindEntry
    boxFindWindow = tk.Toplevel(window)
    boxFindWindow.geometry('500x400')

    window.eval(f'tk::PlaceWindow {str(boxFindWindow)} center')

    HEIGHT = 500
    WIDTH = 800

    canvas = tk.Canvas(boxFindWindow, height = HEIGHT, width = WIDTH)
    canvas.pack()

    boxFindFrame = tk.Frame(boxFindWindow, bg = 'green')
    boxFindFrame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

    partNumberBoxFind = tk.Label(boxFindFrame, text = "Part Number: ")
    partNumberBoxFind.place(relx = 0, rely = 0)

    partNumberBoxFindEntry = tk.Entry(boxFindFrame)
    partNumberBoxFindEntry.place(relx = .27, rely = 0)

    add = tk.Button(boxFindFrame, text = "Find Box", command = findBox)
    add.place(relx = .27, rely = .40)

    return

def menuMovePart():
    global partNumberMoveEntry, boxNumMoveEntry
    movePartWindow = tk.Toplevel(window)
    movePartWindow.geometry('500x400')

    window.eval(f'tk::PlaceWindow {str(movePartWindow)} center')

    HEIGHT = 500
    WIDTH = 800

    canvas = tk.Canvas(movePartWindow, height = HEIGHT, width = WIDTH)
    canvas.pack()

    movePartFrame = tk.Frame(movePartWindow, bg = 'green')
    movePartFrame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

    partNumberMove = tk.Label(movePartFrame, text = "Part Number: ")
    partNumberMove.place(relx = 0, rely = 0)

    boxNumMove = tk.Label(movePartFrame, text = "Box Number: ")
    boxNumMove.place(relx = 0, rely = .08)

    partNumberMoveEntry = tk.Entry(movePartFrame)
    partNumberMoveEntry.place(relx = .27, rely = 0)

    boxNumMoveEntry = tk.Entry(movePartFrame)
    boxNumMoveEntry.place(relx = .27, rely = .08)

    add = tk.Button(movePartFrame, text = "Move part", command = moveClick)
    add.place(relx = .27, rely = .40)
    return

def menuAddListed():
    global partNumberAddListedEntry
    listedWindow = tk.Toplevel(window)
    listedWindow.geometry('500x400')

    window.eval(f'tk::PlaceWindow {str(listedWindow)} center')

    HEIGHT = 500
    WIDTH = 800

    canvas = tk.Canvas(listedWindow, height = HEIGHT, width = WIDTH)
    canvas.pack()

    listedFrame = tk.Frame(listedWindow, bg = 'green')
    listedFrame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

    partNumberAddListed = tk.Label(listedFrame, text = "Part Number: ")
    partNumberAddListed.place(relx = 0, rely = 0)

    partNumberAddListedEntry = tk.Entry(listedFrame)
    partNumberAddListedEntry.place(relx = .27, rely = 0)

    add = tk.Button(listedFrame, text = "Add a \"listed\" tag", command = addListed)
    add.place(relx = .27, rely = .40)

    return

#-------------------------------------------------------------------------------------------------

add = tk.Button(frame, text = "Add Part", command = menuAddPart)
add.place(relx = .05, rely = .05)

add = tk.Button(frame, text = "Move Part To Sold", command = menuMoveToSold)
add.place(relx = .05, rely = .15)

add = tk.Button(frame, text = "Calculate Shipping", command = menuShippingCost)
add.place(relx = .05, rely = .25)

add = tk.Button(frame, text = "Find A Parts Box", command = menuFindBox)
add.place(relx = .05, rely = .35)

add = tk.Button(frame, text = "Move A Part", command = menuMovePart)
add.place(relx = .05, rely = .45)

add = tk.Button(frame, text = "Add A Listed Tag", command = menuAddListed)
add.place(relx = .05, rely = .55)

window.mainloop()