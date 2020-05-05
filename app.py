from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import os
from pathlib import Path



def sample_long_running_recognize_uri(storage_uri):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """
    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    file_object = open('speechText.txt', 'a')
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
      #   print(u"Transcript: {}".format(alternative.transcript))
        file_object.write(alternative.transcript)

    file_object.close()

def sample_long_running_recognize(local_file_path):
    """
    Transcribe a long audio file using asynchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
   #  encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    config = {
        "language_code": language_code,
      #   "sample_rate_hertz": sample_rate_hertz,
      #   "encoding": encoding,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))

def get_local_file_path():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--local_file_path", type=str, default="resources/hello.wav")
    parser.add_argument("--model", type=str, default="phone_call")
    args = parser.parse_args()
    local_file_path = os.path.join(root_dir, "wav", "TheTale.flac")
    sample_recognize(wav_path, args.model)

def main():
    root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(root_dir,"SpeechToText.json")
   
    sample_long_running_recognize_uri(storage_uri)


if __name__ == "__main__":
    main()