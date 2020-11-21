import csv


class FileIO:
    def __init__(self, f_in, sections):
        self._durations = {}
        self._sizes = {}
        self._sections = sections
        self._f_in = f_in

    def filter(self):
        '''
        Фильтрация входных данных из файла по интервалам для операции чтения из 'C:\\ProgramData' и записи
        '''
        with open(self._f_in, 'r') as f:
            reader = csv.reader(f)
            # Пропуск заголовка
            next(reader)

            for row in reader:
                # Исключение, если пропущена какая-нибудь информация
                if len(row) < 11:
                    raise ValueError(f'Invalid number of arguments: {len(row)}')
                if (row[1] == 'Write') or (row[1] == 'Read' and row[10].startswith(r'C:\ProgramData')):
                    try:
                        start = float(row[4].replace(',', '.'))
                        end = float(row[5].replace(',', '.'))
                    except ValueError:
                        raise ValueError(f'Incorrect section: {start}, {end}')
                    for sec in self._sections:
                        # Проверка попадания в один из интервалов
                        if sec.start <= start and end <= sec.end:
                            if row[1] == 'Write':
                                try:
                                    time = float(row[6].replace(',', '.'))
                                except ValueError:
                                    raise ValueError(f'Incorrect time: {time}')
                                # Если интервала нет в словаре, создаем новый словарь для данного интервала
                                if not sec in self._durations:
                                    self._durations[sec] = {}
                                # Если процесса нет в словаре интервала, устанавливаем время для данного процесса в 0
                                if not row[0] in self._durations[sec]:
                                    self._durations[sec][row[0]] = 0
                                # Прибавляем время работы для данного процесса
                                self._durations[sec][row[0]] += time
                            else:
                                try:
                                    size = float(row[9].replace(',', '.'))
                                except ValueError:
                                    raise ValueError(f'Incorrect size: {size}')
                                # Если интервала нет в словаре, создаем новый словарь для данного интервала
                                if not sec in self._sizes:
                                    self._sizes[sec] = {}
                                # Если процесса нет в словаре интервала, устанавливаем количество прочитанных данных для данного процесса в 0
                                if not row[0] in self._sizes[sec]:
                                    self._sizes[sec][row[0]] = 0
                                # Прибавляем количество прочитанных данных для данного процесса
                                self._sizes[sec][row[0]] += size

    def _get_top_duration(self, sec, count):
        '''
        Возвращает список из 'count' кортежей: 
            tuple[0] - процесс, tuple[1] - время работы
        '''
        return FileIO._sort_by_values(self._durations[sec], count)

    def _get_top_size(self, sec, count):
        '''
        Возвращает список из 'count' кортежей: 
            tuple[0] - процесс, tuple[1] - объем прочитанных данных
        '''
        return FileIO._sort_by_values(self._sizes[sec], count)

    @staticmethod
    def _sort_by_values(collection, count):
        '''
        Возвращает список из 'count' кортежей: 
            tuple[0] - процесс, tuple[1] - число, по которому происходит фильтрация
        '''
        res = list(collection.items())
        res.sort(key=lambda i: i[1], reverse=True)
        return res[:count]

    def get_top_durations(self):
        '''
        Возвращает словарь, где ключ - интервал, значение - список из топ 3 кортежей: 
            tuple[0] - процесс, tuple[1] - время работы
        '''
        res = {}
        for sec in self._sections:
            if sec in self._durations:
                res[sec] = self._get_top_duration(sec, 3)
        return res

    def get_top_sizes(self):
        '''
        Возвращает словарь, где ключ - интервал, значение - список из топ 3 кортежей: 
            tuple[0] - процесс, tuple[1] - объем прочитанных данных
        '''
        res = {}
        for sec in self._sections:
            if sec in self._sizes:
                res[sec] = self._get_top_size(sec, 3)
        return res
