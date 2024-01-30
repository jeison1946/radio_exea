import netifaces
from src.utils.message import Message

class LCD:
  def __init__(self):
    self.message = Message()

  def getIp(self):
    try:
        # Crear un socket y conectarlo a un servidor externo (por ejemplo, Google DNS)
        interfaces = netifaces.interfaces()
        for iface in interfaces:
          addrs = netifaces.ifaddresses(iface)
          ip = addrs.get(netifaces.AF_INET)
          if ip and "addr" in ip[0]:
            return ip[0]["addr"]
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