import numpy as np
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
import pygame


class SpeechGenerator:
    def __init__(self):
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        self.speaker1_embeddings = torch.tensor(
            load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")[7306]["xvector"]).unsqueeze(0)
        self.speaker2_embeddings = torch.tensor(
            load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")[1306]["xvector"]).unsqueeze(0)
        self.speech_list = []

    def add_turn(self, utterance:str, voice=1):

        utterance=utterance.replace("-", " ")
        if len(utterance.split()) > 50:
            # Split the utterance into sentences
            sentences = utterance.split('.')

            # Remove empty strings from the list
            sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

            # Iterate through the sentences and generate speech for each
            for sentence in sentences:
                inputs = self.processor(text=sentence, return_tensors="pt")
                speech = self.model.generate_speech(inputs["input_ids"],
                                                    self.speaker1_embeddings if voice == 1 else self.speaker2_embeddings,
                                                    vocoder=self.vocoder)
                self.speech_list.append(speech)
        else:
            # If the utterance has 50 words or less, process it as before
            inputs = self.processor(text=utterance, return_tensors="pt")
            speech = self.model.generate_speech(inputs["input_ids"],
                                                self.speaker1_embeddings if voice == 1 else self.speaker2_embeddings,
                                                vocoder=self.vocoder)
            self.speech_list.append(speech)

    def play(self):
        pygame.init()
        pygame.mixer.init()

        try:
            for speech in self.speech_list:
                sf.write("speech.wav", speech.numpy(), samplerate=16000)
                pygame.mixer.music.load("speech.wav")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            pygame.mixer.quit()

    def play_with_intro(self, intro_file='/Users/georgekour/repositories/pdf_voice/Intro_podcast.wav'):
        pygame.init()
        pygame.mixer.init()

        try:
            # Convert the list of tensors to a list of numpy arrays
            speech_np_list = [speech.numpy() for speech in self.speech_list]

            combined_speech = np.concatenate(speech_np_list, axis=0)  # Concatenate all speeches

            # Write the combined speech to a WAV file
            sf.write("combined_speech.wav", combined_speech, samplerate=16000)

            # Load the intro file and the combined speech
            intro = sf.read(intro_file)[0]
            combined = sf.read("combined_speech.wav")[0]

            if intro.ndim == 2 and intro.shape[1] == 2:
                intro = np.mean(intro, axis=1)

            # Concatenate the intro and the combined speech
            final_audio = np.concatenate((intro, combined), axis=0)

            # Write the final audio to a WAV file
            sf.write("final_audio.wav", final_audio, samplerate=16000)

            # Play the final audio
            pygame.mixer.music.load("final_audio.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            pygame.mixer.quit()


if __name__ == '__main__':

    # Usage:
    generator = SpeechGenerator()

    # Add turns
    generator.add_turn("Hello, this is speaker 1.", voice=1)
    generator.add_turn("Hi, this is speaker 2.", voice=2)

    # Play the generated speech
    generator.play()
