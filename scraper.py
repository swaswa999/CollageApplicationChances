from bs4 import BeautifulSoup
import os
import requests
from openai import OpenAI

OPENAI_API_KEY = 'OPEN_AI'


def webscraper(r):
    req = requests.get(r)
    soup = BeautifulSoup(req.content, 'html.parser')
    text_content = soup.get_text()
    cleaned_text = '\n'.join(line.strip() for line in text_content.split('\n') if line.strip())

    if cleaned_text != ' ':
        client = OpenAI(api_key=OPENAI_API_KEY)
        client = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content":'''MLA citation Generator,
                If the provided WEBSITE URL is not a valid URL return: "Not valid link or links"
                If the provided WEBSITE URL is valid then using the information provided inside the ``` ``` create a MLA citation
            '''},
            {"role": "user", "content": f"```WEBSITE CONTENT{cleaned_text}\n WEBSITE URL:{r}```"}
            ])
        generated_text = client.choices[0].message.content
        print(generated_text)

    return generated_text
