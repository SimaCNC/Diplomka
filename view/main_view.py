from tkinter import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.Piezo_model import Piezo_model
    from model.MCU_model import MCU_model
    from controller.main_controller import MainController
    
#-----------------------------------------------------     
#KORENOVE OKNO - VYTVORENI INSTANCE TK V ATRIBUTU ROOT    
#----------------------------------------------------- 

class RootGUI():
    def __init__(self):
        self.root : Tk = Tk()
        
        self.root.iconbitmap('icon/logo_uprava2.ico')
        self.root.title("Kalibrace snímače malých posunutí")
        self.root.geometry("1250x800")
        self.root.config(bg="white")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.container = Frame(self.root)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {} #ukladani jednotlivych pohledu
        
        #zavreni okna
        self.root.protocol("WM_DELETE_WINDOW", self.window_exit)
        
        #vytvoreni menu
        self.menu = Menu(self.root)
        self.menu.add_command(label="Připojení", command=lambda: self.show_frame("main"))      
        self.menu.add_command(label="Kalibrace", command=lambda: self.show_frame("kalibrace"))
        self.menu.add_command(label="Offline", command=lambda : self.show_frame("offline"))
        self.menu.add_command(label="Nápověda", command=lambda : self.show_frame("napoveda"))
        self.menu.add_command(label="Konec", command=self.window_exit)
        
        self.root.config(menu=self.menu)
        
    def add_frame(self, name, frame_class, *args):
        frame : Frame = frame_class(self.container, *args)
        self.frames[name] = frame 
        frame.grid(row = 0, column = 0, sticky = "nsew")
            
    def show_frame(self, name):
        if name in self.frames:
            self.frames[name].tkraise()
        else:
            print(f"[frame] Frame '{name}' NEEXISTUJE")
        
    def window_exit(self):
        # zavrit = messagebox.askyesno("Ukončení aplikace", "Upravdu si přejete ukončit aplikaci?")
        # if zavrit:
        #     print("Zavirani okna a vypnuti aplikace")
        #     self.root.destroy()
        self.root.destroy()
        print("Zavirani okna a vypnuti aplikace")
        
#-------------------------------------------------------------------------        
#PRVNI OKNO APLIKACE (main) - PRIPOJENI A OVLADANI SUBSYSTEMU PIEZA A MCU
#SPRAVOVANI PRIPOJENI K SERIOVYM KOMUNIKACIM PRO MCU A PIEZOPOHONY    
#------------------------------------------------------------------------- 

class MainPage(Frame):
    def __init__(self, parent, controller : 'MainController', piezo_model, mcu_model):
        super().__init__(parent)
        self.config(bg="white")

        self.com_gui : LabelFrame = ComGUI(self, controller, piezo_model, mcu_model)
        self.com_gui.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        
        self.piezo_gui : LabelFrame = PiezoGUI(self, controller, piezo_model)
        self.piezo_gui.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        
        self.mcu_gui : LabelFrame = McuGUI(self, controller, mcu_model)
        self.mcu_gui.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        
        self.controler = controller
        self.controler.set_main_page(self)
        
class ComGUI(LabelFrame):
    def __init__(self, parent, controller : 'MainController', piezo_model : 'Piezo_model', mcu_model : 'MCU_model'):
        super().__init__(parent, text="COM manažer připojení", padx=5, pady=5, bg="white",fg="black",bd=5, relief="groove")
        self.controller = controller
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        
        #LEVE OKNA - COM PRIPOJENI 
        self.frame_piezo = LabelFrame(self, text="Piezpohony", padx=5, pady=5, bg="white")
        self.frame_MCU = LabelFrame(self, text="MCU", padx=5, pady=5, bg="white")
        
        #LEVE OKNA - PRVKY
        self.label_com_piezo = Label(self.frame_piezo, text="Dostupné porty:", bg="white", width=15, anchor="w")
        self.label_bd_piezo = Label(self.frame_piezo, text="Baud rate:", bg="white", width=15, anchor="w")
        self.btn_refresh_piezo = Button(self.frame_piezo, text="Obnovit", width=10, command=self.com_refresh_piezo)
        self.btn_connect_piezo = Button(self.frame_piezo, text="Připojit", width=10, state="disabled", command=self.controller.M_serial_connect_piezo)
        self.Com_option_piezo()
        self.Baud_option_piezo()
        
        self.label_com_MCU = Label(self.frame_MCU, text="Dostupné porty: ", bg="white", width=15, anchor="w")
        self.label_bd_MCU = Label(self.frame_MCU, text="Baud rate:", bg="white", width=15, anchor="w")
        self.btn_refresh_MCU = Button(self.frame_MCU, text="Obnovit", width=10, command=self.com_refresh_MCU)
        self.btn_connect_MCU = Button(self.frame_MCU, text="Připojit", width=10, state="disabled", command=self.controller.M_serial_connect_MCU)
        self.Com_option_MCU()
        self.Baud_option_MCU()
        
        self.publish()
        #LEVE OKNA - COM PRIPOJENI
        
    def publish(self):
        #LEVE OKNA - COM PRIPOJENI
        # self.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.frame_piezo.grid(row=0, column=0, padx=5, pady=5)
        self.frame_MCU.grid(row=1, column=0, padx=5, pady=5)
        
        #LEVE OKNA PRVKY
        self.label_com_piezo.grid(row=0, column=0, padx=5, pady=5)
        self.label_bd_piezo.grid(row=1, column=0, padx=5, pady=5)
        self.btn_refresh_piezo.grid(row=0, column=2, padx=5, pady=5)
        self.btn_connect_piezo.grid(row=1, column=2, padx=5, pady=5)
        self.drop_com_piezo.grid(row=0, column=1, padx=5, pady=5)
        self.drop_bd_piezo.grid(row=1, column=1, padx=5, pady=5)
        
        self.label_com_MCU.grid(row=0, column=0, padx=5, pady=5)
        self.label_bd_MCU.grid(row=1, column=0, padx=5, pady=5)
        self.btn_refresh_MCU.grid(row=0, column=2, padx=5, pady=5)
        self.btn_connect_MCU.grid(row=1, column=2, padx=5, pady=5)
        self.drop_com_MCU.grid(row=0, column=1, padx=5, pady=5)
        self.drop_bd_MCU.grid(row=1, column=1, padx=5, pady=5)
    
    #LEVE OKNA LOGIKA - COM PRIPOJENI  
    def com_refresh_piezo(self):
        self.drop_com_piezo.destroy()
        self.Com_option_piezo()
        self.drop_com_piezo.grid(row=0, column=1, padx=5, pady=5)
        self.connect_ctrl_piezo("reset")
    
    def com_refresh_MCU(self):
        self.drop_com_MCU.destroy()
        self.Com_option_MCU()
        self.drop_com_MCU.grid(row=0, column=1, padx=5, pady=5)
        self.connect_ctrl_MCU("reset")
        
    def Com_option_piezo(self):
        self.piezo_model.piezo_serial.getCOMlist()
        self.vybrany_com_piezo = StringVar()
        if self.piezo_model.piezo_serial.com_list:
            self.vybrany_com_piezo.set(self.piezo_model.piezo_serial.com_list[0])
        else:
            self.vybrany_com_piezo.set("-")
        self.drop_com_piezo = OptionMenu(self.frame_piezo, self.vybrany_com_piezo, *self.piezo_model.piezo_serial.com_list, command=self.connect_ctrl_piezo)
        self.drop_com_piezo.config(width=10)
        
    def Baud_option_piezo(self):
        self.vybrany_bd_piezo = StringVar()
        bds = ["-", "115200"]
        self.vybrany_bd_piezo.set(bds[0])
        self.drop_bd_piezo = OptionMenu(self.frame_piezo, self.vybrany_bd_piezo, *bds, command=self.connect_ctrl_piezo)
        self.drop_bd_piezo.config(width=10)

    def Com_option_MCU(self):
        self.mcu_model.mcu_serial.getCOMlist()
        self.vybrany_com_MCU = StringVar()
        self.vybrany_com_MCU.set(self.mcu_model.mcu_serial.com_list[0])
        self.drop_com_MCU = OptionMenu(self.frame_MCU, self.vybrany_com_MCU, *self.mcu_model.mcu_serial.com_list, command=self.connect_ctrl_MCU)
        self.drop_com_MCU.config(width=10)
        
    def Baud_option_MCU(self):
        self.vybrany_bd_MCU = StringVar()
        bds = ["-", "9600", "115200"]
        self.vybrany_bd_MCU.set(bds[0])
        self.drop_bd_MCU = OptionMenu(self.frame_MCU, self.vybrany_bd_MCU, *bds, command=self.connect_ctrl_MCU)
        self.drop_bd_MCU.config(width=10)
         
    def connect_ctrl_piezo(self, other):
        if "-" in self.vybrany_com_piezo.get() or "-" in self.vybrany_bd_piezo.get():
            self.btn_connect_piezo["state"] = "disable"
            print("Piezopohony: nutno dovytvorit konfiguraci pripojeni")
        else:
            self.btn_connect_piezo["state"] = "active"
            print("Pripojeni k piezopohonum aktivni")
            
    def connect_ctrl_MCU(self, other):
        if "-" in self.vybrany_com_MCU.get() or "-" in self.vybrany_bd_MCU.get():
            self.btn_connect_MCU["state"] = "disable"
            print("MCU: nutno dovytvorit konfiguraci pripojeni")
        else:
            self.btn_connect_MCU["state"] = "active"
            print("Pripojeni k MCU aktivni")    
 
    
#SPRAVOVANI PRIPOJENI K SERIOVYM KOMUNIKACIM PRO MCU A PIEZOPOHONY - LEVE HORNI OKNO APLIKACE, trida ComGui()         
class PiezoGUI(LabelFrame):
    def __init__(self, parent, controller : 'MainController' ,piezo_model : 'Piezo_model'):
        super().__init__(parent, text="Piezopohony", padx=5, pady=5, bg="white", relief="groove",bd=5)
        self.controller = controller
        self.piezo_model = piezo_model
        
        
        #ovladani
        self.frame_piezo_ovladani = LabelFrame(self,text="Ovládání" ,padx=5, pady=5, bg="white")
        self.frame_piezo_ovladani.grid(row=0, column=0, padx=5, pady=5, sticky="NW") 
        self.frame_piezo_ovladani_leve = Frame(self.frame_piezo_ovladani,padx=5, pady=5, bg="white")
        self.frame_piezo_ovladani_leve.grid(row=0, column=0, padx=5, pady=5, sticky="NW") 
        self.frame_piezo_ovladani_prave = Frame(self.frame_piezo_ovladani,padx=5, pady=5, bg="white")
        self.frame_piezo_ovladani_prave.grid(row=0, column=1, padx=5, pady=5, sticky="NW") 
        
        self.label_index_piezo = Label(self.frame_piezo_ovladani_leve, text="Home pozice:", bg="white", width=20, anchor="w")
        self.label_index_piezo.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.BTN_index_piezo = Button(self.frame_piezo_ovladani_leve, text="HOME", width=10,state="disabled" ,command= self.controller.M_C_Index)#SERIAL - POSLAT INDEX - PRIJEM
        self.BTN_index_piezo.grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        
        
    def publish_PiezoGUI_home_done(self):
        #ovladani
        self.label_piezo_precist_polohu = Label(self.frame_piezo_ovladani_leve, text="Přečíst aktuální polohu:", bg= "white", width=20, anchor="w")
        self.BTN_piezo_precist_polohu = Button(self.frame_piezo_ovladani_leve, text="POLOHA", width=10, command=self.controller.M_C_precti_polohu)
        self.label_reference_piezo = Label(self.frame_piezo_ovladani_leve, text="Nastavit referenční pozici:", bg="white", width=20, anchor="w")
        self.BTN_reference_piezo = Button(self.frame_piezo_ovladani_leve, text="REFERENCE", width=10, command= self.controller.M_C_nastav_referenci)#SERIAL - POSLAT INDEX - PRIJEM
        self.label_rychlost_piezo = Label(self.frame_piezo_ovladani_leve, text="Nastavit rychlost posunu:", bg="white", width=20, anchor="w")
        self.vybrana_rychlost_piezo = StringVar()
        rychlosti = ["10", "100", "500", "1000", "2000", "3000", "4000", "5000", "6000", "8000"]
        self.vybrana_rychlost_piezo.set(rychlosti[6])
        self.drop_rychlost_piezo = OptionMenu(self.frame_piezo_ovladani_leve, self.vybrana_rychlost_piezo, *rychlosti, command=self.piezo_model.nastav_rychlost)
        
        #ovladani - pohyb
        self.label_piezo_pohyb = Label(self.frame_piezo_ovladani_prave, text="Nastavit velikost pohybu v μm:", bg="white", width=25, anchor="w")
        self.entry_piezo_pohyb = Entry(self.frame_piezo_ovladani_prave, width=10)
        self.entry_piezo_pohyb.bind("<Return>", lambda _ : self.controller.M_C_nastav_pohyb_piezo(self.entry_piezo_pohyb.get()))
        self.label_piezo_pohyb_nastavene = Label(self.frame_piezo_ovladani_prave, text="Nastavená velikost pohybu v μm:", bg="white", width=25, anchor="w")
        self.label_piezo_pohyb_nastavene_text = Label(self.frame_piezo_ovladani_prave, text=self.piezo_model.velikost_pohybu, bg="white", width=5, anchor="w")
        self.frame_piezo_pohyb = Frame(self.frame_piezo_ovladani_prave, padx=5, pady=5, bg="white")
        self.BTN_piezo_pohyb_xP = Button(self.frame_piezo_pohyb, text="X+", width=5, command=lambda: self.controller.M_C_pohyb_piezo("x"))
        self.BTN_piezo_pohyb_xM = Button(self.frame_piezo_pohyb, text="X-", width=5, command=lambda: self.controller.M_C_pohyb_piezo("x-"))
        self.BTN_piezo_pohyb_yP = Button(self.frame_piezo_pohyb, text="Y+", width=5, command=lambda: self.controller.M_C_pohyb_piezo("y"))
        self.BTN_piezo_pohyb_yM = Button(self.frame_piezo_pohyb, text="Y-", width=5, command=lambda: self.controller.M_C_pohyb_piezo("y-"))
        self.BTN_piezo_pohyb_zP = Button(self.frame_piezo_pohyb, text="Z+", width=5, command=lambda: self.controller.M_C_pohyb_piezo("z"))
        self.BTN_piezo_pohyb_zM = Button(self.frame_piezo_pohyb, text="Z-", width=5, command=lambda: self.controller.M_C_pohyb_piezo("z-"))
        
        #pozice
        self.frame_piezo_pozice = LabelFrame(self,text="Pozice", padx=5, pady=5, bg="white")
        self.label_pozice_home_piezo = Label(self.frame_piezo_pozice, text="Pozice od home:", padx=5, pady=5, bg="white", width=15,)
        self.label_pozice_homeX_piezo = Label(self.frame_piezo_pozice, text="Xh:", padx=5, pady=5, bg="white", width=10)
        self.label_pozice_homeY_piezo = Label(self.frame_piezo_pozice, text="Yh:", padx=5, pady=5, bg="white", width=10)
        self.label_pozice_homeZ_piezo = Label(self.frame_piezo_pozice, text="Zh:", padx=5, pady=5, bg="white", width=10)
        self.label_pozice_reference_piezo = Label(self.frame_piezo_pozice, text="Pozice od reference:", padx=5, pady=5, bg="white", width=15,)
        self.label_pozice_referenceX_piezo = Label(self.frame_piezo_pozice, text="Xr:", padx=5, pady=5, bg="white", width=10,)
        self.label_pozice_referenceY_piezo = Label(self.frame_piezo_pozice, text="Yr:", padx=5, pady=5, bg="white", width=10,)
        self.label_pozice_referenceZ_piezo = Label(self.frame_piezo_pozice, text="Zr:", padx=5, pady=5, bg="white", width=10,)
        
        #prikaz
        self.frame_piezo_prikaz = LabelFrame(self,text="Příkaz", padx=5, pady=5, bg="white")
        self.label_piezo_prikaz = Label(self.frame_piezo_prikaz, text="Příkaz k odeslání:", bg="white", width=20, anchor="w")
        self.entry_piezo_prikaz = Entry(self.frame_piezo_prikaz, width=33,)
        self.entry_piezo_prikaz.bind("<Return>", lambda _ : self.controller.M_C_send_msg_piezo(self.entry_piezo_prikaz.get()))
        self.BTN_piezo_prikaz = Button(self.frame_piezo_prikaz, text="POSLAT", width=10, command= lambda: self.controller.M_C_send_msg_piezo(self.entry_piezo_prikaz.get()))
        self.label_piezo_odpoved = Label(self.frame_piezo_prikaz, text="Odpověď piezopohony:", bg="white", width=20, anchor="w")
        self.text_piezo_odpoved = Text(self.frame_piezo_prikaz, width=25, height=1)
        self.BTN_piezo_odpoved = Button(self.frame_piezo_prikaz, text="REFRESH", width=10, command=self.controller.M_C_odpoved_piezo_refresh)
        
        #zavolani
        self.publish()
        
    def publish(self):
        #ovladani
        self.label_reference_piezo.grid(row=1, column=0, padx=5, pady=5, sticky="NW")
        self.BTN_reference_piezo.grid(row=1, column=1, padx=5, pady=5, sticky="NW")
        self.label_piezo_precist_polohu.grid(row=2, column=0, padx=5, pady=5, sticky="NW")
        self.BTN_piezo_precist_polohu.grid(row=2, column=1, padx=5, pady=5, sticky="NW")
        self.label_rychlost_piezo.grid(row=3, column=0, padx=5, pady=5, sticky="NW")
        self.drop_rychlost_piezo.grid(row=3, column=1, padx=5, pady=5, sticky="NW")
        self.drop_rychlost_piezo.config(width=6, padx=5, pady=5)
        
        #ovladani - pohyb
        self.label_piezo_pohyb.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.entry_piezo_pohyb.grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.label_piezo_pohyb_nastavene.grid(row=1, column=0, padx=5, pady=5, sticky="NW")
        self.label_piezo_pohyb_nastavene_text.grid(row=1, column=1, padx=5, pady=5, sticky="NW")
        self.frame_piezo_pohyb.grid(row=2, column=0, sticky="NW")
        self.BTN_piezo_pohyb_xP.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.BTN_piezo_pohyb_xM.grid(row=1, column=0, padx=5, pady=5, sticky="NW")
        self.BTN_piezo_pohyb_yP.grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.BTN_piezo_pohyb_yM.grid(row=1, column=1, padx=5, pady=5, sticky="NW")
        self.BTN_piezo_pohyb_zP.grid(row=0, column=2, padx=5, pady=5, sticky="NW")
        self.BTN_piezo_pohyb_zM.grid(row=1, column=2, padx=5, pady=5, sticky="NW")
        
        #pozice
        self.frame_piezo_pozice.grid(row=1, column=0, padx=5, pady=10, sticky="NW")
        self.label_pozice_home_piezo.grid(row=0, column=0)
        self.label_pozice_homeX_piezo.grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.label_pozice_homeY_piezo.grid(row=1, column=1, padx=5, pady=5, sticky="NW")
        self.label_pozice_homeZ_piezo.grid(row=2, column=1, padx=5, pady=5, sticky="NW")
        self.label_pozice_reference_piezo.grid(row=0, column=2)
        self.label_pozice_referenceX_piezo.grid(row=0, column=3, padx=5, pady=5, sticky="NW")
        self.label_pozice_referenceY_piezo.grid(row=1, column=3, padx=5, pady=5, sticky="NW")
        self.label_pozice_referenceZ_piezo.grid(row=2, column=3, padx=5, pady=5, sticky="NW")
        
        #prikaz
        self.frame_piezo_prikaz.grid(row=2, column=0, padx=5, pady=10, sticky="NW")
        self.label_piezo_prikaz.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.entry_piezo_prikaz.grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.BTN_piezo_prikaz.grid(row=0, column=2, padx=5, pady=5, sticky="NW")
        self.label_piezo_odpoved.grid(row=1, column=0, padx=5, pady=5, sticky="NW")
        self.text_piezo_odpoved.grid(row=1, column=1, padx=5, pady=5, sticky="NW")
        self.text_piezo_odpoved.config(state="disabled")
        self.BTN_piezo_odpoved.grid(row=1, column=2, padx=5, pady=5, sticky="NW")
        
    def PiezoGUIClose(self):
        self.controller.piezo = False
        self.disable_children(self)
    
    def disable_children(self, widget):
        if isinstance(widget, (Button, Entry)):
            widget.config(state="disabled")   
        elif isinstance(widget, OptionMenu):
            widget.config(state="disabled")
        for child in widget.winfo_children():
                self.disable_children(child)
        
    def PiezoGUIOpen(self):
        self.controller.piezo = True
        self.enable_children(self)
        
    def enable_children(self, widget):     
        if isinstance(widget, (Button, Entry)):
            widget.config(state="normal")     
        elif isinstance(widget, OptionMenu):
            widget.config(state="normal")       
        for child in widget.winfo_children():
            self.enable_children(child)     
        
    def disable_piezo_buttons(self):
        self.BTN_piezo_pohyb_xP.config(state="disabled")
        self.BTN_piezo_pohyb_xM.config(state="disabled")
        self.BTN_piezo_pohyb_yP.config(state="disabled")
        self.BTN_piezo_pohyb_yM.config(state="disabled")
        self.BTN_piezo_pohyb_zP.config(state="disabled")
        self.BTN_piezo_pohyb_zM.config(state="disabled")
        self.BTN_piezo_prikaz.config(state="disabled")
        
    def enable_piezo_buttons(self):
        self.BTN_piezo_pohyb_xP.config(state="normal")
        self.BTN_piezo_pohyb_xM.config(state="normal")
        self.BTN_piezo_pohyb_yP.config(state="normal")
        self.BTN_piezo_pohyb_yM.config(state="normal")
        self.BTN_piezo_pohyb_zP.config(state="normal")
        self.BTN_piezo_pohyb_zM.config(state="normal")
        self.BTN_piezo_prikaz.config(state="normal")
        
class McuGUI(LabelFrame):
    def __init__(self, parent, controller : 'MainController' ,mcu_model : 'MCU_model'):
        super().__init__(parent, text="MCU", padx=5, pady=5, bg="white", relief="groove",bd=5)
        self.controller = controller
        self.mcu_model = mcu_model

        #Ovladani
        self.frame_mcu_prikaz = LabelFrame(self,text="Příkaz" ,padx=5, pady=5, bg="white")
        self.frame_mcu_prikaz.grid(row=0, column=0, padx=5, pady=5, sticky="NW") 
        
        self.label_mcu_odeslat = Label(self.frame_mcu_prikaz, text="Zpráva k odeslání: ", bg="white", width=15, anchor="w")
        self.entry_mcu_prikaz = Entry(self.frame_mcu_prikaz, width=33)
        self.entry_mcu_prikaz.bind("<Return>", lambda _ : self.controller.M_C_send_msg_MCU(self.entry_mcu_prikaz.get()))
        self.BTN_mcu_prikaz = Button(self.frame_mcu_prikaz, text="POSLAT", width=10, command= lambda: self.controller.M_C_send_msg_MCU(self.entry_mcu_prikaz.get()))
        
        self.label_mcu_odpoved = Label(self.frame_mcu_prikaz, text="Odpověď MCU:", bg="white", width=20, anchor="w")
        self.text_MCU_odpoved = Text(self.frame_mcu_prikaz, width=25, height=1)
        self.BTN_mcu_odpoved = Button(self.frame_mcu_prikaz, text="REFRESH", width=10, command= self.controller.M_C_odpoved_MCU_refresh)
        
        self.publish_gui_MCU()
        self.McuGUIClose()
        
    def publish_gui_MCU(self):
        self.label_mcu_odeslat.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.entry_mcu_prikaz.grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        self.BTN_mcu_prikaz.grid(row=0, column=2, padx=5, pady=5, sticky="NW")   
        self.label_mcu_odpoved.grid(row=1, column=0, padx=5, pady=5, sticky="NW") 
        self.text_MCU_odpoved.grid(row=1, column=1, padx=5, pady=5, sticky="NW")
        self.text_MCU_odpoved.config(state="disabled")
        self.BTN_mcu_odpoved.grid(row=1, column=2, padx=5, pady=5, sticky="NW")    
            
    def McuGUIClose(self):
        self.controller.mcu = False
        self.disable_children(self)
    
    def disable_children(self, widget):
        if isinstance(widget, (Button, Entry)):
            widget.config(state="disabled")   
        elif isinstance(widget, OptionMenu):
            widget.config(state="disabled")
        for child in widget.winfo_children():
                self.disable_children(child)
        
    def McuGUIOpen(self):
        self.controller.mcu = True
        self.enable_children(self)
        
    def enable_children(self, widget):     
        if isinstance(widget, (Button, Entry)):
            widget.config(state="normal")     
        elif isinstance(widget, OptionMenu):
            widget.config(state="normal")       
        for child in widget.winfo_children():
            self.enable_children(child)
               
#------------------------------        
#KALIBRACE PAGE    
#------------------------------           
class KalibracePage(Frame):
    def __init__(self, parent, controller : 'MainController', piezo_model, mcu_model):
        super().__init__(parent)
        self.config(bg="white")
        
        self.stav_gui : LabelFrame = StavGUI(self, controller, piezo_model, mcu_model)
        self.stav_gui.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
                
        self.protokol_gui : LabelFrame = Typ_protokolGUI(self, controller, piezo_model, mcu_model)
        self.protokol_gui.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        
        self.kalibrace_gui : LabelFrame = KalibraceGUI(self, controller, piezo_model, mcu_model, )
        self.kalibrace_gui.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        
        self.controler = controller
        self.controler.set_kalibrace_page(self)

#Frame STAV
class StavGUI(LabelFrame):
    def __init__(self, parent, controller : 'MainController', piezo_model : 'Piezo_model', mcu_model : 'MCU_model'):
        super().__init__(parent, text="Stav", padx=5, pady=5, bg="white",fg="black",bd=5, relief="groove")
        self.controller = controller
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        
        self.label_stav_piezo = Label(self, text="Připojení piezo :", bg="white", width=20, anchor="w")
        self.label_stav_piezo_show = Label(self, text="NEAKTIVNÍ", fg="red", bg="white", width=20, anchor="w")
        self.label_stav_MCU = Label(self, text="Připojení MCU :", bg="white", width=20, anchor="w")
        self.label_stav_MCU_show = Label(self, text="NEAKTIVNÍ", fg="red", bg="white", width=20, anchor="w")
        self.label_teplota = Label(self, text="Teplota okolí senzoru :", bg="white", width=20, anchor="w")
        self.label_teplota_show = Label(self, text="N/A", fg="red", bg="white", width=20, anchor="w")
        
        
        self.label_aktualizace = Label(self, text="Aktualizace :", bg="white", width=20, anchor="w")
        self.BTN_aktualizace = Button(self, text="Aktualizace", width=20, state="active", command=controller.M_C_aktualizace_stav)
        self.publish()
        
    def publish(self):
        self.label_stav_piezo.grid(row=0, column=0, padx=5, pady=5)
        self.label_stav_piezo_show.grid(row=0, column=1, padx=5, pady=5)
        self.label_stav_MCU.grid(row=1, column=0, padx=5, pady=5)
        self.label_stav_MCU_show.grid(row=1, column=1, padx=5, pady=5)
        self.label_teplota.grid(row=2, column=0, padx=5, pady=5)
        self.label_teplota_show.grid(row=2, column=1, padx=5, pady=5)
        
        self.label_aktualizace.grid(row=3, column=0, padx=5, pady=5)
        self.BTN_aktualizace.grid(row=3, column=1, padx=5, pady=5)

#Frame ZPRACOVANI DAT
class Typ_protokolGUI(LabelFrame):
    def __init__(self, parent, controller : 'MainController', piezo_model : 'Piezo_model', mcu_model : 'MCU_model'):
        super().__init__(parent, text="Zpracování dat", padx=5, pady=5, bg="white", fg="black", bd=5, relief="groove")
        self.controller = controller
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        
        self.vybrane_var = StringVar(self, value="1")
        #   volby = {"A/D převodník" : "1",
                    #"Pulzy" : "2",
                    #"Protokol" : "3"}
        self.RB_AD = Radiobutton(self, text="A/D převodník: 0...3,3V", variable=self.vybrane_var, value="1",bg="white" ,command=None, width=20, anchor="w")
        self.RB_pulzy = Radiobutton(self, text="Pulzy: 0...250kHz", variable=self.vybrane_var, value="2",bg="white" ,command=None, width=20, anchor="w")
        self.RB_protokol = Radiobutton(self, text="Protokol (viz. nápověda)", variable=self.vybrane_var, value="3",bg="white" ,command=None, width=20, anchor="w")   
            
        self.publish()
        
    def publish(self):
        self.RB_AD.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.RB_pulzy.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.RB_protokol.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

#Frame KALIBRACE
class KalibraceGUI(LabelFrame):
    def __init__(self, parent, controller : 'MainController', piezo_model : 'Piezo_model', mcu_model : 'MCU_model'):
        super().__init__(parent, text="Kalibrace", padx=5, pady=5, bg="white",fg="black",bd=5, relief="groove")
        self.controller = controller
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        
        self.label_slozka = Label(self, text="Pracovní složka :", bg="white", width=20, anchor="w")
        self.label_metoda = Label(self, text="Metoda zpracování :", bg="white", width=20, anchor="w")
        self.label_krok = Label(self, text="Délka kroku :", bg="white", width=20, anchor="w")
        
        self.label_regulace = Label(self, text="Regulace teploty :", bg="white", width=20, anchor="w")
        self.regulace_var = StringVar(self, value="1")
        self.RB_regulace_teplota = Radiobutton(self, text="Regulace teplota", variable=self.regulace_var, value="0", bg="white", command=None, width=20, anchor="w")
        self.label_odhad_cas = Label(self, text="Odhadovaný čas kalibrace :", bg="white", width=20, anchor="w")
        self.label_kalibraceStart = Label(self, text="Start kalibrace :", bg="white", width=20, anchor="w")
        
        self.publish()
        
    def publish(self):
        self.label_slozka.grid(row=0, column=0, padx=5, pady=5)
        self.label_metoda.grid(row=1, column=0, padx=5, pady=5)
        self.label_krok.grid(row=2, column=0, padx=5, pady=5)
        
        self.label_regulace.grid(row=3, column=0, padx=5, pady=5)
        self.RB_regulace_teplota.grid(row=3, column=1, padx=5, pady=5)
        self.label_odhad_cas.grid(row=4, column=0, padx=5, pady=5)
        self.label_kalibraceStart.grid(row=5, column=0, padx=5, pady=5)

if __name__ == "__main__":
    print("TOTO NENI HLAVNI APLIKACE")
    print("HLAVNI APLIKACE JE V SOUBORU main.py")
