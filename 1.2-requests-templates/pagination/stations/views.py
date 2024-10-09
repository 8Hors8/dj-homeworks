import csv
import os

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def read_bus_stations():
    """
    Читает данные автобусных станций из CSV файла.

    Файл CSV должен находиться в директории проекта.
    Функция возвращает список словарей, где каждый словарь представляет
    собой запись о автобусной станции.

    :return: Список словарей с данными автобусных станций.
    """
    CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'data-398-2018-08-30.csv')
    print('path', CSV_FILE_PATH)
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def index(request):
    """
    Перенаправляет пользователя на страницу с автобусными станциями.
    :param request: HTTP-запрос

     :return: Ответ с перенаправлением на маршрут 'bus_stations'.
    """
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    """
    Отображает страницу с автобусными станциями с пагинацией.

    Читает данные о станциях, обрабатывает номер страницы из запроса
    и возвращает HTML-страницу с данными.

    :param request: HTTP-запрос
    :return: Ответ с отрендеренной HTML-страницей, содержащей рецепт или сообщение об ошибке
    """
    stations = read_bus_stations()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(stations, 10)

    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
