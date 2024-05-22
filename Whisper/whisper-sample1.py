import os
from openai import AzureOpenAI
from playsound import playsound
import threading
import time
from fetchenvironmentvalues import EnvironmentFetcher, EnvironmentVariables

print("Creating the Azure Open AI Client. \n")
client = AzureOpenAI(
    api_key= EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_API_KEY2),  
    api_version= EnvironmentFetcher.get_variable(EnvironmentVariables.API_VERSION),
    azure_endpoint = EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_ENDPOINT2)
)

deployment_name = EnvironmentFetcher.get_variable(EnvironmentVariables.WHISPER_DEPLOYMENT_NAME) #This will correspond to the custom name you chose for your deployment when you deployed a model."
audio_test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Samples/wikipediaOcelot.wav")

def play_audio():
    print("Playing the audio file ...")
    playsound(str(audio_test_file))

def call_azure_open_ai():
    print("Calling the Azure Open AI endpoint to transcribe the audio file. Waiting for response.. \n")
    result = client.audio.transcriptions.create (
        file=open(audio_test_file, "rb"),            
        model=deployment_name
    )
    print("Transcription of the audio file is: \n")
    # print(result.text)

    # Print the result text word by word
    words = result.text.split()
    for word in words:
        time.sleep(0.5)
        print(word, end=" ")
    
# Create and start threads for playing audio and calling Azure Open AI endpoint
audio_thread = threading.Thread(target=play_audio)
api_thread = threading.Thread(target=call_azure_open_ai)

api_thread.start()
time.sleep(5)
audio_thread.start()

# Wait for both threads to finish
audio_thread.join()
api_thread.join()
