class ProcessInfo:
    def __init__(self):
        # Ключ - процесс, значение - сколько раз он встречается в интервале
        self._process_counter = {}
        # Ключ - процесс, значение - словарь модулей
        self._modules_counter = {}

    def add(self, proc, module):
        '''
        Добавляет информацию о процессе и модуле.
        Если процесс встречался раньше, информация о нем обновляется.
        Если модуль встречался раньше, информация о нем обновляется.
        '''
        if not proc in self._process_counter:
            self._process_counter[proc] = 0
            self._modules_counter[proc] = {}

        if not module in self._modules_counter[proc]:
            self._modules_counter[proc][module] = 0

        self._process_counter[proc] += 1
        self._modules_counter[proc][module] += 1

    def get_top_processes(self, count):
        '''
        Возвращает список из 'count' кортежей: 
            tuple[0] - процесс, tuple[1] - сколько раз встречается
        '''
        return ProcessInfo._sort_by_values(self._process_counter, count)

    def get_top_modules_for_proc(self, proc, count):
        '''
        Возвращает список из 'count' кортежей для заданного процесса: 
            tuple[0] - модуль, tuple[1] - сколько раз встречается
        '''
        return ProcessInfo._sort_by_values(self._modules_counter[proc], count)

    @staticmethod
    def _sort_by_values(collection, count):
        '''
        Возвращает список из 'count' кортежей: 
            tuple[0] - модуль/процесс, tuple[1] - сколько раз встречается
        '''
        res = list(collection.items())
        res.sort(key=lambda i: i[1], reverse=True)
        return res[:count]
