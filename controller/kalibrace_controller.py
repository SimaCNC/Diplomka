from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import threading
import time
import pandas as pd
import queue
import re
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from view.main_view import MainPage, KalibracePage
from datetime import datetime
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
        self.pracovni_soubor = None
        self.delka_kroku = None
        self.merena_vzdalenost = None
        self.pocet_kroku = None #pocet kroku pro mereni = pocet iteraci ve for smycce
        self.pocet_zaznamu = 10 #implementovat do GUI pro kalibraci
        
        
        self.vzorky = []
        self.poloha = 0
        
        #fronta pro vytvareni grafu:
        self.queue_graf = queue.Queue()
        
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
        
    def nastavit_delku_kroku(self, krok):       
        self.delka_kroku = krok
        print(f"[{self.__class__.__name__}] delka kroku je {self.delka_kroku} (um)")
        
    def nastavit_delku_vzdalenost(self, vzdalenost):
        self.merena_vzdalenost = vzdalenost
        print(f"[{self.__class__.__name__}] merena vzdalenost je {self.merena_vzdalenost} (um)")
      
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
            
            
    def kalibrace_start_pulzy(self):
        print(f"[{self.__class__.__name__}] kalibrace_start_pulzy !!")
        self.controller.M_C_Index()
        
        if self.pracovni_slozka is not None:
            cesta = os.path.join(self.pracovni_slozka, "temp.csv")
            
            
        #Kalibrace #1
        def kalibrace_start_inner():
            time.sleep(5) #delay kvuli index pozici
            print(f"[{self.__class__.__name__}] VLAKNO KALIBRACE!")
            self.pocet_kroku = int(self.merena_vzdalenost) / int(self.delka_kroku)
            #zacatek vytvoreni docasneho souboru a zapis do nej
            with open(cesta, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["cas", "pozice", "frekvence"]) #hlavicka
                  
                #cekani na vychozi pozici kalibrace
                #zajede na pozici a ceka na dalsi ukoly
                while True:
                    time.sleep(0.5)
                    try:
                        if self.piezo_model.is_homed == True:

                            print(f"[{self.__class__.__name__}] HOMED!")
                            self.controller.M_C_send_msg_piezo("GT x0 y10000 z-5000") #pozice - max v Y
                            time.sleep(5) #CAS NEZ DOJEDE NA POZICI UDANE V self.controller.M_C_send_msg_piezo("GT x0 y10000 z5000")
                            self.controller.M_C_nastav_referenci()
                            break
                    except Exception as e:
                        print(f"[{self.__class__.__name__}] chyba ({e})")

                #smycka pro sber dat a zapis do souboru 
                #doresit - vymenit while za for - a pocitat do max vzdalenosti -- inkrementace piezo dle vzdalenosti
                #zapisovani do souboru vzdalenost - pozice cteni + frekvence X dat,... cas..
                #casova narocnost posunuti pieza urcit ze zrychleni, rychlosti a vzdalenosti posunu - promenny time.sleep(x) 
                #myslet na propojeni s promennymi - mozna do frony pro vykreslovani do grafu v realtime
                #ulozit - nacitani grafu v jinych mistech aplikace - filtrace dat
                iterace = 0
                prvni_zapis = not os.path.exists(cesta)
                for _ in range(int(self.pocet_kroku) + 2):
                    

                    while self.mcu_model.lock_frekvence == False:
                        time.sleep(0.1) 

                    if iterace > 0:
                        #zapsat mcu frekvence a piezo polohu
                        self.vzorky = self.mcu_model.frekvence_vzorky.copy()
                        self.poloha = int(self.piezo_model.y_ref)
                        cas = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                        df = pd.DataFrame({
                                "cas": [cas]*len(self.vzorky),
                                "pozice": [self.poloha]*len(self.vzorky),
                                "frekvence": self.vzorky
                            })
                        
                        df.to_csv(cesta, mode='a', header=prvni_zapis, index=False)
                        prvni_zapis = False

                        self.controller.M_C_nastav_pohyb_piezo(int(self.delka_kroku))
                        self.controller.M_C_pohyb_piezo("y-")
                        while self.controller.lock_pohyb == False:
                            time.sleep(0.1)               

                    #nastavit pozici - prvi iterace nulove posunuti
                    #time sleep dle rychlosti    
                    self.mcu_model.lock_frekvence = False
                    
                    if iterace < int(self.pocet_kroku) + 2:
                        print(iterace)
                        print(f"[{self.__class__.__name__}] CTENI FREKVENCE !!")
                        self.mcu_model.precist_frekvenci(int(self.pocet_zaznamu))
                    
                    iterace = iterace + 1
                  
                print(f"[{self.__class__.__name__}] sběr dat hotový")  
                
                

                
                
            
        
        self.t1 = threading.Thread(target=kalibrace_start_inner, daemon=True)
        self.t1.start()
        
        
