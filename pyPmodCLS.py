"""
MIT License

Copyright (c) 2022 Thibault HILAIRE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from machine import I2C, Pin

DISPLAYSET = {(False,False): '0e', (False, True): '2e', (True, False): '1e', (True, True): '3e'}

class LCD:
	"""This simple class is used to drive the Digilent PmodCLS LCD display"""
	
	def __init__(self, SCL:int, SDA:int, address:int=88):
		"""Initialize the LCD and the I2C protocol
		Parameters:
		- SCL: (int) GPIO number for the SCL line
		- SDA: (int) GPIO number for the SDA line
		- address: (int) I2C address of the LCD (88 by default)"""
		self._i2c = I2C(0,scl=Pin(SCL), sda=Pin(SDA), freq=40000)
		self._address = address
		
	def print(self, string: str):
		"""print a string
		Parameter:
		- string: (str) string to be displayed"""
		self._i2c.writeto(self._address, string.encode())

	def _command(self, string: str):
		"""Intern escape to be sent before a command"""
		self._i2c.writeto(self._address, bytes([0x1b,0x5b]))
		self._i2c.writeto(self._address, string.encode())
	
	def clear(self):
		"""Clear display and home cursor """
		self._command('j')
	
	def turnOnOff(self, setDisplay:bool):
		"""This function turns on or off the display
		Parameters:
		- setDisplay: (bool) set the display on (True) or off (False)"""
		if setDisplay:	
			self._command("1e")
		else:
			self._command("0e")

	def cursorMode(self, cursor:bool, blink:bool):
		"""This function turns the cursor and the blinking option on or off, according to the user's selection
		- cursor: (bool) set the cursor on (True) or off (False)
		- blink: (bool) set the blink option on (True) or off (False)"""
		if not cursor:
			self._command('0c')
		elif not blink:
			self._command("1c")
		else:
			self._command("2c")


	def setCursorPosition(self, row:int, col:int):
		"""Set the cursor position to <row>,<col>
		Parameters:
		- row: (int) row number (0 or 1)
		- col: (int) col number (0 to 39)"""
		self._command("%d;%dH" % (row,col))

	
	def saveCursorPosition(self):
		"""Save the cursor position"""
		self._command("s")


	def restorCursorPosition(self):
		"""Restore the cursor position
		previously saved with `saveCursorPosition`"""
		self._command("u")

	def eraseLine(self, mode:int):
		"""Erase characters within line
		Parameters:
		- mode: (int)
			0 = erase from the current position to end of line,
			1 = erase from the start of line to current position
			2 = erase the entire line """
		self._command("%dK" % mode)


	def eraseChars(self, nbChar:int):
		"""Erase a number of characters starting at the current position
		Parameters:
		- nbChars: (int) number of characters to be erased"""
		self._command("%dN" % nbChar)

	def scrollLeft(self, nbCol: int):
		"""Scroll left the display	with a specified number of columns
		Parameters:
		- nbCol: (int) number of columns to scroll the text"""
		self._command("%d@" % nbCol)

	def scrollRight(self, nbCol: int):
		"""Scroll right the display	with a specified number of columns
		Parameters:
		- nbCol: (int) number of columns to scroll the text"""
		self._command("%dA" % nbCol)		