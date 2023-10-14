"""
Created on Sat 13 Apr 10:00:00 2019
Finished(?) on 2019
@author: Παύλος Λοΐζου (nm16801)
                                       """

import pyaudio,struct,wave
import matplotlib.pyplot as plt
import numpy as np

p = pyaudio.PyAudio()

Channels = p.get_default_input_device_info()['maxInputChannels']
Rate = int(p.get_default_input_device_info()['defaultSampleRate'])
Chunk = 8*1024
Format = pyaudio.paInt16
Record_Seconds = 11

stream = p.open(
    rate=Rate,
    channels=Channels,
    format=Format,
    input=True,
    output=True,
    frames_per_buffer=Chunk,
)

# print("Would you like to do a recording first (10 seconds)?")
# ans = input("Yes or No?")
#
# # If yes then using the wave lib, we write in a .wav file 10secs of recording
# if ans == 'Y' or ans == 'Yes' or ans == 'yes' or ans == 'y':
#     print("Recording")
#     frames = []
#
#     for i in range(int(Rate/Chunk * Record_Seconds)):
#         data = stream.read(Chunk)
#         frames.append(data)
#
#     print("Done recording")
#     wf = wave.open("Recording.wav", 'wb')
#     wf.setnchannels(Channels)
#     wf.setsampwidth(p.get_sample_size(Format))
#     wf.setframerate(Rate)
#     wf.writeframes(b''.join(frames))
#     wf.close()
# else:
#     pass

# Waveform and Fast Fourier Transformation plots
fig = plt.figure()
axis_wave = fig.add_subplot(2, 1, 1)
axis_fft = fig.add_subplot(2, 1, 2)
plt.subplots_adjust(hspace=0.5)

# Creates ploting variables
x = np.arange(0, 2*Chunk)  # waveform X_axis
x_fft = np.linspace(0, 2*Rate, 2*Chunk)  # frequency X_axis

# Sets the title of the figure
fig.suptitle('Pavlos Loizou', fontsize=15)


class Calculations:
    def __init__(self, data_array):
        # Converts data to integers
        self.data_int = struct.unpack(str(2 * Chunk) + 'h', data_array)
        self.ywave = np.array(self.data_int, dtype='i')/ (80)
        self.yf = np.fft.fft(self.ywave)/ (Chunk)
        self.yfft = abs(self.yf[0:self.yf.size])
        self.maximum_y_wave = max(abs(self.ywave))

        # The coordinates of the peak on the fft diagram
        self.maximum_y_fft = max(abs(self.yf))
        self.max_int = np.argmax(abs(self.yf))
        self.maximum_x_fft = axis_fft.semilogx(x_fft, self.yfft)[0]._x[self.max_int]


def closing(event):
    global loop
    loop = False


loop = True; maximum_yf = -1
while loop:

    # Reads binary data from the stream for the selected number of frames
    data = stream.read(Chunk)

    # Calls the ''calculations'' class
    calc = Calculations(data)
    y_wave = calc.ywave
    y_fft = calc.yfft
    maximum_xf = calc.maximum_x_fft
    maximum_yf = calc.maximum_y_fft
    maximum_ywave = calc.maximum_y_wave

    # Checks if the current maximum is greater than the previously established maximum
    # if maximum_yfft > maximum_yf:
    #     maximum_yf = maximum_yfft

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
    axis_wave.set_xlim(0, Chunk)
    axis_wave.set_ylim(-maximum_ywave * 1.2, maximum_ywave * 1.2)
    axis_fft.set_xlim(20, Rate / 2)
    axis_fft.set_ylim(0, 1.2 * maximum_yf)
    axis_wave.set_title('AUDIO WAVEFORM')
    axis_wave.set_xlabel('Samples')
    axis_wave.set_ylabel('Volume')
    axis_fft.set_title('Fast Fourier Transformation Signal')
    axis_fft.set_xlabel('Frequency [Hz]')
    axis_fft.set_ylabel('Amplitude [dB]')

    # Annotates the frequency of the highest peak of the fft plot
    ann = axis_fft.annotate(str(maximum_xf)[0:6], xy=(maximum_xf, maximum_yf),
                         xytext=(maximum_xf, maximum_yf + maximum_yf * 0.1))
    plt.show()
    plt.pause(1/Rate)  # refreshes the plot

    # Handles the closing of the figure
    fig.canvas.mpl_connect('close_event', closing)

print('Stream ended')
