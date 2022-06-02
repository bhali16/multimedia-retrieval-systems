from flask import Flask, render_template, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict
import matplotlib.pyplot as plt
from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import numpy as np
import glob
from scipy.spatial import distance
import os
import json

app = Flask(__name__)
app.secret_key = "Bhalee ki secret key"

#Search Route
@app.route('/')
def index():
    return render_template('index.html')

#Results Route
@app.route('/search', methods=['POST', 'GET'])
def results():
    RESULTS_ARRAY = []
    if request.method == "POST":
        file = request.files['audio']
        file.save(os.path.join('uploads', file.filename))
        filepath = '.\\uploads\\' + file.filename
        get_query_mfcc = generate_mfcc(filepath)
        query_mfcc_file = 'queryfile.txt'
        mfcc_files = get_mfcc_paths()
        query_file = file.filename
        query_file_id = query_file.split(".")
        query_file_id = query_file[0]
        for f in mfcc_files:
            score = find_distance(query_mfcc_file, f)
            fileno = f[25:]
            fileno = fileno.split(".")
            fileno = fileno[0]
            RESULTS_ARRAY.append({"audio": str(fileno), "score": int(score)})

        sorted_audios = sorted(RESULTS_ARRAY, key = lambda i: i['score'])
    return render_template('results.html',query_audio=query_file,qurey_id=query_file_id,audio_results=sorted_audios)


def get_mfcc_paths():
    mfccFiles = []
    i = "identifier"
    basePath = r"./system/mfcc_text_files/"
    files = glob.glob(os.path.join(basePath, '*.txt'.format(i)))
    if files:
        for file in files:
            mfccFiles.append(file)
    else:
        print("No File in Directory")

    return mfccFiles

def generate_mfcc(audiopath):
    (rate,sig) = wav.read(audiopath, 'rb')
    mfcc_features_audio = mfcc(sig,rate)
    f = open("queryfile.txt", "w")
    for row in mfcc_features_audio:
        np.savetxt(f, row)
    f.close()

def find_distance(file1, file2):
    print('file1: ',file1,'file2: ',file2)
    file1 = np.loadtxt(file1, dtype=int)
    file2 = np.loadtxt(file2, dtype=int)
    if file1.size >= file2.size:
        arr2 = file1[0:file2.size]
        arr1 = file2
    elif file2.size >= file1.size:
        arr1 = file1
        arr2 = file2[0:file1.size]
    
    dist = distance.euclidean(arr1, arr2)
    return dist

# run!
if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)