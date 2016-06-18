# !/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Simulador de Sistema de Memória."""
# Professor: Paulo André (PA)
# Disciplina: CES-25
# Autor: Felipe Tuyama
import threading
import time

exitFlag = 0


class Queue(object):
    u"""Implementação simples de Fila para FIFO."""

    def __init__(self):
        u"""Inicialização da fila."""
        self.dados = []

    def insert(self, elemento):
        u"""Inserção de elemento na fila."""
        self.dados.append(elemento)

    def remove(self):
        u"""Remoção de elemento na fila."""
        return self.dados.pop(0)

    def empty(self):
        u"""Verifica se fila é vazia."""
        return len(self.dados) == 0

    def length(self):
        u"""Retorna comprimento da fila."""
        return len(self.dados)


class Thread (threading.Thread):
    u"""Implementação de Thread para busca em paralelo."""

    def __init__(self, thread_id, name, counter):
        u"""Inicialização de uma nova thread."""
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        u"""Execução da thread."""
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name


def parse_line(line):
    u"""Decompõe linha em endereço e operação."""
    address = line[:line.find(' ')]
    operation = line[line.find(' '):]
    return [address, operation]


def print_time(thread_name, delay, counter):
    u"""Imprime o horário atual."""
    while counter:
        if exitFlag:
            thread_name.exit()
        time.sleep(delay)
        print "%s: %s" % (thread_name, time.ctime(time.time()))
        LRU.insert(thread_name)
        print LRU.dados
        counter -= 1


def main():
    u"""Rotina main do Simulador de Memória."""
    print "*************************************"
    print "*                                   *"
    print "*  Simulador de Sistema de Memória  *"
    print "*                                   *"
    print "*************************************"

    # Opening the input file
    file = open('gcc.txt', 'r')

    # For each line on input file:
    for line in file.readlines():
        # Avoiding empty lines on file
        if not line.strip('\n'):
            continue
        # Parsing read line into Address and Operation
        [address, operation] = parse_line(line)
        print "Address: " + address
        print "Operation: " + operation

    # Closing the input files
    file.close()

    # Create new threads
    thread1 = Thread(1, "Thread-1", 1)
    thread2 = Thread(2, "Thread-2", 2)

    # Start new Threads
    thread1.start()
    thread2.start()

    print "Exiting Main Thread"

u"""Escopo global para chamada da main."""
LRU = Queue()
main()
