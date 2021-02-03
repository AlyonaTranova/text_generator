import zipfile


class TextStatistics:

    def __init__(self, file_name):
        self.file_name = file_name
        self.chars_count = {}
        self.total_quantity = {'total': 0}
        self.data = {}
        self.sequence_count = {}
        self.analyze_count = 4

    def unzip(self):
        zip_file = zipfile.ZipFile(self.file_name, 'r')
        for filename in zip_file.namelist():
            zip_file.extract(filename)

    def collect_chars(self, encoding):
        if self.file_name.endswith('.zip'):
            self.unzip()
        with open(self.file_name, mode='r', encoding=encoding) as file:
            for line in file:
                self._collect_chars(line)

    def _collect_chars(self, line):
        for char in line:
            if char.isalpha() is True:
                if char in self.chars_count:
                    self.chars_count[char] += 1
                else:
                    self.chars_count[char] = 1

    def chars_sorting(self):
        self.data = {}
        self.data = sorted(self.chars_count.items(), key=lambda i: i[1], reverse=True)

    def total_chars_count(self):
        for chars in self.chars_count.values():
            self.total_quantity['total'] += chars
        print('Итого: {}'.format(self.total_quantity['total']))

    def run_function(self, encoding):
        self.collect_chars(encoding=encoding)
        self.chars_sorting()
        self.total_chars_count()


class SortByKey(TextStatistics):

    def chars_sorting(self):
        self.data = sorted(self.chars_count, key=self.chars_count.get, reverse=False)


class SortByValue(TextStatistics):

    def chars_sorting(self):
        self.data = sorted(self.chars_count.items(), key=lambda i: i[1], reverse=False)


class SortByKeyReversed(TextStatistics):

    def chars_sorting(self):
        self.data = sorted(self.chars_count, key=self.chars_count.get, reverse=True)
