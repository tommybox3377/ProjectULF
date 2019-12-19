import datetime
import os

import requests
from bs4 import BeautifulSoup as bs

import MySQL
import Parse

main_url = "http://mirl.sr.unh.edu/ULF/incoming/database/HAL_converted/"


def get_files_to_dl():
    rtn_url = []
    response = requests.get(main_url)
    content = response.text
    soup = bs(content, "html.parser")

    urls = soup.find_all("td")
    for url in urls:
        if "txt" in url.get_text():
            rtn_url.append(url.get_text().strip())
    return rtn_url[0:5]  # if you just want a some of the files
    # return rtn_url#if you want all


def dl_file(url):
    f = open("data.txt", "a")
    f.write(requests.get(url).text)
    f.close()


def transfer_from_online_to_db():
    dl_count = 0
    files = get_files_to_dl()
    dl_start = datetime.datetime.now()
    for file in files:
        url, index = Parse.get_info_from_file_name(file)
        dl_file(url)
        data = Parse.get_data_from_txt_file(index)
        MySQL.insert_data_for_day(data)
        os.remove("data.txt")
        dl_count += 1
        print(f"downloaded {dl_count} at {(datetime.datetime.now() - dl_start) / dl_count} per dl")
