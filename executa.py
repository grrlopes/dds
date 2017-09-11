#!/usr/bin/env python3
from leituraproc import Leituraproc

class Executa(Leituraproc):
    def __init__(self):
        Leituraproc.__init__(self)
        self.chamador()

class Principal:
    if __name__ == "__main__":
        Executa()
