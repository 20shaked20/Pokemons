import threading
import time
from tkinter import *

from Ex4.client_python.Arena import Arena
from Ex4.client_python.RunServerScript import RunServerScript


class Login:

    def __init__(self):
        self.server_script = RunServerScript()
        self.cases = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"}
        self.size = 800, 480
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
        t1 = threading.Thread(target=self.server_script.server_activate, args=[self.case.get()])
        t2 = threading.Thread(target=Arena)
        t1.start()
        time.sleep(1)
        t2.start()

    def home_screen(self):
        if self.case.get() in self.cases:
            label4 = Label(self.login, text="Game loading... ", width=25, font=("arial", 40, "bold"))
            label4.place(x=0, y=400)
            self.login.update()
            time.sleep(0.5)
            self.login.withdraw()
            self.play()

        else:  # incorrect case id
            label4 = Label(self.login, text="cases are 0 - 15 !", width=25, font=("arial", 40, "bold"))
            label4.place(x=0, y=400)
            self.login.update()

    def login_lables(self):
        label1 = Label(self.login, text=" Game Login ", fg="black", font=("new times roman", 40, "bold"))
        label1.place(x=250, y=15)

        # label2 = Label(self.login, text="Username :", font=("arial", 16, "bold"))
        # label2.place(x=144, y=150)
#
        # textBox1 = Entry(self.login, textvar=self.user_name, width=30, font=("arial", 16, "bold"))
        # textBox1.place(x=290, y=150)

        label3 = Label(self.login, text="Case :", font=("arial", 16, "bold"))
        label3.place(x=147, y=200)
        # label3.place(x=150, y=250)

        textBox2 = Entry(self.login, textvar=self.case, width=30, font=("arial", 16, "bold"))
        textBox2.place(x=260, y=200)
        # textBox2.place(x=290, y=250)

        button1 = Button(self.login, text="   Login   ", fg="black", bg="white", relief="raised",
                         font=("arial", 16, "bold"),
                         command=self.home_screen)
        button1.place(x=335, y=260)


if __name__ == '__main__':
    run = Login()
