from os import stat
import time
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread
from ttkbootstrap import Style


class FlyerFrame(Frame):

    cacheImageBufs = []
    def cacheImage(self, id, imagetk):
        for cacheImageBuf in self.cacheImageBufs:
            if cacheImageBuf[0] == id:
                cacheImageBuf[1] = imagetk
        else:
            self.cacheImageBufs.append([id, imagetk])

    def createImage(self, x, y, image, callback=None):
        imagetk = ImageTk.PhotoImage(image)
        id = self.canvas.create_image(x, y, anchor='nw', image=imagetk)        
        if callback is not None:
            self.canvas.tag_bind(id, "<Button-1>", lambda event: callback())
        self.cacheImage(id, imagetk)
        return id

    def updateImage(self, id, image):
        imagetk = ImageTk.PhotoImage(image)
        self.canvas.itemconfigure(id, image=imagetk)
        self.cacheImage(id, imagetk)

    def createText(self, x, y, text, size=14, callback=None):
        id = self.canvas.create_text(x, y, text=text, font=('WenQuanYi Zen Hei', size))
        if callback is not None:
            self.canvas.tag_bind(id, "<Button-1>", lambda event: callback())
        return id

    def updateText(self, id, text):
        self.canvas.itemconfigure(id, text=text)

    def createButton(self, x, y, w, h, text, callback, **kw):
        object = ttk.Button(self.canvas, style='TButton', text=text, command=callback, **kw)
        object.place(x=x, y=y, width=w, height=h)
        return object

    def createLine(self, xOrigin, yOrigin, xTarget, yTarget, color, **kw):
        return self.canvas.create_line(xOrigin, yOrigin, xTarget, yTarget, fill=color, **kw)

    def startLoop(self, callback):
        def loop():
            while True:
                callback()
        loopThread = Thread(target=loop)
        loopThread.daemon = True
        loopThread.start()
        return loopThread

    def destory(self, object):
        if isinstance(object, int):
            self.canvas.delete(object)
        else:
            object.place_forget()
            object.destroy()

    def __init__(self):
        self.style = Style("yeti")
        self.style.configure('TButton', font=('WenQuanYi Zen Hei', 11))
        super().__init__(self.style.master)
        self.master.geometry('240x320')
        self.master.resizable(0, 0)
        self.pack(fill='both', expand=1)

        self.canvas = Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)

        def checkAlive():
            self.after(500, checkAlive)
        checkAlive()

flyFrame = FlyerFrame()
flyFrame.master.title("FlyerFrame Demo")

flyFrame.createImage(0, 0, Image.open('welcome.png'))
buttonTest = flyFrame.createButton(0, 0, 100, 28, "test", lambda:print("test"))
line1 = flyFrame.createLine(0, 0, 2, 2, 'red')


text = flyFrame.createText(30,300, "测试程序")

image = flyFrame.createImage(0, 0, Image.open('logo.png'), lambda:print("here"))

imagelogo = flyFrame.createImage(200, 200, Image.open('logo.png'), lambda:print("here"))


import cv2
vid = cv2.VideoCapture(0)

def loop():
    ret, frame = vid.read()

    frame = cv2.resize(frame, (240, int(frame.shape[0]*240/frame.shape[1])))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    flyFrame.updateImage(image, frame)


def buttonLoop():
    global buttonTest
    if buttonTest is not None:
        flyFrame.destory(buttonTest)
        buttonTest = None
        flyFrame.updateImage(imagelogo, Image.open('logo.png'))
    else:
        buttonTest = flyFrame.createButton(0, 0, 100, 28, "乔英杰", lambda:print("test"))
        flyFrame.updateImage(imagelogo, Image.open('logoNew.png'))
        
    time.sleep(1)


flyFrame.startLoop(loop)
flyFrame.startLoop(buttonLoop)

flyFrame.mainloop()
