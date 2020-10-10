import keras
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import string
import re
from flask import Flask
#hello
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

keras.backend.clear_session()
    
t = pickle.load(open('t' , "rb"))

Xlen = 30#max([len(i) for i in q])
Ylen = 30#max([len(i) for i in a])

Xvocab = 15000#len(t.word_index) + 1
Yvocab = 15000#len(t.word_index) + 1

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

units = 100

inp1 = keras.layers.Input(shape=(Xlen , ))
enc1 = keras.layers.Embedding(Xvocab , 100 ,input_length = Xlen)(inp1)
enc1 = keras.layers.LSTM(units , return_sequences = True)(enc1)
enc1 = keras.layers.Dropout(0.5)(enc1)
enc1 = keras.layers.BatchNormalization()(enc1)

attention = keras.layers.Dense(1, activation='tanh')(enc1)
attention = keras.layers.Flatten()(attention)
attention = keras.layers.Activation('softmax')(attention)
attention = keras.layers.RepeatVector(units)(attention)
attention = keras.layers.Permute([2, 1])(attention)

sent_representation = keras.layers.multiply([enc1, attention])
sent_representation1 = keras.layers.Lambda(lambda xin: keras.backend.sum(xin, axis=-2), output_shape=(units,))(sent_representation)

inp2 = keras.layers.Input(shape=(Ylen, ))
enc2 = keras.layers.Embedding(Yvocab , 100, input_length = Ylen)(inp2)
enc2 = keras.layers.LSTM(units , return_sequences = True)(enc2)
enc2 = keras.layers.Dropout(0.5)(enc2)
enc2 = keras.layers.BatchNormalization()(enc2)

attention = keras.layers.Dense(1, activation='tanh')(enc2)
attention = keras.layers.Flatten()(attention)
attention = keras.layers.Activation('softmax')(attention)
attention = keras.layers.RepeatVector(units)(attention)
attention = keras.layers.Permute([2, 1])(attention)

sent_representation = keras.layers.multiply([enc2, attention])
sent_representation2 = keras.layers.Lambda(lambda xin: keras.backend.sum(xin, axis=-2), output_shape=(units,))(sent_representation)

decoder = keras.layers.add([sent_representation1,sent_representation2])
out = keras.layers.Dense(Yvocab , activation='softmax')(decoder)

model = keras.models.Model(inputs = [inp1,inp2] , outputs = out)

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy')
model.load_weights('di.hdf5')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def prediction(model , inp_que , inp = '' , totlen=Ylen):

  que = pad_sequences(t.texts_to_sequences([inp_que]) , maxlen = Xlen , padding='pre' , truncating = 'pre')
  if inp == '':
    text = 'startseq'
  else:
    text = 'startseq ' + inp
  for i in range(totlen):
    ans = pad_sequences(t.texts_to_sequences([text]) , maxlen = Ylen , padding='pre' , truncating = 'pre')
    y_pred = t.sequences_to_texts([[np.argmax(model.predict([que.reshape(1,Xlen) , ans.reshape(1,Ylen)]))]])[0]

    text += ' ' + y_pred

    if y_pred == 'endseq':
      break

  return text

re_print = re.compile('[^%s]' % re.escape(string.printable))
table = str.maketrans('' , '' , string.punctuation)

def clean(docs , l=True):

  cleaned = []

  for line in docs:
    
    line = ''.join([x if x in string.printable else '' for x in line])
    line = line.lower()

    for i in string.punctuation:
      line = line.replace(i,'')

    line = ' '.join([word for word in line.split() if word.isalpha()])
    line = 'startseq ' + line + ' endseq'

    cleaned.append(line)

  return cleaned
    
@app.route('/<process>')
@cross_origin()
def index(process):
    
    keras.backend.clear_session()
    process = process.replace('_' , ' ')
    process = clean([process])
    print(process)
    return prediction(model , process[0])[9:-7]
    keras.backend.clear_session()

if __name__ == "__main__":
    app.run()
