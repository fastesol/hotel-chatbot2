from platform import system
import datatest
import datetime
from AIResponse import AIA as aia
import tempfile
import subprocess
import io
import os

class Utils():
    def __init__(self) -> None:
        self.system=system()
    """validating the date format to be 'YYYY-mm-dd'"""

    @staticmethod
    def convert_audio_to_wav(audio_data):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_input_file:
                temp_input_file.write(audio_data)
                temp_input_file.flush()
                
                command = [
                    "ffmpeg",
                    "-y",  # Overwrite output files without asking
                    "-i", temp_input_file.name,  # Input file
                    temp_wav_file.name  # Output file
                ]
                
                subprocess.run(command, check=True)
                temp_input_file.close()
                temp_wav_file.flush()
                wav_data = None
                with open(temp_wav_file.name, 'rb') as f:
                    wav_data = f.read()
                temp_wav_file.close()   
                os.remove(temp_input_file.name)
                os.remove(temp_wav_file.name) 
                return io.BytesIO(wav_data)


    def strftime_format(self,format):
        def func(value):
            try:
                datetime.datetime.strptime(value, format)
            except ValueError:
                return False
            return True
        func.__doc__ = f'should use date format {format}'
        return func

    def validateDate(self ,json):
        validDate = False
        while(not validDate):
            validDate = True
            try:
                datatest.validate(json['check_in'] ,self.strftime_format('%Y-%m-%d'))
                datatest.validate(json['check_out'],self.strftime_format('%Y-%m-%d'))
            except datatest.ValidationError:
                validDate = False
                aia.setUserMessage("Reformat all dates to 'YYYY-mm-dd' then return the json again")
                json = aia.getResponse()
                json=eval( self.response[self.response.find("{"):self.response.rfind("}")+1])
                print("new JSON: ", json, "\n\n")
        return json

    
    """correcting the path if the current platform is not windows"""
    def os_path(self,path):
        if self.system != 'Windows':
            path = path.replace("\\", "/")
        del self.system
        return path
