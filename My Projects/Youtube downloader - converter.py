"""
Created on Mon 29 Jun 00:34 2020
Finished on
@author: Cpt.Ender

Downloading video and/or audio of a
Youtube Video
                                  """
import pytube

path = 'D:\\plabc\\Downloads'
# url = input()
urlList = []
# url = 'https://www.youtube.com/watch?v=LEyb3NewkKQ'
url = "https://www.youtube.com/playlist?list=PLlLV8Yl1h97akTCR7ZOwGLnjAi7e_uBMx"
# while url != "Stop":
urlList.append(url)
#     url = input()


def download(_url, _path: str):
    try:
        video = pytube.YouTube(_url)
        title = video.title
        for stream in video.streams:
            print(stream)
        print("Downloading " + title + ".............")
        audio_streams = video.streams.filter(only_audio=True, subtype='mp4').order_by('abr').desc()
        audio = audio_streams[0].download(output_path=_path, filename=title)
        print("Done")
    except IndexError:
        return


for url in urlList:
    if url.count("playlist"):
        playlist = pytube.Playlist(url)
        for _ in playlist.videos:
            print(_)
        # for _url in playlist.video_urls[:3]:
        #     download(_url, path+playlist.title)
    else:
        download(url, path)

# ytb = YouTube(url)
# title = ytb.title
# audio_streams = ytb.streams.filter(only_audio=True, subtype='mp4').order_by('abr').desc()
# audio = audio_streams[0].download(output_path=path, filename=title)
