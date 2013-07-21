import os
import random
import pyglet

class musicClient():

    baseUrl = "/home/fahran/Music/hacked"

    def playRandomMoodSong(self, mode):
        directory = (self.baseUrl + "/" + mode)
        songs = os.listdir(directory)
        song = random.choice(songs)
        self.music = pyglet.media.load(directory + "/" + song)
        self.music.play()
        pyglet.app.run()

    def stopMusic(self):
        self.music.stop

player = musicClient()
player.playRandomMoodSong("fire")
# playlist_id = api.create_playlist('Rad muzak')
# api.change_playlist(playlist_id, sweet_tracks)