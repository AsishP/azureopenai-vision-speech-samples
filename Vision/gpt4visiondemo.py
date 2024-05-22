import json
import os
from openai import AzureOpenAI
import base64
from mimetypes import guess_type
from fetchenvironmentvalues import EnvironmentFetcher, EnvironmentVariables

print("Starting the process to Analyse the image \n")

imagefound = False

## Capturing inputs from the user
while not imagefound:
    imagepath = input("Please enter the relative path of the image file you want to analyse: ")

    if (not imagepath.startswith("\\")): imagepath = "\\" + imagepath

    # Get the parent directory of the current script
    parent_dir = os.path.dirname(__file__)

    # Combine the parent directory and relative path to get the absolute path
    imagepath = os.path.join(parent_dir + imagepath)

    if not os.path.exists(imagepath):
        print("The image file does not exist. Please enter a valid path.")
    else:
        imagefound = True
        
text = input("Please enter the text you want to analyse the image with: ")
jsonpref = input("Do you want the output in JSON format? (Y/N): ")

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

# Example usage
if not("http" in imagepath or "https" in imagepath):
    print("Encoding the image into a data URL \n")
    image_path = imagepath ## Provide the path with respect to Parent folder
    data_url = local_image_to_data_url(image_path)

print("Creating the Azure Open AI Client. \n")
## Create the Azure Open AI client
client = AzureOpenAI(
    api_key= EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_API_KEY1),  
    api_version= EnvironmentFetcher.get_variable(EnvironmentVariables.API_VERSION),
    azure_endpoint = EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_ENDPOINT1)
)

deployment_name = EnvironmentFetcher.get_variable(EnvironmentVariables.VISION_DEPLOYMENT_NAME) 
imageURL = EnvironmentFetcher.get_variable(EnvironmentVariables.IMAGEURL)

sysmsg = "You are a helpful assistant that analyses images with descriptive analysis divided into paragraphs."
sysmsgjson = "You are a helpful assistant that analyses images and provides a description of various elements in the picture and generate output in raw JSON format."

print("Calling Azure Open AI endpoint to analyse the image. Waiting for response.. \n")
## Call the Azure Open AI endpoint to analyse the image using the local Data Url
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": sysmsgjson if jsonpref.lower() == 'y' else sysmsg},
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "{}".format(text) 
            },
            { 
                "type": "image_url", ##Image Url can be a SAS url or public accessible image
                "image_url": {
                    "url": "{0}".format(data_url)
                }
            }
        ] } 
    ],
    max_tokens=2000 
)

## Print the response from the Azure Open AI endpoint
print("Got response from the Azure Open AI endpoint \n")
responseval = response.choices[0].message.content

if responseval == "":
    print("No response from the model")
    exit();

if "json" in responseval:
    s = responseval
    # Remove '```json\n' from the start and '\n```' from the end
    s = s[7:-4]
    responseval = s
    print("Outputting the response \n")
    responsejson = json.loads(responseval)
    pretty_object = json.dumps(responsejson, indent=4)
    print("Response output: \n", pretty_object)
else:
    print("Response: \n", responseval)

