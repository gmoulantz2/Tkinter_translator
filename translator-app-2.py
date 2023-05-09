#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:48:16 2023

@author: george
"""

import tkinter as tk
from gtts import gTTS
from playsound import playsound
from transformers.models.mgp_str.processing_mgp_str import AutoTokenizer
from transformers.models.auto.modeling_auto import AutoModelForSeq2SeqLM


class Translator:

  def __init__(self):

    self.model = AutoModelForSeq2SeqLM.from_pretrained('Helsinki-NLP/opus-mt-en-fr')
    self.tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-fr')
    self.languages = ['en', 'fr', 'de']

  def translate(self, text, src_lang, tgt_lang):

    if src_lang not in self.languages:
      raise RuntimeError('Source language not supported.')
    if tgt_lang not in self.languages:
      raise RuntimeError('Target language not supported')

    model_name = 'Helsinki-NLP/opus-mt-' + src_lang + '-' + tgt_lang
    self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs = self.tokenizer.encode(text, return_tensors = 'pt')
    tokens = self.model.generate(inputs, max_length = 512)
    decoded = self.tokenizer.decode(tokens[0], skip_special_tokens = True)

    return decoded


def speak_src():
    text = src_text.get('1.0', 'end-1c')
    tts = gTTS(text = text, lang = src_lang_input.get())
    tts.save('audio.mp3')
    playsound('audio.mp3')
    
def speak_tgt():
    text = tgt_text.get('1.0', 'end-1c')
    tts = gTTS(text = text, lang = tgt_lang_input.get())
    tts.save('audio.mp3')
    playsound('audio.mp3')
    
def translate():
    translator_object = Translator()
    tgt_text.delete('1.0', 'end-1c')
    text = src_text.get('1.0', 'end-1c')
    translated_text = translator_object.translate(text, src_lang_input.get(), tgt_lang_input.get())
    tgt_text.insert('1.0', translated_text)
    
    
root = tk.Tk()
root.geometry('845x300')
root.title('Language Translator')

#Left column
src_lang_label = tk.Label(root, text = 'Select Source Language:')
src_lang_label.grid(row = 0, column = 0, padx = 10, pady = 10)


src_lang_input = tk.StringVar()
src_lang_input_dropdown = tk.OptionMenu(root, src_lang_input, 'en', 'fr', 'de')
src_lang_input_dropdown.grid(row = 1, column = 0, padx = 10, pady = 10)
#src_lang_input.set('en')

src_text = tk.Text(root, height = 5, width = 50)
src_text.grid(row = 2, column = 0, padx = 10, pady = 10)

src_speak_button = tk.Button(root, text = 'Speak', command = speak_src)
src_speak_button.grid(row = 3, column = 0)

#Middle column
translate_button = tk.Button(root, text = 'Translate', command = translate)
translate_button.grid(row = 2, column = 1)


#Right column
tgt_lang_label = tk.Label(root, text = 'Select Source Language:')
tgt_lang_label.grid(row = 0, column = 2, padx = 10, pady = 10)

tgt_lang_input = tk.StringVar()
tgt_lang_input_dropdown = tk.OptionMenu(root, tgt_lang_input, 'en', 'fr', 'de')
tgt_lang_input_dropdown.grid(row = 1, column = 2, padx = 10, pady = 10)
#tgt_lang_input.set('de')

tgt_text = tk.Text(root, height = 5, width = 50)
tgt_text.grid(row = 2, column = 2, padx = 10, pady = 10)

tgt_speak_button = tk.Button(root, text = 'Speak', command = speak_tgt)
tgt_speak_button.grid(row = 3, column = 2)



root.mainloop()
