import sqlite3


# Создаём бд и табличку для последних настроек
def create_table_recent():
    database_path = "res/slasher.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recent_set (
                batch_mode TEXT,
                split_mode TEXT,
                pixels_mode TEXT,
                num_pixel TEXT,
                num_split TEXT,
                output_files_type TEXT,
                slicing_sensitivity TEXT,
                ignorable_edges_pixels TEXT,
                scan_line_step TEXT,
                after_slash_mode,
                original_save_mode,
                psd_to_png_mode,
                png_to_gif_mode
            )""")

        # Проверяем количество строк в таблице
        cursor.execute("SELECT COUNT(*) FROM recent_set")
        row_count = cursor.fetchone()[0]

        # Если нет строк, вставляем новую строку
        if row_count == 0:
            cursor.execute("""
                INSERT INTO recent_set VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ))
    finally:
        connection.commit()
        connection.close()


# Передаём словарь данных для замены для последних настроек
def update_recent_set(update_data=None):
    if not update_data or not isinstance(update_data, dict):
        return

    connection = sqlite3.connect("res/slasher.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM recent_set LIMIT 1")
        existing_row = cursor.fetchone()

        if existing_row:
            update_query = "UPDATE recent_set SET "
            update_values = []

            for key, value in update_data.items():
                update_query += f"{key} = ?, "
                update_values.append(value)

            update_query = update_query.rstrip(', ')

            cursor.execute(update_query, update_values)
    finally:
        connection.commit()
        connection.close()


# Получаем словарь данных для последних настроек
def get_recent_set(table_name="recent_set"):
    db_path = "res/slasher.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY ROWID ASC LIMIT 1")
        row = cursor.fetchone()
        if row:
            column_names = [description[0] for description in cursor.description]
            row_dict = dict(zip(column_names, row))
            return row_dict
        else:
            print("Таблица пуста.")
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    finally:
        connection.close()


# Создаём табличку для сохранения пресетов
def create_table_presets():
    database_path = "res/slasher.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS presets (
                name TEXT,
                batch_mode TEXT,
                split_mode TEXT,
                pixels_mode TEXT,
                num_pixel TEXT,
                num_split TEXT,
                output_files_type TEXT,
                slicing_sensitivity TEXT,
                ignorable_edges_pixels TEXT,
                scan_line_step TEXT,
                after_slash_mode,
                original_save_mode,
                psd_to_png_mode,
                png_to_gif_mode
            )""")
    finally:
        connection.commit()
        connection.close()


# Создаём строку для сохранения пресетов
def create_new_preset(data=None):
    database_path = "res/slasher.db"
    if not data or not isinstance(data, dict) or "name" not in data:
        return

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM presets WHERE name = ?", (data["name"],))
        existing_row = cursor.fetchone()

        if existing_row:
            update_query = "UPDATE presets SET "
            update_values = []

            for key, value in data.items():
                update_query += f"{key} = ?, "
                update_values.append(value)

            update_query = update_query.rstrip(', ') + " WHERE name = ?"
            update_values.append(data["name"])

            cursor.execute(update_query, update_values)
        else:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            insert_query = f"INSERT INTO presets ({columns}) VALUES ({placeholders})"

            cursor.execute(insert_query, tuple(data.values()))
    finally:
        connection.commit()
        connection.close()


# Получаем все пресеты
def get_all_presets():
    database_path = "res/slasher.db"
    table_name = "presets"
    # Подключаемся к базе данных
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Выбираем все строки из таблицы
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Получаем имена столбцов
        columns = [column[0] for column in cursor.description]

        # Преобразуем строки в словари
        rows_as_dicts = [dict(zip(columns, row)) for row in rows]

        return rows_as_dicts
    finally:
        # Закрываем соединение
        connection.close()


# Удаляем строку из пресетов
def delete_preset(name_to_delete=None):
    database_path = "res/slasher.db"
    if not name_to_delete:
        return

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Проверяем, существует ли запись с указанным именем
        cursor.execute("SELECT * FROM presets WHERE name = ?", (name_to_delete,))
        existing_row = cursor.fetchone()

        if existing_row:
            # Если запись существует, удаляем её
            delete_query = "DELETE FROM presets WHERE name = ?"
            cursor.execute(delete_query, (name_to_delete,))
    finally:
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()


# Получаем один пресет по имени
def get_one_preset(name_to_fetch=None):
    database_path = "res/slasher.db"
    if not name_to_fetch:
        return None

    # Подключаемся к базе данных
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Выбираем строку из таблицы по значению "name"
        cursor.execute("SELECT * FROM presets WHERE name = ?", (name_to_fetch,))
        row = cursor.fetchone()

        if row:
            # Получаем имена столбцов
            columns = [column[0] for column in cursor.description]

            # Преобразуем строку в словарь
            row_as_dict = dict(zip(columns, row))

            return row_as_dict
    finally:
        # Закрываем соединение
        connection.close()
