from tkinter import *
from tkinter import messagebox
import threading
import time
import re
from view.main_view import MainPage, KalibracePage
from typing import TYPE_CHECKING
from controller.kalibrace_controller import KalibraceController

if TYPE_CHECKING:
    from view.main_view import RootGUI, ComGUI, PiezoGUI,McuGUI, StavGUI, Typ_protokolGUI, KalibraceGUI
    from model.Piezo_model import Piezo_model
    from model.MCU_model import MCU_model
    import tkinter as Tk
    
class MainController():   
    def __init__(self, root : 'Tk', view: 'RootGUI', piezo_model : 'Piezo_model', mcu_model : 'MCU_model'):
        self.root = root
        self.view = view
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        self.piezo = False
        self.piezo_is_homed_kalibrace = False
        self.mcu = False
        self.main_page = None
        

        
        self.kalibrace = KalibraceController(controller=self, piezo_model=piezo_model, mcu_model=mcu_model)
        self.lock_1 = True #odemknuto
        self.lock_pohyb = True
        
#PRIRAZOVANI POHLEDU
    def set_main_page(self, main_page : 'MainPage'):
        self.main_page = main_page
        self.com : 'ComGUI' = main_page.com_gui
        self.piezo_gui : 'PiezoGUI' = main_page.piezo_gui
        self.mcu_gui : 'McuGUI'= main_page.mcu_gui 
    
    def set_kalibrace_page(self, kalibrace_page : 'KalibracePage'):
        self.kalibrace_page = kalibrace_page
        self.stav_gui : StavGUI = kalibrace_page.stav_gui
        self.protokol_gui : Typ_protokolGUI = kalibrace_page.protokol_gui
        self.kalibrace_gui : KalibraceGUI = kalibrace_page.kalibrace_gui
    
#Vytvoreni pohledu a definovani prvniho okna - Pripojeni = main      
    def setup_gui(self):
        self.view.add_frame("main", MainPage, self, self.piezo_model, self.mcu_model)
        self.view.add_frame("kalibrace", KalibracePage, self, self.piezo_model, self.mcu_model)
        #self.view.add_frame("nápověda")
        self.view.show_frame("main")

#zablokovani vsech widgetu
    def blok_widgets(self, root : 'Tk'):
        for widget in root.winfo_children():
            if isinstance(widget, (Button, Entry, OptionMenu)):
                widget.config(state="disabled")
            elif widget.winfo_children():
                self.blok_widgets(widget)
                
#odblokovani vsech widgetu
    def odblok_widgets(self, root : 'Tk'):
        for widget in root.winfo_children():
            if isinstance(widget, (Button, Entry, OptionMenu)):
                widget.config(state="normal")
            elif widget.winfo_children():
                self.odblok_widgets(widget)    
    
#MAIN PAGE
#M_C GUI PRO MAIN POHLED
    def M_serial_connect_piezo(self):
        if self.com.btn_connect_piezo["text"] in "Připojit" :
            #Zacatek seriove komunikace - pripojeni metodou SerialOpen
            self.piezo_model.piezo_serial.SerialOpen(self.com.vybrany_com_piezo.get(), int(self.com.vybrany_bd_piezo.get()))
            
            #jestli je pripojeni uspesne:
            if self.piezo_model.piezo_serial.status:
                self.com.btn_connect_piezo["text"] = "Odpojit"
                self.com.btn_refresh_piezo["state"] = "disable"
                self.com.drop_bd_piezo["state"] = "disable"
                self.com.drop_com_piezo["state"] = "disable"
                self.piezo_gui.PiezoGUIOpen()
                InfoMsg = f"Piezo\nÚspěšně připojeno pomocí sériové komunikace k {self.com.vybrany_com_piezo.get()}"
                messagebox.showinfo("Piezo info", InfoMsg)
            else:
                ErrorMsg = f"Piezo\nChyba v připojení pomocí sériové komunikace k {self.com.vybrany_com_piezo.get()}"
                messagebox.showerror("Piezo CHYBA", ErrorMsg)       
        else:
            self.piezo_model.piezo_serial.SerialClose()
            self.piezo_gui.PiezoGUIClose()
            InfoMsg = f"Piezo\nÚspěšně odpojeno pomocí sériové komunikace k {self.com.vybrany_com_piezo.get()}"
            messagebox.showinfo("Piezo info", InfoMsg)  
            self.com.btn_connect_piezo["text"] = "Připojit"
            self.com.btn_refresh_piezo["state"] = "active"
            self.com.drop_bd_piezo["state"] = "active"
            self.com.drop_com_piezo["state"] = "active"
                
    def M_serial_connect_MCU(self):
        if self.com.btn_connect_MCU["text"] in "Připojit" :
            #Zacatek seriove komunikace - pripojeni metodou SerialOpen
            self.mcu_model.mcu_serial.SerialOpen(self.com.vybrany_com_MCU.get(), int(self.com.vybrany_bd_MCU.get()))
            
            #jestli je pripojeni uspesne:
            if self.mcu_model.mcu_serial.status:
                self.com.btn_connect_MCU["text"] = "Odpojit"
                self.com.btn_refresh_MCU["state"] = "disable"
                self.com.drop_bd_MCU["state"] = "disable"
                self.com.drop_com_MCU["state"] = "disable"
                self.mcu_gui.McuGUIOpen()
                InfoMsg = f"MCU\nÚspěšně připojeno pomocí sériové komunikace k {self.com.vybrany_com_MCU.get()}"
                messagebox.showinfo("MCU info", InfoMsg)
            else:
                ErrorMsg = f"MCU\nChyba v připojení pomocí sériové komunikace k {self.com.vybrany_com_MCU.get()}"
                messagebox.showerror("MCU CHYBA", ErrorMsg)       
        else:
            self.mcu_model.mcu_serial.SerialClose()
            self.mcu_gui.McuGUIClose()
            InfoMsg = f"MCU\nÚspěšně odpojeno pomocí sériové komunikace k {self.com.vybrany_com_MCU.get()}"
            messagebox.showinfo("MCU info", InfoMsg)  
            self.com.btn_connect_MCU["text"] = "Připojit"
            self.com.btn_refresh_MCU["state"] = "active"
            self.com.drop_bd_MCU["state"] = "active"
            self.com.drop_com_MCU["state"] = "active"

    #obas je pouziti slov/promennych home a index matouci - jedna se o totez jsou to synonyma
    #OVLADANI
    def M_C_Index(self):
        print("VOLANI HOME")
        self.piezo_model.is_homed = False
        self.piezo_is_homed_kalibrace = False
        self.piezo_model.index_pozice()
        send = "RI x y z\n"
        expect = r"^\$RI x1 y1 z1$" 
        self.piezo_model.t1 = threading.Thread(target=self.piezo_model.piezo_serial.get_msg_stream, args=(send, expect, self.M_C_Index_done,), daemon=True)
        self.piezo_model.t1.start()
        self.piezo_gui.disable_children(self.piezo_gui)
    
    def M_C_odpoved_wait(self, send, expect, callback_fun = None):
        send = send
        expect = expect
        self.piezo_model.t2 = threading.Thread(target=self.piezo_model.piezo_serial.get_msg_stream, args=(send, expect, callback_fun), daemon=True)
        self.piezo_model.t2.start() 
    
    #HODNE SKAREDE RESENI mc index done...!!!  
    def M_C_Index_done(self, msg):
        print(f"zprava z piezo: {msg}")
        if msg == "$RI x1 y1 z1":
            self.root.after(0, self.piezo_gui.publish_PiezoGUI_home_done)
            # self.piezo_model.is_homed = True
            # self.M_C_precti_polohu()
            time.sleep(0.2)
            self.piezo_model.piezo_serial.send_msg_simple(msg="SR x0.002 y0.002 z0.002;\n")
            time.sleep(0.2)
            self.piezo_model.piezo_serial.send_msg_simple(msg="GT x0 y0 z0;\n")
            time.sleep(0.2)
            self.M_C_odpoved_wait(send="RS x y z\n", expect=r"^\$RS x[27] y[27] z[27]$", callback_fun = self.M_C_precti_polohu)
        else:
            print("[INDEX]: Neuspesne")
        #POSLAT PRES SERIAL POZADAVEK O ZASLANI NA HOME POZICI! - Zatim nedodelane, netreba
    
    #POZICE
    def M_C_precti_polohu(self, msg = None):
        print(f"[{self.__class__.__name__}] [VOLANI AKTUALNI POLOHY] piezo_model.is_homed = True !")
        self.piezo_model.is_homed = True
        if self.piezo_model.is_homed == True:
            self.piezo_model.precti_polohu_stojici(self.M_C_precti_polohu_done)
        else:
            print(f"[{self.__class__.__name__}] najizdeni do home polohy 0,0,0")
            ErrorMsg = f"Piezo\nNejprve je nutné zavolat home!!"
            messagebox.showerror("Piezo CHYBA", ErrorMsg)
        
    def M_C_precti_polohu_done(self):
        self.piezo_is_homed_kalibrace = True
        self.piezo_gui.label_pozice_homeX_piezo.config(text=f"Xh: {self.piezo_model.x:.3f}")
        self.piezo_gui.label_pozice_homeY_piezo.config(text=f"Yh: {self.piezo_model.y:.3f}")
        self.piezo_gui.label_pozice_homeZ_piezo.config(text=f"Zh: {self.piezo_model.z:.3f}")
        
        self.piezo_gui.label_pozice_referenceX_piezo.config(text=f"Xr: {self.piezo_model.x_ref:.3f}")
        self.piezo_gui.label_pozice_referenceY_piezo.config(text=f"Yr: {self.piezo_model.y_ref:.3f}")
        self.piezo_gui.label_pozice_referenceZ_piezo.config(text=f"Zr: {self.piezo_model.z_ref:.3f}")
        
        if self.kalibrace.kalibrace == True:
            self.lock_pohyb = True
        else:
            self.M_C_enable_piezo_buttons()
            self.lock_pohyb = True
        
                                    
    def M_C_nastav_referenci(self):
        print("[NASTAVENI REFERENCE]")
        self.piezo_model.nastav_referenci()
        self.M_C_nastav_referenci_done()
       
    def M_C_nastav_referenci_done(self):
        self.piezo_gui.label_pozice_referenceX_piezo.config(text=f"Xr: {self.piezo_model.x_ref:.3f}")
        self.piezo_gui.label_pozice_referenceY_piezo.config(text=f"Yr: {self.piezo_model.y_ref:.3f}")
        self.piezo_gui.label_pozice_referenceZ_piezo.config(text=f"Zr: {self.piezo_model.z_ref:.3f}")

    #PRIKAZ
    def M_C_send_msg_piezo(self, msg):
        self.piezo_model.piezo_serial.send_msg_simple(msg=msg+"\n")
        self.M_C_disable_piezo_buttons()
        
        def callback_po_odpovedi_piezo():
            self.M_C_update_piezo_odpoved_do_GUI()
            self.M_C_odpoved_wait(send="RS x y z\n", expect=r"^\$RS x[27] y[27] z[27]$", callback_fun = self.M_C_precti_polohu) #aktualni pozice po zastaveni
        
        self.piezo_model.msg_odpoved(callback_fun=callback_po_odpovedi_piezo)
               
    def M_C_update_piezo_odpoved_do_GUI(self):
        odpoved = self.piezo_model.posledni_odpoved_piezopohony
        
        if odpoved:
            self.piezo_gui.text_piezo_odpoved.config(state="normal")
            self.piezo_gui.text_piezo_odpoved.delete("1.0", "end")
            self.piezo_gui.text_piezo_odpoved.insert("1.0", odpoved)
            self.piezo_gui.text_piezo_odpoved.config(state="disabled")    

    def M_C_odpoved_piezo_refresh(self):
        self.piezo_gui.text_piezo_odpoved.config(state="normal")
        self.piezo_gui.text_piezo_odpoved.delete("1.0", "end")
        self.piezo_gui.text_piezo_odpoved.insert("1.0", "")
        self.piezo_gui.text_piezo_odpoved.config(state="disabled")
    
    def M_C_nastav_pohyb_piezo(self, pohyb):
        self.piezo_model.nastav_pohyb_piezo(pohyb=pohyb)
        self.piezo_gui.label_piezo_pohyb_nastavene_text.config(text=self.piezo_model.velikost_pohybu)

    def M_C_pohyb_piezo(self, smer):
        self.lock_pohyb = False
        self.M_C_disable_piezo_buttons()
        self.piezo_model.pohyb_piezo(smer)
        
        def callback_po_odpovedi_piezo():
            self.M_C_odpoved_wait(send="RS x y z\n", expect=r"^\$RS x[27] y[27] z[27]$", callback_fun = self.M_C_precti_polohu) #aktualni pozice po zastaveni
            
        self.piezo_model.msg_odpoved(callback_fun=callback_po_odpovedi_piezo)
        
    #deaktivovani tlacitek pri pohybu - mozna implementovat do view a pak jen funkce volat z controlleru    
    def M_C_disable_piezo_buttons(self):
        self.piezo_gui.disable_piezo_buttons()

    #zpetne aktivovani tlacitek
    def M_C_enable_piezo_buttons(self):
        self.piezo_gui.enable_children(self.piezo_gui)
        # self.piezo_gui.enable_piezo_buttons()


    def M_C_send_msg_MCU(self, msg):
        self.mcu_model.mcu_serial.send_msg_simple(msg = msg+"\n")
        
        def callback_po_odpovedi_MCU():
            self.M_C_update_MCU_odpoved_do_GUI()

        self.mcu_model.msg_odpoved(callback_fun=callback_po_odpovedi_MCU)
    
    def M_C_update_MCU_odpoved_do_GUI(self):
        odpoved = self.mcu_model.posledni_odpoved_MCU
        
        if odpoved:
            self.mcu_gui.text_MCU_odpoved.config(state="normal")
            self.mcu_gui.text_MCU_odpoved.delete("1.0", "end")
            self.mcu_gui.text_MCU_odpoved.insert("1.0", odpoved)
            self.mcu_gui.text_MCU_odpoved.config(state="disabled")
            
    def M_C_odpoved_MCU_refresh(self):
        self.mcu_gui.text_MCU_odpoved.config(state="normal")
        self.mcu_gui.text_MCU_odpoved.delete("1.0", "end")
        self.mcu_gui.text_MCU_odpoved.insert("1.0", "")
        self.mcu_gui.text_MCU_odpoved.config(state="disabled")

#KALIBRACE PAGE
    def M_C_aktualizace_stav(self):
        if self.piezo == True:
            self.stav_gui.label_stav_piezo_show.config(text="AKTIVNÍ", fg="green")
        else:
            self.stav_gui.label_stav_piezo_show.config(text="PIEZO NEAKTIVNÍ", fg="red")

        if self.mcu == True:
            self.stav_gui.label_stav_MCU_show.config(text="AKTIVNÍ", fg="green")
            self.mcu_model.precti_teplotu()
            time.sleep(0.1)
            self.stav_gui.label_teplota_show.config(text=self.mcu_model.teplota_okoli + "°C", fg="green")
        else:
            self.stav_gui.label_stav_MCU_show.config(text="MCU NEAKTIVNÍ", fg="red")
        
        print(f"[M_C_aktualizace_stav]: aktualizace stavu")
        
    
        