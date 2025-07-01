from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from controller.main_controller import MainController
from typing import TYPE_CHECKING
import threading
import numpy as np

import functools

import controller.main_controller
from model.Serial_model import SerialCtrl

if TYPE_CHECKING:
    from view.main_view import ComGUI
    from model.Serial_model import SerialCtrl
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
        
        #LEVE OKNA - COM PRIPOJENI
        self.frame_left = LabelFrame(root, text="COM manažer připojení", padx=5, pady=5, bg="white")
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
        self.frame_left.grid(row=0, column=0, rowspan=3, columnspan=3, padx=5, pady=5)
        self.frame_piezo.grid(row=0, column=0, padx=5, pady=10)
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
        self.btn_refresh_MCU.grid(row=0, column=2)
        self.btn_connect_MCU.grid(row=1, column=2)
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
    
    
        
if __name__ == "__main__":
    print("TOTO NENI HLAVNI APLIKACE")
    print("HLAVNI APLIKACE JE V SOUBORU main.py")
          