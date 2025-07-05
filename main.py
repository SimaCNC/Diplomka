from controller.main_controller import MainController
from view.main_view import RootGUI, ComGUI

from model.Piezo_model import Piezo_model
from model.MCU_model import MCU_model
from model.Serial_model import SerialCtrl





#-----VIEW-----
root_view = RootGUI()
#-----VIEW-----

#-----MODEL----
piezo_serial = SerialCtrl()
mcu_serial = SerialCtrl()

piezo_model = Piezo_model(piezo_serial)
mcu_model = MCU_model(mcu_serial)
#-----MODEL----

#-----CONTROLLER----
controller = MainController(root_view.root, None, piezo_model, mcu_model)
#-----CONTROLLER----

#vytvoreni com_view a prirazeni controlleru
com_view = ComGUI(root_view.root, controller, piezo_model, mcu_model)

#napojeni controlleru na com_view
controller.com = com_view
controller.M_init_view_data()




#----ZAPNUTI GUI APLIKACE----
root_view.root.mainloop()
#----ZAPNUTI GUI APLIKACE----