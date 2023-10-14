"""
Created on Sat 13 Apr 10:00:00 2019
Finished on Fri 31 May 10:00:00 2019
@author: Παύλος Λοΐζου (nm16801)
                                       """

import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import wave

audio = pyaudio.PyAudio()

Channels = audio.get_default_input_device_info()['maxInputChannels']
Rate = int(audio.get_default_input_device_info()['defaultSampleRate'])
Chunk = 8 * 1024
Format = pyaudio.paInt16
Record_Seconds = 11

stream = audio.open(
    rate=Rate,
    channels=Channels,
    format=Format,
    input=True,
    output=True,
    frames_per_buffer=Chunk)

print("Would you like to do a recording first (10 seconds)?")
ans = input("Yes or No?")

# If yes then using the wave lib, we write in a .wav file 10secs of recording
if ans == 'Y' or ans == 'Yes' or ans == 'yes' or ans == 'y':
    print("Recording")
    frames = []

    for i in range(int(Rate / Chunk * Record_Seconds)):
        data = stream.read(Chunk)
        frames.append(data)

    print("Done recording")
    wf = wave.open("Recording.wav", 'wb')  # "wb" = write only
    wf.setnchannels(Channels)
    wf.setsampwidth(audio.get_sample_size(Format))
    wf.setframerate(Rate)
    wf.writeframes(b''.join(frames))
    wf.close()
else:
    pass

# Waveform and Fast Fourier Transformation plots
fig = plt.figure()
axis_wave = fig.add_subplot(2, 1, 1)
axis_fft = fig.add_subplot(2, 1, 2)
plt.subplots_adjust(hspace=0.5)

# Creates plotting variables
x = np.linspace(0, 2 * Chunk / 100, 2 * Chunk)  # waveform X_axis
# x_fft = np.linspace(100, Rate, 2 * Chunk)  # frequency X_axis
x_fft = np.linspace(0, 2 * Rate, 2 * Chunk)  # frequency X_axis

# Sets the title of the figure
fig.suptitle('Pavlos Loizou (nm16801)', fontsize=15)


class Calculations:
    def __init__(self, data_array):
        # Converts data to integers
        self.data_int = np.frombuffer(data_array, dtype=np.int16)

        self.ywave = np.array(self.data_int, dtype='i')
        self.yf = np.fft.fft(self.ywave) / Chunk * 10
        self.yfft = abs(self.yf[0:self.yf.size])
        self.maximum_y_wave = max(abs(self.ywave))

        # The coordinates of the peak on the fft diagram
        self.maximum_y_fft = max(abs(self.yf))
        self.max_int = np.argmax(abs(self.yf))
        self.maximum_x_fft = axis_fft.semilogx(x_fft, self.yfft)[0]._x[self.max_int]


def closing():
    global loop
    loop = False


loop = True
while loop:
    # Reads binary data from the stream for the selected number of frames
    data = stream.read(Chunk)

    # Calls the ''Calculations'' class
    calc = Calculations(data)
    y_wave = calc.ywave
    y_fft = calc.yfft
    maximum_xf = calc.maximum_x_fft
    maximum_yf = calc.maximum_y_fft
    maximum_ywave = calc.maximum_y_wave

    # First iteration error handling
    try:
        ann.remove()
    except NameError:
        pass

    # Draws the waveform and the fft lines
    axis_wave.clear()
    axis_fft.clear()
    axis_wave.plot(x, y_wave, '-', lw=1)
    axis_fft.semilogx(x_fft, y_fft, '-', lw=1)

    # Sets the limits and titles of the axis for each subplot
    axis_wave.set_xlim(0, 1)
    axis_wave.set_ylim(-maximum_ywave * 1.05, maximum_ywave * 1.05)
    axis_fft.set_xlim(right=max(x_fft) / 2)
    axis_fft.set_ylim(0, 1.2 * maximum_yf)
    axis_wave.set_title('Audio Waveform')
    axis_wave.set_xlabel('Samples [ms]')
    axis_wave.set_ylabel('Amplitude')
    axis_fft.set_title('Fast Fourier Transformation Signal')
    axis_fft.set_xlabel('Frequency [Hz]')
    axis_fft.set_ylabel('Amplitude')

    # Annotates the frequency of the highest peak on the fft diagram
    ann = axis_fft.annotate(str(maximum_xf)[0:6], xy=(maximum_xf, maximum_yf))
    plt.show()
    plt.pause(1 / Rate)  # refreshes the plot

    # Handles the closing of the figure
    fig.canvas.mpl_connect('close_event', closing)

print('Stream ended')
