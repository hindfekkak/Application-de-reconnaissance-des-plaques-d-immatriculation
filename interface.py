from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import cv2
from easyocr import Reader

root=Tk()
root.title('Matricules')
root.geometry('900x500+300+200')


#LOGO
ig=PhotoImage(file='image/logo.png')
root.iconphoto(False,ig)
root.config(bg='#fff')
root.resizable(False,False)

def uploadimg():
    image_name = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(
    ("png files", "*.png"), ("jpeg files", "*.jpg"), ("all files", "*.*")))
    path_img_txt.delete(0, 'end')
    path_img_txt.insert(0, image_name)

def predict():

    print(path_img_txt.get())
    # Charger l'image
    car = cv2.imread(path_img_txt.get())
    #resize the image dimensions
    car = cv2.resize(car, (800, 600))

    gray = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)

    # Appliquer le filtre de flou gaussien
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Edge detection
    edged = cv2.Canny(blur, 10, 200)
    #contours
    cont, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(cont)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)[:5]

    for c in cont:
        arc = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * arc, True)
        if len(approx) == 4:
            plate_cnt = approx
            break
    #plate_cnt array
    print(plate_cnt)
    (x, y, w, h) = cv2.boundingRect(plate_cnt)
    #plate
    plate = gray[y:y + h, x:x + w]
    #read text from the plate
    reader = Reader(["en"], gpu=False, verbose=False)
    detection = reader.readtext(plate)
    print(detection)

    if len(detection) == 0:
        text = "Impossible to read the text from \nthe license plate\n****"
        cv2.putText(car, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
        cv2.imshow('Image', car)
        cv2.waitKey(0)
        champ_label.config(text=text,fg='red')
    else:
        cv2.drawContours(car, [plate_cnt], -1, (0, 255, 0), 3)
        text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"
        cv2.putText(car, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        print(text)
        cv2.imshow('license plate', plate)
        cv2.imshow('Image', car)
        cv2.waitKey(0)
        champ_label.config(text=text,fg='#A555EC')

####____________________________________________________________________________________________________________________
#interface


#IMAGE d'arreire plan

img = PhotoImage(file='image/Mon projet.png')
Label(root, image=img, bg='white').place(x=50, y=50)
#frame
frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)
heading = Label(frame, text='Drag & Drop, \nUpload or Paste image', fg='#2F86A6', bg='white',font=('Microsoft YaHei UI Light', 15, 'bold'))
heading.place(x=100, y=5)

#button browse
def on_enter(e):
    path_img_txt.delete(0,'end')
def on_leave(e):
    path_img=path_img_txt.get()
    if path_img=='':
        path_img_txt.insert(0,'Entrer a URL')


car_img = Button(frame, text="Browse",width=15,height=3,bg='#A555EC',command=uploadimg)
car_img.place(x=150,y=70)

#image path
path_img_txt=Entry(frame,width=40,fg='black',border=2,bg='white',font=('Microsoft YaHei UI Light', 11))
path_img_txt.place(x=30,y=150)
path_img_txt.insert(0,'Entrer a URL')
path_img_txt.bind('<FocusIn>',on_enter)
path_img_txt.bind('<FocusOut>',on_leave)



#submit Button
predict=Button(frame, width=10,height=2,text='Submit',bg='#472183',fg='white',border=0,command=predict)
predict.place(x=250,y=200)


#result label
champ_label = Label(frame,border=2,font=('Microsoft YaHei UI Light', 15), text='')
champ_label.place(x=35,y=270)

#####__________________________________________________________________________
root.mainloop()