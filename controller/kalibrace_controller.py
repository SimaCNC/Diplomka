from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import threading
import time
import queue
import re
from view.main_view import MainPage, KalibracePage
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from view.main_view import RootGUI, ComGUI, PiezoGUI,McuGUI
    from model.Piezo_model import Piezo_model
    from model.MCU_model import MCU_model
    import tkinter as Tk
    from controller.main_controller import MainController
    
class KalibraceController():
    def __init__(self, controller, piezo_model, mcu_model):
        self.controller : MainController = controller
        self.piezo_model : Piezo_model = piezo_model
        self.mcu_model : MCU_model = mcu_model
        self.pracovni_slozka = None
        self.delka_kroku = None
        
        #Zpracovani dat
        self.protokol ={"1" : "A/D převodník",
                        "2" : "Pulzy",
                        "3" : "Protokol"}
        
        #Strategie zpracovani a kalibrace
        self.strategie = {"Dopředná" : "Dopředná",
                          "Zpětná" : "Zpětná",
                          "Hystereze" : "Hystereze",
                          "Hystereze2" : "Hystereze2"}
        
    def protokol_kalibrace(self, protokol):
        print(f"[KalibraceController] vybrany protokol : {self.protokol[protokol]}")
        # print(f"[{self.__class__.__name__}] protokol: {self.controller.protokol_gui.vybrane_var.get()}") #stejna odpoved
        
    def nastavit_delku_kroku(self, delka):       
        self.delka_kroku = delka
        print(f"[{self.__class__.__name__}] delka kroku je {self.delka_kroku}")
      
    def vybrat_pracovni_slozku(self):
        self.pracovni_slozka = filedialog.askdirectory(title="Pracovní složka")
        print(f"[{self.__class__.__name__}] složka {self.pracovni_slozka}")
        
        if self.pracovni_slozka:
            self.controller.kalibrace_gui.Entry_slozka_pracovni.config(state="normal")
            self.controller.kalibrace_gui.Entry_slozka_pracovni.delete(0, "end")
            self.controller.kalibrace_gui.Entry_slozka_pracovni.insert(0, f"{self.pracovni_slozka}")
            self.controller.kalibrace_gui.Entry_slozka_pracovni.config(state="readonly")
            
        else:
            self.controller.kalibrace_gui.Entry_slozka_pracovni.config(state="normal")
            self.controller.kalibrace_gui.Entry_slozka_pracovni.delete(0, "end")
            self.controller.kalibrace_gui.Entry_slozka_pracovni.insert(0, f"N/A")
            self.controller.kalibrace_gui.Entry_slozka_pracovni.config(state="readonly")
            
            
    def kalibrace_start(self):
        print(f"[{self.__class__.__name__}] kalibrace_start")
        self.controller.M_C_Index()
        
        def kalibrace_start_inner():
            time.sleep(5) #delay kvuli index pozici
            print(f"[{self.__class__.__name__}] VLAKNO!")
            while True:
                time.sleep(0.5)
                try:
                    if self.piezo_model.is_homed == True:
                        print(f"[{self.__class__.__name__}] HOMED!")
                        self.controller.M_C_send_msg_piezo("GT x0 y10000 z-5000")
                        time.sleep(4) #CAS NEZ DOJEDE NA POZICI UDANE V self.controller.M_C_send_msg_piezo("GT x0 y10000 z5000")
                        self.controller.M_C_nastav_referenci()
                        break
                            
                
                except Exception as e:
                    print(f"[{self.__class__.__name__}] chyba ({e})")
                    break
        
        self.t1 = threading.Thread(target=kalibrace_start_inner, daemon=True)
        self.t1.start()
        
        
