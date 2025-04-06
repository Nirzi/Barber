from django.shortcuts import render, get_object_or_404

# Данные
masters = [
    {"id": 1, "name": "Эльдар 'Бритва' Рязанов"},
    {"id": 2, "name": "Зоя 'Ножницы' Космодемьянская"},
    {"id": 3, "name": "Борис 'Фен' Пастернак"},
    {"id": 4, "name": "Иннокентий 'Лак' Смоктуновский"},
    {"id": 5, "name": "Раиса 'Бигуди' Горбачёва"},
]

services = [
    "Стрижка под 'Горшок'",
    "Укладка 'Взрыв на макаронной фабрике'",
    "Королевское бритье опасной бритвой",
    "Окрашивание 'Жизнь в розовом цвете'",
    "Мытье головы 'Душ впечатлений'",
    "Стрижка бороды 'Боярин'",
    "Массаж головы 'Озарение'",
    "Укладка 'Ветер в голове'",
    "Плетение косичек 'Викинг'",
    "Полировка лысины до блеска"
]

orders = [
    {
        "id": 1,
        "client_name": "Пётр 'Безголовый' Головин",
        "services": ["Стрижка под 'Горшок'", "Полировка лысины до блеска"],
        "master_id": 1,
        "date": "2025-03-20",
        "status": "новая"
    },
]

# Представления
def landing(request):
    context = {"masters": masters, "services": services}
    return render(request, "landing.html", context)

def thanks(request):
    return render(request, "core/thanks.html")

def orders_list(request):
    context = {"orders": orders}
    return render(request, "core/orders_list.html", context)

def order_detail(request, order_id):
    order = next((o for o in orders if o["id"] == order_id), None)
    if order is None:
        return render(request, "core/404.html", status=404)
    context = {"order": order}
    return render(request, "core/order_detail.html", context)
