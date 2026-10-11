import tkinter as tk
from tkinter import filedialog, messagebox
import psutil
import subprocess

# окно и глобальные переменные
root = tk.Tk()
root.title("Injector Launcher")
root.geometry("400x500")

#Живые переменные, которые будут хранить наш выбор
selected_dll_path = tk.StringVar()
#Мозг кнопок

def refresh_process_list():
    """Очищает список и заполняет его актуальными процессами."""
    process_listbox.delete(0, tk.END)
    for process in psutil.process_iter(['name']):
        try:
            #используем process а не 'proc', и правильный доступ к '.info['name']'
            process_listbox.insert(tk.END, process.info['name'])
        except (psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied):
            pass  # Игнорируем проблемные процессы
def select_dll():
    """Открывает диалог выбора файла и сохраняет путь к DLL"""
    filepath = filedialog.askopenfilename(
        title="Select DLL to Inject",
        filetypes=(("DLL files", "*.dll"), ("All files", "*.*"))  # фильтр для удобства
    )
    if filepath:
        selected_dll_path.set(filepath)  # Обновляем живую переменную
def perform_injection():
    """Главная функция: собирает данные и запускает C++ инжектор."""

    #Правильная логика получения выбранного процесса ---
    try:
        selected_index = process_listbox.curselection()[0]
        proc_name = process_listbox.get(selected_index)
    except IndexError:
        # Эта ошибка происходит, если в списке ничего не выбрано
        messagebox.showerror("Error", "No process selected in the list!")
        return

    #логика получения пути к DLL ---
    dll_path = selected_dll_path.get()
    if not dll_path:
        messagebox.showerror("Error", "No DLL file selected!")
        return
    try:
        print(f"Attempting to inject '{dll_path}' into '{proc_name}'...")

        # Убедись, что injector.exe находится в той же папке, что и этот скрипт
        command = ["injector.exe", proc_name, dll_path]

        # Запускаем C++ программу, передавая ей имя процесса и путь к DLL
        subprocess.run(command, check=True)

        messagebox.showinfo("Success", f"Injection command sent to '{proc_name}'.")

    except FileNotFoundError:
        # Эта ошибка произойдет, если injector.exe не найден
        messagebox.showerror("Error", "injector.exe not found!\nPlace it in the same folder as the launcher.")
    except subprocess.CalledProcessError:
        # Эта ошибка произойдет, если C++ инжектор вернет код ошибки (return 1)
        messagebox.showerror("Injection Failed",
                             "The injector failed. This can happen if the target process has administrator rights and our tool doesn't.")
    except Exception as e:
        # Ловим любые другие непредвиденные ошибки
        messagebox.showerror("An Unknown Error Occurred", str(e))
# Рамка для списка и скроллбара
list_frame = tk.Frame(root)
list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
# Скроллбар для списка
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Список процессов
process_listbox = tk.Listbox(list_frame, height=15, yscrollcommand=scrollbar.set)
process_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=process_listbox.yview)  # Связываем скроллбар со списком
# Кнопка обновления
refresh_button = tk.Button(root, text="Refresh Process List", command=refresh_process_list)
refresh_button.pack(pady=5)
# Метка, которая будет показывать путь к выбранной DLL
# wraplength переносит длинный текст на новую строку
dll_label_info = tk.Label(root, text="Selected DLL:")
dll_label_info.pack()
dll_label = tk.Label(root, textvariable=selected_dll_path, fg="blue", wraplength=380)
dll_label.pack(padx=10)
# Кнопка выбора DLL
select_dll_button = tk.Button(root, text="Select DLL...", command=select_dll)
select_dll_button.pack(pady=5)
# Главная кнопка инъекции
inject_button = tk.Button(root, text="INJECT!", bg="red", fg="white", font=("Arial", 16, "bold"),command=perform_injection)
inject_button.pack(pady=20, ipadx=10, ipady=5)
refresh_process_list()
root.mainloop()
