from django.http import HttpRequest, HttpResponse
import json
import os


class StringHasher:
    @staticmethod
    def get_hash(s):
        number = 0
        for letter in s:
            number += ((ord(letter)**2) << 2 >> 1)

        result = str(number)
        ret = ''
        for i in range(0, len(result), 2):
            ret += chr(int(result[i] + result[i+1]))

        return ret


class ClientsProfilingFile:
    def __init__(self, path='clients', file_name='clients.json'):
        if not os.path.exists(path):
            os.mkdir(path)

        self.path = path
        self.file_name = file_name
        self.file = open(self.path + '/' + self.file_name, 'w+')
        self.json_file = {}
        try:
            self.json_file = json.load(self.file)
        except json.decoder.JSONDecodeError:
            pass

    def write(self):
        json.dump(self.json_file, self.file)
        self.file.flush()

    def add_client(self, data):
        if data[0] not in self.json_file:
            self.json_file[data[0]] = data[1]

    def __del__(self):
        self.write()

