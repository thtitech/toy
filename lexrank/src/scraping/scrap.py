import json
import sys
import requests
from bs4 import BeautifulSoup
import re
import numpy as np

def get_data(query, page=1, per_page=100):
    url = 'https://qiita.com/api/v2/items?'

    param = {
        'query': query,
        'page': page,
        'per_page': per_page
    }
    r = requests.get(url, params=param)
    return r.text

def convert_json(json_str):
    data = json.loads(json_str)
    return data

def isascii(s):
    asciiReg = re.compile(r'^[!-~]+$')
    return asciiReg.match(s) is not None

def main():
    result = []
    file_name = "../../data/database.txt"
    for page_num in range(1, 10):
        obj = convert_json(get_data(query="aws+ec2", page=page_num))
        print(len(obj))
        for i in range(len(obj)):
            soup = BeautifulSoup(obj[i]['rendered_body'], "html.parser")
            sent_list = list(filter(lambda x: x != "", re.split("\n|。", soup.text)))
            index_list = list(map(lambda x: not isascii(x.replace(" ", "")), sent_list))
            sent_list = np.array(sent_list)[index_list]
            result.append(sent_list)

    with open(file_name, "w", encoding='UTF-8') as f:
        for sent_list in result:
            for sent in sent_list:
                f.write(sent + "。")
            f.write("\n")
    
if __name__ == "__main__":
    main()
