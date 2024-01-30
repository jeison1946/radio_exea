import platform

class Message:
  def __init__(self):
    self.linux = True
    self.channel = self.getChannel()
  
  def getChannel(self):
    if platform.machine() == 'x86_64':
      from rich.console import Console
      return Console()
    else:
      from src.utils.GPIOlibrary import GPIOlibrary
      self.linux = False
      return GPIOlibrary()
  
  def showMesssage(self, message):
    if self.linux:
      self.channel.print(message, style="bold green")
    else:
      self.channel.message(message + "\n")