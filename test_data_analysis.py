import unittest
from file_io import FileIO
from cpu import CPU
from cpu_data import ProcessInfo
from data_analysis import Section


class TestDataAnalysis(unittest.TestCase):

    def test_FileIO_methods(self):
        f_in = 'file_io_test.csv'
        sections = [Section(11, 15), Section(15, 17)]

        with open(f_in, 'w') as f:
            f.write(f'Process,Event Type,Event SubType,Thread,Start (s),End (s),Duration (µs),IRP,File Object,Size (B),File Path,Offset,Flags,Result,Count\n')
            f.write(f'p1,Create,,,"11,1","11,2","100000",,,0,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p1,Create,,,"11,1","12,1","1000000",,,0,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p1,Read,,,"13,1","14,2","1100000",,,1,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p1,Read,,,"13,1","14,2","1100000",,,2,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p1,Read,,,"15,1","16,2","1100000",,,3,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p1,Read,,,"15,1","16,2","1100000",,,4,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p1,Write,,,"12,1","12,4","300000",,,5,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p1,Write,,,"15,1","15,4","300000",,,6,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p2,Create,,,"11,1","11,2","100000",,,0,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p2,Create,,,"11,1","12,1","1000000",,,0,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p2,Read,,,"13,1","14,2","1100000",,,1,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p2,Read,,,"13,1","14,2","1100000",,,2,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p2,Read,,,"15,1","16,2","1100000",,,3,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p2,Read,,,"15,1","16,2","1100000",,,4,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p2,Write,,,"12,1","12,4","300000",,,5,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p2,Write,,,"15,1","15,4","300000",,,6,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p3,Create,,,"11,1","11,2","100000",,,0,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p3,Create,,,"11,1","12,1","1000000",,,0,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p3,Read,,,"13,1","14,2","1100000",,,1,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p3,Read,,,"13,1","14,2","1100000",,,2,C:\\Program Files...,0,...,...,1\n')
            f.write(f'p3,Read,,,"15,1","16,2","1100000",,,3,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p3,Read,,,"15,1","16,2","1100000",,,4,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p3,Write,,,"12,1","12,4","300000",,,5,C:\\ProgramData...,0,...,...,1\n')
            f.write(f'p3,Write,,,"15,1","15,4","300000",,,6,C:\\Program Files...,0,...,...,1\n')

        file_io = FileIO(f_in, sections)
        file_io.filter()

        top_durations = file_io.get_top_durations()
        top_sizes = file_io.get_top_sizes()

        expected_top_durations = {
            Section(11, 15): [('p1', 300000), ('p2', 300000), ('p3', 300000)], 
            Section(15, 17): [('p1', 300000), ('p2', 300000), ('p3', 300000)]
        }
        expected_top_sizes = {
            Section(11, 15): [('p1', 1), ('p2', 1), ('p3', 1)], 
            Section(15, 17): [('p1', 7), ('p2', 7), ('p3', 7)]
        }

        self.assertEquals(top_durations, expected_top_durations)
        self.assertEquals(top_sizes, expected_top_sizes)

    def test_CPU_methods(self):
        f_in = 'cpu_test.csv'
        sections = [Section(1, 3), Section(4, 6)]

        with open(f_in, 'w') as f:
            f.write(f'Process,Module,TimeStamp (s)\n')
            f.write(f'p1,m1,"1,1"\n')
            f.write(f'p3,m2,"1,2"\n')
            f.write(f'p1,m3,"1,3"\n')
            f.write(f'p1,m2,"1,35"\n')
            f.write(f'p2,m1,"2,1"\n')
            f.write(f'p1,m3,"2,2"\n')
            f.write(f'p2,m1,"2,3"\n')
            f.write(f'p1,m3,"3,2"\n')
            f.write(f'p3,m2,"3,3"\n')
            f.write(f'p1,m3,"3,35"\n')
            f.write(f'p1,m3,"4,1"\n')
            f.write(f'p3,m1,"4,2"\n')
            f.write(f'p3,m2,"4,3"\n')
            f.write(f'p2,m1,"4,4"\n')
            f.write(f'p2,m1,"5,1"\n')
            f.write(f'p2,m2,"5,2"\n')
            f.write(f'p1,m2,"5,3"\n')
            f.write(f'p1,m3,"5,4"\n')
            f.write(f'p3,m1,"6,1"\n')
            f.write(f'p1,m2,"6,2"')

        cpu = CPU(f_in, sections)
        cpu.filter()

        top_processes = cpu.get_top_processes()
        top_modules = cpu.get_top_modules()

        expected_top_processes = {
            Section(1, 3): [('p1', 4), ('p2', 2), ('p3', 1)],
            Section(4, 6): [('p1', 3), ('p2', 3), ('p3', 2)]
        }
        expected_top_modules = {
            Section(1, 3): {
                'p1': [('m3', 2), ('m1', 1), ('m2', 1)],
                'p2': [('m1', 2)],
                'p3': [('m2', 1)]
            },
            Section(4, 6): {
                'p1': [('m3', 2), ('m2', 1)],
                'p2': [('m1', 2), ('m2', 1)],
                'p3': [('m1', 1), ('m2', 1)]
            }
        }

        self.assertEquals(top_processes, expected_top_processes)
        self.assertEquals(top_modules, expected_top_modules)

    def test_ProcessInfo_methods(self):
        pi = ProcessInfo()
        pi.add('p1', 'm1')
        pi.add('p1', 'm1')
        pi.add('p1', 'm1')
        pi.add('p1', 'm1')
        pi.add('p1', 'm2')
        pi.add('p1', 'm2')

        pi.add('p2', 'm1')
        pi.add('p2', 'm1')
        pi.add('p2', 'm2')

        pi.add('p3', 'm1')

        pi.add('p4', 'm1')
        pi.add('p4', 'm2')
        pi.add('p4', 'm2')
        pi.add('p4', 'm3')
        pi.add('p4', 'm4')

        top_processes = pi.get_top_processes(2)
        top_modules_p1 = pi.get_top_modules_for_proc('p1', 2)
        top_modules_p2 = pi.get_top_modules_for_proc('p2', 2)
        top_modules_p3 = pi.get_top_modules_for_proc('p3', 2)
        top_modules_p4 = pi.get_top_modules_for_proc('p4', 2)

        expected_top_processes = [('p1', 6), ('p4', 5)]
        expected_top_modules_p1 = [('m1', 4), ('m2', 2)]
        expected_top_modules_p2 = [('m1', 2), ('m2', 1)]
        expected_top_modules_p3 = [('m1', 1)]
        expected_top_modules_p4 = [('m2', 2), ('m1', 1)]

        self.assertEquals(top_processes, expected_top_processes)
        self.assertEquals(top_modules_p1, expected_top_modules_p1)
        self.assertEquals(top_modules_p2, expected_top_modules_p2)
        self.assertEquals(top_modules_p3, expected_top_modules_p3)
        self.assertEquals(top_modules_p4, expected_top_modules_p4)


if __name__ == '__main__':
    unittest.main()
