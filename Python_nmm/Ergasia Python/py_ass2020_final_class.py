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
rec_seconds = 3
wave_output_filename = 'assigment_rec.wav'

audio = pyaudio.PyAudio()
fig, ax2 = plt.subplots()


class spec_analyzer:
    def __init__(self,mic_format,mic_channels,mic_freq,mic_chunck,rec_seconds,wave_output_filename):
        self.mic_format=mic_format
        self.mic_channels = mic_channels
        self.mic_freq = mic_freq
        self.mic_chunck = mic_chunck
        self.rec_seconds = rec_seconds
        self.wave_output_filename =wave_output_filename

#recording process
    def recording(self):
        self.tape = audio.open(format = self.mic_format, channels = self.mic_channels, rate = self.mic_freq , input = True , frames_per_buffer = self.mic_chunck )
        print('Recording process is on...')

        '''we create an array named frames in which we will add in the next loop all the data
        the microphone records'''
        frames=[]
        frame_end=int(self.mic_freq/self.mic_chunck * self.rec_seconds)


 
        '''the data aray in this form is in bytes version. We must convert it'''
        '''the loop below is responsible for continious esit of the input(microphone) data'''
        for i in range(0,frame_end):
            '''read command is responsible for reading the info from the input(in this case the microphone)
            np.frombuffer is an interpreter which transforms the information in a number array'''
            self.data = np.frombuffer(self.tape.read(self.mic_chunck),dtype=np.int16)
            frames.append(self.data)  
    
            '''Fast Fourier Transformation applied on the input data'''
  
            self.fft_data=abs(fft(np.abs(self.data)))
            self.y_line=self.fft_data[10:len(self.fft_data)-10]
    
            '''x_fft represents the x axis of the spectrum. mic_chunck is multiplied with 2
            so it has the same size with y axis(in this case fft_data)'''
            self.x_fft=np.linspace(0,self.mic_freq,2*self.mic_chunck)
            self.x_line=self.x_fft[10:len(self.x_fft)-10]
    
            '''The lines below find the maximum amblitude and the frequency of the spectrum'''
            self.max_y=max(abs(self.y_line))
            self.max_x=self.x_line[self.y_line.argmax()]
            '''the following lines are for plotting graphs for the process above'''
            '''ax2 is for fft, ax1 is for waveform'''    
     
    
            '''we create a figure in which the spectrum will be displayed'''
            '''we might need to get the figure out of the loop'''

            #fig, (ax,ax2) = plt.subplots(2)
    
            '''There is also the possibility to plot waveform if we uncomment the following lines 
            and the line above
    
            ax.set_title('Waveform')
            ax.set_xlabel('Num of samples')
            ax.set_ylabel('Amplitude')
            ax.plot(data,'-')
            '''
    
            #plt.grid()
            #plt.semilogx(x_fft,fft_data)
            #plt.semilogx(max_x,max_y,'ro')
            #plt.xlim(left=0)
            #plt.ylim(0,1.2*max_y)
            #plt.annotate('max point',xy=(max_x,max_y))
            #
   
            ax2.grid(which='major')
            ax2.set_title('Spectrum')
            ax2.set_xlabel('Frequency')
            ax2.set_ylabel('Amplitude')
            ax2.set_xlim(10,10000)
            '''we exclude for x axis the value 0 because there is the highest value for some reason.
            that's why we start from point 10 in y axis'''
            ax2.set_ylim(bottom=0,top=1.2*max(self.fft_data[10:len(self.fft_data)]))
    
    
            ax2.semilogx(self.x_fft,self.fft_data,'-')
            ax2.semilogx(self.max_x,self.max_y,'ro')
            ax2.annotate('max point',xy=(self.max_x,self.max_y))
            print('Frequency: ',self.max_x,'Amptitude: ',self.max_y)
    
            plt.show()
    
    
    
   
   
    
    
            print('The recording is over')

            '''the following lines stop the recording process after the time we have given'''
            self.tape.stop_stream()
            self.tape.close()
            audio.terminate()


        '''The lines below create and save the recording file in the directory of the python file
        it is required to determine the characteristics of microphone to procced'''
        waveFile = wave.open(self.wave_output_filename, 'wb')
        waveFile.setnchannels(self.mic_channels)
        waveFile.setsampwidth(audio.get_sample_size(self.mic_format))
        waveFile.setframerate(self.mic_freq)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


tape1=spec_analyzer( pyaudio.paInt16,2,44100,1024,3,'apollon.wav')
tape1.recording()