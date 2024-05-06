import pygame
import glob
import os
import requests
from src.utils.config import Config
from src.services.conectionService import ConectionService;
import vlc
from src.utils.lcd import LCD


class Player():
  def __init__(self):
    self.config = Config().getConfig()
    self.lcd = LCD()
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)

  def initPlayer(self):
    if self.checkConection():
      self.playerPointOfSale()
    else:
      self.lcd.showNotInternet()
      folder = glob.glob(os.path.join('./songs', '*.mp3'))
      if (folder):
        player: vlc.MediaPlayer = vlc.MediaPlayer()
        for file in folder:
          media = vlc.Media(file)
          player.set_media(media)
          try:
            player.play()
          except Exception:
            print('Error')

          while True:
            if player.get_state() == vlc.State.Ended:
              if self.checkConection():
                return self.playerPointOfSale()
              break
          if file == folder[-1]:
            self.initPlayer()

      else:
        print("Carpeta vacia")
  
  def checkConection(self):
    try:
      response = requests.head("https://www.google.com", timeout=5)
      if response.status_code == 200:
        return True
    except requests.ConnectionError:
      return False
    return False
    
  def playerPointOfSale(self):
    self.lcd.showIp()
    try:
      conection = ConectionService()
      response = conection.getNext(self.config)
      if(response['code'] == 200):
        player: vlc.MediaPlayer = vlc.MediaPlayer()
        song = response['response']['song']
        media = vlc.Media(song['url'])
        player.set_media(media)
        player.play()
        conection.logSong(response['response'], self.config)
        while True:
          state = player.get_state()
          if state == vlc.State.Ended:
            self.initPlayer()
      else:
        self.lcd.showMessageCustom('Not Rules')
    except Exception:
        self.lcd.showMessageCustom('Conection error api')