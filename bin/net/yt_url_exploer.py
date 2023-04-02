from pytube.contrib.playlist import Playlist
import numpy
def search(url: str) :

    playlist = Playlist(url=url)
    list = numpy.array(playlist.video_urls)

    return list