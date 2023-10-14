import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import pyaudio 
import wave
from scipy.fftpack import fft
from scipy import signal

'''we write the characteristics of our pc microphone'''
mic_format = pyaudio.paInt16
mic_channels = 2
mic_freq = 44100
mic_chunck = 1024 
rec_seconds = 15
wave_output_filename = 'assigment_rec.wav'

audio = pyaudio.PyAudio()


#recording process
tape = audio.open(format = mic_format, channels = mic_channels, rate = mic_freq , input = True , frames_per_buffer = mic_chunck )
print('Recording process is on...')

'''we create an array named frames in which we will add in the next loop all the data
the microphone records'''
frames=[]
frame_end=int(mic_freq/(mic_chunck) * rec_seconds)
fig, ax2 = plt.subplots()

'''the data aray in this form is in bytes version. We must convert it'''
for i in range(0,frame_end):
    '''read command is responsible for reading the info from the input(in this case the microphone)
    np.frombuffer is an interpreter which transforms the information in a number array'''
    data = np.frombuffer(tape.read(mic_chunck),dtype=np.int16)
    frames.append(data)  
    
    '''Fast Fourier Transformation applied on the input data'''
  
    fft_data=fft(np.abs(data))
    '''x_fft represents the x axis of the spectrum. mic_chunck is multiplied with 2
    so it has the same size with y axis(in this case fft_data)'''
    x_fft=np.linspace(0,mic_freq,2*mic_chunck)
    
    '''the following lines are for plotting graphs for the process above'''
    '''ax2 is for fft, ax1 is for waveform'''    
     
    #fig, (ax,ax2) = plt.subplots(2)

    #ax.set_title('Waveform')
    #ax.set_xlabel('Num of samples')
    #ax.set_ylabel('Amplitude')
    #ax.plot(data,'-')
    
    ax2.clear()
    ax2.set_title('Spectrum')
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel('Amplitude')
    ax2.set_xlim(10,5000)
    ax2.set_ylim(bottom=0,top=5000000)
    ax2.semilogx(x_fft,fft_data,'-')
    
    plt.show()
    plt.pause(1/600)
   
    
    
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



