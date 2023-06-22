import webbrowser
from Youtube import Youtube
from Media import Media

working_directory = r'D:/Downloads/Music'
yt = Youtube(working_directory)
# yt.download_channel(r'', file_list='1:11', index_start=None)
# yt.download_playlist(index_start=1)
# yt.download_single_video('videos.txt')

media = Media(working_directory)
# media.add_index(r'D:\Downloads\Video\Statistics')
media.trim_media_file(dir_path='Media', times_to_cut="times to cut.csv")
# media.merge_media(dir_path='Media', fade_time=0)
# media.change_audio_speed(speed=1.1)
# media.trim_multiple_videos(dir_path='Media', times_to_cut='0:40')
# media.change_video_speed(speed=1.33)
# media.change_volume(dir_path="Media", volume='0dB')
# media.remove_index()
# media.convert(output_format='mp3', from_video=False)
# media.delete_files(exclude={'mp3'})
# media.create_slideshow_video(image_path='images', audio_path='audios', fps=10)
# media.static_natural_sound(duration='10:43', fps=8, fade_in=0)
# media.animated_natural_sound(duration='10:0:0', fps=24, resize=True)

# Open a link after done
# webbrowser.open_new_tab("https://www.youtube.com/watch?v=JfRpGrRonA4&list=RDEMQu7cMineIFcyhdQFaKOywA&index=3")
