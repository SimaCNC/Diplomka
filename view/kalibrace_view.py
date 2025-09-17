
from main_view import KalibraceGUI
from tkinter import *
from tkinter import ttk
from controller.kalibrace_controller import MainController
import inspect
from typing import TYPE_CHECKING
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


if TYPE_CHECKING:
    pass


class KalibracniOkno(Toplevel):
    def __init__(self, parent, kalibrace_gui, controller : 'MainController'):
        super().__init__(parent)
        self.kalibrace_gui : KalibraceGUI = kalibrace_gui
        self.controller = controller
        self.title("Probíhá kalibrace")
        self.geometry("1400x800")
        self.config(bg="white")
        self.iconbitmap('icon/logo_uprava2.ico')
        
        # self.scroll_frame = ScrollableFrame(self)
        # self.scroll_frame.pack(fill="both", expand=True)
        
        # #toto je FRAME hlavni
        # self.frame = self.scroll_frame.scrollable_frame
        
        self.protocol("WM_DELETE_WINDOW", self.window_exit)
        
        #graf vlevo, data vpravo
        self.frame_graf = Frame(self, bg="white")
        self.frame_graf.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        
        self.separator = ttk.Separator(self, orient="vertical")
        self.separator.grid(row=0, column=1, pady=5, sticky="ns")
        
        self.frame_text = Frame(self, bg="white")
        self.frame_text.grid(row=0, column=2, padx=5, pady=5, sticky="NSEW")
        self.text = Text(self.frame_text, width=80, height=30, relief="flat")
        self.text.grid(row=0, column=0, padx=0, pady=0)
        
        
         #data ze subysystemu MCU
        self.data_casy = []
        self.data_pozice = []
        self.data_vzorky = []
        self.data_teplota = []
        self.data_vlhkost = []    
        self.data_tlak = []
        
        
        #VYBER METODY KALIBRACE A JEHO SPUSTENI PRES CONTROLLER
        #AD
        if self.controller.protokol_gui.vybrane_var.get() == "1" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Zpětná":
            self.controller.kalibrace.kalibrace_start_ad_zpetna()
            self.controller.blok_widgets(self.controller.root)
            if self.controller.piezo_model.prostor == False:
                self.window_exit()
                return
            
        
        elif self.controller.protokol_gui.vybrane_var.get() == "1" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Dopředná":
            print(f"[{self.__class__.__name__}] TATO VOLBA NEEXISTUJE, NONE")
            pass
        
        #PULZY
        elif self.controller.protokol_gui.vybrane_var.get() == "2" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Dopředná":
            self.controller.kalibrace.kalibrace_start_pulzy_dopredna()
            self.controller.blok_widgets(self.controller.root)
            if self.controller.piezo_model.prostor == False:
                self.window_exit()
                return
            
        elif self.controller.protokol_gui.vybrane_var.get() == "3" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Dopředná":
            print(f"[{self.__class__.__name__}] TATO VOLBA NEEXISTUJE, NONE")
            pass

        else:
            print("Špatně vybraná konfigurace kalibrace !!, neexistujici kombinace vyberu zpracovani dat a strategie kalibrace")
            self.after(0, self.window_exit) #zavreni okna po dokonceni konstruktoru
        #VYBER METODY KALIBRACE A JEHO SPUSTENI PRES CONTROLLER    
            
    
        self.fig, self.ax = plt.subplots()
        #POPISKY GRAFU
        if self.controller.protokol_gui.vybrane_var.get() == "1" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Zpětná":
            self.ax.set_title("Závislost velikosti napětí na vzdálenosti přiblíženi stěny k snímači od reference")
            self.ax.set_xlabel("Vzdálenost (μm)")
            self.ax.set_ylabel("Napětí (V)")
            print(f"[{self.__class__.__name__}] vybrané napětí")
          
        elif self.controller.protokol_gui.vybrane_var.get() == "2" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Dopředná":
            self.ax.set_title("Závislost frekvence pulzů na vzdálenosti stěny od snímače")
            self.ax.set_xlabel("Vzdálenost (μm)")
            self.ax.set_ylabel("Frekvence (Hz)")
            print(f"[{self.__class__.__name__}] vybraná frekvence")
        #POPISKY GRAFU
            
        #canvas pro vlozeni matplotlib do tkinter okna
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_graf)
        self.widget = self.canvas.get_tk_widget()
        self.widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        #SPUSTENI FUNKCE ZA 500ms SE FUNKCE PRO AKTUALIZACI GRAFU
        if self.controller.protokol_gui.vybrane_var.get() == "1" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Zpětná":
            self.after(500, self.aktualizace_graf_ad)
        
        elif self.controller.protokol_gui.vybrane_var.get() == "2" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Dopředná":
            self.after(500, self.aktualizace_graf_frekvence)
        #SPUSTENI FUNKCE ZA 500ms SE FUNKCE PRO AKTUALIZACI GRAFU
        
        self.ax.clear()
        self.ax.minorticks_on()
        self.ax.grid(which='major', linestyle='--', linewidth=0.7, alpha=0.8)
        self.ax.grid(which='minor', linestyle='-', linewidth=0.3, alpha=0.4)
        
        
        
    #GRAF PRO AD: if self.controller.protokol_gui.vybrane_var.get() == "1" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Zpětná":
    def aktualizace_graf_ad(self):
        #zpracovavani dat ve fronte
        print(f"[{self.__class__.__name__}] [{inspect.currentframe().f_code.co_name}] AKTUALIZACE GRAFU")
        while not self.controller.kalibrace.queue_graf.empty():
            zaznam = self.controller.kalibrace.queue_graf.get()
            
            pozice = zaznam["pozice"]
            napeti = zaznam["napeti"]
            
            print(f"[{self.__class__.__name__}] {pozice} {napeti}")
            
            self.data_pozice.append(round(float(pozice), 3))
            self.data_vzorky.append(int(napeti))
            
        #VYCISTIT GRAF + AKTUALIZACE
        self.ax.clear()
        self.ax.set_title("Závislost napětí na přiblížení stěny (reference) ke snímači")
        self.ax.set_xlabel("Přiblížení (μm)")
        self.ax.set_ylabel("Napětí (V)")
        self.ax.minorticks_on()
        self.ax.grid(which='major', linestyle='--', linewidth=0.7, alpha=0.8)
        self.ax.grid(which='minor', linestyle='--', linewidth=0.3, alpha=0.4)
            
        try:
            self.ax.plot(self.data_pozice, self.data_vzorky, 'o', markersize=5, color='red')
        except Exception as e:
            print(f"[{self.__class__.__name__}] CHYBA: {e}")
            
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.tight_layout()  # zajistí správné layoutování popisků
        self.canvas.draw_idle()
        print(f"[{self.__class__.__name__}] Počet bodů v grafu: {len(self.data_pozice)}")
        
        
        #VYCISTIT TEXT + AKTUALIZACE
        
        if self.controller.kalibrace.kalibrace == True:
            self.after(600, self.aktualizace_graf_frekvence) #rekurzivne, cyklicky chod
        
        
        
    #GRAF PRO FREKVENCI: elif self.controller.protokol_gui.vybrane_var.get() == "2" and self.controller.kalibrace_gui.vybrany_drop_strategie.get() == "Dopředná":
    def aktualizace_graf_frekvence(self):
        #zpracovavani dat ve fronte
        print(f"[{self.__class__.__name__}] [{inspect.currentframe().f_code.co_name}] AKTUALIZACE GRAFU")
        while not self.controller.kalibrace.queue_graf.empty():
            zaznam = self.controller.kalibrace.queue_graf.get()
            
            pozice = zaznam["pozice"]
            frekvence = zaznam["frekvence"]
            
            print(f"[{self.__class__.__name__}] {pozice} {frekvence}")
            
            self.data_pozice.append(round(float(pozice), 3))
            self.data_vzorky.append(int(frekvence))
                  
            
        # VYCISTIT GRAF + AKTUALIZACE
        self.ax.clear()
        self.ax.set_title("Závislost frekvence pulzů na vzdálenosti stěny od snímače")
        self.ax.set_xlabel("Vzdálenost (μm)")
        self.ax.set_ylabel("Frekvence (Hz)")
        self.ax.minorticks_on()
        self.ax.grid(which='major', linestyle='--', linewidth=0.7, alpha=0.8)
        self.ax.grid(which='minor', linestyle='--', linewidth=0.3, alpha=0.4)

        try:
            self.ax.plot(self.data_pozice, self.data_vzorky, 'o', markersize=5, color='red')
        except Exception as e:
            print(f"[{self.__class__.__name__}] CHYBA: {e}")

        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.tight_layout()  # zajistí správné layoutování popisků
        self.canvas.draw_idle()
        print(f"[{self.__class__.__name__}] Počet bodů v grafu: {len(self.data_pozice)}")
        
        
        #VYCISTIT TEXT + AKTUALIZACE
        
        
        
        
        if self.controller.kalibrace.kalibrace == True:
            self.after(600, self.aktualizace_graf_frekvence) #rekurzivne, cyklicky chod
             

    def window_exit(self):
        # zavrit = messagebox.askyesno("Ukončení aplikace", "Upravdu si přejete ukončit aplikaci?")
        # if zavrit:
        #     print("Zavirani okna a vypnuti aplikace")
        self.controller.odblok_widgets(self.controller.root)
        self.kalibrace_gui.BTN_kalibraceStart.config(state="active")
        self.destroy()
        print(f"[{self.__class__.__name__}] Zavirani okna")
        
        #zastaveni kalibrace
        self.controller.kalibrace.kalibrace = False
        
        #vymazani dat
        for attr in ["data_casy", "data_pozice", "data_vzorky", "data_teplota", "data_vlhkost", "data_tlak"]:
            if hasattr(self, attr):
                lst = getattr(self, attr)
                if isinstance(lst, list):
                    lst.clear()