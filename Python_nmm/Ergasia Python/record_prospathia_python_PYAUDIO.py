import pyaudio as pa
import numpy as np
import os
# audio data into integers
import struct
# na einai pio omorfo
import matplotlib.pyplot as plt

from scipy.fftpack import fft

# matplotlib tk

p = pa.PyAudio()
chunk = 1024 * 3
FORMAT = pa.paInt16
CHANNELS = p.get_default_input_device_info()['maxInputChannels']
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=chunk
)

fig, ax2 = plt.subplots(1)
# timi pou kanoume plot
x = np.arange(0, 2 * chunk, 2)
x_fft = np.linspace(0, RATE, chunk)

line_fft, = ax2.semilogx(x_fft, np.random.rand(chunk), '-', lw=2)

ax2.set_xlim(20, RATE / 2)

while True:
    data = stream.read(chunk)
    data_int = np.array(struct.unpack(str(chunk) + 'i', data), dtype=np.int16)

    y_fft = abs(fft(data_int)) * 2 / chunk
    ax2.set_ylim(0, 1.2 * max(y_fft))

    line_fft.set_ydata(y_fft[0:chunk])
    x_max = x_fft[np.argmax(y_fft)]

    ann = plt.annotate(str(round(x_max)), xy=(x_max, max(y_fft)))

    fig.canvas.draw()
    fig.canvas.flush_events()
    ann.remove()
