import sqlite3
import requests
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
with sqlite3.connect('database.db') as db:
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS useful(
        id_pallet TEXT,
        status TEXT
    )""") # мы создали базу данных с 2-мя  столбцами(ID палета и его статус)

    sql_delete_query = """DELETE FROM useful """
    cursor.execute(sql_delete_query)

    def get_data_from_server_1(id):
        response1 = requests.get('Запрос данных с QR-кода от палетообмотчика') # делаем get-запрос

        if response1.status_code == 200: # проверка запроса
            data = response1.json()
            print(f"Данные от сервера 1 по ID {id}: {data}")
            return data
        else:
            print(f"Ошибка при получении данных от сервера 1. Код ошибки: {response1.status_code}")
            return None

    id_from_pallet_wrapper = 'EUR00008' # эти данные нам дал палетообмотчик
    value = ("EUR00008", "waiting in A")
    cursor.execute("INSERT INTO useful(id_pallet, status) VALUES(?, ?)", value) # вносим id известного палета и его статус в базу данных
    logging.info('Поддон начал существовать!')
    logging.info('Поддон ожидается в пункте А')
    # далее происходит транспортировка палета в пункт А
    # нам нужно проверить камеру на адресе А и проверить тот ли палет нам приехал
    QR_pallet_from_cam_A = 'EUR00008' # это данные, полученные с камеры в пункте А
    status_2 = "in A"
    status_3 = "waiting in B"
    status_4 = "in B"
    if id_from_pallet_wrapper == QR_pallet_from_cam_A:
        cursor.execute("UPDATE useful SET status = ?", [status_2])
        logging.info('Поддон прибыл в пункт А')
        logging.info('Запрос транспортной единицы')
        cursor.execute("UPDATE useful SET status = ?", [status_3])
        logging.info('Поддон ожидается в пункт В')
        # далее происходит транспортировка палета в пункт В
        # нам нужно проверить камеру на адресе B и проверить тот ли палет нам приехал
        QR_pallet_from_cam_B = 'EUR00008' # это данные, полученные с камеры в пункте В
        if QR_pallet_from_cam_B == QR_pallet_from_cam_A:
            cursor.execute("UPDATE useful SET status = ?", [status_4])
            logging.info('Поддон прибыл в пункт В')
            value1 = ("EUR00007", "in B")
            cursor.execute("INSERT INTO useful(id_pallet, status) VALUES(?, ?)", value1)
            def send_data_to_server_2(data):
                response2 = requests.post( json=data) # делаем post-запрос
                if response2.status_code == 200: # проверяем запрос
                    print("Данные успешно отправлены на сервер 2")
                else:
                    print(f"Ошибка при отправке данных на сервер 2. Код ошибки: {response2.status_code}")
        else:
            logging.error('Неизвестный поддон!')
    else:
        logging.error('Неизвестный поддон!')


    cursor.execute("SELECT id_pallet, status FROM useful")
    rows = cursor.fetchall()

    data_as_tuples = [(row[0], row[1]) for row in rows]

def create_table():
    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()
    clear_frame()
    table = ttk.Treeview(frame)
    table["columns"] = ("ID-поддона", "Статус")
    table.column("#0", width=0, stretch=tk.NO)
    table.column("ID-поддона", anchor=tk.W, width=100)
    table.column("Статус", anchor=tk.CENTER, width=100)

    table.heading("#0", text="", anchor=tk.W)
    table.heading("ID-поддона", text="ID-поддона")
    table.heading("Статус", text="Статус")

    for row in data_as_tuples:
        table.insert('', tk.END, values=row)
    table.pack(expand=True, fill=tk.BOTH)
def check_log():
    try:
        with open('py_log.log', 'r') as file:
            log_text = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, log_text)
    except FileNotFoundError:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "Файл логов не найден")

def return_to_menu():
    global frame
    text_area.delete(1.0, tk.END)
    frame.destroy()
    frame = tk.Frame(root)
    frame.pack()

    button1 = tk.Button(frame, text="Показать базу данных", command=create_table)
    button1.pack()
    button2 = tk.Button(frame, text="Показать лог", command=check_log)
    button2.pack()

root = tk.Tk()
root.title("Меню")

text_area = scrolledtext.ScrolledText(root, width=100, height=10)
text_area.pack(padx=10, pady=10)

frame = tk.Frame(root)
frame.pack()

button1 = tk.Button(frame, text="Показать базу данных", command=create_table)
button1.pack()
button2 = tk.Button(frame, text="Показать лог", command=check_log)
button2.pack()

return_button = tk.Button(root, text="Вернуться в меню", command=return_to_menu)
return_button.pack()

root.mainloop()