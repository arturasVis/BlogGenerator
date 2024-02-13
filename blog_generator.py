import os
from openai import OpenAI
import json
import fpdf 
import pandas as pd
fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__),'fonts'))

def load_api_key(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
        return config['openai_api']['key']

def create_pdf(text, title):
    pdf = fpdf.FPDF()
    pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSans", style="B", fname="NotoSans-Bold.ttf", uni=True)
    pdf.add_font("NotoSans", style="I", fname="NotoSans-Italic.ttf", uni=True)
    pdf.add_font("NotoSans", style="BI", fname="NotoSans-BoldItalic.ttf", uni=True)
    pdf.add_page()
    pdf.set_font("NotoSans", size=12)
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.multi_cell(0, 10, text)
    pdf_file = f"{title.replace(' ', '_')}.pdf"
    pdf.output(pdf_file)
    print(f"PDF generated and saved as: {pdf_file}")

config_file="secret.json"

def generate_blog(title):
    OPEN_API_KEY=load_api_key(config_file)
    client = OpenAI(api_key=OPEN_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Write a comprehensive, detailed blog post about '{title}'. It should be at least 1000 words long"}
        ],
        model="gpt-4",
        max_tokens=3000,
    )

    create_pdf(chat_completion.choices[0].message.content,title)


#message = input("Enter the blog title: ")
df=pd.read_csv("titles.csv");
for index,row in df.iterrows():
    title=row["titles"]
    generate_blog(title)
#print(df);
#generate_blog(message)