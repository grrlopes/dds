# -*- coding: utf-8 -*-
import os
import yaml
from credencial import Credencial
from pyremedy import ARS, ARSError
__author__ = 'Equipe Automação'

class Leituraproc(Credencial):
    def __init__(self):
        Credencial.__init__(self)
        self.rede = None
        self.porta = None
        self.login = None
        self.senha = None
        self.cred = None
        self.conexao = None
        self.query = None

    def _conf(self):
        if os.path.isfile('config.yaml'):
            self.cred = yaml.load(open('config.yaml', 'r'))
            for nivel in self.cred:
                for valor in self.cred[nivel]:
                    if valor == 'login':
                        self.login = self.cred[nivel][valor]
                    elif valor == 'senha':
                        self.senha = self.cred[nivel][valor]
                    elif valor == 'rede':
                        self.rede = self.cred[nivel][valor]
                    elif valor == 'porta':
                        self.porta = self.cred[nivel][valor]
        else:
            print('não achei')

    def campos(self):
        for campo in self.conexao.fields('CHG:Change'):
            print(campo)

    def _schema(self):
        for schema in self.conexao.schemas():
            print(schema)

    #query(schema, qualifier, fields, offset=0, limit=0)
    def filtros(self):
        self.conexao.query(
            schema='CHG:Change',
            qualifier=qual,
            fields=(campos)
        )

    def chamador(self):
        try:
            self._conf()
            self.conexao = ARS(server=self.rede, port=self.porta, \
             user=self.login, password=self.senha)
        except ARSError:
            for message_number, message_text, appended_text in self.conexao.errors:
                if appended_text:
                    print(
                        'Message {}: {} ({})'.format(message_number, message_text, appended_text)
                    )
                else:
                    print('Message {}: {}'.format(message_number, message_text))
        finally:
            self.conexao.terminate()
            print("Terminado")
