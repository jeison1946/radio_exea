import platform

class Message:
  def __init__(self):
    self.channel = self.getChannel()
    self.linux = True
  
  def getChannel(self):
    if platform.machine() == 'x86_64':
      from rich.console import Console
      return Console()
    else:
      import Adafruit_CharLCD as LCD
      self.linux = False
      return LCD.Adafruit_CharLCDPlate()
  
  def showMesssage(self, message):
    if self.linux:
      self.channel.print(message, style="bold green")
    else:
      self.channel.clear()
      self.channel.message(message)