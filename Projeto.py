# !/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Simulador de Sistema de Memória."""
# Professor: Paulo André (PA)
# Disciplina: CES-25
# Autor: Felipe Tuyama
import threading
import time

exitFlag = 0


class Queue (object):
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


class L1cache (object):
    u"""Cache L1."""

    cache = []
    LRU = Queue()

    def __init__(self):
        u"""Inicialização da Cache L1."""
        for i in range(10):
            self.cache.append(0)
            self.LRU.insert(i)

    def search(self, address):
        u"""Procura endereço na cache L1."""
        stats.stats['memtime'] += 1
        if address in self.cache:
            stats.stats['l1hits'] += 1
            stats.stats['memtime'] += 2
        else:
            slot = self.LRU.remove()
            self.cache[slot] = address
            self.LRU.insert(slot)
            l2.search(address)


class L2cache (object):
    u"""Cache L1."""

    cache = []
    LRU = Queue()

    def __init__(self):
        u"""Inicialização da Cache L1."""
        for i in range(64):
            self.cache.append(0)
            self.LRU.insert(i)

    def search(self, address):
        u"""Procura endereço na cache L2."""
        stats.stats['memtime'] += 2
        if address in self.cache:
            stats.stats['l2hits'] += 1
            stats.stats['memtime'] += 4
        else:
            slot = self.LRU.remove()
            self.cache[slot] = address
            self.LRU.insert(slot)
            mem.search(address)


class Memory (object):
    u"""Memória RAM principal."""

    def __init__(self):
        u"""Inicialização da memória."""
        self.memory = []

    def search(self, address):
        u"""Procura endereço na memória."""
        stats.stats['memhits'] += 1
        stats.stats['memtime'] += 60
        if address in self.memory:
            return
        else:
            self.memory.append(address)


class Statistics (object):
    u"""Estatísticas do programa para a sua execução."""

    stats = {
        'l1hits': 0,
        'l2hits': 0,
        'memhits': 0,
        'memtime': 0,
        'total': 0
    }

    def print_stats(self):
        u"""Exibe as estatísticas da execução do benchmark."""
        self.stats['memhits'] -= 1
        l1_hit_rate = (100.0 * self.stats['l1hits'] / self.stats['total'])
        l2_hit_rate = (100.0 * self.stats['l2hits'] / self.stats['total'])
        mem_hit_rate = (100.0 * self.stats['memhits'] / self.stats['total'])
        print stats.stats
        print "L1  hit rate: " + str(l1_hit_rate)
        print "L2  hit rate: " + str(l2_hit_rate)
        print "Mem hit rate: " + str(mem_hit_rate)


def parse_line(line):
    u"""Decompõe linha em endereço e operação."""
    address = line[:line.find(' ')]
    operation = line[line.find(' '):]
    stats.stats['total'] += 1
    return [address, operation]


def search_address(address, operation):
    u"""Busca o endereço na memória."""
    l1.search(address)


def print_time(thread_name, delay, counter):
    u"""Imprime o horário atual."""
    while counter:
        if exitFlag:
            thread_name.exit()
        time.sleep(delay)
        print "%s: %s" % (thread_name, time.ctime(time.time()))
        fila.insert(thread_name)
        print fila.dados
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
        print "Address: " + address + " " + "Operation: " + operation

        # Searching address on memory
        search_address(address, operation)

        # Performing selected operation

    # Closing the input files
    file.close()

    # Create new threads
    # thread1 = Thread(1, "Thread-1", 1)
    # thread2 = Thread(2, "Thread-2", 2)

    # Start new Threads
    # thread1.start()
    # thread2.start()

    print "Exiting Main Thread"
    stats.print_stats()

u"""Escopo global para chamada da main."""
fila = Queue()
stats = Statistics()
l1 = L1cache()
l2 = L2cache()
mem = Memory()
main()
