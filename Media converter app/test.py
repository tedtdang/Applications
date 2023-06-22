from Converter import Media
from pathlib import Path as p

tester = Media('./original audio.m4a')
tester.convert_to_audio('mp3')