from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Cancel

from app.dialogs.start import states, callbacks, getters


def start_window():
    return Window(
        Format(
            "*Добро Пожаловать в study helper™ *👋{weather_str}\n\nЭто - Менеджер домашнего задания, здесь можно найти актуальное "
            "Д/З, полезные материалы, конспекты, а также учебники 📚\n\nСкрафтил @fadegor05 ⭐\nРедактирует @TGRTX"
            "📝\n\nВыберите то, что вас интересует 🤔"
        ),
        Button(
            Const("📑 Домашнее задание"),
            "homework_button",
            callbacks.on_chosen_hometask,
        ),
        Button(Const("📆 Расписание"), "schedule_button", callbacks.on_chosen_schedule),
        Button(Const("⚙️ Настройки"), "settings_button", callbacks.on_chosen_settings),
        Cancel(Const("❌ Выход")),
        state=states.StartMenu.select_menu,
        getter=getters.get_start
    )
