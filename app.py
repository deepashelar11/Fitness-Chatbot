from flask import Flask, render_template, request
import os
from langchain.prompts import PromptTemplate
#from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.chains import LLMChain
import re

import os
import re
os.environ['OPENAI_API_KEY'] = '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' # your openai key





app = Flask(__name__)

llm_resto = OpenAI(temperature=0.5)
prompt_template_resto = PromptTemplate(
    input_variables=['age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'allergics', 'foodtype'],
    template="Diet Recommendation System:\n"
             "I want you to recommend 6 breakfast names, 6 lunch names, 5 dinner names, and 6 workout names, "
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
             "list suggestion in simple & easy language & {region} wise breakfast, lunch, dinner. workout could be suitable, its not strict to region."
            "please write response in below format[note - it should be in below format only] with the actual names - \n"
            
            "Breakfast:\n"
            "1. Breakfast Item 1\n"
            "2. Breakfast Item 2\n"
            "3. Breakfast Item 3\n"
            "4. Breakfast Item 4\n"
            "5. Breakfast Item 5\n"
            "6. Breakfast Item 6\n"
             
             "Lunch:\n"
            "1. Lunch Name 1\n"
            "2. Lunch Name 2\n"
            "3. Lunch Name 3\n"
            "4. Lunch Name 4\n"
            "5. Lunch Name 5\n"
            "6. Lunch Name 6\n"
            
            "Dinner:\n"
            "1. Dinner Item 1\n"
            "2. Dinner Item 2\n"
            "3. Dinner Item 3\n"
            "4. Dinner Item 4\n"
            "5. Dinner Item 5\n"
            
            "Workout:\n"
            "1. Workout Plan 1\n"
            "2. Workout Plan 2\n"
            "3. Workout Plan 3\n"
            "4. Workout Plan 4\n"
            "5. Workout Plan 5\n"
            "6. Workout Plan 6\n"
)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        veg_or_noveg = request.form['veg_or_nonveg']
        disease = request.form['disease']
        region = request.form['region']
        allergics = request.form['allergics']
        foodtype = request.form['foodtype']

        chain_resto = LLMChain(llm=llm_resto, prompt=prompt_template_resto)
        input_data = {'age': age,
                              'gender': gender,
                              'weight': weight,
                              'height': height,
                              'veg_or_nonveg': veg_or_noveg,
                              'disease': disease,
                              'region': region,
                              'allergics': allergics,
                              'foodtype': foodtype}
        #results = chain_resto.run(input_data)
        results = chain_resto.invoke(input_data)
        results = str(results)
        print(results)

        # Extracting the different recommendations using regular expressions
        breakfast_names = re.findall(r'Breakfast:(.*?)Lunch:', results, re.DOTALL)
        lunch_names = re.findall(r'Lunch:(.*?)Dinner:', results, re.DOTALL)
        dinner_names = re.findall(r'Dinner:(.*?)Workout:', results, re.DOTALL)
        workout_names = re.findall(r'Workout:(.*?)$', results, re.DOTALL)

        # Cleaning up the extracted lists
        # restaurant_names = [name.strip() for name in restaurant_names[0].strip().split('\n') if name.strip()]
        # breakfast_names = [name.strip() for name in breakfast_names[0].strip().split('\n') if name.strip()]
        # dinner_names = [name.strip() for name in dinner_names[0].strip().split('\n') if name.strip()]
        # workout_names = [name.strip() for name in workout_names[0].strip().split('\n') if name.strip()]

        breakfast_names = [name.strip() for name in breakfast_names[0].strip().split('\\n') if
                           name.strip()] if breakfast_names else []
        lunch_names = [name.strip() for name in lunch_names[0].strip().split('\\n') if
                       name.strip()] if lunch_names else []
        dinner_names = [name.strip() for name in dinner_names[0].strip().split('\\n') if
                        name.strip()] if dinner_names else []
        workout_names = [name.strip() for name in workout_names[0].strip().split('\\n') if
                         name.strip()] if workout_names else []

        print(f'Breakfast names - {breakfast_names}')
        print(f'Lunch names - {lunch_names}')
        print(f'Dinner names - {dinner_names}')
        print(f'Workout names - {workout_names}')

        return render_template('result.html', lunch_names=lunch_names,breakfast_names=breakfast_names,dinner_names=dinner_names,workout_names=workout_names)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
