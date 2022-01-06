import time
from tkinter import *

from Ex4.client_python.Arena import Arena


class Login:

    def __init__(self):
        self.size = 800, 480
        self.login = Tk()
        self.window()
        self.user_name = StringVar()
        self.password = StringVar()
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
        Arena()

    def home_screen(self):
        users = {'John': 'id', 'Shaked': '318985165', '1': '1'}
        username = self.user_name.get()
        print(username)
        passwd = self.password.get()
        if username in users:
            if users[username] == passwd:
                label4 = Label(self.login, text="Game loading... ", width=25, font=("arial", 40, "bold"))
                label4.place(x=0, y=400)
                self.login.update()
                time.sleep(0.5)
                self.login.withdraw()
                self.play()

            else:  # incorrect id
                label4 = Label(self.login, text="Wrong id's enter again", width=25, font=("arial", 40, "bold"))
                label4.place(x=0, y=400)
                self.login.update()

    def login_lables(self):

        label1 = Label(self.login, text=" Game Login ", fg="black", font=("new times roman", 40, "bold"))
        label1.place(x=250, y=15)

        label2 = Label(self.login, text="Username :", font=("arial", 16, "bold"))
        label2.place(x=144, y=150)

        textBox1 = Entry(self.login, textvar=self.user_name, width=30, font=("arial", 16, "bold"))
        textBox1.place(x=290, y=150)

        label3 = Label(self.login, text="Password :", font=("arial", 16, "bold"))
        label3.place(x=150, y=250)

        textBox2 = Entry(self.login, textvar=self.password, width=30, font=("arial", 16, "bold"))
        textBox2.place(x=290, y=250)

        button1 = Button(self.login, text="   Login   ", fg="black", bg="white", relief="raised",
                         font=("arial", 16, "bold"),
                         command=self.home_screen)
        button1.place(x=335, y=340)


if __name__ == '__main__':
    run = Login()
