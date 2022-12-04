from cgitb import text
from doctest import master
from tkinter import *
from tkinter.tix import COLUMN
import customtkinter
from tkinter import filedialog
from threading import *
from tkinter.messagebox import showerror, showinfo
import pyttsx3


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.files = []

        self.title("Text To Speech")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # call .on_closing() when app gets closed


        # ============ create two frames ============

        # configure grid layout 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe", rowspan=2)

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20)

        self.frame_right_bottom = customtkinter.CTkFrame(master=self,
                                                        height=50)
        self.frame_right_bottom.grid(row=1, column=1, sticky="nswe", padx=20,pady=(10,0))

        self.frame_bottom = customtkinter.CTkFrame(master=self,
                                                     height=40)
        self.frame_bottom.grid(row=2, column=0,columnspan=2, sticky="nswe",pady=10,padx=10)
        # ============ frame_left ============

        # configure grid layout
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Text To Speech",
                                              text_font=("Roboto Medium", -20))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.listBtn = customtkinter.CTkButton(master=self.frame_left,
                                                text="Listen",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.buildThread)
        self.listBtn.grid(row=2, column=0, pady=5, padx=20)

        self.clearBtn = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=lambda:self.textBox.textbox.delete(1.0,END))
        self.clearBtn.grid(row=3, column=0, pady=5, padx=20)

        self.importBtn = customtkinter.CTkButton(master=self.frame_left,
                                                text="Import Text",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.import_file)
        self.importBtn.grid(row=4, column=0, pady=5, padx=20)

        

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Voice")
        self.label_mode.grid(row=10, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Male", "Female"],
                                                        )
        self.optionmenu_1.grid(row=11, column=0, pady=10, padx=20, sticky="w")


         # ============ frame_right ============

        # configure grid layout
        
        self.textBox = customtkinter.CTkTextbox(master=self.frame_right,
                                                width=App.WIDTH-270,
                                                height=App.HEIGHT-165,
                                                text_font=("Roboto Medium", -18),)
        self.textBox.grid(row=0, column=0, pady=20, padx=(20,0))

        self.scrollbar = customtkinter.CTkScrollbar(master=self.frame_right, command=self.textBox.yview,width=20,height=App.HEIGHT-300)
        self.scrollbar.grid(row=0, column=1, rowspan=4, sticky="ns",pady=20)
        self.textBox.configure(yscrollcommand=self.scrollbar.set)
        self.textBox.bind("<Configure>", lambda e: self.textBox.configure())

        

        # ============ frame_righy_bottom ============
        self.rate = customtkinter.CTkLabel(master=self.frame_right_bottom,
                                                text="Rate:")
        self.rate.grid(row=0, column=0, pady=5)

        self.slider = customtkinter.CTkSlider(master=self.frame_right_bottom,
                                            from_=100,
                                            to=180,
                                            )
        self.slider.set(130)
        self.slider.grid(row=0, column=2, pady=5)




        # ============ frame_bottom ============

        self.fName = customtkinter.CTkEntry(master=self.frame_bottom, placeholder_text="Output file name",width=App.WIDTH-300)

        self.fName.grid(row=0, column=0, rowspan=3, columnspan=2, pady=20, padx=20, sticky="w")

        self.button_5 = customtkinter.CTkButton(master=self.frame_bottom,
                                                border_width=2,
                                                text="Export!",
                                                command=self.save_audio)
        self.button_5.grid(row=0, column=2, columnspan=1, pady=20, padx=20, sticky="e")



    
    #functions
    def on_closing(self, event=0):
        self.destroy()

    def import_file(self):
        filePath = filedialog.askopenfilenames(title="Select File",
                                                filetypes=[("Text File","*.txt")])
        try:
            for filename in filePath:
                with open (filename, encoding = 'utf8') as f_obj:
                    contents = f_obj.read()
                self.textBox.textbox.delete('1.0', END)
                self.textBox.textbox.insert('end',contents)

        except Exception:
            showerror("Error","File cannot be open")

    def save_audio(self):
        engine = pyttsx3.init()
        audio_string = self.textBox.textbox.get(1.0,END)
        voices=engine.getProperty('voices')
        engine.setProperty('rate', self.slider.get())

        folder = filedialog.askdirectory()
        voiceType = self.optionmenu_1.get()
        if ".mp30" in self.fName.get():
            fileName = folder + '/' + self.fName.get()
        else:
            fileName = folder + '/' + self.fName.get()+".mp3"

        if voiceType == 'Male':
            engine.setProperty('voice', voices[0].id)
        else:
            engine.setProperty('voice', voices[1].id)

        engine.save_to_file(audio_string,fileName)
        showinfo("Done","File generated successfully!")
        
        engine.runAndWait()
        engine.stop()

    def speak(self):

        engine = pyttsx3.init()
        audio_string = self.textBox.textbox.get(1.0,END)
        voices=engine.getProperty('voices')
        engine.setProperty('rate',self.slider.get())

        voiceType = self.optionmenu_1.get()
        if voiceType == 'Male':
            engine.setProperty('voice', voices[0].id)
            
        else:
            engine.setProperty('voice', voices[1].id)
            
        engine.say(audio_string)
        engine.runAndWait()
        engine.stop()

    def buildThread(self):
        t1=Thread(target=self.speak)
        t1.start()

if __name__ == "__main__":
    app = App()
    app.resizable(False,False)
    app.mainloop()
