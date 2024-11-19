# main.py
import requests
from bs4 import BeautifulSoup
def main():
    res = requests.get('https://github.com/trending')
    sel = BeautifulSoup(res.content)
    rows = sel.select('article.Box-row')
    print("rows",rows)
if __name__ == '__main__':
    main()