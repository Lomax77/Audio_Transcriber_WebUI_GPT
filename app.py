from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__) # create flask app

openai.api_key = "YOUR_API_KEY"

@app.route('/') # home page
def index():
    return render_template('index.html') # render index.html

@app.route('/transcribe', methods=['POST']) # transcribe audio
def transcribe():
    if 'audio_file' not in request.files:
        return render_template('index.html', error='No audio file selected.') # error if no file selected
    
    audio_file = request.files['audio_file']

    if audio_file.filename == '':
        return render_template('index.html', error='Audio file is empty.') # error if file is empty
    
    audio_path = f'tmp/{audio_file.filename}' # save file to tmp folder
    audio_file.save(audio_path)          # save file to tmp folder

    try:
        transcription = transcribe_audio(audio_path)
        return render_template('index.html', transcription = transcription) # render index.html with transcription
    
    except Exception as e:
        return render_template('index.html', error = str(e)) # render index.html with error
    
def transcribe_audio(audio_path):
    file = open(audio_path, "rb") # open audio file

    response = openai.Audio.transcribe("whisper-1", file) # transcribe audio file

    transcription = response["text"] # get transcription

    return transcription # return transcription

if __name__ == '__main__':
    os.makedirs('tmp', exist_ok=True) # create tmp folder if it doesn't exist

    app.run(debug=True) # run app in debug mode