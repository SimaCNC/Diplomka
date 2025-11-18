#Trida pro filtraci dat
from typing import TYPE_CHECKING
from tkinter import filedialog
import pandas as pd

if TYPE_CHECKING:
    from controller.main_controller import MainController

class FiltraceData():
    def __init__(self, controller : 'MainController'):
        self.controller = controller
        self.data = None
        self.data_cas = None
        self.data_x = None
        self.data_y = None
        self.data_teplota = None
        self.data_tlak = None
        self.data_vlhkost = None
        self.data_osvetleni = None
        self.typy_dat = ["Frekvence", "Napeti"]
        self.data_typ = None
        self.data_jednotka = None
        self.cesta_soubor = None
        self.pracovni_slozka = None
        
        self.metody_filtrace = ["Průměr", "Medián", "MA", "EMA", "S-G"]
        
    def priradit_data(self,typ,jednotka):
        self.data_typ = typ
        self.data_jednotka = jednotka
        self.data_x = self.data.iloc[:,1]
        self.data_y = self.data.iloc[:,2]
        self.data_teplota = self.data.iloc[:,3]
        self.data_tlak = self.data.iloc[:,4]
        self.data_vlhkost = self.data.iloc[:,5]
        self.data_osvetleni = self.data.iloc[:,6]
        
        cas_series = self.data.iloc[:, 0]
        cas_dt = pd.to_datetime(cas_series, format="%H:%M:%S.%f")
        cas_offset = cas_dt - cas_dt.iloc[0]
        self.data_cas = cas_offset.dt.total_seconds()
        
        print(f"[{self.__class__.__name__}] DATA PRIRAZENA")

        
    def nahrat_data(self):
        self.cesta_soubor = filedialog.askopenfilename(title="Data pro filtraci", filetypes=[("Excel files", "*.xlsx *.xls")])
        if not self.cesta_soubor:
            return
        
        try:
            excel_soubor = pd.ExcelFile(self.cesta_soubor)
            
            self.data = pd.read_excel(self.cesta_soubor, sheet_name="MD005")
            
            if "Napětí (V)" in self.data.columns:
                print(f"[{self.__class__.__name__}] TYP DAT NAPETI")
                self.priradit_data(typ="napětí", jednotka="(V)")
                   
            elif "Frekvence (Hz)" in self.data.columns:
                print(f"[{self.__class__.__name__}] TYP DAT FREKVENCE")
                self.priradit_data(typ="frekvence", jednotka="(Hz)")
                
            #pokud soubor nesedi - vypnout
            else:
                print(f"[{self.__class__.__name__}] nepodporovany typ dat")
                return
            
            print(f"[{self.__class__.__name__}] USPESNE NAHRANY DATA ZE SOBORU !!!")
            
            if self.cesta_soubor:
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.config(state="normal")
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.delete(0, "end")
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.insert(0, f"{self.cesta_soubor}")
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.config(state="readonly")
            
            else:
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.config(state="normal")
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.delete(0, "end")
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.insert(0, f"N/A")
                self.controller.original_filtrace_gui.Entry_pracovni_soubor.config(state="readonly")
            
        except:
            print(f"[{self.__class__.__name__}] CHYBA SE SOUBOREM, EXISTUJE?")
            
            
            
    def vybrat_pracovni_slozku(self):
        self.pracovni_slozka = filedialog.askdirectory(title="Pracovní složka")
        print(f"[{self.__class__.__name__}] složka {self.pracovni_slozka}")
        
        if self.pracovni_slozka:
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.config(state="normal")
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.delete(0, "end")
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.insert(0, f"{self.pracovni_slozka}")
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.config(state="readonly")
            
        else:
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.config(state="normal")
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.delete(0, "end")
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.insert(0, f"N/A")
            self.controller.filtrace_data_gui.Entry_pracovni_slozka.config(state="readonly")
            
            
            
            
    
        
        
        
            
            
         