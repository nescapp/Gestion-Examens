from typing import Optional, Tuple, Union
import customtkinter
from PIL import Image
from tkinter import messagebox
from functools import partial

# set appearance mode and default color theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("images/color_theme.json")


class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.label_list = []

    def add_item(self, item, command=None):
        button_item = customtkinter.CTkButton(
            self,
            text=item,
            font=customtkinter.CTkFont(size=20, weight="bold"),
            height=220,
            width=1000,
            command=command,
        )
        button_item.grid(
            row=len(self.label_list), column=0, padx=10, pady=10
        )
        self.label_list.append(button_item)


class App(customtkinter.CTk):
    # window size
    width = 1000
    height = 500

    def __init__(self, *args, **kwargs):
        # call super constructor
        super().__init__(*args, **kwargs)
        print("initializing app")

        # configure root
        self.title("Gestion des examens")
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(800, 500)
        # self.config(background="#4c4f69")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create main frame
        self.frame_main = customtkinter.CTkFrame(self)
        self.frame_main.grid(row=1, column=0, sticky="nsew", padx=50, pady=50)
        self.frame_main.grid_columnconfigure(0, weight=1)
        self.frame_main.grid_columnconfigure(1, weight=1)
        self.frame_main.grid_columnconfigure(2, weight=1)
        self.frame_main.grid_rowconfigure(2, weight=1)

        # create main frame widgets
        self.label_heading = customtkinter.CTkLabel(
            self.frame_main,
            text="Choisisez votre mode",
            font=customtkinter.CTkFont(size=42, weight="bold"),
        )
        self.label_heading.grid(row=0, column=0, padx=30, pady=30, columnspan=3)

        self.image_eleve = Image.open("images/student.png")
        self.image_eleve = customtkinter.CTkImage(self.image_eleve, size=(100, 100))
        self.image_label = customtkinter.CTkLabel(
            self.frame_main, image=self.image_eleve
        )

        self.button_eleve = customtkinter.CTkButton(
            self.frame_main,
            text="Mode étudiant",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            command=self.show_frame_login,
            image=self.image_eleve,
            compound="top",
            width=200,
            height=300,
        )
        self.button_eleve.grid(row=2, column=0, padx=30, pady=15, sticky="nsew")

        self.image_prof = Image.open("images/teacher.png")
        self.image_prof = customtkinter.CTkImage(self.image_prof, size=(100, 100))
        self.image_label = customtkinter.CTkLabel(
            self.frame_main, image=self.image_prof
        )

        self.button_prof = customtkinter.CTkButton(
            self.frame_main,
            text="Mode professeur",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            command=self.show_frame_prof,
            image=self.image_prof,
            compound="top",
            width=200,
            height=300,
        )
        self.button_prof.grid(row=2, column=1, padx=30, pady=15, sticky="nsew")

        self.image_quit = Image.open("images/hand.png")
        self.image_quit = customtkinter.CTkImage(self.image_quit, size=(100, 100))
        self.image_label = customtkinter.CTkLabel(
            self.frame_main, image=self.image_quit
        )

        self.button_quit = customtkinter.CTkButton(
            self.frame_main,
            text="Quitter",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            command=self.quit,
            image=self.image_quit,
            compound="top",
            width=200,
            height=300,
        )
        self.button_quit.grid(row=2, column=2, padx=30, pady=15, sticky="nsew")

        # create eleve frame
        self.frame_eleve = customtkinter.CTkFrame(self)
        self.frame_eleve.grid_columnconfigure(0, weight=1)
        self.frame_eleve.grid_rowconfigure(1, weight=1)

        # create eleve frame widgets
        self.label_heading = customtkinter.CTkLabel(
            self.frame_eleve,
            text="Eleve",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label_heading.grid(row=0, column=0, padx=30, pady=30)

        self.scrollable_frame = ScrollableFrame(
            master=self.frame_eleve,
            height=500,  # item_list=[f"QCM {i}" for i in range(10)]
        )
        # print item_list
        self.scrollable_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nesw")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.scrollable_frame.add_item("QCM #1", lambda: self.show_qcm_frame(1))
        for i in range(2, 10):
            action_with_arg = partial(self.show_qcm_frame, i)
            self.scrollable_frame.add_item(f"QCM #{i}", action_with_arg)

        # create qcm frame
        self.frame_qcm = customtkinter.CTkFrame(self, width=200, height=200)

        self.label_qcm_heading = customtkinter.CTkLabel(
            self.frame_qcm,
            text="Show QCM",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label_qcm_heading.grid(row=0, column=0, padx=30, pady=30)

        self.button_back = customtkinter.CTkButton(
            self.frame_qcm,
            text="Back",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            command=self.show_frame_eleve,
        )
        self.button_back.grid(row=1, column=0, padx=30, pady=30)

        # create prof frame
        self.frame_prof = customtkinter.CTkTabview(self, width=250)
        self.frame_prof.add("Créer un QCM")
        self.frame_prof.add("Créer un élève")
        self.frame_prof.add("Corriger un QCM")
        self.frame_prof.tab("Créer un QCM").grid_columnconfigure(0, weight=1)
        self.frame_prof.tab("Créer un élève").grid_columnconfigure(0, weight=1)
        self.frame_prof.tab("Corriger un QCM").grid_columnconfigure(0, weight=1)

        self.label_heading = customtkinter.CTkLabel(
            self.frame_prof.tab("Créer un QCM"),
            text="Créer un QCM",
            font=customtkinter.CTkFont(size=28, weight="bold"),
        )
        self.label_heading.grid(row=2, column=0, padx=30, pady=30)

        self.label_heading = customtkinter.CTkLabel(
            self.frame_prof.tab("Créer un élève"),
            text="Créer un élève",
            font=customtkinter.CTkFont(size=28, weight="bold"),
        )
        self.label_heading.grid(row=2, column=0, padx=30, pady=30)

        self.frame_form_create_student = customtkinter.CTkFrame(self.frame_prof.tab("Créer un élève"))
        self.frame_form_create_student.grid(row=3, column=0, padx=30, pady=15)

        self.label_heading = customtkinter.CTkLabel(
            self.frame_form_create_student,
            text="Login",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label_heading.grid(row=0, column=0, padx=30, pady=15)

        self.label_username = customtkinter.CTkLabel(
            self.frame_form_create_student,
            text="Nom d'utilisateur",
            font=customtkinter.CTkFont(size=20),
        )
        self.label_username.grid(row=1, column=0, sticky="w", padx=30, pady=(15, 0))

        self.entry_username_create_student = customtkinter.CTkEntry(
            self.frame_form_create_student,
            font=customtkinter.CTkFont(size=20),
            width=220,
        )
        self.entry_username_create_student.grid(row=2, column=0, padx=30)  # renumerate

        self.label_password = customtkinter.CTkLabel(
            self.frame_form_create_student,
            text="Mot de passe",
            font=customtkinter.CTkFont(size=20),
        )
        self.label_password.grid(row=3, column=0, sticky="w", padx=30, pady=(15, 0))

        self.entry_password_create_student = customtkinter.CTkEntry(
            self.frame_form_create_student,
            font=customtkinter.CTkFont(size=20),
            width=220,
            show="*",
        )
        self.entry_password_create_student.grid(row=4, column=0, padx=30)

        self.button_register = customtkinter.CTkButton(
            self.frame_form_create_student,
            text="Créer l'élève",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            command=self.register,
            width=220,
        )
        self.button_register.grid(row=5, column=0, padx=30, pady=(60, 15))

        self.label_heading = customtkinter.CTkLabel(
            self.frame_prof.tab("Corriger un QCM"),
            text="Corriger un QCM",
            font=customtkinter.CTkFont(size=28, weight="bold"),
        )
        self.label_heading.grid(row=2, column=0, padx=30, pady=30)

        # create login frame
        self.frame_login = customtkinter.CTkFrame(self)
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_rowconfigure(1, weight=1)

        self.frame_form = customtkinter.CTkFrame(self.frame_login)
        self.frame_form.grid(row=1, column=0, padx=30, pady=15)

        self.label_heading = customtkinter.CTkLabel(
            self.frame_form,
            text="Login",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label_heading.grid(row=0, column=0, padx=30, pady=15)

        self.label_username = customtkinter.CTkLabel(
            self.frame_form,
            text="Nom d'utilisateur",
            font=customtkinter.CTkFont(size=20),
        )
        self.label_username.grid(row=1, column=0, sticky="w", padx=30, pady=(15, 0))

        self.entry_username = customtkinter.CTkEntry(
            self.frame_form,
            font=customtkinter.CTkFont(size=20),
            width=220,
        )
        self.entry_username.grid(row=2, column=0, padx=30)  # renumerate

        self.label_password = customtkinter.CTkLabel(
            self.frame_form,
            text="Mot de passe",
            font=customtkinter.CTkFont(size=20),
        )
        self.label_password.grid(row=3, column=0, sticky="w", padx=30, pady=(15, 0))

        self.entry_password = customtkinter.CTkEntry(
            self.frame_form,
            font=customtkinter.CTkFont(size=20),
            width=220,
            show="*",
        )
        self.entry_password.grid(row=4, column=0, padx=30)

        self.button_login = customtkinter.CTkButton(
            self.frame_form,
            text="Login",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            command=self.login,
            width=220,
        )
        self.button_login.grid(row=5, column=0, padx=30, pady=(60, 15))

        self.button_back = customtkinter.CTkButton(
            self.frame_form,
            text="< Retour à l'accueil",
            font=customtkinter.CTkFont(size=10, weight="bold", underline=True),
            command=self.show_frame_main,
            fg_color="transparent",
            hover_color="gray85",
            text_color="gray16",
        )
        self.button_back.grid(row=6, column=0, padx=30, pady=(0, 15))

        # create top bar frame
        self.frame_topbar = customtkinter.CTkFrame(
            self, height=30, fg_color="transparent"
        )

        self.button_back = customtkinter.CTkButton(
            self.frame_topbar,
            text="< Retour",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            command=self.show_frame_main,
        )
        self.button_back.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    def show_frame_main(self):
        print("show main frame")
        # hide all frames
        self.frame_eleve.grid_forget()
        self.frame_prof.grid_forget()
        self.frame_login.grid_forget()
        self.frame_topbar.grid_forget()
        self.frame_qcm.grid_forget()
        # show main frame
        self.frame_main.grid(row=1, column=0, sticky="nsew", padx=50, pady=50)

    def show_frame_login(self):
        print("show login frame")
        # hide main frame
        self.frame_main.grid_forget()
        # show login frame
        self.frame_login.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        # show top bar frame
        # self.frame_topbar.grid(row=0, column=0, sticky="new", padx=20, pady=20)

    def show_frame_eleve(self):
        print("show eleve frame")
        # hide main frame
        self.frame_login.grid_forget()
        self.frame_qcm.grid_forget()
        # show eleve frame
        self.frame_eleve.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        # show top bar frame
        self.frame_topbar.grid(row=0, column=0, sticky="new", padx=20, pady=20)

    def show_frame_prof(self):
        print("show prof frame")
        # hide main frame
        self.frame_main.grid_forget()
        # show prof frame
        self.frame_prof.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        # show top bar frame
        self.frame_topbar.grid(row=0, column=0, sticky="new", padx=20, pady=20)

    def show_qcm_frame(self, qcm_id):
        print(f"show qcm frame {qcm_id}")
        self.frame_eleve.grid_forget()
        self.label_qcm_heading.configure(text=f"QCM {qcm_id}")
        self.frame_qcm.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_topbar.grid(row=0, column=0, sticky="new", padx=20, pady=20)

    def register(self):
        # Check if the username and password are not empty
        if self.entry_username_create_student.get() == "" or self.entry_password_create_student.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
            return
        
        print(self.entry_username_create_student.get(), self.entry_password_create_student.get())

        with open("accounts.txt", mode="r", encoding='utf-8') as file:
            accounts = file.readlines()
            for account in accounts:
                # extract username and password from the line
                username, password = account.split(":")
                # remove the \n from the password
                password = password.strip()
                # check if the username already exists
                if username == self.entry_username_create_student.get():
                    messagebox.showerror("Error", "Username already exists")
                    return

        with open("accounts.txt", mode="a", encoding='utf-8') as file:
            file.write(f"{self.entry_username_create_student.get()}:{self.entry_password_create_student.get()}\n")
            self.show_frame_eleve()


    def login(self):
        # Check if the username and password are not empty
        if self.entry_username.get() == "" or self.entry_password.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
            return

        with open("accounts.txt", mode="r", encoding='utf-8') as file:
            accounts = file.readlines()
            for account in accounts:
                # extract username and password from the line
                username, password = account.split(":")
                # remove the \n from the password
                password = password.strip()
                # check if the username and password are correct
                if username == self.entry_username.get() and password == self.entry_password.get():
                    self.show_frame_eleve()
                    return

            messagebox.showerror("Error", "Wrong username or password")


if __name__ == "__main__":
    app = App()
    app.mainloop()
