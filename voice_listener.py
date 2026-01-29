from vosk import Model, KaldiRecognizer
from func import resolve_action, brain_chooses
import pyaudio, subprocess, json, sys

#LOAD JSON CONFING - OS DEPENDENT
with open("cases.json") as f:
    CONFIG = json.load(f)
    f.close()

#-------------------------------------------------------------
#LISTENER-MODEL AGNOSTIC
#-------------------------------------------------------------
model = Model("vosk-model-small-en-us-0.15")

#Handle the vocabulary
with open("lexic.json") as f:
    DICTIONNARY = json.load(f)

with open("cases2.json") as f2:
    CASES = json.load(f2)

#Dynamic container for all grammar
grammar = "["

#Handles app related actions
for app in DICTIONNARY["apps"]:
    for action in CASES["apps"][app].keys():
        x = '"' + action + ' ' + app + '"'
        print(x)
        grammar = grammar + x + ","

grammar = grammar[:-1]
grammar += "]"
print(grammar)



#OLD GRAMMAR
#grammar = '["terminate delta", "open brave", "open atom", "close brave", "close atom"]'

#INITIAL LISTENING
recognizer = KaldiRecognizer(model, 16000, grammar)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

#LISTENER KILLSWITCH
BOOL_RUNNER = True

while BOOL_RUNNER:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):

        result = json.loads(recognizer.Result())
        text = result["text"]

        print(recognizer.Result())
        print(text)

        if text != "":
            if text == "terminate delta" or text == "kill delta":
                BOOL_RUNNER=False
            else:
                brain_chooses(text, CONFIG)

print("shutting down")
stream.stop_stream()
stream.close()
mic.terminate()
