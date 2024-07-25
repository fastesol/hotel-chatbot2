from speechRecognition import STT 
from AIResponse import AIA 
from TTS import TTS  
from system_roles import sys_manage
from hotelAPI import hotelAPI as hAPI
import json
hApi = hAPI()
tts=TTS()
aia=AIA(hApi.getHotelData(),  hApi.getTravelAgents())
sr=STT()

class chatbot:
    def __init__(self) -> None:
        self.response = ""
        self.ai_audio = None 

    def transfer_audio_data(self,audio_data):
        return sr.getText(language="ar-AR",audio_data=audio_data) 
        

        
    def get_ai_response(self,user_message):
        aia.setUserMessage(user_message)
        self.response = aia.getResponse()
        return self.response
    
    def transfer_response_to_audio(self):
        self.ai_audio = tts.generateAudio(self.response)
        return self.ai_audio

    def confirm_user_choice(self):
        if("json" in self.response.lower() ):
            while (type(self.response) != type({})):
                self.response=json.loads( self.response[self.response.find("{"):self.response.rfind("}")+1])
            if(self.response["json_type"] == 0): # when returned json data has the parameter json type 0: needs rooms available, json type 1: needs to create booking
         
                #collect available rooms and give the chatgpt instructions on how to proceed
                del aia.systemRole["content"]
                aia.systemRole["content"] = sys_manage.base_insturctions(hApi.getHotelData(), hApi.getTravelAgents())+sys_manage.Create_booking_scenario(hApi.getRoomsAvailable(self.response["check_in"], self.response["check_out"])) 
                # updating system role of the chatgpt.
                aia.gMessages.remove(aia.gMessages[0])
                aia.gMessages.insert(0,aia.systemRole)
                self.response = aia.getResponse("none")
            elif(self.response["json_type"] == 1):
                del aia.systemRole["content"]
                aia.systemRole["content"] =sys_manage.base_insturctions(hApi.getHotelData(), hApi.getTravelAgents())+sys_manage.Create_booking_scenario(hApi.getRoomsAvailable(self.response["check_in"], self.response["check_out"])) + sys_manage.confirm_Price(hApi.postBookingPrice(self.response))
                aia.gMessages.remove(aia.gMessages[0])
                aia.gMessages.insert(0,aia.systemRole)
                self.response = aia.getResponse("none")
            elif(self.response["json_type"] == 2):
                bookingNumber= hApi.postCreateBooking(self.response)
                self.terminate(f"لقد تم الحجز بنجاح ورفم الحجز هو {bookingNumber}, شكرا ﻷختياركم فندقنا")
            elif(self.response["json_type"] == 3):
                if (self.response["group_booking"] == 1 and self.response["agency_exist"] == 0):
                    self.terminate("برجاء اضافة وكيل السفر الي موقع الفندق")
                else:
                    self.response = aia.getResponse("none")
            elif(self.response["json_type"] == -1):
                self.terminate("شكرا ﻷستخدامكم لنا")


    
    def terminate(self, endMessage):
        self.response = endMessage
        aia.clearHistory()
        

    def converse(self, audio_data):
        user_speech = self.transfer_audio_data(audio_data=audio_data)

        if user_speech != None:
            self.response = self.get_ai_response(user_speech)
        else:
            self.response = "لم اسمعك جيدا هلا تعد ما قلت"
        self.confirm_user_choice()

        return self.transfer_response_to_audio()