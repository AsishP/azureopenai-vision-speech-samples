import azure.cognitiveservices.speech as speechsdk
import time
import threading
from fetchenvironmentvalues import EnvironmentFetcher, EnvironmentVariables

print("Starting the process to Synthesize the text \n")
#Set up configuration
speechkey = EnvironmentFetcher.get_variable(EnvironmentVariables.TTS_SPEECH_KEY)
speechregion = EnvironmentFetcher.get_variable(EnvironmentVariables.TTS_SPEECH_REGION)

print("Creating the SSML to speak \n")
ssml_text = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US" xmlns:mstts="https://www.w3.org/2001/mstts">
    <voice name="en-US-NovaMultilingualNeural" effect="eq_car">
        Good morning Onyx! <break /> <s> How are you going? </s>
    </voice>
    <voice name="en-US-OnyxMultilingualNeural" effect="eq_car">
       <break time="750ms" /> Good morning to you too Nova! <s>  <break strength="medium" /> I am going well, thank you for asking. </s>
       <s> So, have you heard about the <sub alias="Text to Speech">TTS</sub> SSML? </s>
    </voice>
    <voice name="en-US-NovaMultilingualNeural" effect="eq_car">
        <break strength="strong" /> <s> Yes, I have heard about it. </s> <break /> <s> <sub alias="Speech Synthesis Markup Language"> SSML </sub> is a markup language that allows developers to control aspects of speech synthesis </s>
        <s> It supports about <say-as interpret-as="cardinal"> 50 </say-as> different tags and <say-as interpret-as="cardinal"> 77 </say-as> locales. </s>
        <s> It can be used to control aspects of speech synthesis such as pronunciation, volume, pitch, rate, etc. too. </s>
    </voice>
    </speak>
    """

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
print("Configuing the speech synthesizer \n")
speech_config = speechsdk.SpeechConfig(subscription=speechkey, region=speechregion)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

def speakingwithssml():
    print("Speaking the SSML \n")
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for the conversation")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

def printssmlwordbyword():
    print("Printing the SSML word by word \n")
    words = ssml_text.split()
    for word in words:
        time.sleep(0.3)
        print(word, end=" ")

# Create and start threads for playing audio and calling Azure Open AI endpoint
ssml_thread = threading.Thread(target=printssmlwordbyword)
speech_thread = threading.Thread(target=speakingwithssml)

ssml_thread.start()
speech_thread.start()

# Wait for both threads to finish
ssml_thread.join()
speech_thread.join()