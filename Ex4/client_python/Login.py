import os
import threading
import time
from tkinter import *
from PIL import ImageTk, Image
from Ex4.client_python.client import Client
from Ex4.client_python.Arena import Arena
from Ex4.client_python.RunServerScript import RunServerScript


class Login:

    def __init__(self):
        self.server_script = RunServerScript()
        self.cases = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"}
        self.size = 512, 256  # y,x
        parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.images_path = parent_path + "/imgs/"
        self.login = Tk()
        self.window()
        self.case = StringVar()
        self.login_lables()
        self.login.mainloop()

    def window(self):
        self.login.title("Game Login")
        self.login.minsize(self.size[0], self.size[1])
        self.login.maxsize(self.size[0], self.size[1])
        self.login.resizable(FALSE, FALSE)
        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (self.size[0] / 2))
        y_cordinate = int((screen_height / 2) - (self.size[1] / 2))

        self.login.geometry("{}x{}+{}+{}".format(self.size[0], self.size[1], x_cordinate, y_cordinate))

    def play(self):
        Arena(self.case.get())

    def home_screen(self):
        if self.case.get() in self.cases:
            label4 = Label(self.login, text="Game loading... ", width=25, font=("arial", 40, "bold"))
            label4.place(x=0, y=200)
            self.login.update()
            time.sleep(0.5)
            self.login.withdraw()
            self.play()

        else:  # incorrect case id
            label4 = Label(self.login, text="cases are 0 - 15 !", width=25, font=("arial", 40, "bold"))
            label4.place(x=0, y=200)
            self.login.update()

    def login_lables(self):
        # label1 = Label(self.login, text="Choose Case", fg="black", font=("new times roman", 40, "bold"))
        # label1.place(x=125, y=10)
        img = Image.open(self.images_path + "loginlogo2.png")
        img = ImageTk.PhotoImage(img)
        panel = Label(self.login, image=img)
        panel.image = img
        panel.pack()

        label3 = Label(self.login, text="Case :", font=("arial", 16, "bold"))
        label3.place(x=125, y=120)

        textBox2 = Entry(self.login, textvar=self.case, width=15, font=("arial", 16, "bold"))
        textBox2.place(x=200, y=120)

        button1 = Button(self.login, text="   CatchEmAll   ", fg="black", bg="white", relief="raised",
                         font=("arial", 16, "bold"),
                         command=self.home_screen)
        button1.place(x=185, y=170)


if __name__ == '__main__':
    run = Login()
