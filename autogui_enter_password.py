# Entering the password with pyautogui

import pyautogui as pag


# Get password input and enter text
x, y = pag.locateCenterOnScreen('text_field.png') #If the file is not a png file it will not work
pag.leftClick(x/2, y/2)
pag.typewrite('password') # Write in text field

# Get unlock button coordinates and click it
x, y = pag.locateCenterOnScreen('unlock_button.png') #If the file is not a png file it will not work
pag.leftClick(x/2, y/2)



#pag.moveTo(start)#Moves the mouse to the coordinates of the image
#pag.moveTo(x/2, y/2)






