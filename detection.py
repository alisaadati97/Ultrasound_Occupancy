import requests

import pyaudio
import numpy as np

from time import sleep
""" RealTime Audio Basic FFT plot """

#motion score 
find_ystill = []
Last_score = 0
Train = True
ystill = 0

# VARS CONSTS:
url = "http://127.0.0.1:8000/getdata"

_VARS = {'window': False,
         'stream': False,
         'audioData': np.array([])}

# INIT vars:
CHUNK = 128  # Samples: 1024,  512, 256, 128
RATE = 44100  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 1  # Sampling Interval in Seconds ie Interval to listen
TIMEOUT = 10  # In ms for the event loop
GAIN = 10
pAud = pyaudio.PyAudio()

# FUNCTIONS:

def senddata():

    # Not the most elegant implementation but gets the job done.
    # Note that we are using rfft instead of plain fft, it uses half
    # the data from pyAudio while preserving frequencies thus improving
    # performance, you might also want to scale and normalize the fft data
    # Here I am simply using hardcoded values/variables which is not ideal.
    global Last_score , Train ,ystill 

    barStep = 100/(CHUNK/2)  # Needed to fit the data into the plot.
    fft_data = np.fft.rfft(_VARS['audioData'])  # The proper fft calculation
    fft_data = np.absolute(fft_data)  # Get rid of negatives
    fft_data = fft_data/10000  # ghetto scaling
    
    sumfreq = int(sum(fft_data[54:62]))

    if not Train:
        score = sumfreq - ystill
        if score > 0 :
            payload = {'MotionScoreValue':score}
            requests.post(url, data=payload)
            Last_score = score

    if Train : 
        find_ystill.append(sumfreq)
    
    if len(find_ystill)  == 100 :
        ystill = sum(find_ystill)//len(find_ystill)
        Train = False
        Last_score = sumfreq - ystill



# PYAUDIO STREAM :
def callback(in_data, frame_count, time_info, status):
    _VARS['audioData'] = np.frombuffer(in_data, dtype=np.int16)
    return (in_data, pyaudio.paContinue)


def listen():
    _VARS['stream'] = pAud.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK,
                                stream_callback=callback)
    _VARS['stream'].start_stream()



def updateData():
    senddata()


listen()


# MAIN LOOP
while True:
    sleep(0.01)
    if _VARS['audioData'].size != 0:
        updateData()