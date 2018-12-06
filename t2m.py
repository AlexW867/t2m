#!/usr/bin/env python3
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
import os
import sys
import subprocess

# 參數指定小數範圍
def restricted_float(s):
    s = float(s)
    if s < 0.1 or s > 5.0:
       raise ArgumentTypeError('speed not in range [0.1-5.0]')
    return s

# 播放 mp3
def play_mp3(mp3_file):
    mp = AudioSegment.from_mp3(mp3_file)
    mp.export('temp.wav', format='wav')
    wave_obj = sa.WaveObject.from_wave_file('temp.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove('temp.wav')

def get_voice(text):
    tts = gTTS(text, lang='zh')
    tts.save('output.mp3')

def speed_proc(speed):
    cmd = '''ffmpeg -loglevel quiet -i output.mp3 -filter:a "atempo=%.1f" -vn output_%.1fx.mp3 -y''' % (speed, speed)
    subprocess.call(cmd, shell=True)

parser = ArgumentParser()
parser.add_argument('text', help='Text to Speech')
parser.add_argument('-s', '--speed', dest='speed', default=1.8, type=restricted_float, help='set speed(0.0-5.0)')
parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='quiet or play it')
args = parser.parse_args()

get_voice(args.text)
if args.speed != 1.0:
    speed_proc(args.speed)
if args.quiet == False:
    play_mp3('output_%.1fx.mp3' % args.speed)
