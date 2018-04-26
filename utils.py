import os
import torch
import glob
import json
from ast import literal_eval


def get_number_processors():
    """Получить количество процессоров CPU.
    Возвращает:
        num (int): Число процессоров.
    Пример:
        >>> get_number_processors()
        8
    """
    try:
        num = os.cpu_count()
    except Exception:
        import multiprocessing  # исключение, если отсутствует мультипроцессор
        num = multiprocessing.cpu_count()
    return num


get_number_processors()


def get_gpu_name():
    """ Получить GPUs системы
    Пример:
        >>> get_gpu_name()
        ['GeForce GTX 970']
    """
    try:
        gpu_name = [torch.cuda.get_device_name(0)]
        return gpu_name
    except Exception as e:
        print(e)


def get_gpu_memory():
    """ Получить память GPUs системы
    Пример:
        >>> get_gpu_memory()
        [865280]
    """
    try:
        gpu_memory = [torch.cuda.memory_allocated()]
        return gpu_memory
    except Exception as e:
        print(e)


def get_cuda_version():
    """ Получить версию CUDA
    Пример:
        >>> get_cuda_version()
        '8.0'
    """
    try:
        cuda_version = torch.version.cuda
        return cuda_version
    except Exception as e:
        print(e)


def format_dictionary(dct, indent=4):
    """ Форматирует словарь для вывода на консоль
    Параметры:
        dct (dict): Словарь.
        indent (int): Отступ по левому краю.
    Возвращяет:
        result (str): Форматированный словарь
    Пример:
        >>> dct = {'bkey':1, 'akey':2}
        >>> print(format_dictionary(dct))
        {
            "akey": 2,
            "bkey": 1
        }
    """
    return json.dumps(dct, indent=indent, sort_keys=True)


def get_filenames_in_folder(folderpath):
    """ Возвращает имена файлов в директории.
    Параметры:
        folderpath (str): Путь директории
    Возвращяет:
        number (list): Число файлов в директории
    Пример:
        >>> get_filenames_in_folder('C:/run3x/codebase/python/minsc')
        ['paths.py', 'system_info.py', '__init__.py']
    """
    names = [os.path.basename(x) for x in glob.glob(os.path.join(folderpath, '*'))]
    return sorted(names)


def get_files_in_folder_recursively(folderpath):
    """ Возвращает файлы директории рекурсивно recursivaly.
    Параметры:
        folderpath (str): folder path
    Возвращяет:
        filelist (list): list of files
    Пример:
        >>> get_files_in_folder_recursively(r'C:\\run3x\\codebase\\command_line')
        ['linux\\compress.txt', 'linux\\paths.txt', 'windows\\resources_management.txt']
    """
    if folderpath[-1] != os.path.sep: #Add final '/' if it doesn't exist
        folderpath += os.path.sep
    names = [x.replace(folderpath,'') for x in glob.iglob(folderpath+'/**', recursive=True) if os.path.isfile(x)]
    return sorted(names)


def _make_directory(directory):
    """ Создать папку """
    if not os.path.isdir(directory):
        os.makedirs(directory)


def decode_string(s):
    """ Конвертировать символ строки в число или bool.
    Параметры:
        s (str): String
    Возвращяет:
        val (str,float,int or bool): Декодированное значение
    Пример:
        >>> decode_string('a')
        'a'
        >>> val = decode_string('1.0')
        >>> type(val)
        <class 'int'>
        >>> val
        1
        >>> val = decode_string('1')
        >>> type(val)
        <class 'int'>
        >>> val
        1
        >>> val = decode_string('1.5')
        >>> type(val)
        <class 'float'>
        >>> val
        1.5
        >>> val = decode_string('True')
        >>> type(val)
        <class 'bool'>
        >>> val
        True
    """
    if isinstance(s, str):
        # Does it represent a literal?
        try:
            val = literal_eval(s)
        except:
            # if it doesn't represent a literal, no conversion is done
            val = s
    else:
        # It's already something other than a string
        val = s
    # Is the float actually an int? (i.e. is the float 1.0 ?)
    if isinstance(val, float):
        if val.is_integer():
            return int(val)
        return val
    return val
