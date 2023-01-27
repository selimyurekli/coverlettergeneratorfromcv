import os

import openai
from flask import Flask, redirect, render_template, request, url_for
#from resume_parser import resumeparse
import os
import spacy
import warnings
nlp = spacy.load("en_core_web_sm")
warnings.filterwarnings("ignore")
app = Flask(__name__)


openai.api_key = os.getenv("OPENAI_API_KEY")




@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        name = request.form["name"]
        companyName = request.form["companyName"]
        pdf_file = request.files.get('pdf_file')
        pdf_file.save('./pdf_file.pdf')

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(name,companyName),
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
  

    return render_template("index.html", result=result)


def generate_prompt(name,companyName):
    data =  extract_information_from()
    skills = ",".join(data["skills"])
    prompt = """Write me a cover letter for applying to company called {}, please use my informations below:\n Skills: {} \n Name: {}""".format(companyName,skills,name)
    print(prompt)
    return prompt


from pyresparser import ResumeParser

def extract_information_from():
    data = ResumeParser('./pdf_file.pdf').get_extracted_data()
    return data

