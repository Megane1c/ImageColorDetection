import cv2
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import messagebox


#Read image 
img = cv2.imread('sample-image.jpg')
img0 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img1 = cv2.resize(img, (960, 540))
na = np.array(img0)
colours, counts = np.unique(na.reshape(-1,3), axis=0, return_counts=1)
h,w, _ = img.shape

#Global variables
clicked = False
r = g = b = xpos = ypos = 0

#Read csv file using pandas and declare names of each column
index = ["color_name","hex","R","G","B", "id"]
csv = pd.read_csv('1400colors.csv', names = index, header = None)

#Calculate closest color using vectorized
def getColor(R,G,B):
    calc = np.abs(R - csv["R"].values) + np.abs(G - csv["G"].values) + np.abs(B - csv["B"].values)
    min = np.array(np.where(calc == calc.min()))
    min_array = min.flatten()
    clrname = csv.loc[min_array,"color_name"].values
    clrsize = clrname.size
    hex_value = csv.loc[min_array,"hex"].values
    hexsize = hex_value.size
    return clrname, clrsize, hex_value, hexsize

#Function to get x,y coordinates of mouse double click
def draw_function(event, x,y,*args):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img1[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

#Display color information
def showColor(colorname, rgbvalue, hexvalue, clrfill):
    win = Tk()
    win.title("Color Information")
    win.resizable(0,0) 
    w = 400     
    h = 120     
    screenw = win.winfo_screenwidth()
    screenh = win.winfo_screenheight()
    x = (screenw - w)/2
    y = (screenh - h)/2
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    canvas = Canvas(win, width = 400, height = 100)
    canvas.pack()
    canvas.create_rectangle(20, 10, 100, 90, outline="#000000" , fill = clrfill)

    label1 = Label(canvas, text = "Color Name: " + colorname)
    label1.place(x = 150, y = 10)
    label2 = Label(canvas, text = "RGB Value: " + rgbvalue)
    label2.place(x = 150, y = 40)
    label3 = Label(canvas, text = "Hex Value: " + hexvalue)
    label3.place(x = 150, y = 70)

    mainloop()

#Dominant Color
filt = counts[counts>((h*w/(2*(h+w))))]
clr_ind = []
for i in range(filt.size):
    ind = np.array(np.where(counts == filt[i]))
    for j in range(ind.size):
        inx = ind[0][j]
        clr_ind.append(inx)
        
f_list = []
for length in range(len(clr_ind)):
    r,g,b = colours[clr_ind[length]]
    clr_list_name,clr_list_size , _ ,_ = getColor(r,g,b)
    clr_list_str = clr_list_name
    for k in range(clr_list_size):
        clr_list_str = clr_list_name[k]

    f_list.append(clr_list_str)
clrlst, lstcts = np.unique(np.array(f_list), axis=0, return_counts=1)

hex_list = []
for i in range(len(clrlst)):
    hexclr = csv.loc[csv['color_name'] == clrlst[i], 'hex'].item()
    hex_list.append(hexclr)

clr_dict = dict(zip(clrlst, hex_list)) #Dictionary of dominant color

#Function for Dominant Color
def showDominantColor():
    dcolor = Tk()
    dcolor.title("Dominant Color") 
    w = 300   
    h = 525  
    screenw = dcolor.winfo_screenwidth()
    screenh = dcolor.winfo_screenheight()
    x = (screenw - w)/2
    y = (screenh - h)/2
    dcolor.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    canvas = Canvas(dcolor, width = 300, height = 200)
    canvas.pack(expand = 1)

    mxrw = len(clrlst)
    rw = 0
    cl = 0
    for key, value in clr_dict.items():
            btn = Button(canvas, bg=value, height = 1, width = 300, command = lambda key=key, value=value: messagebox.showinfo("Information", 'Color Name: ' + key + '\n' + 'Hex Value: ' + value))
            btn.grid(row=rw, column=cl, sticky="ew")
            rw += 1
            if rw > mxrw:
                rw = 0
                cl += 1
                            
    mainloop()

#Condition for specific color
vrb = 0
def cont(val):
    global vrb
    vrb = val

#Dominant or Specific
def showChoice():
    chc = Tk()
    chc.title(" ") 
    w = 350 
    h = 45  
    screenw = chc.winfo_screenwidth()
    screenh = chc.winfo_screenheight()
    x = (screenw - w)/2
    y = (screenh - h)/2
    chc.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    cnv = Canvas(chc, width = 350, height = 45)
    cnv.pack()
  
    btn1 = Button(cnv, text = 'Show Dominant Color', height =2, width = 20, font = ('Sans','10','bold'), bg = 'black', fg = 'white', command = lambda: [chc.destroy(), showDominantColor()])
    btn1.grid(row = 0, column = 1)

    btn2 = Button(cnv, text = 'Show Specific Color', height =2, width = 20, font = ('Sans','10','bold'), bg = 'white', fg = 'black', command = lambda: [chc.destroy(), cont(1)]) 
    btn2.grid(row = 0, column = 2)
    
    mainloop()


cv2.namedWindow('Image')
cv2.setMouseCallback('Image',draw_function)
        
while(1):

    cv2.imshow("Image", img1)
    

    if (clicked):
        showChoice()

        if vrb == 1:
            #Create text (Color name, RGB value, Hex value)
            clrstr, num_clr, hexna, num_hex = getColor(r,g,b)
            text1 = clrstr
            for i in range(num_clr):
                if i > 0:
                    text1 = f'{text1} or {clrstr[i]}'
                else:
                    text1 = clrstr[i]
            #text2 = 'R = '+ str(r) +  ' G = '+ str(g) +  ' B = '+ str(b)
            text2 = f'R = {r} G = {g} B = {b}'

        
            text3 = hexna
            for i in range(num_hex):
                if i > 0:
                    text3 = text3 + " or " + hexna[i]
                else:
                    text3 = hexna[i]
            colorfill = "#%02x%02x%02x" % (r, g, b)

            #Display information
            showColor(text1, text2, text3, colorfill)

            vrb = 0
        
        #Reset click
        clicked = False
        
    #Break loop using esc key   
    if cv2.waitKey(20) & 0xFF == 27:
        break

     
cv2.destroyAllWindows()
