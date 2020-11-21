import csv
from cpu_data import ProcessInfo


class CPU:
    def __init__(self, f_in, sections):
        self._sections_info = {}
        self._sections = sections
        self._f_in = f_in

    def filter(self):
        '''
        Фильтрация входных данных из файла по заданным интервалам
        '''
        with open(self._f_in, 'r') as f:
            reader = csv.reader(f)
            # Пропуск заголовка
            next(reader)

            for row in reader:
                # Исключение, если пропущены процесс/модуль/время
                if len(row) < 3:
                    raise ValueError(f'Invalid number of arguments: {len(row)}')
                # Пропуск 'Idle (0)' по условию
                if row[0] == 'Idle (0)':
                    continue
                try:
                    time = float(row[2].replace(',', '.'))
                except ValueError:
                    raise ValueError(f'Incorrect input: {time}')
                for sec in self._sections:
                    # Проверка попадания в один из интервалов
                    if sec.start <= time <= sec.end:
                        # Если интервала нет в словаре, добавляем объект информации о процессах для данного интервала
                        if not sec in self._sections_info:
                            self._sections_info[sec] = ProcessInfo()
                        # Добавляю инфу о процессе и модуле в объект информации о процессах
                        self._sections_info[sec].add(row[0], row[1])

    def get_top_processes(self):
        '''
        Возвращает словарь, где ключ - интервал, значение - список из топ 3 кортежей: 
            tuple[0] - процесс, tuple[1] - сколько раз встречается
        '''
        res = {key: self._sections_info[key].get_top_processes(3) for key in self._sections_info}
        return res

    def get_top_modules(self):
        '''
        Возвращает словарь, где ключ - интервал, значение - словарь из топ 3 процессов, 
        где ключ - процесс, значение - список кортежей: 
            tuple[0] - модуль, tuple[1] - сколько раз встречается
        '''
        res = {}
        for key in self._sections_info:
            prcs = self._sections_info[key].get_top_processes(3)
            res[key] = {}
            for prc in prcs:
                res[key][prc[0]] = self._sections_info[key].get_top_modules_for_proc(prc[0], 5)
        return res
