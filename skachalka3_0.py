from pytube import YouTube
import whisper
import json
import os
import re

model = whisper.load_model("tiny")  # or "small", "medium", "large", "tiny"gf

# output_audio_file = ""
# output_audio_file_title = ""
output_dir=r"C:\Users\putni\Desktop\skachalka";

class YouTubeHelper:

    @staticmethod
    def get_youtube_id(url):
        regex = r"(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, url)
        if match:
            return match.group(1)
        return None
    
def starter():
    url = input("Enter the URL of the YouTube video: ")
    word_to_search = input("Слово поиска: ")
    file_path = download_audio(url)
    print('FILE PATH: ', file_path)
    json_path = convert_audio_to_text(file_path)
    search_data(json_path, word_to_search)
    
def download_audio(url):
    # global output_audio_file
    # global output_audio_file_title
    
    # print(torch.__version__)
    try:
        video_id = YouTubeHelper.get_youtube_id(url)
        print("-==log VIDEO ID: ", video_id)
        output_audio_file = video_id + '.mp3'
        output_audio_path = output_dir + '\\' + output_audio_file
        print('-== log output_audio_path ', output_audio_path)
        
        if os.path.exists(output_audio_path):
            print('-== CACHE EXCISTS ', output_audio_path)
            return output_audio_path
        
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        print("-==log AUDIO STREAM RECEIVED: ")
        # output_audio_file = yt.title + '.mp3'
        
        # output_audio_file_title = yt.title
        print("-==log AUDIO FILE NAME: ", output_audio_file)
        
        audio_path = audio_stream.download(output_path=output_dir, filename=output_audio_file)
        print("-==log AUDIO STREAM DOWNLOADED")
        print("-==log AUDIO FILE PATH: ", audio_path)
        return audio_path
    except Exception as e:
        print(f"Error: {e}")
        
def convert_audio_to_text(file_path):
    file_name = output_dir + '\\' + os.path.basename(file_path)
    output_file_JSON = file_name + '_JSON' + '.txt';
    
    if os.path.exists(output_file_JSON):
            print('-== DB CACHE EXCISTS ', output_file_JSON)
            return output_file_JSON
        
    result = model.transcribe(file_path)
    
    res = ''
    for segment in result["segments"]:
        res += '[start: '+ str(segment['start']) + ' end: '+ str(segment['end'])+ '] ' + str(segment['text'])
        res += '\n'
        
    with open(output_file_JSON, "w") as file:
        json.dump(result, file, indent=4)
    
    return output_file_JSON

def search_data(json_path, keyword):
    
    data = ''
    with open(json_path, 'r') as file:
        data = json.load(file)

    videoId = os.path.basename(json_path)
    res = ''
    for segment in data["segments"]:
        if keyword in segment['text']:
            link_txt = generate_youtube_link(videoId, segment['start'])
            res += '[start: '+ str(segment['start']) + ' end: '+ str(segment['end'])+ '] ' + str(segment['text'] + ' URL: ' + link_txt)
            res += '\n'
            print('[start: ', segment['start'], ' end: ', segment['end'], '] ' , segment['text']  + ' URL: ' + link_txt)

def generate_youtube_link(video_id, seconds):
    return f"https://www.youtube.com/watch?v={video_id}&t={seconds}s"


starter()