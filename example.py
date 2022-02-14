from pyPmodCLS import LCD

lcd = LCD(SCL=1, SDA=0)

lcd.clear()

lcd.cursorMode(True, True)
lcd.print("It works")
lcd.setCursorPosition(0,12)
lcd.print("!!")

