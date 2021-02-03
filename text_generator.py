from random import randint

from char_sorting import *


class TextGeneration(TextStatistics):

    def collect_sequence(self, encoding):
        if self.file_name.endswith('.zip'):
            self.unzip()
        self.sequence = ' ' * self.analyze_count
        with open(self.file_name, 'r', encoding=encoding) as file:
            for line in file:
                self._collect_sequence(line=line[:-1])

    def _collect_sequence(self, line):
        for char in line:
            if self.sequence in self.sequence_count:
                if char in self.sequence_count[self.sequence]:
                    self.sequence_count[self.sequence][char] += 1
                else:
                    self.sequence_count[self.sequence][char] = 1
            else:
                self.sequence_count[self.sequence] = {char: 1}
            self.sequence = self.sequence[1:] + char

    def prep_for_generation(self):
        self.total_quantity = {}
        self.stat_for_generate = {}
        for sequence, char_stat in self.sequence_count.items():
            self.total_quantity[sequence] = 0
            self.stat_for_generate[sequence] = []
            for char, count in char_stat.items():
                self.total_quantity[sequence] += count
                self.stat_for_generate[sequence].append([count, char])
                self.stat_for_generate[sequence].sort(reverse=True)

    def chat(self, number_of_tokens, out_file_name=None):
        printed = 0
        if out_file_name is not None:
            file = open(out_file_name, 'w', encoding='utf8')
        else:
            file = None

        sequence = ' ' * self.analyze_count
        spaces_printed = 0
        while printed < number_of_tokens:
            char = self._get_char(char_stat=self.stat_for_generate[sequence], total=self.total_quantity[sequence])
            if file:
                file.write(char)
            else:
                print(char, end='')
            if char == ' ':
                spaces_printed += 1
                if spaces_printed >= 10:
                    if file:
                        file.write('\n')
                    else:
                        print()
                    spaces_printed = 0
            printed += 1
            sequence = sequence[1:] + char
        if file:
            file.close()

    def _get_char(self, char_stat, total):
        dice = randint(1, total)
        pos = 0
        for count, char in char_stat:
            pos += count
            if dice <= pos:
                break
        return char

    def run_function(self, encoding):
        self.collect_sequence(encoding=encoding)
        self.prep_for_generation()
        self.chat(number_of_tokens=1000, out_file_name=None)


def main():
    generator = TextGeneration(TextStatistics)
    generator.run_function(encoding='utf8')


if __name__ == '__main__':
    main()
