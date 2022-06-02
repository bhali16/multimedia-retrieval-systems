import matplotlib.pyplot as plt
from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import numpy as np
import glob
import os
import pymongo
import numpy as np
import pickle
from pymongo import MongoClient
from bson.binary import Binary

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

def generate_mfcc(fileno,audiopath):
    (rate,sig) = wav.read(audiopath, 'rb')
    mfcc_features_audio = mfcc(sig,rate)
    #features = mfcc_features_audio.tolist()
    features = {'cpickle': Binary(pickle.dumps(mfcc_features_audio, protocol=2))}
    # Insert Record in MongoDB
    mydict = { "audiopath": audiopath, "features": features }
    mycol.insert_one(mydict)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase1"]
mycol = mydb["audio_features"]


for fileno, audiofile in enumerate(audio_files):
    generate_mfcc(fileno, audiofile)
