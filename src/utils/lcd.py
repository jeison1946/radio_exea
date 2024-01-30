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
          if netifaces.AF_INET in addrs:
            return addrs[netifaces.AF_INET][0]['addr']
    except Exception as e:
        return 'Sin internet'
  def showIp(self):
    self.message.showMesssage(self.getIp())