import tkinter as tk
import utils
import database

class MainWindow(tk.Tk):
    # Главное окно

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.attributes('-toolwindow', True) # Оставляет только кнопку закрытия приложения

        self.attributes('-topmost', 'true') # Закрепить поверх всех окон

        self.frame_one = FrameWithTasks(master = self)
        self.frame_one.pack()


class Listbox(tk.Listbox):
    def _add_data(self, data):
        self.insert('end', data)
        return True
    
    def remove_selected_data(self):
        index = self._get_selected_index()
        if index:
            self.delete(index)
        return True             
    
    def _get_selected_index(self):
        index = self.curselection()
        return index
    
    def get_selected_data(self):
        index = self._get_selected_index()
        if index:
            selected_data = self.get(index)
        return selected_data

    def is_selected(self):
        if self.curselection():
            return True
        else:
            return False

    def clear_listbox(self):
        self.delete(0,'end')

    def clear(self):
        self.clear_listbox()
        database.clear_completed_tasks()

    def delete_from_db_and_listbox(self):
        data = self.get_selected_data()
        self.remove_selected_data()
        database.delete_active_tasks(data)
        return True



class ActiveListbox(Listbox):
    def add_to_db_and_listbox(self, data:str):
        if data.strip()!='':
            self._add_data(data)
            database.add_active_task(data)
            return True
    
    def load_data(self):
        data = database.load_data()['active_tasks']
        for row in data:
            self._add_data(row[1])
        return True

class CompletedListbox(Listbox):
    def add_to_db_and_listbox(self, data):
        self._add_data(data)
        database.add_completed_task(data)
        return True

    def load_data(self):
        data = database.load_data()['completed_tasks']
        for row in data:
            self._add_data(row[1])
        return True



class Input(tk.Entry):
    def get_and_delete_text(self):
        data = self.get()
        self.delete(0, 'end')
        return data
        
        
        
class FrameWithTasks(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)

        # Listboxes

        tasks_listbox = ActiveListbox(master=self)
        tasks_listbox.load_data()
        tasks_listbox.pack()

        complete_listbox = CompletedListbox(master=self)
        complete_listbox.load_data()
        complete_listbox.pack()

        # Inputs

        self.input = Input(master=self)
        self.input.pack()

        # Buttons

        self.add_button = tk.Button(text='Добавить', command=lambda:tasks_listbox.add_to_db_and_listbox(self.input.get_and_delete_text()))
        self.add_button.pack()

        self.remove_button = tk.Button(text='Удалить', command=tasks_listbox.delete_from_db_and_listbox)
        self.remove_button.pack()

        self.remove_button = tk.Button(text='Выполнено', command=lambda:utils.mark_as_completed(tasks_listbox, complete_listbox))
        self.remove_button.pack()

        self.clear_button = tk.Button(text='Очистить', command=complete_listbox.clear)
        self.clear_button.pack()
        

def run():
    main_window = MainWindow()
    main_window.mainloop()


if __name__=='__main__':
    run()