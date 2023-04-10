import speech_recognition as sr
import os
import torch
import torchaudio

from transformers import AutoTokenizer, AutoModelForCausalLM
import string
import re

from modules import compare_vecs
from google_scrapping import scrape_search

def speech_2_text(number, recognizer):
    name = 'voice_' + str(number) + '.wav'
    text = str
    with sr.Microphone() as source:
        print('говорите')
        audio = recognizer.listen(source)

        with open(name, 'wb') as f:
            f.write(audio.get_wav_data())

            try:
                result = recognizer.recognize_google(audio, language='ru')
                text = ' '.join([result])
            except:
                text = ''
    return text


def response_gen(text, tokenizer, model):
    response = str
    text = text.lower()

    if compare_vecs(text):
        response = scrape_search(text)

    else:
        input_text = ' """<s>- ' + text + ' -""" '
        encoded_prompt = tokenizer.encode(input_text, add_special_tokens=False, return_tensors="pt").to(device)
        output_sequences = model.generate(input_ids=encoded_prompt, max_length=100, num_return_sequences=1,
                                          pad_token_id=tokenizer.pad_token_id)
        try:
            response = tokenizer.decode(output_sequences[0].tolist(), clean_up_tokenization_spaces=True)[len(input_text):]
            response = response.split('<')[0].translate(str.maketrans('', '', string.punctuation))
            response = re.sub('[^\x00-\x7Fа-яА-Я]', '', response)
        except:
            response = 'не совсем вас поняла'

    return response

def text_2_speech(text, number, model):
    sample_rate = 48000
    speaker = 'xenia'
    name = 'response_' + str(number) + '.wav'
    audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate)
    torchaudio.save(name, src=audio.expand(1, -1), sample_rate=sample_rate)
    os.system(name)
    return name


# main -------------------------------------------------------------------------------------------
recognizer = sr.Recognizer()

device = "cuda" if torch.cuda.is_available() else "cpu"
response_model_name = "inkoziev/rugpt_chitchat"   # sberbank-ai/rugpt3large_based_on_gpt2
tokenizer = AutoTokenizer.from_pretrained(response_model_name)
tokenizer.add_special_tokens({'bos_token': '<s>', 'eos_token': '</s>', 'pad_token': '<pad>'})
response_model = AutoModelForCausalLM.from_pretrained(response_model_name)
response_model.to(device)
response_model.eval()

device = torch.device('cpu')
torch.set_num_threads(4)
local_file = 'model.pt'
if not os.path.isfile(local_file):
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt', local_file)
speech_model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
speech_model.to(device)

text = speech_2_text(0, recognizer)
response = response_gen(text, tokenizer, response_model)
text_2_speech(response, 0, speech_model)





