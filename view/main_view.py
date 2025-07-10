from tkinter import *
from controller.main_controller import MainController
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from model.Piezo_model import Piezo_model
    from model.MCU_model import MCU_model

class RootGUI():
    
    def __init__(self):
        self.root : Tk = Tk()
        
        self.root.iconbitmap('icon/logo_uprava2.ico')
        self.root.title("Kalibrace snímače malých posunutí")
        self.root.minsize(375, 290)
        self.root.geometry("375x290")
        self.root.config(bg="white")
        
        menu = Menu(self.root)
        self.root.config(menu=menu)
        
        #Hlavni menu
        def hlavni_menu_gui():
            pass
        
        hlavni_menu = Menu(menu)
        
        menu.add_cascade(label="Připojení", menu=hlavni_menu, command=hlavni_menu_gui)
        
        
        #Kalibrace menu
        def kalibrace_napoveda():
            pass
        
        def kalibrace_kalibrovat():
            pass
        
        kalibrace_menu = Menu(menu)
        
        menu.add_cascade(label="Kalibrace", menu=kalibrace_menu)
        kalibrace_menu.add_command(label="Nápověda", command=kalibrace_napoveda)
        kalibrace_menu.add_command(label="Kalibrovat", command=kalibrace_kalibrovat)
        
        
        #zavreni okna
        self.root.protocol("WM_DELETE_WINDOW", self.window_exit)
    
    def window_exit(self):
        # zavrit = messagebox.askyesno("Ukončení aplikace", "Upravdu si přejete ukončit aplikaci?")
        # if zavrit:
        #     print("Zavirani okna a vypnuti aplikace")
        #     self.root.destroy()
        self.root.destroy()
        print("Zavirani okna a vypnuti aplikace")
        
       
        
#SPRAVOVANI PRIPOJENI K SERIOVYM KOMUNIKACIM PRO MCU A PIEZOPOHONY - LEVE HORNI OKNO APLIKACE, trida ComGui()     
class ComGUI():
    def __init__(self, root : 'Tk', controller : 'MainController', piezo_model : 'Piezo_model', mcu_model : 'MCU_model'):
        self.root = root
        self.controller = controller
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        self.controller.window_num = 1
        
        #LEVE OKNA - COM PRIPOJENI 
        self.frame_left = LabelFrame(self.root, text="COM manažer připojení", padx=5, pady=5, bg="white",fg="black",bd=5, relief="groove")
        self.frame_piezo = LabelFrame(self.frame_left, text="Piezpohony", padx=5, pady=5, bg="white")
        self.frame_MCU = LabelFrame(self.frame_left, text="MCU", padx=5, pady=5, bg="white")
        
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
        self.frame_left.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
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
        #LEVE OKNA - COM PRIPOJENI
    
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
        self.vybrany_com_piezo.set(self.piezo_model.piezo_serial.com_list[0])
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
 
    #LEVE OKNA LOGIKA - COM PRIPOJENI
    
#SPRAVOVANI PRIPOJENI K SERIOVYM KOMUNIKACIM PRO MCU A PIEZOPOHONY - LEVE HORNI OKNO APLIKACE, trida ComGui()     
    
class PiezoGUI():
    def __init__(self, root: 'Tk', controller : 'MainController' ,piezo_model : 'Piezo_model'):
        self.root = root   
        self.controller = controller
        self.piezo_model = piezo_model
        self.controller.piezo = True
        
        self.frame_piezo_gui = LabelFrame(self.root, text="Piezopohony", padx=5, pady=5, bg="white", relief="groove",bd=5)
        self.frame_piezo_gui.grid(row=0, column=1, padx=5, pady=5, sticky="NW")
        
        if self.controller.mcu is False:
            self.root.geometry("1000x600")        
            self.root.minsize(1000, 600)
        else:
            self.root.geometry("1500x800")
            self.root.minsize(1500, 800)
        #ovladani
        self.frame_piezo_ovladani = LabelFrame(self.frame_piezo_gui,text="Ovládání" ,padx=5, pady=5, bg="white")
        self.frame_piezo_ovladani.grid(row=0, column=0, padx=5, pady=5, sticky="NW") 
        self.frame_piezo_ovladani_leve = Frame(self.frame_piezo_ovladani,padx=5, pady=5, bg="white")
        self.frame_piezo_ovladani_leve.grid(row=0, column=0, padx=5, pady=5, sticky="NW") 
        self.frame_piezo_ovladani_prave = Frame(self.frame_piezo_ovladani,padx=5, pady=5, bg="white")
        self.frame_piezo_ovladani_prave.grid(row=0, column=1, padx=5, pady=5, sticky="NW") 
        
        self.label_index_piezo = Label(self.frame_piezo_ovladani_leve, text="Home pozice:", bg="white", width=20, anchor="w")
        self.label_index_piezo.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.BTN_index_piezo = Button(self.frame_piezo_ovladani_leve, text="HOME", width=10, command= self.controller.M_C_Index)#SERIAL - POSLAT INDEX - PRIJEM
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
        self.frame_piezo_pozice = LabelFrame(self.frame_piezo_gui,text="Pozice", padx=5, pady=5, bg="white")
        self.label_pozice_home_piezo = Label(self.frame_piezo_pozice, text="Pozice od home:", padx=5, pady=5, bg="white", width=15,)
        self.label_pozice_homeX_piezo = Label(self.frame_piezo_pozice, text="Xh:", padx=5, pady=5, bg="white", width=10)
        self.label_pozice_homeY_piezo = Label(self.frame_piezo_pozice, text="Yh:", padx=5, pady=5, bg="white", width=10)
        self.label_pozice_homeZ_piezo = Label(self.frame_piezo_pozice, text="Zh:", padx=5, pady=5, bg="white", width=10)
        self.label_pozice_reference_piezo = Label(self.frame_piezo_pozice, text="Pozice od reference:", padx=5, pady=5, bg="white", width=15,)
        self.label_pozice_referenceX_piezo = Label(self.frame_piezo_pozice, text="Xr:", padx=5, pady=5, bg="white", width=10,)
        self.label_pozice_referenceY_piezo = Label(self.frame_piezo_pozice, text="Yr:", padx=5, pady=5, bg="white", width=10,)
        self.label_pozice_referenceZ_piezo = Label(self.frame_piezo_pozice, text="Zr:", padx=5, pady=5, bg="white", width=10,)
        
        #prikaz
        self.frame_piezo_prikaz = LabelFrame(self.frame_piezo_gui,text="Příkaz", padx=5, pady=5, bg="white")
        self.label_piezo_prikaz = Label(self.frame_piezo_prikaz, text="Příkaz k odeslání:", bg="white", width=20, anchor="w")
        self.entry_piezo_prikaz = Entry(self.frame_piezo_prikaz, width=33,)
        self.entry_piezo_prikaz.bind("<Return>", lambda _ : self.controller.M_C_send_msg_piezo(self.entry_piezo_prikaz.get()))
        self.BTN_piezo_prikaz = Button(self.frame_piezo_prikaz, text="POSLAT", width=10, command= lambda: self.controller.M_C_send_msg_piezo(self.entry_piezo_prikaz.get()))
        self.label_piezo_odpoved = Label(self.frame_piezo_prikaz, text="Odpověď piezopohony:", bg="white", width=20, anchor="w")
        self.text_piezo_odpoved = Text(self.frame_piezo_prikaz, width=25, height=1)
        self.BTN_piezo_odpoved = Button(self.frame_piezo_prikaz, text="REFRESH", width=10, command=self.controller.M_C_odpoved_piezo_refresh)
        
        if self.controller.mcu is False:
            self.root.geometry("1000x600")        
            self.root.minsize(1000, 600)
        else:
            self.root.geometry("1500x800")
            self.root.minsize(1500, 800)
        
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
        for widget in self.frame_piezo_gui.winfo_children():
            widget.destroy()
        self.controller.pocet_frame -= 1
        self.frame_piezo_gui.destroy()
        if self.controller.mcu:
            self.root.geometry("800x400")
            self.root.minsize(800, 400)
        else:
            self.root.geometry("375x290")
            self.root.minsize(375, 290)   
        
class McuGUI():
    
    def __init__(self, root: 'Tk', controller : 'MainController' ,mcu_model : 'MCU_model'):
        self.root = root
        self.controller = controller
        self.mcu_model = mcu_model
        
        self.controller.mcu = True

        self.frame_MCU_gui = LabelFrame(self.root, text="MCU", padx=5, pady=5, bg="white", relief="groove",bd=5)
        self.frame_MCU_gui.grid(row=0, column=2, padx=5, pady=5, sticky="NW")

        if self.controller.piezo is False:
            self.root.geometry("800x400")
            self.root.minsize(800, 400)
        else:
            self.root.geometry("1500x800")
            self.root.minsize(1500, 800)
            
    def McuGUIClose(self):
        self.controller.mcu = False
        for widget in self.frame_MCU_gui.winfo_children():
            widget.destroy()
        self.controller.pocet_frame -= 1
        self.frame_MCU_gui.destroy()
        if self.controller.piezo:
            self.root.geometry("1000x600")        
            self.root.minsize(1000, 600)
        else:
            self.root.geometry("375x290")
            self.root.minsize(375, 290)   
        
if __name__ == "__main__":
    print("TOTO NENI HLAVNI APLIKACE")
    print("HLAVNI APLIKACE JE V SOUBORU main.py")
          