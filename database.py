import sqlite3

def execute(execution, *args):
    connection = sqlite3.connect('tasks_database.db')
    cursor = connection.cursor()
    cursor.execute(execution, *args)

    data = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()

    return data

def load_data():
    active_saved_tasks_sql = 'SELECT * FROM active_tasks'
    completed_saved_tasks_sql = 'SELECT * FROM completed_tasks'

    active_saved_tasks = execute(active_saved_tasks_sql)
    completed_saved_tasks = execute(completed_saved_tasks_sql)

    return {'active_tasks':active_saved_tasks, 'completed_tasks': completed_saved_tasks}

def delete_active_tasks(element:str):
    execute('DELETE FROM active_tasks WHERE body=?', (element, ))
    return True

def clear_completed_tasks():
    execute('DELETE FROM completed_tasks')
    return True

def add_active_task(element:str):
    execute('insert into active_tasks(body) VALUES (?)', (element, ))
    return True

def add_completed_task(element:str):
    execute('insert into completed_tasks(body) VALUES (?)', (element, ))
    return True