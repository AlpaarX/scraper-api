# scraping and analyzing the suumo rental pricing (Odawara)


import bs4 as bs
import requests

url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14206&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&pc=50"

bs.BeautifulSoup(requests.get(url).text, "html.parser")