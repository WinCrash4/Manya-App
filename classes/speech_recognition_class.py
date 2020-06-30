import speech_recognition as SpeechRecognitionModule


class SpeechRecognition:
    def __init__(self, deviceIndex=1):
        self.deviceIndex = deviceIndex
        self.recognizer = SpeechRecognitionModule.Recognizer()

        with SpeechRecognitionModule.Microphone(device_index=self.deviceIndex) as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def recognize(self):
        with SpeechRecognitionModule.Microphone(device_index=self.deviceIndex) as source:
            audio = self.recognizer.listen(source)

        try: 
            result = {
                "error": False, 
                "text": self.recognizer.recognize_google(audio, language="ru-RU")
            }
            return result
  
        except SpeechRecognitionModule.UnknownValueError:
            return {
                "error": True, 
                "text": "Error: Can't recognize command"
            }

        except SpeechRecognitionModule.RequestError:
            return {
                "error": True, 
                "text": "Error: Check internet connection"
            }
            
        return {
            "error": True, 
            "text": "Error: Unknown error in speech recognize function"
        }
