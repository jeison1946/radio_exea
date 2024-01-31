import netifaces
from src.utils.message import Message

class LCD:
  def __init__(self):
    self.message = Message()

  def getIp(self):
    try:
      interfaces = [interface for interface in netifaces.interfaces(
      ) if interface.startswith("eth")]

      for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        ip = addrs.get(netifaces.AF_INET)
        if ip and "addr" in ip[0]:
            return "IP: " + ip[0]["addr"]
        return False
    except Exception as e:
        return False
  def showIp(self):
    ip = self.getIp()
    if ip:
      message = ip
    else:
      message = 'Error detectando'
    self.message.showMesssage(message)

  def showNotInternet(self):
    self.message.showMesssage('Sin internet')