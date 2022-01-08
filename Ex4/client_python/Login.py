"""
 * Authors - Yonatan Ratner & Shaked Levi
 * Date - 7.1.2022
"""
import os
import time
from tkinter import *
from PIL import ImageTk, Image
from Arena import Arena
from Misc import Misc
from RunServerScript import RunServerScript


class Login:
    """
    This class is our Login menu. it handles the case number to start the server with.
    """

    def __init__(self):
        self.server_script = RunServerScript()
        self.cases = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"}
        self.size = 512, 256  # y,x
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        parent_path = Misc.resource_path(relative_path='data')
        self.images_path = parent_path + "/imgs/"
        self.login = Tk()
        self.window()
        self.case = StringVar()
        self.login_lables()
        self.login.mainloop()

    def window(self):
        """
        This method is responsible for creating the tkinter login window and centring it.
        """
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
        """
        This method handles the input to the login labels
        """
        if self.case.get() in self.cases:
            label4 = Label(self.login, text="Game loading... ", width=25, font=("arial", 20, "bold"))
            label4.place(x=125, y=200)
            self.login.update()
            time.sleep(0.5)
            self.login.withdraw()
            self.play()

        else:  # incorrect case id
            label4 = Label(self.login, text="cases are 0 - 15 ! enter again", width=25, font=("arial", 20, "bold"))
            label4.place(x=100, y=200)
            self.login.update()

    def login_lables(self):
        """
        This method creates the login labels.
        """
        img = Image.open(self.images_path + "loginlogo2.png")
        img = ImageTk.PhotoImage(img)
        logo = Label(self.login, image=img)
        logo.image = img
        logo.pack()

        case = Label(self.login, text="Case :", font=("arial", 16, "bold"))
        case.place(x=125, y=120)

        case_txt = Entry(self.login, textvar=self.case, width=15, font=("arial", 16, "bold"))
        case_txt.place(x=200, y=120)

        start_game = Button(self.login, text="   CatchEmAll   ", fg="black", bg="white", relief="raised",
                            font=("arial", 16, "bold"),
                            command=self.home_screen)
        start_game.place(x=185, y=170)


if __name__ == '__main__':
    run = Login()
