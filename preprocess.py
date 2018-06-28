import matplotlib.pyplot as plt
from scipy.fftpack import rfft, irfft
from scipy.io import wavfile # get the api
import numpy as np
from scipy.signal import butter, iirdesign, freqz, lfilter


def smooth(x, window_len=25,window='hanning'):
    if x.ndim != 1 or x.size < window_len:
        print("no")

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        print("no")

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def process_and_save(src, dst):
    """
    src : source file of .wav
    dst : destination file for .wav
    destination is 1 second long with 1600 sampling rate
    """
    # load wav file and load data
    #fs, data = wavfile.read(src) # load the data
    #data = data.T[0]

    data = np.load(src)
    fs = int(1./data[0])
    data = data[1:]

    # apply bandpass and 
    out = butter_bandpass_filter(data, 50, 650, fs)
    out = out/np.max(np.abs(out))
    avg = np.mean(np.sqrt(np.abs(out)))

    # cutoff-ish and then smooth
    out[np.abs(out) > 5*avg] = 0
    out = smooth(out, window_len=25,window="hanning")

    # need to possibly resample at 16,000
    wavfile.write(dst, 1400, out)


def graph_and_save(src, dst):
    """
    src : source file of .npy 
    dst : destination file for .png for matplotlib
    destination is 1 second long with 1600 sampling rate
    """
    data = np.load(src)
    interval = data[0]
    data = data[1:]
    time_data = np.arange(2800)*interval

    plt.figure()
    plt.plot(time_data, data)
    plt.savefig(dst)


if __name__ == "__main__":
    import os
    graph = True
    # assumes files only located in word directories
    for folder, subdirList, fileList in os.walk("./data/raw"):
        word = folder.split('/')[-1]
        for f in fileList:
            src = folder + '/' + f
            if graph:
                dst = "./data/graphs/" + word + '/' + f[:-3] + "png"
                graph_and_save(src, dst)
            else:
                dst = "./data/processed/" + word + '/' + f[:-3] + "wav"
                process_and_save(src, dst)
            print("process: ", src, " to ", dst)
