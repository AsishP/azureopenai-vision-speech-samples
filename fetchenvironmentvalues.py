import os
from enum import Enum
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

class EnvironmentVariables(Enum):
    SPEECH_KEY = "SPEECH_KEY"
    SPEECH_REGION = "SPEECH_REGION"
    AZURE_OPENAI_API_KEY1 = "AZURE_OPENAI_API_KEY1"
    AZURE_OPENAI_API_KEY2 = "AZURE_OPENAI_API_KEY2"
    AZURE_OPENAI_ENDPOINT1 = "AZURE_OPENAI_ENDPOINT1"
    AZURE_OPENAI_ENDPOINT2 = "AZURE_OPENAI_ENDPOINT2"
    API_VERSION = "API_VERSION"
    WHISPER_DEPLOYMENT_NAME = "WHISPER_DEPLOYMENT_NAME"
    DEPLOYMENT_NAME = "DEPLOYMENT_NAME"
    IMAGEURL = "IMAGEURL"
    DESTINATION_CONTAINER_URL = "DESTINATION_CONTAINER_URL"
    WHISPERMODELID = "WHISPERMODELID"
    VISION_DEPLOYMENT_NAME = "VISION_DEPLOYMENT_NAME"
    COMPUTERVISIONENDPOINT = "COMPUTERVISIONENDPOINT"
    COMPUTERVISIONKEY = "COMPUTERVISIONKEY"
    VISION_API_VERSION = "VISION_API_VERSION"
    VIDEOURL1 = "VIDEOURL1"
    VIDEOURL2 = "VIDEOURL2"
    VIDEOINDEXERENPOINT = "VIDEOINDEXERENPOINT"
    VIDEOINDEXERKEY = "VIDEOINDEXERKEY"
    TTS_SPEECH_KEY = "TTS_SPEECH_KEY"
    TTS_SPEECH_REGION = "TTS_SPEECH_REGION"
    TTS_DEPLOYMENT_NAME = "TTS_DEPLOYMENT_NAME"
    TTS_API_VERSION = "TTS_API_VERSION"
    VISION_API_VERSION_E = "VISION_API_VERSION_E"

class EnvironmentFetcher:
    @staticmethod
    def get_variable(env_var: EnvironmentVariables) -> str:
        return os.getenv(env_var.value, "")
    
    @staticmethod
    def get_contentUrls() -> list:
        return [
                    "https://crbn.us/hello.wav",
                    "https://crbn.us/whatstheweatherlike.wav"
                ]

# Example usage
##api_key = EnvironmentFetcher.get_variable(EnvironmentVariables.API_KEY)
#print(EnvironmentFetcher.get_variable(EnvironmentVariables.SPEECH_KEY))
#print('Hello')
