from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
import os.path
import platform

def play_music():
    if platform.system() == "Windows":
        global playlist, player
        playlist = QMediaPlaylist()
        url = QUrl.fromLocalFile(os.path.join(os.pardir, "files", "music.mp3"))
        playlist.addMedia(QMediaContent(url))
        playlist.setPlaybackMode(QMediaPlaylist.Loop)

        player = QMediaPlayer()
        player.setPlaylist(playlist)
        player.play()
