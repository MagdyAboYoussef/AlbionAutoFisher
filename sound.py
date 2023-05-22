import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import resample
import pyaudio
import threading
from pynput.mouse import Button, Controller
from time import sleep
import helper
import os
import sys

with open('temp_file.txt', 'r') as f:
    temp_file_name = f.read().strip()

# Load the fish sound file
fishing_lock = threading.Lock()
fs_fish, fish_sound = wavfile.read('resources/fishSound.wav')
mouse = Controller()
# Resample the fish sound to match the sampling rate of the live audio
fs = 44100  # sampling rate
fish_sound_resampled = resample(
    fish_sound, int(len(fish_sound) * fs / fs_fish))
fish_sound_resampled = np.mean(fish_sound_resampled, axis=1)  # convert to mono

# Set the length of each audio chunk to 0.1 second
chunk_duration = 0.1  # in seconds
chunk_size = int(chunk_duration * fs)

# Set the overlap between consecutive audio chunks to 100%
overlap = 0.1
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=fs,
                 input=True,
                 output=True,  # set the stream to be a duplex stream
                 frames_per_buffer=chunk_size,
                 input_device_index=helper.indexOfSound())

# Function to process each chunk of audio


def process_audio_chunk(chunk):
    # Compute the cross-correlation between the audio chunk and the fish sound
    corr = np.correlate(chunk, fish_sound_resampled, mode='same')
    # adjust this value to control the sensitivity of the matching
    correlation_threshold = 10000
    print(np.max(corr))
    if np.max(corr) > correlation_threshold:
        if fishing_lock.acquire(blocking=False):
            mouse.press(Button.left)
            mouse.release(Button.left)
            sleep(5)
            fishing_lock.release()


# Continuously record audio and check for matches
while True:
    if not os.path.exists(temp_file_name):
        # The temp file has been deleted, stop the script
        sys.exit()
    # Read a chunk of audio from the stream
    audio_data = stream.read(chunk_size)
    audio_samples = np.frombuffer(audio_data, dtype=np.int16) / 32768.0

    # Write the audio data back to the stream to play it back
    # stream.write(audio_data)

    # Divide the audio sample into overlapping chunks
    chunk_starts = np.arange(0, len(audio_samples),
                             int((1 - overlap) * chunk_size))
    chunk_ends = np.minimum(chunk_starts + chunk_size, len(audio_samples))
    chunks = [audio_samples[start:end]
              for start, end in zip(chunk_starts, chunk_ends)]

    # Process each chunk of audio in a separate thread
    threads = []
    for chunk in chunks:
        t = threading.Thread(target=process_audio_chunk, args=(chunk,))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()
