import sys
from time import time
from os import mkdir
from sys import stdout

from typing import IO

from minion import Lineup

class Analysis:
    std_out: IO = sys.stdout

    def __init__(self, stdout: bool = True):
        self.stdout = stdout

    def __enter__(self):
        self.start_time = time()
        self.name = str(int(self.start_time * 1000))

        mkdir(f"./anal/{self.name}")
        self.outcomes = open(f"./anal/{self.name}/outcomes.csv", "w")
        self.outcomes.write("iteration, outcomes\n")

        self.lineups = open(f"./anal/{self.name}/linesups.txt", "w")
        self.log = open(f"./anal/{self.name}/log.txt", "w")

        if self.stdout:
            sys.stdout = StreamTee(sys.stdout, self.log)
        else:
            sys.stdout = self.log

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.outcomes.close()
        self.lineups.close()
        self.log.close()

        sys.stdout = Analysis.std_out


class StreamTee(object):
    # Based on https://gist.github.com/327585 by Anand Kunal
    def __init__(self, stream1, stream2):
        self.stream1 = stream1
        self.stream2 = stream2
        self.__missing_method_name = None  # Hack!

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        self.__missing_method_name = name  # Could also be a property
        return getattr(self, '__methodmissing__')

    def __methodmissing__(self, *args, **kwargs):
        # Emit method call to the log copy
        callable2 = getattr(self.stream2, self.__missing_method_name)
        callable2(*args, **kwargs)

        # Emit method call to stdout (stream 1)
        callable1 = getattr(self.stream1, self.__missing_method_name)
        return callable1(*args, **kwargs)