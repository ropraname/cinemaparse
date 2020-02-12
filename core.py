"""Файл, содержащий class CinemaParser"""
import requests as re
from bs4 import BeautifulSoup
from _datetime import datetime


class CinemaParser:
    """Class с функциями для работы с html-содержимым subcity"""

    def __init__(self, city: object = 'msk') -> object:
        """Считывание данных о городе, сохранение данных"""
        self.city = city
        self.content = None
        self.films = []
        self.url = None

    def extract_raw_content(self):
        """Скачивание html-содержимого главной страницы сайта, cохранение данных"""
        if self.city == 'msk':
            self.url = 'https://msk.subscity.ru'
        else:
            self.url = 'https://spb.subscity.ru'
        self.content = re.get(self.url)
        self.content = self.content.text

    def print_raw_content(self) -> object:
        """Вывод html-содержимого главной страницы сайта"""
        soup = BeautifulSoup(self.content, 'html.parser')
        print(soup.prettify())

    def get_films_list(self):
        """Вывод списка с названиями фильмов"""
        self.extract_raw_content()
        soup = BeautifulSoup(self.content, 'html.parser')
        all_films = soup.find_all("div", class_='movie-plate')
        for film in all_films:
            self.films.append(str(film["attr-title"]))
        return self.films

    def get_film_nearest_session(self, film):
        """Вывод кортежа с ближайшим временем показа нужного фильма и кинотеатром"""
        self.extract_raw_content()
        soup = BeautifulSoup(self.content, 'html.parser')
        all_films = soup.find_all("div", class_='movie-plate')
        for films in all_films:
            if str(film).lower() == str(films["attr-title"]).lower():
                href = films.find_all("a")[0]
                href = href["href"]
                one_film = re.get(self.url + str(href))
                one_film = BeautifulSoup(one_film.text, 'html.parser')
                teats = one_film.find_all("div", class_="cinema-name")
                time_all = one_film.find_all("td", class_="text-center cell-screenings")
                time_list = []
                teat_list = []
                number = 0
                for teat in teats:
                    time_list.append(int(time_all[number]["attr-time"]))
                    teat_list.append(teat.text)
                    number += 1
                time_teat = (teat_list[time_list.index(min(time_list)) - 1],
                             str(datetime.fromtimestamp(min(time_list))).split()[1][:-3])
                return time_teat
