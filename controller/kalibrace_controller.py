from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import threading
import time
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
        
        self.protokol ={"1" : "A/D převodník",
                        "2" : "Pulzy",
                        "3" : "Protokol"}
        
    def protokol_kalibrace(self, protokol):
        print(f"[KalibraceController] vybrany protokol : {self.protokol[protokol]}")
      
    def vybrat_pracovni_slozku(self):
        cesta = filedialog.askdirectory(title="Pracovní složka")
        
        if cesta:
            self.controller.kalibrace_gui.label_slozka_pracovni.config(text=f"{cesta}")
        else:
            self.controller.kalibrace_gui.label_slozka_pracovni.config(text=f"N/A")