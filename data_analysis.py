import sys
import zipfile
from collections import namedtuple
from cpu import CPU
from file_io import FileIO

Section = namedtuple('Section', ['start', 'end'])


def main():
    args = sys.argv[1:]

    # Проверка количества аргументов
    if len(args) < 5 or (len(args) & 1) != 1:
        raise ValueError(f'Invalid number of arguments: {len(args)}')

    f_in = args[0]
    f_out = args[1]
    prof = args[2].upper()

    sections = []

    for i in range(3, len(args), 2):
        try:
            start = float(args[i])
            end = float(args[i + 1])
        except ValueError:
            raise ValueError(f'Incorrect input: [{start}, {end}]')

        # Проверка корректности интервала
        if start > end or start < 0:
            raise ValueError(f'Incorrect section: [{start}, {end}]')

        # Проверка дублирования интервала
        sec = Section(start, end)
        if not sec in sections:
            sections.append(sec)

    # Для .zip файлов
    if f_in.endswith('.zip'):
        with zipfile.ZipFile(f_in, 'r') as zp:
            f_in = f_in[:-4] + '.csv'
            if f_in in zp.namelist():
                zp.extract(f_in)
            else:
                raise ValueError(f'File {f_in} was not found in archive')

    if prof == 'CPU':
        cpu = CPU(f_in, sections)
        cpu.filter()

        top_processes = cpu.get_top_processes()
        top_modules = cpu.get_top_modules()

        # Вывод в файл
        log_cpu(f_out, top_processes, top_modules)

    elif prof == 'FILE_IO':
        file_io = FileIO(f_in, sections)
        file_io.filter()

        top_durations = file_io.get_top_durations()
        top_sizes = file_io.get_top_sizes()

        # Вывод в файл
        log_file_io(f_out, top_durations, top_sizes)


def log_cpu(filename, top_proc, top_mods):
    '''
    Запись в файл информации для CPU файла
    '''
    with open(filename, 'w') as f:
        for key in sorted(top_proc):
            f.write(f'Section: ({key.start} - {key.end}):\n')
            for prc in top_proc[key]:
                f.write(f'{" " * 3}Process: {prc[0]} - {prc[1]}:\n')
                for line in top_mods[key][prc[0]]:
                    f.write(f'{" " * 6}Module: {line[0]} - {line[1]}\n')


def log_file_io(filename, top_dur, top_sz):
    '''
    Запись в файл информации для FILE_IO файла
    '''
    with open(filename, 'w') as f:
        f.write('Write:\n')
        for key in sorted(top_dur):
            f.write(f'{" " * 3}Section: ({key.start} - {key.end}):\n')
            for prc in top_dur[key]:
                f.write(f'{" " * 6}Process: {prc[0]} - {round(prc[1], 2)}\n')
        f.write('Read:\n')
        for key in sorted(top_sz):
            f.write(f'{" " * 3}Section: ({key.start} - {key.end}):\n')
            for prc in top_sz[key]:
                f.write(f'{" " * 6}Process: {prc[0]} - {prc[1]}\n')


if __name__ == '__main__':
    main()
