from pytube import Playlist, YouTube
import os
from moviepy.editor import VideoFileClip  # pip install moviepy
import pytube
import urllib.error


class YouTubeDownloader:
    def download_video(self, url, resolution):
        itag = self.choose_resolution(resolution)
        video = YouTube(url)
        stream = video.streams.get_by_itag(itag)
        stream.download()
        return stream.default_filename

    def download_videos(self, urls, resolution):
        for url in urls:
            self.download_video(url, resolution)

    def download_playlist(self, url, resolution):
        playlist = Playlist(url)
        self.download_videos(playlist.video_urls, resolution)

    def choose_resolution(self, resolution):
        if resolution in ["low", "360", "360p"]:
            itag = 18
        elif resolution in ["medium", "720", "720p", "hd"]:
            itag = 22
        elif resolution in ["high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
            itag = 137
        elif resolution in ["very high", "2160", "2160p", "4K", "4k"]:
            itag = 313
        else:
            itag = 18
        return itag

    def input_links(self):
        print("Enter the links of the videos (end by entering 'STOP'):")

        links = []
        link = ""

        while link != "STOP" and link != "stop":
            link = input()
            links.append(link)

        links.pop()

        return links

    def convert_to_mp3(self, filename):
        clip = VideoFileClip(filename)
        clip.audio.write_audiofile(filename[:-4] + ".mp3")
        clip.close()

def downloader():
    print("Welcome to ARIA YouTube Downloader and Converter v0.2 Delta")
    print("Loading...")

    print('''
    What do you want?

    (1) Download YouTube Videos Manually
    (2) Download a YouTube Playlist
    (3) Download YouTube Videos and Convert Into MP3

    Copyright (c) 
    ''')

    choice = input("Choice: ")
    youtube_downloader = YouTubeDownloader()

    if choice == "1" or choice == "2":
        quality = input("Please choose a quality (low, medium, high, very high):")
        if choice == "2":
            link = input("Enter the link to the playlist: ")
            print("Downloading playlist...")
            youtube_downloader.download_playlist(link, quality)
            print("Download finished!")
        if choice == "1":
            links = youtube_downloader.input_links()
            for link in links:
                try:
                    youtube_downloader.download_video(link, quality)
                except pytube.exceptions.HTTPError as e:
                    print(f"Error downloading the video: {e}")

    elif choice == "3":
        links = youtube_downloader.input_links()
        for link in links:
            print("Downloading...")
            filename = youtube_downloader.download_video(link, 'medium')
            print("Converting...")
            youtube_downloader.convert_to_mp3(filename)
    else:
        print("Invalid input! Terminating...")


if __name__ == "__main__":
    downloader()
    
    # https://youtu.be/ZVVt0HlzZf0?si=Xd2BBY2FHDn1qFGI