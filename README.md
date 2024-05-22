# azureopenai-vision-speech-samples

## Setup Instructions

1. Create a `.env` file in the root directory of the project.
2. Copy the values from the `.envcopy` file and paste them into the `.env` file.
3. Set up a virtual environment using the `requirements.txt` file.
4. Create an Azure Cognitive Services - Computer Vision, Speech and Azure Open AI resources by following the steps in Azure documentation
5. Retrieve the connection details (endpoint and key) from the Azure portal.
6. Update the `.env` file with the appropriate values for the connection details.
7. Create the models for Vision, Whisper, and Text To Speech in the appropriate regions by following the steps in the Azure documentation.
8. Fetch the model names from the Azure Open AI deployments and update the `.env` file 

### Folders

The project contains the following folders:
 
- Vision: Contains code related to GPT 4 vision tasks.
- Whisper: Contains code related to whisper tasks.
- Text To Speech: Contains code related to text-to-speech tasks.
