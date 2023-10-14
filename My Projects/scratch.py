"""
Created on Mon 29 Jun 18:23 2020
Finished on
@author: Cpt.Ender
                                  """
# import sys
# import urllib.request
# from urllib.request import urlopen, FancyURLopener
# from urllib.parse import urlparse, parse_qs, unquote
#
#
# class UndercoverURLopener(FancyURLopener):
#     version = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.9 Safari/533.2"
#
#
# urllib.request._urlopener = UndercoverURLopener()
#
#
# def youtube_download(video_url):
#     video_id = parse_qs(urlparse(video_url).query)['v'][0]
#
#     url_data = urlopen('http://www.youtube.com/get_video_info?&video_id=' + video_id).read()
#     url_info = parse_qs(unquote(url_data.decode('utf-8')))
#     token_value = url_info['token'][0]
#
#     download_url = "http://www.youtube.com/get_video?video_id={0}&t={1}&fmt=18".format(
#         video_id, token_value)
#
#     video_title = url_info['title'][0] if 'title' in url_info else ''
#     # Unicode filenames are more trouble than they're worth
#     filename = video_title.encode('ascii', 'ignore').decode('ascii').replace("/", "-") + '.mp4'
#
#     print("\t Downloading '{}' to '{}'...".format(video_title, filename))
#
#     try:
#         download = urlopen(download_url).read()
#         f = open(filename, 'wb')
#         f.write(download)
#         f.close()
#     except Exception as e:
#         print("\t Downlad failed! {}".format(str(e)))
#         print("\t Skipping...")
#     else:
#         print("\t Done.")
#
#
# print("\n--------------------------")
# print(" Youtube Video Downloader")
# print("--------------------------\n")
#
# # try:
# #     video_urls = sys.argv[1:]
# # except:
# #     video_urls = input('Enter (space-separated) video URLs: ')
# video_urls = 'https://www.youtube.com/watch?v=LEyb3NewkKQ'
# youtube_download(video_urls)
# print("\n Done.")
#
# ---------------------------------------------------------------------------
# import pafy
#
# url = 'https://www.youtube.com/watch?v=LEyb3NewkKQ'
# # url = "https://www.youtube.com/watch?v=bMt47wvK6u0"
# video = pafy.new(url)
# audiostreams = video.audiostreams
# for a in audiostreams:
#     print(a.bitrate, a.extension, a.get_filesize())
# ------------------------------------------------------------------------------
# Load imports
import librosa.display
import matplotlib.pyplot as plt

filename1 = 'Sources/Los_Angelenos.mp3'
plt.figure(figsize=(12, 4))
data1, sample_rate1 = librosa.load(filename1, mono=True, offset=0.0, duration=50)
librosa.display.waveplot(data1, sr=sample_rate1, max_points=50000.0, x_axis='time', offset=0.0, max_sr=1000)
