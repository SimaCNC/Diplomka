from tkinter import *
from tkinter import messagebox
import threading
import time
import re
from view.main_view import MainPage, KalibracePage
from typing import TYPE_CHECKING
from main_controller import MainController

if TYPE_CHECKING:
    from view.main_view import RootGUI, ComGUI, PiezoGUI,McuGUI
    from model.Piezo_model import Piezo_model
    from model.MCU_model import MCU_model
    import tkinter as Tk
    
class KalibraceController():
    def __init__(self, controller, piezo_model, mcu_model):
        self.controller = controller
        self.piezo_model = piezo_model
        self.mcu_model = mcu_model
        
        
        