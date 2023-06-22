import os
import re
import time
from moviepy.editor import AudioFileClip
from itertools import starmap
from pathlib import Path
from typing import Union, Optional
import pandas as pd
import unicodedata
from pytube import Channel, Playlist, YouTube
from tqdm import tqdm


class Youtube:
    """Download YouTube videos
    Convert videos to mp3
    """

    def __init__(self, directory: str):
        self.directory = directory

    @staticmethod
    def strip_accents(text: str) -> str:
        return ''.join(char for char in
                       unicodedata.normalize('NFKD', text)
                       if unicodedata.category(char) != 'Mn')

    @staticmethod
    def add_index(file_path: str, index: int) -> None:
        """Add index to a file name given the file path
        Parameters
        ----------
        file_path: str :
        index: int :
        -------
        """
        #
        name = Path(file_path).name
        folder = Path(file_path).parent
        new_name = f"{index}. {name}"
        new_file_path = Path(folder) / new_name
        Path(file_path).rename(new_file_path)

    @staticmethod
    def to_second(time_string: str) -> int:
        """Parse a string of time under the form xx:xx(:xx) to a number of seconds
        Parameters
        ----------
        time_string: str :
        Returns
        -------
        int
        """
        if isinstance(time_string, str):
            units = [1, 60, 3600]
            time_list = [map(int, time_string.split(":"))][::-1]
            if not all(0 <= i < 60 for i in time_list):
                print('Time is not right')
                return
            time_list = sum(starmap(lambda x, y: x * y, zip(units, time_list)))
            assert type(time_list) in ['int', 'float']
            assert time_list >= 0
            return time_list

        raise TypeError('time_string has to be a string under the form xx:xx(:xx)')

    def clean_title(self, title: str, to_english=True) -> str:
        """Remove non-words and non-spaces from title
        Parameters
        ----------
        title: str :
        to_english :
             Convert to English accents if the original is non-English
        Returns
        -------
        str: a cleaned title
        """
        result = re.sub(r"[^\w\s]", "", title)
        result = ' '.join(result.split()).strip()
        if to_english:
            return self.strip_accents(result)
        return result

    def attempt(self, url: str, directory: str) -> None:
        """Tries to download a video with the highest resolution given a Youtube object and storing directory
        Parameters
        ----------
        url: str :
        directory: str : Location the file will be downloaded to
        -------
        """
        try:
            downloaded_file_path = (
                YouTube(url.strip()).streams.filter(progressive=True)
                .get_highest_resolution()
                .download(directory)
            )
            return downloaded_file_path
        except OSError:
            print(f"Cannot download video {YouTube(url.strip()).title}")
            with open((Path(self.directory) / 'failed downloads.txt'), 'a') as file:
                file.write(f'{url}\n')

    @staticmethod
    def extract_list(pytube_object: Channel, filelist: Optional[str] = None):
        """Extracts a string of the range of video indices from either channel (pytube_object)
        Parameters
        ----------
        pytube_object : Channel
        filelist: Optional[str] : "3:7" -> 4th to 7th videos, '5:last' -> 6th to last videos
        Returns
        -------
        """

        def add_last(n: int) -> int:
            """Assigns a number to be equal to the length of pytube_object
            Parameters
            ----------
            n : int
            -------
            """
            n = n if n > 0 else len(pytube_object)
            return n

        if not filelist:
            # Return all urls if a specific filelist is not given
            return pytube_object.video_urls
        start, end = map(str.strip, filelist.split(":"))
        if start <= end:
            url_lists = tqdm(pytube_object.video_urls[start:end], desc="Loading...")
        else:
            url_lists = tqdm(pytube_object.video_urls[end:start], desc="Loading...")
        return url_lists, pytube_object.video_urls[start], pytube_object.video_urls[end]

    def download_channel(
            self,
            channel_url: str,
            file_list: str = None,
            highest_quality: bool = None,
            index_start: int = None
    ) -> None:
        """Downloads videos from a channel given a file_list
        Parameters
        ----------
        channel_url: str
        file_list: str
        highest_quality: bool: highest quality of video?
        index_start: int: The index of the beginning video
        -------
        """
        # Download specific videos included in file_list from channel_url
        if not highest_quality:
            highest_quality = True if Path(self.directory).name.strip().lower() == 'video' else False
        channel = Channel(url=channel_url)
        channel_name = self.clean_title(channel.channel_name)
        file_path = Path(self.directory) / channel_name
        downloaded_file_path = ''
        try:
            os.mkdir(file_path)
            print(f"Folder {channel_name} created")
        except OSError:
            pass
        url_lists, start, end = self.extract_list(channel, file_list)
        print(f'Your list is from {YouTube(start).title} to {YouTube(end).title}\n')
        confirm = input('Enter y if correct else n')
        if confirm.strip().lower() == 'y':
            for index, url in enumerate(url_lists, 1):
                if YouTube(url).length < 120:
                    continue
                yt = YouTube(url.strip())
                if highest_quality:
                    try:
                        downloaded_file_path = self.attempt(url, file_path)
                    except OSError:
                        pass
                else:
                    try:
                        downloaded_file_path = (
                            yt.streams.filter(only_audio=True)
                            .order_by("abr")
                            .desc()
                            .first()
                            .download(file_path)
                        )
                    except OSError:
                        pass
                if index_start:
                    try:
                        self.add_index(
                            file_path=downloaded_file_path, index=index + index_start
                        )
                    except OSError:
                        pass
        else:
            return

    def download_playlist(
            self,
            url_file: str = 'playlist_urls.txt',
            highest_quality: Union[None, bool] = None,
            index_start: Union[None, int] = None
    ) -> None:
        """Downloads some videos from playlists
        Parameters
        ----------
        url_file: str : the text file containing all playlist ủls
        highest_quality: Union[None: bool] :
        index_start: Union[None :int] :
        -------
        """
        # File list contains names of files in the playlist
        assert (not index_start) or (index_start > 0), "Index has to be either None or positive!"
        # Download specific videos included in file_list from playlist_url
        if not highest_quality:
            highest_quality = True if Path(self.directory).name.strip().lower() == 'video' else False
        downloaded_file_path = ''
        with open(url_file, 'r') as f:
            playlist_urls = [line.rstrip() for line in f]
        for playlist_url in playlist_urls:
            playlist_obj = Playlist(playlist_url)
            # Remove forbidden symbols from title
            try:
                title = playlist_obj.title
            except OSError:
                title = str(round(time.time() * 1000))
            title = self.clean_title(title)
            file_path = Path(self.directory) / title
            try:
                os.mkdir(file_path)
                print(f"Folder {file_path} created")
            except OSError:
                pass
            print()
            for index, pl_url in tqdm(enumerate(playlist_obj.videos_generator()), total=len(playlist_obj)):
                if highest_quality:
                    try:
                        audio_file = pl_url.streams.filter(
                            progressive=True).get_highest_resolution().download(file_path)
                    except OSError:
                        print(f"Cannot download video {pl_url.title}")
                        with open((Path(self.directory) / 'failed downloads.txt'), 'a') as file:
                            file.write(f'{pl_url.video_id}\n')
                else:
                    try:
                        audio_file = (
                            pl_url.streams.filter(only_audio=True)
                            .order_by("abr")
                            .desc()
                            .first()
                            .download(file_path)
                        )
                        # Get the extension of the downloaded audio stream
                        audio_extension = os.path.splitext(audio_file)[1]
                        # Convert the audio file to MP3 with a bitrate of 128 kbps
                        audio = AudioFileClip(audio_file)
                        audio.write_audiofile(audio_file.replace(audio_extension, ".mp3"), bitrate="128k")
                        # Delete the original audio file
                        os.remove(audio_file)
                    except OSError:
                        pass
                if index_start:
                    try:
                        self.add_index(
                            file_path=audio_file, index=index + index_start
                        )
                    except OSError:
                        pass

    def download_single_video(self, url_file: str, highest_quality: Union[None, bool] = None) -> None:
        """Download all videos in a url text file
        Parameters
        ----------
        url_file: str : the text file containing all playlist url
        highest_quality: Union[None: bool] :
        Returns
        -------
        """
        if not highest_quality:
            highest_quality = True if Path(self.directory).name.strip().lower() == 'video' else False
        # Remove duplicated urls
        urls = pd.read_csv(url_file, names=["urls"])
        urls.drop_duplicates(subset='urls', inplace=True)
        for url in urls['urls']:
            yt = YouTube(url.strip())
            print(f"Downloading...{yt.title}")
            if highest_quality:
                self.attempt(url, self.directory)
            else:
                audio_file = yt.streams.filter(only_audio=True).order_by("abr").desc().first().download(
                    self.directory)
                # Get the extension of the downloaded audio stream
                audio_extension = os.path.splitext(audio_file)[1]
                # Convert the audio file to MP3 with a bitrate of 128 kbps
                audio = AudioFileClip(audio_file)
                audio.write_audiofile(audio_file.replace(audio_extension, ".mp3"), bitrate="128k")
                # Delete the original audio file
                os.remove(audio_file)
