# Ваша задача - написать программу, которая принимает на вход директорию и рекурсивно обходит эту директорию и все
# вложенные директории. Результаты обхода должны быть сохранены в нескольких форматах: JSON, CSV и Pickle. Каждый
# результат должен содержать следующую информацию:
#
# Путь к файлу или директории: Абсолютный путь к файлу или директории. Тип объекта: Это файл или директория.
# Размер: Для файлов - размер в байтах, для директорий - размер, учитывая все вложенные файлы и директории в байтах.
# Важные детали:
#
# Для дочерних объектов (как файлов, так и директорий) укажите родительскую директорию.
#
# Для файлов сохраните их размер в байтах.
#
# Для директорий, помимо их размера, учтите размер всех файлов и директорий, находящихся внутри данной директории,
# и вложенных директорий.
#
# Программа должна использовать рекурсивный обход директорий, чтобы учесть все вложенные объекты.
#
# Результаты должны быть сохранены в трех форматах: JSON, CSV и Pickle. Форматы файлов должны быть выбираемыми.
#
# Для обхода файловой системы вы можете использовать модуль os.
#
# Вам необходимо написать функцию traverse_directory(directory), которая будет выполнять обход директории и возвращать
# результаты в виде списка словарей. После этого результаты должны быть сохранены в трех различных файлах
# (JSON, CSV и Pickle) с помощью функций save_results_to_json, save_results_to_csv и save_results_to_pickle.
#
# Файлы добавляются в список results в том порядке, в котором они встречаются при рекурсивном обходе директорий.
# При этом сначала добавляются файлы, а затем директории.
#
# Для каждого файла (name в files), сначала создается полный путь к файлу (path = os.path.join(root, name)), и затем
# получается размер файла (size = os.path.getsize(path)). Информация о файле добавляется в список results в виде
# словаря {'Path': path, 'Type': 'File', 'Size': size}.
#
# Затем, для каждой директории (name в dirs), также создается полный путь к директории (path = os.path.join(root, name)),
# и вызывается функция get_dir_size(path), чтобы получить размер всей директории с учетом ее содержимого.
# Информация о директории добавляется в список results в виде словаря {'Path': path, 'Type': 'Directory', 'Size': size}.


########################################################################################################################
# old task
# Задание
# 📌 Решить задачи, которые не успели решить на семинаре.
# 📌 Напишите функцию, которая получает на вход директорию и рекурсивно
# обходит её и все вложенные директории. Результаты обхода сохраните в файлы json, csv и pickle.
# ○ Для дочерних объектов указывайте родительскую директорию.
# ○ Для каждого объекта укажите файл это или директория.
# ○ Для файлов сохраните его размер в байтах, а для директорий размер файлов в ней
#   с учётом всех вложенных файлов и директорий.
# 📌 Соберите из созданных на уроке и в рамках домашнего задания функций пакет для работы с файлами разных форматов.

# Ожидаемый ответ:
#
# [{'Path': 'geekbrains/california_housing_train.csv', 'Type': 'File', 'Size': 1457}, {'Path': 'geekbrains/student_performance.txt', 'Type': 'File', 'Size': 21}, {'Path': 'geekbrains/covid.json', 'Type': 'File', 'Size': 35228079}, {'Path': 'geekbrains/input2.txt', 'Type': 'File', 'Size': 9}, {'Path': 'geekbrains/avg_list.txt', 'Type': 'File', 'Size': 21}, {'Path': 'geekbrains/age_report.csv', 'Type': 'File', 'Size': 85}, {'Path': 'geekbrains/my_ds_projects', 'Type': 'Directory', 'Size': 171}, {'Path': 'geekbrains/my_ds_projects/My-code', 'Type': 'Directory', 'Size': 171}, {'Path': 'geekbrains/my_ds_projects/My-code/GB_data', 'Type': 'Directory', 'Size': 171}, {'Path': 'geekbrains/my_ds_projects/My-code/GB_data/fruits.csv', 'Type': 'File', 'Size': 101}, {'Path': 'geekbrains/my_ds_projects/My-code/GB_data/list_of_names.txt', 'Type': 'File', 'Size': 70}]
#
# Ваш ответ:
#
# [{'Path': 'geekbrains/california_housing_train.csv', 'Type': 'File', 'Size': 1457}, {'Path': 'geekbrains/student_performance.txt', 'Type': 'File', 'Size': 21}, {'Path': 'geekbrains/my_ds_projects', 'Type': 'Directory', 'Size': 171}, {'Path': 'geekbrains/covid.json', 'Type': 'File', 'Size': 35228079}, {'Path': 'geekbrains/input2.txt', 'Type': 'File', 'Size': 9}, {'Path': 'geekbrains/avg_list.txt', 'Type': 'File', 'Size': 21}, {'Path': 'geekbrains/age_report.csv', 'Type': 'File', 'Size': 85}, {'Path': 'my_ds_projects/My-code', 'Type': 'Directory', 'Size': 171}, {'Path': 'My-code/GB_data', 'Type': 'Directory', 'Size': 171}, {'Path': 'GB_data/fruits.csv', 'Type': 'File', 'Size': 101}, {'Path': 'GB_data/list_of_names.txt', 'Type': 'File', 'Size': 70}]
#


import csv
import json
import os
import pathlib
import pickle


TYPE_FILE = 'File'
TYPE_DIRECTORY = 'Directory'
PATH = 'Path'
TYPE = 'Type'
SIZE = 'Size'


def traverse_directory(path):
    files = pathlib.Path(path)
    directory = list()
    for file in files.rglob('*'):
        files_dict = dict()
        basename = os.path.basename(file)  # parent directory
        parent_name = file.parent.name  # get tail from path
        parent_file_name = os.path.join(parent_name, basename)  # parent directory
        is_dir = os.path.isdir(file)
        type_of_file: str = TYPE_FILE
        size: int = int()
        if is_dir:
            for path, dirs, files in os.walk(file):
                for f in files:
                    fp = os.path.join(path, f)
                    size += os.path.getsize(fp)
            type_of_file = TYPE_DIRECTORY
        else:
            size = os.path.getsize(file)
        files_dict[PATH] = parent_file_name
        files_dict[TYPE] = type_of_file
        files_dict[SIZE] = size
        directory.append(files_dict)
    return directory


def save_results_to_json(directories, file_name=None):
    f_json = open(file_name, 'w', encoding='utf-8')
    json.dump(directories, f_json, ensure_ascii=False, indent=2)


def save_results_to_csv(directories, file_name=None):
    f_csv = open(file_name, 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(f_csv, dialect='excel', delimiter=';')
    for index, f_item in enumerate(directories):
        if index == 0:
            head = list(f_item.keys())
            csv_writer.writerow(head)
        csv_writer.writerow([f_item[PATH], f_item[TYPE], f_item[SIZE]])


def save_results_to_pickle(directories, file_name=None):
    f_pickle = open(file_name, 'wb')
    pickle.dump(directories, f_pickle)


path_to_directorie = os.getcwd()
directories = traverse_directory(path_to_directorie)
save_results_to_json(directories, 'directories-JSON.json')
save_results_to_csv(directories, 'directories-CSV.csv')
save_results_to_pickle(directories, 'directories-PICKLE.pickle')
