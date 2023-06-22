import os
from pathlib import Path as p
from typing import Union
import pandas as pd
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips, concatenate_audioclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment
from tqdm import tqdm
from moviepy.video.io.VideoFileClip import VideoFileClip


class Media:
    """Convert videos to mp3
    Delete videos with specific extensions in a folder
    Adjust media speed, and more
    """

    def __init__(self, directory: str):
        self.directory = directory

    @staticmethod
    def add_index(dirpath: str, start: int = 1):
        """Sort all files in folder in terms of time created and add index before titles
        Parameters
        ----------
        dirpath: str: directory
        start: The starting index
        """

        dirpath = r'D:\Downloads\Video\Statistics'
        paths = sorted(p(dirpath).iterdir(), key=os.path.getmtime)
        for index, path, in enumerate(paths, start):
            if path.name.split()[0][0].isnumeric():
                print(f"File {path.stem} is already indexed")
            else:
                os.rename(path, f'{path.parent}\{" ".join(path.name.split())}')

    @staticmethod
    def to_second(time_string: str) -> Union[int, float]:
        """Parse a string of time under the form xx:xx(:xx) to a number of seconds
        Parameters
        ----------
        time_string: str :
        Returns
        -------
        int
        """
        str_time = time_string.split(':')
        num_time = list(map(int, str_time))
        total_secs = list(zip(num_time[::-1], [1, 60, 3600]))
        total_secs = sum(a * b for a, b in total_secs)
        return total_secs

    @staticmethod
    def find_repeat(audio_duration, img_num: int, seconds_per_image: Union[int, float]):
        """Returns the times that images have to repeat to fill in the audio duration
        Parameters
        ----------
        audio_duration : int:
        img_num: int : The number of images to be processed
        seconds_per_image: Union[int, float]
        Returns
        -------
        """
        return int(audio_duration / (seconds_per_image * img_num) + 1)

    def trim_audio_file(self, dir_path: str = "Media", times_to_cut="times to cut.csv") -> None:
        """Trims one video file into multiple ones
        Parameters
        ----------
        dir_path : str: A sub path relative to main directory
        times_to_cut : a text file that contains starts and ends to trim media files
                        "start, end
                        0:5, 3:29"
        -------
        """
        # Get the audio file name and path
        audio_file = p(self.directory) / dir_path
        audio_path = next(audio_file.glob('*'))

        audio_segment = AudioSegment.from_file(audio_path)
        duration = audio_segment.duration_seconds

        # Define the path to the CSV file containing the trim times
        trim_times = pd.read_csv(times_to_cut, header=None, usecols=['start', 'end'], names=['start', 'end'])

        # Use applymap() to apply strip() to each element in the DataFrame
        trim_times = trim_times.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        for index, r in enumerate(tqdm(trim_times.itertuples(), total=len(trim_times)), 1):
            start = self.to_second(r.start)
            if r.end.lower() == 'end':
                end = duration
            else:
                end = self.to_second(r.end)
            name = audio_path.name
            path = audio_path.parent
            title = audio_path.stem
            extension = audio_path.suffix
            if start >= end:
                print(f"Start {r.start} > end {r.end}");
                break
            else:
                new_path = f"{path}/trimmed/{title}_{index}{extension}"
            try:
                # audio = AudioSegment.from_file(r['file'])
                sub_audio = audio_segment[start * 1000:end * 1000]
                sub_audio.export(new_path, format="mp3")
            except OSError:
                pass

    def trim_media_file(self, dir_path: str = "Media", times_to_cut="times to cut.csv", merge=False) -> None:
        """Trims one media file into multiple ones
        Parameters
        ----------
        dir_path : str: A sub path relative to main directory
        times_to_cut : a text file that contains starts and ends to trim media files
                        "start, end
                        0:5, 3:29"
        -------
        """
        is_video = False
        # Define the directory path
        directory = p(self.directory) / dir_path

        # Get the media file name and path
        media_file = next(directory.glob("*"))
        media_path = str(media_file)

        extension = media_file.suffix
        if extension in [".mp4", ".avi", ".mov", ".mkv"]:  # Video
            clip = VideoFileClip(media_path)
            is_video = True
        else:  # Audio
            clip = AudioFileClip(media_path)

        # Read the trim times from the CSV file
        trim_times = pd.read_csv(times_to_cut, header=None, usecols=[0, 1], names=["start", "end"])

        # Use applymap() to apply strip() to each element in the DataFrame
        trim_times = trim_times.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        final_clips = []

        # Iterate over the trim times and write each subclip to a new file
        for i, row in enumerate(trim_times.itertuples(), 1):
            start_time = self.to_second(row.start)
            end_time = clip.duration if row.end.lower() == 'end' else self.to_second(row.end)
            if start_time > end_time:
                print(f'Start {start_time} has to be smaller than end {end_time}');
                break
            # Trim the clip
            trimmed_clip = clip.subclip(start_time, end_time)
            final_clips.append(trimmed_clip)
            if not merge:
                # Determine the output file name and path
                file_name = f"{media_file.stem}_{i}{media_file.suffix}"
                output_path = str(directory / "Trimmed" / file_name)
                if is_video:
                    trimmed_clip.write_videofile(output_path)
                else:
                    trimmed_clip.write_audiofile(output_path)
        if merge:
            # Concatenate the subclips into a final media
            if is_video:
                final_clip = concatenate_videoclips(final_clips)
            else:
                final_clip = concatenate_audioclips(final_clips)
            # Determine the output file name and path
            file_name = f"{media_file.stem}_merged{media_file.suffix}"
            output_path = str(directory / "Trimmed" / file_name)
            # Save the trimmed clip
            if is_video:
                final_clip.write_videofile(output_path)
            else:
                final_clip.write_audiofile(output_path)

    def trim_multiple_videos(self, dir_path: str = "Media", times_to_cut="0:40") -> None:
        """Trims multiple files at the same time
        Parameters
        ----------
        dir_path : str: A sub path relative to main directory
        times_to_cut : str -> 0:40 means all files will start at 0:40
        Returns
        -------
        """
        dir_path = p(self.directory) / dir_path
        for file in dir_path.glob('*'):
            if file.is_file():
                new_path = f"{dir_path}/trimmed/{file.name}"
                ffmpeg_extract_subclip(
                    filename=str(file),
                    t1=self.to_second(times_to_cut),
                    t2=AudioFileClip(str(file)).duration,
                    targetname=new_path,
                )

    def remove_index(self, dir_path: str = 'Media'):
        """Take off index from medias
        Parameters
        ----------
        dir_path : str: A sub path relative to main directory
        Returns
        -------
        """
        dir_path = p(self.directory) / dir_path
        for file in dir_path.glob('*'):
            if file.is_file():
                new_name = file.name.split('.', 1)[-1]
                new_path = dir_path / new_name
                os.rename(file, new_path)

    def create_slideshow_video(self, image_path: str, audio_path: Union[str, None] = None, dir_path='Media',
                               seconds_per_image: Union[int, float] = 5,
                               fps: int = 12, fade_in: Union[int, float] = 2) -> None:
        """Insert a slideshow of images to an audio -> video
        Parameters
        ----------
        image_path : str :
        audio_path : str :
        dir_path : str: A sub path relative to main directory
        seconds_per_image : Union[int, float] : How long does an image will show up
        fps : int :
        fade_in : Union[int, float]: fade-in time
        -------
        """
        image_path = p(self.directory) / dir_path / image_path
        if audio_path:
            audio_path = p(self.directory) / dir_path / audio_path
            # Get the only audio in audio_path
            audio_list = sorted(list(p(audio_path).glob('*')))
            audio_clip = AudioFileClip(str(audio_list[0]))
            images = [img_file for img_file in p(image_path).glob('*')]
            if len(images) == 1:
                seconds_per_image = audio_clip.duration
            images = [ImageClip(str(img)).set_duration(seconds_per_image).fadein(fade_in) for img in images]
            # Return a repeated list of the same images
            images = images * self.find_repeat(audio_clip.duration, len(images), seconds_per_image=audio_clip.duration)
            # Concatenate images to a video
            concat_clip = concatenate_videoclips(images, method="compose")
            concat_clip = concat_clip.set_audio(audio_clip).subclip(0, audio_clip.duration)
            concat_clip.write_videofile(f'{audio_path}/{audio_list[0].stem}.mp4', fps=fps)
        else:
            images = [img_file for img_file in p(image_path).glob('*')]
            images = [ImageClip(str(img)).set_duration(seconds_per_image) for img in images]
            concat_clip = concatenate_videoclips(images, method="compose")
            concat_clip.write_videofile(f'{audio_path}.mp4', fps=fps)
