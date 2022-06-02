import matplotlib.pyplot as plt
from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import numpy as np
import glob
import os


def get_audio_paths():
    audioFiles = []
    i = "identifier"
    basePath = r"../assets/new_wav/"
    files = glob.glob(os.path.join(basePath, '*.wav'.format(i)))
    if files:
        for file in files:
            audioFiles.append(file)
    else:
        print("No File in Directory")

    return audioFiles

audio_files = get_audio_paths()

def generate_mfcc(audiopath):
    fileno = audiopath[18:]
    fileno = fileno.split(".")
    fileno = fileno[0]
    (rate1,sig1) = wav.read(audiopath, 'rb')
    mfcc_features_audio = mfcc(sig1,rate1)
    f = open("./mfcc_text_files/new/"+str(fileno) + ".txt", "w")
    for row in mfcc_features_audio:
        np.savetxt(f, row)
    f.close()

    # plt.plot(mfcc_features_audio)
    # plt.show()


for fileno, audiofile in enumerate(audio_files):
    generate_mfcc(audiofile)
