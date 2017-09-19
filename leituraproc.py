# -*- coding: utf-8 -*-
import os
from time import strftime
import base64
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
        self.resultado = None
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
                    elif valor == 'query':
                        self.query = self.cred[nivel][valor]
                        print(self.query)
        else:
            print('não achei')

    def campos(self):
        '''
            Lista todos os attrs possíveis, com a finalidade
            de facilitar o arranjo de query.
        '''
        for campo in self.conexao.fields('CHG:Change'):
            print(campo)

    def _schema(self):
        ''' Lista os schemas '''
        for schema in self.conexao.schemas():
            print(schema)

    def filtros(self):
        query = """ 'Status*' == "Resolved" AND 'Region' = "Santander Brasil" """
        lista = ['Change ID+', 'Summary', 'Status', 'Department', 'Region', \
        'Description', 'Requester Login Name+', 'Requester ID+', 'Requester Name+']
        inicio = strftime("%a, %d %b %Y %H:%M:%S +0000")
        self.resultado = self.conexao.query(
            schema='CHG:Change',
            qualifier=self.query,
            fields=lista,
            offset=0,
            limit=10
        )
        for base_chave, base_valor in self.resultado:
            for chave, valor in base_valor.items():
                print('{}:{}'.format(chave, valor))
            print(' ###############################\n ')
        print(inicio+' - '+strftime("%a, %d %b %Y %H:%M:%S +0000"))

    def chamador(self):
        try:
            self._conf()
            self.conexao = ARS(server=base64.b64decode(self.rede), port=self.porta, \
             user=base64.b64decode(self.login), password=base64.b64decode(self.senha))
            self.filtros()
        except ARSError:
            for message_number, message_text, appended_text in self.conexao.errors:
                if appended_text:
                    print(
                        '\nMessage {}: {} ({})'.format(message_number, message_text, appended_text)
                        +'\nVerique conexao ou query'
                    )
                else:
                    print(
                        'Message {}: {}'.format(message_number, message_text)
                        +'\nVerique configuracao de conexao'
                    )
        finally:
            if self.conexao is not None:
                self.conexao.terminate()
            print("\nExecução finalizada\n")
