import json
import os
from openai import AzureOpenAI
import base64
from mimetypes import guess_type
from fetchenvironmentvalues import EnvironmentFetcher, EnvironmentVariables

print("Starting the process to Analyse the image \n")

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

## get the image base64
def get_image_base64(promptmsg):
    imagefound = False
    data_url = ""

    while not imagefound:
        imagepath = input(promptmsg)

        if (not imagepath.startswith("\\")): imagepath = "\\" + imagepath

        # Get the parent directory of the current script
        parent_dir = os.path.dirname(__file__)

        # Combine the parent directory and relative path to get the absolute path
        imagepath = os.path.join(parent_dir + imagepath)

        if not os.path.exists(imagepath):
            print("The image file does not exist. Please enter a valid path.")
        else:
            imagefound = True
        
    # Check if http or not and return data in base64
    if not("http" in imagepath or "https" in imagepath):
        print("Encoding the image into a data URL \n")
        image_path = imagepath ## Provide the path with respect to Parent folder
        data_url = local_image_to_data_url(image_path)
    
    return data_url

inputImagedata = get_image_base64("Please enter the relative path of the image file you want to analyse: ")
refImageData = get_image_base64("Please enter the relative path of the reference image file: ")        
jsonpref = input("Do you want the output in JSON format? (Y/N): ")


print("Creating the Azure Open AI Client. \n")
## Create the Azure Open AI client
client = AzureOpenAI(
    api_key= EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_API_KEY1),  
    api_version= EnvironmentFetcher.get_variable(EnvironmentVariables.API_VERSION),
    azure_endpoint = EnvironmentFetcher.get_variable(EnvironmentVariables.AZURE_OPENAI_ENDPOINT1)
)

deployment_name = EnvironmentFetcher.get_variable(EnvironmentVariables.VISION_DEPLOYMENT_NAME) 
imageURL = EnvironmentFetcher.get_variable(EnvironmentVariables.IMAGEURL)

sysmsg = """
You're a professional defect detector.
Your job is to compare the test image with reference image, please answer the question with "No defect detected" or "Defect detected", 
also explain your decision as detail as possible. 
"""
sysmsgjson = """
You're a professional defect detector.
Your job is to compare the test image with reference image, please answer the question with "No defect detected" or "Defect detected", 
also explain your decision as detail as possible.
Return the output in JSON format with type of defect, the location of the defect in X and Y coordinates and serverity of the defect. Also provide a defect confidence score from 0 to 1 based on the refernce image.
"""

print("Calling Azure Open AI endpoint to analyse the image. Waiting for response.. \n")
## Call the Azure Open AI endpoint to analyse the image using the local Data Url
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        { "role": "system", "content": sysmsgjson if jsonpref.lower() == 'y' else sysmsg},
        { "role": "user", "content": [
            {
                "type": "text",
                "text": "Here is the reference image",  # Pass the prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"{refImageData}"  # Pass the encoded reference image
                },
            },
            {
                "type": "text",
                "text": "Here is the test image",  # Pass the prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"{inputImagedata}"  # Pass the encoded test image
                }, 
            },
        ],
        } 
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

