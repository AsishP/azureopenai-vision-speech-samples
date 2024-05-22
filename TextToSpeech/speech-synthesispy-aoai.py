import azure.cognitiveservices.speech as speechsdk
import inquirer
import requests
import json
import os
from tempfile import NamedTemporaryFile
from openai import AzureOpenAI
from fetchenvironmentvalues import EnvironmentFetcher, EnvironmentVariables

print("Starting the process to Synthesize the text \n")
deployment_model = EnvironmentFetcher.get_variable(EnvironmentVariables.TTS_DEPLOYMENT_NAME)

print("Creating the Azure Open AI Client. \n")
## Create the Azure Open AI client
client = AzureOpenAI(
    api_key= EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_API_KEY2),  
    api_version= EnvironmentFetcher.get_variable(EnvironmentVariables.API_VERSION),
    azure_endpoint = EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_ENDPOINT2)
)

vocalchoices = [
  inquirer.List('vocalchoices',
                message="What voice you would like to choose?",
                choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'],
            ),
]


## Neural voice choices - Apr 24
# 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'

vocalchoice = inquirer.prompt(vocalchoices)

text = input("Enter the text you would like to speak > \n")

print("Calling Azure Open AI endpoint to generate the voice based on provided text. Waiting for response.. \n")
## Call the Azure Open AI endpoint to analyse the image using the local Data Url
requestbody = {
    "model" : EnvironmentFetcher.get_variable(EnvironmentVariables.TTS_DEPLOYMENT_NAME),
    "input":  text,
    "voice" :  vocalchoice['vocalchoices']
}

requestEndPoint = "{0}openai/deployments/{1}/audio/speech?api-version={2}".format(EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_ENDPOINT2), EnvironmentFetcher.get_variable(EnvironmentVariables.TTS_DEPLOYMENT_NAME), EnvironmentFetcher.get_variable(EnvironmentVariables.TTS_API_VERSION))

response = requests.post(requestEndPoint, data=json.dumps(requestbody), headers={"Content-Type": "application/json", "api-key" : EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_API_KEY2)})

print("Response from the Azure Open AI endpoint received \n")
if(response.ok):
    try:
        with NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(response.content)
            f.close()
            os.startfile(f.name)
    except Exception as e:
        print("Error in playing the audio file.\n {}\n".format(e))
else:
    print("Found error in the response {}. Exiting... \n".format(response.text))