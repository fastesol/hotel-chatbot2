from openai import OpenAI
from playsound import playsound
import base64

class TTS():
    def __init__(self):
        self.openai = OpenAI(api_key="sk-proj-A8QEabiGhY556kM5Bki9T3BlbkFJTgeXFQ1YDXyXG0lJdPyS",
                              organization="org-kRKVED7K5kqdCCYmM7LW87hn")
        self.response = None
        self.path = None
    
    def generateAudio(self,text:str, returnType="base64"):
        self.response = self.openai.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=text
        )
        if returnType=="base64":
            return base64.b64encode(self.response.read())
        else:
            return self.response.read()
    
    def saveAudioToFile(self, path):
        self.path = path
        from platform import system
        system = system()
        if system != 'Windows':
            self.path = path.replace("\\", "/")
        del system
        import os
        os.remove(self.path)
        
        with open(self.path, mode="wb") as f:
            for data in self.response.iter_bytes():
                f.write(data)
    
    def play_audio(self, path=None):
        if path is None:
            path = self.path
        playsound(path)