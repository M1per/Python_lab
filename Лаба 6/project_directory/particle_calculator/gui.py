# particle_calculator/gui.py

import PySimpleGUI as sg
from .calculations import calculate_specific_charge, calculate_compton_wavelength
from .file_operations import save_to_docx, save_to_xlsx

def create_gui():
    """Создание и запуск графического интерфейса."""
    layout = [
        [sg.Text("Выберите частицу"), sg.Combo(["Электрон", "Нейтрон", "Протон"], default_value="Электрон", key='-PARTICLE-')],
        [sg.Button("Рассчитать"), sg.Button("Сохранить как DOCX"), sg.Button("Сохранить как XLSX")],
        [sg.Text("Удельный заряд:"), sg.Text("", size=(20, 1), key='-SPECIFIC_CHARGE-')],
        [sg.Text("Комптоновская длина волны:"), sg.Text("", size=(20, 1), key='-COMPTON_WAVELENGTH-')]
    ]

    window = sg.Window("Калькулятор частиц", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Рассчитать":
            particle = values['-PARTICLE-']
            if particle == "Электрон":
                mass = 9.10938356e-31  # кг
                charge = -1.602176634e-19  # Кл
            elif particle == "Нейтрон":
                mass = 1.674927471e-27  # кг
                charge = 0  # Кл
            elif particle == "Протон":
                mass = 1.67262192369e-27  # кг
                charge = 1.602176634e-19  # Кл

            specific_charge = calculate_specific_charge(mass, charge)
            compton_wavelength = calculate_compton_wavelength(mass)

            window['-SPECIFIC_CHARGE-'].update(specific_charge)
            window['-COMPTON_WAVELENGTH-'].update(compton_wavelength)

            data = {
                "Частица": particle,
                "Удельный заряд (Кл/кг)": specific_charge,
                "Комптоновская длина волны (м)": compton_wavelength
            }

        elif event == "Сохранить как DOCX":
            filename = sg.popup_get_file("Сохранить как DOCX", save_as=True, no_window=True, file_types=(("Файлы Word", "*.docx"),))
            if filename:
                save_to_docx(filename, data)

        elif event == "Сохранить как XLSX":
            filename = sg.popup_get_file("Сохранить как XLSX", save_as=True, no_window=True, file_types=(("Файлы Excel", "*.xlsx"),))
            if filename:
                save_to_xlsx(filename, data)

    window.close()