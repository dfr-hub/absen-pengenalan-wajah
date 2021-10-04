import tkinter
from tkinter import *
from tkinter import messagebox as mess
from tkinter import ttk
import tkinter.simpledialog as tsd
import os
import cv2
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

#Untuk Keluar Aplikasi
def on_closing():
    if mess.askyesno("Keluar", "Tutup Aplikasi?"):
        window.destroy()

#Hapus Input
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    res = "1) Ambil Gambar => 2) Simpan Profil"
    message1.configure(text=res)

#Check untuk Folder
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#Check Haarcascade File
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='File Missing!', message='File yang dibutuhkan tidak ditemukan')
        window.destroy()

#Check Password untuk Melakukan Perubahan Password
def save_pass():
    assure_path_exists("Pass_Train/")
    exists1 = os.path.isfile("Pass_Train\pass.txt")
    if exists1:
        tf = open("Pass_Train\pass.txt", "r")
        str = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Password belum diatur', 'Masukkan Password di bawah', show='*')
        if new_pas == None:
            mess._show(title='Password Kosong', message='Mohon masukkan Password dengan Benar')
        else:
            tf = open("Pass_Train\pass.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password telah Terdaftar!', message='Password Baru telah berhasil didaftarkan!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == str):
        if(newp == nnewp):
            txf = open("Pass_Train\pass.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Konfirmasi Password tidak sesuai')
            return
    else:
        mess._show(title='Password Salah', message='Password yang Anda masukkan Salah')
        return
    mess._show(title='Password telah diubah', message='Password telah berhasil diubah')
    master.destroy()

#Ubah Password
def change_pass():
    global master
    master = tkinter.Tk()
    master.geometry("600x160")
    master.resizable(False,False)
    master.title("Ubah Password Admin")
    master.configure(background="white")
    lbl4 = tkinter.Label(master,text='Masukkan Password Lama',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=90,y=10)
    global old
    old=tkinter.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=300,y=10)
    lbl5 = tkinter.Label(master, text='Masukkan Password Baru', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=90, y=45)
    global new
    new = tkinter.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=300, y=45)
    lbl6 = tkinter.Label(master, text='Konfirmasi Password Baru', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=90, y=80)
    global nnew
    nnew = tkinter.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=300, y=80)
    cancel=tkinter.Button(master,text="Cancel", command=master.destroy, fg="white" , bg="#413c69", height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=300, y=120)
    save1 = tkinter.Button(master, text="Save", command=save_pass, fg="white", bg="#413c69", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=110, y=120)
    master.mainloop()

#Tanya Password
def psw():
    assure_path_exists("Pass_Train/")
    exists1 = os.path.isfile("Pass_Train\pass.txt")
    if exists1:
        tf = open("Pass_Train\pass.txt", "r")
        str_pass = tf.read()
    else:
        new_pas = tsd.askstring('Password Tidak Ditemukan', 'Masukkan Password Baru di bawah', show='*')
        if new_pas == None:
            mess._show(title='Ada Kesalahan', message='Masukkan Password!!')
        else:
            tf = open("Pass_Train\pass.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password telah didaftarkan', message='Password Baru telah berhasil dibuat')
            return
    password = tsd.askstring('Password', 'Masukkan Password', show='*')
    if (password == str_pass):
        TrainImages()

    elif (password == None):
        pass
    else:
        mess._show(title='Password Salah!', message='Masukkan Password dengan Benar')


#Untuk Ambil Gambar
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAMA']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(3)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                sampleNum = sampleNum + 1
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('Ambil Gambar', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Pengambilan Gambar untuk ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Masukkan Nama yang benar"
            message.configure(text=res)

#Training Gambar
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("Pass_Train/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='Tidak Terdaftar', message='TIdak ada Data Siswa yang Terdaftar')
        return
    recognizer.save("Pass_Train\Trainner.yml")
    res = "Profil berhasil Disimpan"
    message1.configure(text=res)
    message.configure(text='Total Terdaftar sampai Saat ini  : ' + str(ID[0]))

#Identifikasi Gambar
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

#Track Gambar
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tb.get_children():
        tb.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer =cv2.face.LBPHFaceRecognizer_create() 
    exists3 = os.path.isfile("Pass_Train\Trainner.yml")
    if exists3:
        recognizer.read("Pass_Train\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Tidak ada Data yang Tersedia')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['ID', '', 'NAMA', '', 'Tanggal', '', 'Waktu']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Check kembali Detail Data Siswa')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAMA'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (0, 251, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tb.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

#Tampilan Utama Aplikasi
window = tkinter.Tk()
window.title("Sistem Kehadiran dengan Pengenalan Wajah")
window.geometry("1280x720")
window.resizable(True,True)
window.configure(background='#28527a')

#Menubar Help
menubar=Menu(window)
help=Menu(menubar,tearoff=0)
help.add_command(label="Change Password!",command=change_pass)
help.add_separator()
help.add_command(label="Exit",command=on_closing)
menubar.add_cascade(label="Help",menu=help)

window.config(menu=menubar)

#Main Window
message3 = tkinter.Label(window, text="Sistem Kehadiran dengan Pengenalan Wajah" ,fg="white",bg="#28527a" ,width=60 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=25,relwidth=1)

#Frame
frame1 = tkinter.Frame(window, bg="white")
frame1.place(relx=0.11, rely=0.15, relwidth=0.39, relheight=0.80)

frame2 = tkinter.Frame(window, bg="white")
frame2.place(relx=0.51, rely=0.15, relwidth=0.39, relheight=0.80)

#Frame Header
fr_head1 = tkinter.Label(frame1, text="Daftarkan Murid Baru", fg="white",bg="black" ,font=('times', 17, ' bold ') )
fr_head1.place(x=0,y=0,relwidth=1)

fr_head2 = tkinter.Label(frame2, text="Data Kehadiran Siswa", fg="white",bg="black" ,font=('times', 17, ' bold ') )
fr_head2.place(x=0,y=0,relwidth=1)

#Frame Registrasi
lbl = tkinter.Label(frame1, text="Masukkan ID",width=20  ,height=1  ,fg="black"  ,bg="white" ,font=('times', 17, ' bold ') )
lbl.place(x=-15, y=55)

txt = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold '))
txt.place(x=55, y=88,relwidth=0.75)

lbl2 = tkinter.Label(frame1, text="Masukkan Nama",width=20  ,fg="black"  ,bg="white" ,font=('times', 17, ' bold '))
lbl2.place(x=3, y=140)

txt2 = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold ')  )
txt2.place(x=55, y=173,relwidth=0.75)

message0=tkinter.Label(frame1,text="Ikuti Langkah Berikut:",bg="white" ,fg="black"  ,width=39 ,height=1,font=('times', 16, ' bold '))
message0.place(x=7,y=275)

message1 = tkinter.Label(frame1, text="1) Ambil Gambar => 2) Simpan Profil" ,bg="white" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=300)

message = tkinter.Label(frame1, text="" ,bg="white" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=500)

#Frame Kehadiran
lbl3 = tkinter.Label(frame2, text="Tabel Kehadiran",width=20  ,fg="black"  ,bg="white"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

#Menampilkan Total yang Terdaftar
res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Terdaftar : '+str(res))

#Button
clearButton = tkinter.Button(frame1, text="Clear", command=clear, fg="white", bg="#413c69", width=11, activebackground = "white", font=('times', 12, ' bold '))
clearButton.place(x=55, y=230,relwidth=0.29)

takeImg = tkinter.Button(frame1, text="Ambil Gambar", command=TakeImages, fg="white", bg="#413c69", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
takeImg.place(x=30, y=350,relwidth=0.89)

trainImg = tkinter.Button(frame1, text="Simpan Profil", command=psw, fg="white", bg="#413c69", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
trainImg.place(x=30, y=430,relwidth=0.89)

trackImg = tkinter.Button(frame2, text="Ambil Gambar", command=TrackImages, fg="white", bg="#413c69", height=1, activebackground = "white" ,font=('times', 16, ' bold '))
trackImg.place(x=30,y=60,relwidth=0.89)

quitWindow = tkinter.Button(frame2, text="Keluar", command=window.destroy, fg="white", bg="#413c69", width=35, height=1, activebackground = "white", font=('times', 16, ' bold '))
quitWindow.place(x=30, y=450,relwidth=0.89)

#Tabel Kehadiran
style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading",font=('times', 13,'bold')) # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
tb= ttk.Treeview(frame2,height =13,columns = ('NAMA','TANGGAL','WAKTU'),style="mystyle.Treeview")
tb.column('#0',width=90)
tb.column('NAMA',width=130)
tb.column('TANGGAL',width=133)
tb.column('WAKTU',width=133)
tb.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tb.heading('#0',text ='ID')
tb.heading('NAMA',text ='NAMA')
tb.heading('TANGGAL',text ='TANGGAL')
tb.heading('WAKTU',text ='WAKTU')

#Scrollbar
scroll=ttk.Scrollbar(frame2,orient='vertical',command=tb.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tb.configure(yscrollcommand=scroll.set)

#Garis Tutup
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
