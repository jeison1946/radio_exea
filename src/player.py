import pygame
import glob
import os
import urllib.request
from src.utils.config import Config
from src.services.conectionService import ConectionService;
import vlc
from src.utils.lcd import LCD


class Player():
  def __init__(self):
    self.config = Config().getConfig()
    self.lcd = LCD()

  def initPlayer(self):
    self.lcd.showIp()
    if self.checkConection():
      self.playerPointOfSale()
    else:
      folder = glob.glob(os.path.join('./songs', '*.mp3'))
      if (folder):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        for file in folder:
          pygame.mixer.music.load(file)
          pygame.mixer.music.play()
          finish = False
          while not finish:
            for event in pygame.event.get():
              if event.type == pygame.USEREVENT:
                  finish = True
                  if self.checkConection():
                    return self.playerPointOfSale()
        pygame.mixer.music.set_endevent(0)
        self.initPlayer()
      else:
        print("Carpeta vacia")
  
  def checkConection(self):
    try:
      urllib.request.urlopen('http://www.google.com', timeout=1)
      return True
    except urllib.error.URLError:
      return False
    
  def playerPointOfSale(self):
    conection = ConectionService()
    response = conection.getNext(self.config)
    if(response['code'] == 200):
      player: vlc.MediaPlayer = vlc.MediaPlayer()
      song = response['payload']['song']
      media = vlc.Media(song['url'])
      player.set_media(media)
      try:
        player.play()
        conection.logSong(response['payload'], self.config)
      except Exception:
        print('Error')

      while True:
        state = player.get_state()
        if state == vlc.State.Ended:
          self.initPlayer()