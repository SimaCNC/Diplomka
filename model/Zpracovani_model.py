import time
import pandas as pd
import re
import csv
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
import matplotlib.pyplot as plt
from view.main_view import MainPage, KalibracePage
from datetime import datetime
import math

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controller.main_controller import MainController

class Zpracovani_model():
    def __init__(self, controller : "MainController"):
        self.controller = controller
        
        
        self.data = pd.DataFrame()