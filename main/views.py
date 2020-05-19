from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from music21 import converter, instrument, note, chord, stream
import pickle
import os.path as p
import os
import numpy as np
from tensorflow.keras.models import load_model

pathh = './'
# pathh = '/app'

def get_model_ouput(model, notes, seq_len, start = None, num_notes = 100):
    
    pitchnames = sorted(set(notes))
    n_vocab = len(pitchnames)
    len(notes), len(set(notes))
    
    ele_to_int = dict([(ele, i) for i, ele in enumerate(pitchnames)])

    network_input = []
    for i in range(len(notes) - seq_len):
        seq_in = notes[i:i+seq_len]
        network_input.append([ele_to_int[ele] for ele in seq_in])
   
    if start is None:
        start = np.random.randint(len(network_input) - 1)
    
#     Used Later for debugging and validation.
    print('start:', start)
    
    int_to_ele = dict([(i, ele) for i,ele in enumerate(pitchnames)])
    pattern = network_input[start]

    prediction_output = []
    
    for i in range(num_notes):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input/n_vocab

        prediction = model.predict(prediction_input)
        idx = np.argmax(prediction)

        result = int_to_ele[idx]

        prediction_output.append(result)

        pattern.append(idx)
        pattern = pattern[1:]
        if i%10 == 0:
            print(i, end = '\r')
        
    return prediction_output
    
def get_output_notes(prediction_output):
    offset = 0
    output_notes = []
    k = 0
    last = len(prediction_output)
    for pattern in prediction_output:

        # if pattern is chord
        if ('+' in pattern) or (pattern.isdigit()):
            notes_in_chord = pattern.split('+')
            temp_notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                temp_notes.append(new_note)
            new_chord = chord.Chord(temp_notes) 
            new_chord.offset = offset
            output_notes.append(new_chord)
            continue

        #if pattern is note
        new_note = note.Note(pattern)
        new_note.storedInstrument = instrument.Piano()
        new_note.offset = offset
        output_notes.append(new_note)

        if k < 5:
            offset += 1.0
            print(k)
        else:
            offset += 0.5
        k += 1
    return output_notes

def get_midi_file(output_notes, save = False, file_name = None):
    
    midi_stream = stream.Stream(output_notes)
    
    if save == True:
        midi_stream.write('midi', fp = file_name)
    
    return midi_stream

def predict():
    with open(pathh + '/static/main/ml/notes', 'rb') as file:
        notes = pickle.load(file)
    if not p.exists("model-5.hdf5"):
        print('Downloading')
        os.system('wget https://www.dropbox.com/s/auun8vngdv2f6jx/model-5.hdf5')
    else:
        print('present')
    print('loading model')
    model = load_model('model-5.hdf5')
    # model = load_model(pathh + 'static/main/ml/model-5.hdf5')
    seq_len = 100

    prediction_output = get_model_ouput(model, notes, 100, num_notes=100)
    output_notes = get_output_notes(prediction_output)
    fname = pathh + '/media/music/AI_music.mid'
    get_midi_file(output_notes, save = True, file_name=fname)
    return fname


# Create your views here.
def index(request):
    if request.method == 'POST': 
        fname = predict()
        # fname = pathh + '/media/music/AI_music.mid'
        with open(fname, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + 'AI_music.mid'
            return response
    
    return render(request, 'main/index.html')
    # return HttpResponse('Hello, This is my Music Generator.')