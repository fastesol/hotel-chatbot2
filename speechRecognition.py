import  speech_recognition as sr
from utils import Utils



class STT():
    def __init__(self, AudioSourceFile=None):
        """
        AudioSourceFile: is the path to the mp3 or wav file. if the source of the audio is from an audio file, if the source from the mic keep is as None
        """
        self.speechRecog=sr.Recognizer() # object to process the audio and converte it to text.
        self.audio = None #audio data if the source is from the mic
        self.audioDataReady = 0 #to check if the audio data is ready (used if the source is from the mic)
        self.isSystemListening = 0 #used to check if the system is listening through the mic or not
        self.AudioSourceFile = AudioSourceFile

        """if the source is an audio file and the audio file is mp3 convert it to wav format, since the recognizer works only with wav formats"""
        if self.AudioSourceFile!=None and "mp3" in self.AudioSourceFile:
            import subprocess
            import os
            subprocess.call(['ffmpeg', '-i', self.AudioSourceFile,r".\tts_output\output.wav"])
            os.remove(self.AudioSourceFile)
            self.AudioSourceFile =r".\tts_output\output.wav"

    def listen(self):
        """
        This method is used to listen through default mic and prepare an audio.
        """
        if  self.AudioSourceFile==None:
            if(not self.isSystemListening): #check if the system is already listeing to not create multiple instances for listening.
                self.isSystemListening = 1
                with sr.Microphone() as src: #use default mic
                    
                    while(not self.audioDataReady): #listen until there is audio data to be processed.
                        try:
                            print('Say something....')
                            self.audio=self.speechRecog.listen(src, timeout=10, phrase_time_limit=None)
                            self.audioDataReady=1
                                
                        except sr.WaitTimeoutError:
                            continue
                self.isSystemListening=0
            else:
                raise Exception("System is already listening. Listen method can be called only once.\nYou can't call listen method a second time until the first listen method finishes")
            
    def getText(self, language="ar-AR",audio_data=None):
         """
         this method is used to convert the audio data into text,
         language: language of the audio data.
         """
         if audio_data!= None: #if the audio data is brought from an aduio file and not from the mic directly
            
            audio_data = Utils.convert_audio_to_wav(audio_data)

        

            audio_file = sr.AudioFile(audio_data)
            with audio_file as source:
                audio_data = self.speechRecog.record(source)
           
            try:
                userSpeech = self.speechRecog.recognize_google(audio_data, language= language)
            except:
                userSpeech = None
            return userSpeech     

         elif(self.audioDataReady): # if the audion data is brought from mic and checking if audio data is ready to be processed.

            try:
                self.audioDataReady=0
                userSpeech=self.speechRecog.recognize_google(self.audio,language=language)
                return userSpeech
            
            except sr.UnknownValueError as U:
                print(U)
            except sr.RequestError as R:
                print(R)
         else:
             raise Exception("Audio data is not ready. use listen method first to get audio data then use getText method to get the text")