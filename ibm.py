from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(
    'Nj4dLesw5ogJ6gVPBJON74AOMEKTEnBz3C2Whh7LS49y')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url(
    'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/9523c78e-dbdf-49cb-a8b9-6751080ac382')

with open('4.wav', 'wbr') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            'First We need to set working directory. for that go to Session. set working directory. choose directory. and open the working directory Make sure the exported text file is here.',
            voice='en-GB_JamesV3Voice',
            accept='audio/wav'
        ).get_result().content)
