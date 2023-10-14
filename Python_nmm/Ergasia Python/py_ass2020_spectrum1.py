import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import pyaudio
import wave

'''we write the characteristics of our pc microphone'''
mic_format = pyaudio.paInt16
mic_channels = 2
mic_freq = 44100
mic_chunck = 2 * 1024
rec_seconds = 3
wave_output_filename = 'assigment_rec.wav'

audio = pyaudio.PyAudio()

'''I give y_fft (y_line) and x_fft(x_line) so the class 'Calculations' gives back max_y and max_x of the graph'''


class calculations:
    def __init__(self, y_line, x_line):
        self.maximum_y = max(abs(y_line))
        self.maximum_x = x_line[y_line.argmax()]


# recording process
tape = audio.open(format=mic_format, channels=mic_channels, rate=mic_freq, input=True, frames_per_buffer=mic_chunck)
print('Recording process is on...')

'''we create an array named frames in which we will add in the next loop all the data
the microphone records'''
frames = []
frame_end = int(mic_freq / (mic_chunck) * rec_seconds)
fig, ax2 = plt.subplots()

'''the data aray in this form is in bytes version. We must convert it'''
'''the loop below is responsible for continious esit of the input(microphone) data'''
for i in range(0, frame_end):
    '''read command is responsible for reading the info from the input(in this case the microphone)
    np.frombuffer is an interpreter which transforms the information in a number array'''
    data = np.frombuffer(tape.read(mic_chunck), dtype=np.int16)
    frames.append(data)

    '''Fast Fourier Transformation applied on the input data'''

    fft_data = np.fft.fft(np.abs(data))
    fft_data = abs(fft_data)
    y_line = fft_data[10:len(fft_data) - 10]

    '''x_fft represents the x axis of the spectrum. mic_chunck is multiplied with 2
    so it has the same size with y axis(in this case fft_data)'''
    x_fft = np.linspace(0, mic_freq, 2 * mic_chunck)
    x_line = x_fft[10:len(x_fft) - 10]

    '''If i dont use class calculator, the lines below find the maximum amblitude and the frequency of the spectrum'''
    # max_y=max(abs(y_line))
    # max_x=x_line[y_line.argmax()]
    '''the following lines are for plotting graphs for the process above'''
    '''ax2 is for fft, ax1 is for waveform'''

    # calls calculator class
    calc = calculations(y_line, x_line)
    max_y = calc.maximum_y
    max_x = calc.maximum_x
    '''we create a figure in which the spectrum will be displayed'''
    '''we might need to get the figure out of the loop'''

    # fig, (ax,ax2) = plt.subplots(2)

    '''There is also the possibility to plot waveform if we uncomment the following lines 
    and the line above
    
    ax.set_title('Waveform')
    ax.set_xlabel('Num of samples')
    ax.set_ylabel('Amplitude')
    ax.plot(data,'-')
    '''

    # plt.grid()
    # plt.semilogx(x_fft,fft_data)
    # plt.semilogx(max_x,max_y,'ro')
    # plt.xlim(left=0)
    # plt.ylim(0,1.2*max_y)
    # plt.annotate('max point',xy=(max_x,max_y))
    #
    ax2.clear()
    ax2.grid(which='major')
    ax2.set_title('Spectrum: Christoforos Lefkiou, Michalis Lefkiou')
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel('Amplitude')
    ax2.set_xlim(10, mic_freq)
    '''we exclude for x axis the value 0 because there is the highest value for some reason.
    that's why we start from point 10 in y axis'''
    ax2.set_ylim(bottom=0, top=1.2 * max(fft_data[10:len(fft_data)]))

    ax2.semilogx(x_fft, fft_data, '-')
    ax2.semilogx(max_x, max_y, 'ro')
    ax2.annotate(str(round(max_x)), xy=(max_x, max_y))
    print('Frequency: ', max_x, 'Amptitude: ', max_y)

    plt.show()
    plt.pause(1 / 60)

print('The recording is over')

'''the following lines stop the recording process after the time we have given'''
tape.stop_stream()
tape.close()
audio.terminate()

'''The lines below create and save the recording file in the directory of the python file
    it is required to determine the characteristics of microphone to procced'''
waveFile = wave.open('output.wav', 'wb')
waveFile.setnchannels(mic_channels)
waveFile.setsampwidth(audio.get_sample_size(mic_format))
waveFile.setframerate(mic_freq)
waveFile.writeframes(b''.join(frames))
waveFile.close()
