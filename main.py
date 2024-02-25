from flask import Flask, render_template, request
import os
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import os
import re
os.environ['OPENAI_API_KEY'] = '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' # your openai key

llm_resto = OpenAI(temperature=0.6)
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 restaurants names, 6 breakfast names, 5 dinner names, and 6 workout names, "
             "based on the following criteria:\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}."
)

chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
input_data = {'age': '60',
                              'gender': 'male',
                              'weight': '120',
                              'height': 5,
                              'veg_or_nonveg': 'veg',
                              'disease': 'aneamia',
                              'region': 'India',
                              'allergics': 'latex allergy',
                              'foodtype': 'fruits'}

# Instead of using chain.run(input_data), use chain.invoke(input_data)
results = chain_resto.invoke(input_data)

print(results)
