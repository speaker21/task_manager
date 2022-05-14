class Settings:
    frame_active_tasks = None
    frame_completed_tasks = None

    @classmethod
    def set_data(cls, frame_active_tasks, frame_completed_tasks):
        cls.frame_active_tasks = frame_active_tasks
        cls.frame_completed_tasks = frame_completed_tasks

def mark_as_completed():
    listbox_tasks = Settings.frame_active_tasks.tasks_listbox
    listbox_complete = Settings.frame_completed_tasks.complete_listbox
    
    if listbox_tasks.is_selected():
        selected_data = listbox_tasks.get_selected_data()
        listbox_tasks.delete_from_db_and_listbox()

        listbox_complete.add_to_db_and_listbox(selected_data)

def switch_visible_frame_completed_tasks():
    Settings.frame_completed_tasks.switch_visible()