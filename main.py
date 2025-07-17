from controller.main_controller import MainController
from view.main_view import RootGUI
from model.Piezo_model import Piezo_model
from model.MCU_model import MCU_model
from model.Serial_model import SerialCtrl

#-----MODEL---- M
piezo_serial = SerialCtrl()
mcu_serial = SerialCtrl()

piezo_model = Piezo_model(piezo_serial)
mcu_model = MCU_model(mcu_serial)
#-----MODEL---- 

#-----VIEW----- V
root_view = RootGUI()
#-----VIEW----- 

#-----CONTROLLER---- C
controller = MainController(root_view.root, root_view, piezo_model, mcu_model)
controller.setup_gui()

#vytvoreni pohledu a prirazeni


#-----CONTROLLER----


#----ZAPNUTI GUI APLIKACE----
root_view.root.mainloop()
#----ZAPNUTI GUI APLIKACE----