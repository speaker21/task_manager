import tkinter as tk
import utils
import database


class MainWindow(tk.Tk):
    # Главное окно

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title('Менеджер задач')

        self.pined = False
        self.pin()

        # Оставляет только кнопку закрытия приложения, при этом пропадает кнопка на панели задач
        #self.attributes('-toolwindow', True)

        self.frame_completed_tasks = FrameWithCompletedTasks(master=self)
        self.frame_active_tasks = FrameWithActiveTasks(master=self)
        utils.Settings.set_data(self.frame_active_tasks, self.frame_completed_tasks)

        self.frame_active_tasks.grid(column=0, row=0, sticky = "NSEW", pady=20, padx=20)

    def pin(self):
        if self.pined:
            self.pined = False
            self.attributes('-topmost', 'false')
        else:
            self.pined = True
            self.attributes('-topmost', 'true')  # Закрепить поверх всех окон


# Listbox =============================

class Listbox(tk.Listbox):
    def __init__(self, *args, **kwargs):
        tk.Listbox.__init__(self, *args, **kwargs)

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
        self.delete(0, 'end')

    def clear(self):
        self.clear_listbox()
        database.clear_completed_tasks()

    def delete_from_db_and_listbox(self):
        data = self.get_selected_data()
        self.remove_selected_data()
        database.delete_active_tasks(data)
        return True


class ActiveListbox(Listbox):
    def add_to_db_and_listbox(self, data: str):
        if data.strip() != '':
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

# Button   ============================

class Button(tk.Button):
    def grid(self, *args, **kwargs):
        tk.Button.grid(self, *args, pady=2, padx=2, **kwargs)

# Input   =============================



class Input(tk.Entry):
    def get_and_delete_text(self):
        data = self.get()
        self.delete(0, 'end')
        return data

# Frame ============================

class Frame(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, bd=0, highlightthickness=0, *args, **kwargs)
        self.columnconfigure(0, weight=1)
        
        self.grid_propagate(0) # Размер не зависит от child


class FrameWithCompletedTasks(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.hided = True

        # Listboxes

        self.complete_listbox = CompletedListbox(master=self)
        self.complete_listbox.load_data()
        self.complete_listbox.grid(column=0, row=0, sticky='nswe', columnspan=4)

        # Buttons

        self.clear_button = Button(
            master=self, text='Очистить', command=self.complete_listbox.clear)
        self.clear_button.grid(column=0, row=1)

    def switch_visible(self):
        if self.hided == True:
            self.grid(column=0, row=1)
            self.hided = False
        else:
            self.grid_remove()
            self.hided = True


class FrameWithActiveTasks(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, height = 300, **kwargs)

        # Listboxes

        self.tasks_listbox = ActiveListbox(master=self)
        self.tasks_listbox.load_data()
        self.tasks_listbox.grid(column=0, row = 1, sticky='nswe', columnspan=4)

        # Inputs

        self.input = Input(master=self)
        self.input.grid(sticky='nswe', columnspan=1, column=0, row=2)

        # Buttons

        self.pin_button = Button(master=self, text='Закрепить', command=self.master.pin) 
        self.pin_button.grid(column=0, row=0)

        self.add_button = Button(master=self, text='Добавить', command=lambda: self.tasks_listbox.add_to_db_and_listbox(
            self.input.get_and_delete_text()))
        self.add_button.grid(column=2, row=2)
        self.master.bind('<Return>', lambda event: self.tasks_listbox.add_to_db_and_listbox(
            self.input.get_and_delete_text())) # Также дублируем для нажатия Enter

        self.remove_button = Button(
            master=self, text='Удалить', command=self.tasks_listbox.delete_from_db_and_listbox)
        self.remove_button.grid(column=2, row=3)

        self.done_button = Button(master=self, text='Выполнено', command=lambda: utils.mark_as_completed())
        self.done_button.grid(column=0, row=3)

        self.show_completed_button = Button(
            master=self, text='Показать выполненные', command=utils.switch_visible_frame_completed_tasks)
        self.show_completed_button.grid(column=0, row=4)


def run():
    main_window = MainWindow()
    main_window.mainloop()


if __name__ == '__main__':
    run()
