import os
import random
import pygame
import time

pygame.mixer.init()
class musicClient():

    baseUrl = os.path.dirname(__file__)

    def playRandomMoodSong(self, mode):
        directory = (self.baseUrl + "/" + mode)
        songs = os.listdir(directory)
        song = random.choice(songs)
        self.music = pygame.mixer.music
        self.music.load(directory + "/" + song)
        self.music.play()

    def stopMusic(self):
        self.music.stop()

if __name__ == '__main__':
    try:
        player = musicClient()
        player.playRandomMoodSong("fire")
        time.sleep(20)
        player.stopMusic()
    except SystemExit:
        player.stopMusic()
        quit
    except KeyboardInterrupt:
        player.stopMusic()
        quit


# playlist_id = api.create_playlist('Rad muzak')
# api.change_playlist(playlist_id, sweet_tracks)