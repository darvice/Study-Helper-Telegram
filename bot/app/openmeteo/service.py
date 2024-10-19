from datetime import datetime, timedelta, time

from app.crud.schedule import get_first_last_lesson_time_by_day
from app.crud.weather import create_weather
from app.openmeteo.api import request_openmeteo


async def hour_rounder(t: time) -> time:
    t_datetime = datetime.combine(datetime.now(), t)
    return (t_datetime.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=t.minute // 30)).time()


async def weather_code_handler(code: int) -> str:
    if 0 <= code <= 1:
        return '☀️'
    elif 2 <= code <= 3:
        return '⛅️'
    elif 4 <= code < 61:
        return '☁️'
    elif 61 <= code <= 67:
        return '🌧️'
    elif 71 <= code <= 77:
        return '🌨️'
    elif 80 <= code <= 82:
        return '🌧️'
    elif 85 <= code <= 86:
        return '🌨️'
    elif 95 <= code <= 99:
        return '⛈️'
    return '⚠️'


async def update_weather_from_openmeteo():
    today = datetime.now()
    date = today
    if (today.hour >= 16 and today.isoweekday() != 6) or today.isoweekday() == 7:
        date += timedelta(days=1)
    elif today.hour >= 16 and today.isoweekday() == 6:
        date += timedelta(days=2)

    first_lesson_time, last_lesson_time = await get_first_last_lesson_time_by_day(date.isoweekday())
    data = await request_openmeteo(date)
    hourly = data.get("hourly")
    temperature = hourly.get("temperature_2m")
    weather_codes = hourly.get("weather_code")
    morning_temp = temperature[(await hour_rounder(first_lesson_time)).hour - 1]
    day_temp = temperature[(await hour_rounder(last_lesson_time)).hour - 1]
    morning_icon = await weather_code_handler(weather_codes[(await hour_rounder(first_lesson_time)).hour - 1])
    day_icon = await weather_code_handler(weather_codes[(await hour_rounder(last_lesson_time)).hour - 1])

    await create_weather(date.date(), morning_temp, day_temp, morning_icon, day_icon, first_lesson_time, last_lesson_time)
