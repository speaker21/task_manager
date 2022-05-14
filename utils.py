import tkinter as tk
from gui import ActiveListbox, CompletedListbox 

LIST = ['one', 'two', 'three']

def mark_as_completed(listbox_tasks: ActiveListbox, listbox_complete: CompletedListbox):
    if listbox_tasks.is_selected():
        selected_data = listbox_tasks.get_selected_data()
        listbox_tasks.delete_from_db_and_listbox()

        listbox_complete.add_to_db_and_listbox(selected_data)