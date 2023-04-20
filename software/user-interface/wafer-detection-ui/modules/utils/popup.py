from kivy.uix.popup import Popup
from  kivy.uix.label import Label

def pop(title_string, error_message):
    popup = Popup(title=title_string, content=Label(text=error_message),size_hint=(None, None), size=(400, 200))
    popup.open()

# def display_error(num):
#     match num:
#         case 1:
#             pop("MOVEMENT FAILED", "Please check your connection and try again.")
#         case 2: 
#             pop("CONNECTION FAILED", "Please verify your COM port and cable connectivity\nand try again.")
#         case 3: 
#             pop("HOMING FAILED", "Please check your connection and try again.")
#         case 4: 
#             pop("AUTO SCAN FAILED", "Please check your connection and try again.")

def display_error(num):
    if num == 1:
        pop("MOVEMENT FAILED", "Please check your connection and try again.")
    elif num == 2: 
        pop("CONNECTION FAILED", "Please verify your COM port and cable connectivity\nand try again.")
    elif num == 3: 
        pop("HOMING FAILED", "Please check your connection and try again.")
    elif num == 4: 
        pop("AUTO SCAN FAILED", "Please check your connection and try again.")