import platform

class Message:
  def __init__(self):
    self.linux = True
    self.channel = self.getChannel()
    if not self.linux:
      self.current_row = 0
      self.max_rows = 2  # Suponiendo que tu LCD tiene 2 filas

  def getChannel(self):
    if platform.machine() == 'x86_64':
      from rich.console import Console
      return Console()
    else:
      from src.utils.GPIOlibrary import GPIOlibrary
      self.linux = False
      return GPIOlibrary()

  def showMessage(self, message):
    if self.linux:
      self.channel.print(message, style="bold green")
    else:
      if self.current_row >= self.max_rows:
        self.current_row = 0
        self.channel.clear()
      self.channel.setCursor(0, 1, self.current_row)
      self.channel.message(message + "\n")
      self.current_row += 1