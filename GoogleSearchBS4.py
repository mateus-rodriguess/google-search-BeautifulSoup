from bs4 import BeautifulSoup
import requests
import json
from google_trans_new import google_translator 
from time import sleep
import json

# cabeçalho 
headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }


def translate_text(text):
    """
    function that receives a text is translated into 5 different languages. \n
    portugues, ingles, chines tradiconal, frances, russo 
    """
    translator = google_translator()
    # portugues, ingles, chines tradiconal, frances, russo  
    languages = ['pt', 'en', 'zh-CN', 'fr', 'ru']
    text_list = []
    
    for lang in languages:
        try:
            phrase = translator.translate(text,lang_tgt=lang)
            text_list.append(phrase)
        except:
            sleep(2)
            phrase = translator.translate(text,lang_tgt=lang)
            text_list.append(phrase)
    
    return text_list


def beautiful_soup(search):
    """
    function that searches for the translated phrase and returns a dict of results
    """
    summary = []
    html = requests.get(f'https://www.google.com/search?q={search}',headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    for container in soup.findAll('div', class_='tF2Cxc'):

        heading = container.find('h3', class_='LC20lb DKV0Md').text
        article_summary = container.find('span', class_='aCOpRe').text
        href =  container.find('div', class_='yuRUbf').text

        summary.append({
            'Heading': heading,
            'Article Summary': article_summary,
            'href': href,
        })

    #print(json.dumps(summary, indent=4, ensure_ascii=False))
    return summary



if __name__ == "__main__":
    """
    main
    """
    i = 0
    search = "como criar uma função no python"

    search_list = []
    text_list = translate_text(search)
    print(text_list)

    languages = ['portugues', 'ingles', 'chines', 'frances', 'russo']
   
    for text in text_list:
        answer = beautiful_soup(text)
        print(f">: {languages[i]}")
        print(answer)
        print("-" *200)
        search_list.append({languages[i]: answer})
        i += 1

    print(json.dumps(search_list, indent=4, ensure_ascii=False))
    with open("search.json", "w") as json_file:
        # faz virar objeto do python
        json.dump(search_list, json_file, indent=4)



    

