# The goal of this module is to retrieve current events and append them to a database

import torch
from transformers import pipeline, Conversation
from functools import partial
from geopy.geocoders import Nominatim
import spacy

nlp = spacy.load("en_core_web_sm")

pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta", torch_dtype=torch.bfloat16, device_map="auto") # The other option for the pipeline is to make it "text-generation" instead of "conversational"


def NLP_pipeline(title, article):
    # This function returns None if the article is not relevant

    # Deduce the broad class
    messages = [
        {
            "role": "system",
            "content": "You are an intelligent chatbot who always gives short, concise answers, of a length of one sentence maximally.",
        },
        {
            "role": "user",
            "content": f"""Of the following classes: Nature, Politics, Entertainment, Economics, Culture and Science; to which one does the article with the following headline belong to: "{title}"?""",
            },
    ]

    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    print(outputs[0]["generated_text"])

    classes = ["Nature", "Politics", "Entertainment", "Economics", "Culture", "Science"]
    response = outputs[0]["generated_text"].split("<|assistant|>")[1]

    for category in classes:
        if category in response:
            break

    print(f"The article belong to the {category} class")

    if category == "Nature" or category == "Entertainment" or category == "Culture" or category == "Science":
        return None

    # Deduce the risk measure

    messages = [
        {
            "role": "system",
            "content": "You are an intelligent chatbot who always gives short, concise answers, of a length of one sentence at most.",
        },
        {
            "role": "user",
            "content": f"""
            The risk measure is a number from 1 to 10 that quantifies the magnitude of risk facing a country. Every event causes a change to the risk measure. The following defines values for changes to the risk measure:

            -2	De-escalation of situation
            0	Unrelated to risk
            +2	Minor threat; creates difficulty
            +4	Notable threat to communities and stability
            +6	Major threat; threatens lives and livelihoods

            What is the risk measure associated to the following article:

            {article}
            """,
        },
    ]

    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    print(outputs[0]["generated_text"])

    response = outputs[0]["generated_text"].split("<|assistant|>")[1]

    risk_score = 0

    for i in range(len(response)):
        if response[i] == "+":
            try:
                risk_score = int(response[i + 1])
            except ValueError:
                pass

    if risk_score == 0:
        pass

    # Find if it is international or domestic

    doc1 = nlp(article)

    places = []

    for ent in doc1.ents:
        if ent.label_ == "GPE" :
            places.append(ent.text)

    geolocator = Nominatim(user_agent="diplomacy-software")

    geocode = partial(geolocator.geocode, language="en")

    countries = {}

    for place in places:
        try:
            country = geocode(place)[0].split(',')[-1].strip()

            if country not in countries:
                countries[country] = 1
            else:
                countries[country] += 1

        except TypeError:
            pass

    total = sum(list(countries.values()))

    threshold = total / len(countries)

    RelevantCountry = []

    for country in countries:
        
        if countries[country] > threshold:
            RelevantCountry.append(country)

    print(RelevantCountry)

    # Deduce the narrow risk dimension

    