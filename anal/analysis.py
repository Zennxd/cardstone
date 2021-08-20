import sys
from time import time
from os import mkdir
from sys import stdout

from minion import Lineup

class Analysis:
    std_out = sys.stdout

    def __enter__(self):
        self.start_time = time()
        self.name = str(int(self.start_time * 1000))

        mkdir(f"./anal/{self.name}")
        self.outcomes = open(f"./anal/{self.name}/outcomes.csv", "w")
        self.outcomes.write("iteration, outcomes\n")

        self.lineups = open(f"./anal/{self.name}/linesups.txt", "w")
        self.log = open(f"./anal/{self.name}/log.txt", "w")

        sys.stdout = self.log

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.outcomes.close()
        self.lineups.close()
        self.log.close()

        sys.stdout = Analysis.std_out
