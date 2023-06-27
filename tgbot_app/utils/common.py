from datetime import datetime

from tgbot_app.models import Airport, Airline


async def date_validate(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        if date_obj.date() < datetime.now().date():
            raise ValueError
        return True
    except ValueError:
        return False


async def mins_to_str(num):
    if num < 60:
        return f'{num}мин.'
    if num == 60:
        return '1ч.'

    hours = num // 60
    mins = num % hours
    return f'{hours}ч. {mins}мин.'


async def gen_avia_result_text(data):
    origin_airport = await Airport.objects.aget(code=data['origin_airport'])
    destination_airport = await Airport.objects.aget(code=data['destination_airport'])
    airline = await Airline.objects.aget(code=data['airline'])
    flight_number = data['flight_number']
    departure_at = datetime.fromisoformat(data['departure_at']).strftime('%d.%m.%Y %H:%M')
    duration_to = await mins_to_str(data['duration_to'])
    duration_back = await mins_to_str(data['duration_back'])
    price = data['price']
    transfers = data['transfers']
    return_transfers = data['return_transfers']
    return_at = data.get('return_at', None)

    text = f'<b>Авиакомпания:</b> <i>{airline.title}</i>\n' \
           f'<b>Номер рейса:</b> <i>{flight_number}</i>\n\n' \
           f'<b>Маршрут:</b> <i>{origin_airport.title} - {destination_airport.title}</i>\n' \
           f'<b>Дата и время вылета:</b> <i>{departure_at}</i>\n'

    if transfers > 0:
        text += f'<b>Количество пересадок:</b> <i>{transfers}</i>\n'

    text += f'<b>Время в пути:</b> <i>{duration_to}</i>\n\n'

    if return_at:
        return_at = datetime.fromisoformat(return_at).strftime('%d.%m.%Y %H:%M')
        text += f'<b>Маршрут:</b> <i>{destination_airport.title} - {origin_airport.title}</i>\n' \
                f'<b>Дата и время вылета:</b> <i>{return_at}</i>\n'
        if return_transfers > 0:
            text += f'<b>Количество пересадок:</b> <i>{return_transfers}</i>\n'
        text += f'<b>Время в пути:</b> <i>{duration_back}</i>\n\n'

    text += f'<b>Цена:</b> <i>{price}₽</i>'

    return text
