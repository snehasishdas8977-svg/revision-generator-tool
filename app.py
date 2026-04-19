from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

# PDF theke text extract korar function
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Notes generate korar function (example: prothom 5 line)
import re

def clean_text(text):
    # Remove extra spaces & line breaks
    text = re.sub(r'\n+', ' ', text)        # remove new lines
    text = re.sub(r'\s+', ' ', text)        # remove extra spaces
    text = re.sub(r'\d+\s*', '', text)      # remove random numbers like 1 2 3
    return text.strip()


def generate_notes(text):
    text = clean_text(text)

    # Split properly into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    notes = []
    for s in sentences:
        s = s.strip()

        # ignore very small or useless lines
        if len(s) > 40:
            notes.append(s)

    return notes 

@app.route("/", methods=["GET", "POST"])
def home():
    notes = []
    if request.method == "POST":
        # Textarea theke text
        text = request.form.get("text", "")
        
        # PDF file handle
        pdf_file = request.files.get("pdf_file")
        if pdf_file and pdf_file.filename.endswith(".pdf"):
            pdf_path = os.path.join("temp.pdf")
            pdf_file.save(pdf_path)
            text = extract_text_from_pdf(pdf_path)
            os.remove(pdf_path)  # temporary PDF delete kore de

        if text:
            notes = generate_notes(text)

    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    app.run()