from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def home_view(request):
    """
    Отображает главную страницу с перечнем доступных рецептов.

        На основе данных из переменной DATA генерирует ссылки на страницы каждого блюда с параметром
    servings, установленным на 1 по умолчанию.
    Возвращает отрендеренный шаблон 'home.html' с контекстом, содержащим ссылки на блюда.

    :param request: HTTP-запрос

    :return: Ответ с отрендеренной HTML-страницей главной страницы
    """
    pages = {dish: f'/{dish}/?servings=1' for dish in DATA.keys()}

    context = {
        'pages': pages
    }
    return render(request, 'calculator/home.html', context)


def recipe_view(request, dish: str):
    """
        Отображает рецепт для указанного блюда, масштабируя количество ингредиентов в зависимости
    от числа порций.

        Извлекает рецепт для указанного блюда из переменной DATA и масштабирует количество
    ингредиентов в зависимости от параметра servings, переданного в запросе.
    Если блюда не существует в данных, возвращает сообщение об ошибке с кодом 404.

    :param request: HTTP-запрос
    :param dish: Название блюда, для которого нужно отобразить рецепт

    :return: Ответ с отрендеренной HTML-страницей, содержащей рецепт или сообщение об ошибке
    """
    recipe = DATA.get(dish)
    if recipe is None:
        # Если рецепт не найден
        return HttpResponse(f"Рецепт для '{dish}' не найден.", status=404)

    servings = int(request.GET.get('servings', 1))
    scaled_recipe = {ingredient: round(amount * servings, 2)
                     for ingredient, amount in recipe.items()
                     }
    context = {
        'recipe': scaled_recipe
    }
    return render(request, 'calculator/index.html', context)
