# !/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Simulador de Sistema de Memória."""
# Professor: Paulo André (PA)
# Disciplina: CES-25
# Autor: Felipe Tuyama


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


class L1cache (object):
    u"""Cache L1."""

    cache = []
    cacheM = []
    LRU = Queue()
    write_policy = 'WT'
    subst_policy = 'FIFO'
    write_fail_policy = 'WA'

    def __init__(self):
        u"""Inicialização da Cache L1."""
        for i in range(10):
            self.cache.append(-1)
            self.cacheM.append(0)
            self.LRU.insert(i)

    def search(self, address):
        u"""Procura endereço na cache L1."""
        stats.stats['memtime'] += 1
        if address in self.cache:
            stats.stats['l1hits'] += 1
            return self.cache.index(address)
        else:
            return -1

    def substitute(self, address):
        u"""Substituição de bloco na Cache L1."""
        if self.subst_policy == 'FIFO':
            slot = self.LRU.remove()
            self.cache[slot] = address
            self.cacheM[slot] = 0
            self.LRU.insert(slot)

    def available(self):
        u"""Procura slot disponível na Cache L1."""
        if -1 in self.cache:
            slot = self.cache.index(-1)
            self.cache[slot] = 0
            return slot
        else:
            return -1

    def read(self, address):
        u"""Operação de leitura na Cache L1."""
        # Busca endereço na Cache L1
        index = self.search(address)
        if index != -1:
            # Realização da leitura na Cache L1
            stats.stats['memtime'] += 2
        else:
            # Continua a busca no nível inferior
            l2.read(address)
            # Traz o bloco para a Cache L1
            self.substitute(address)

    def write(self, address):
        u"""Operação de escrita na Cache L1."""
        # Busca endereço na Cache L1
        index = self.search(address)
        if index != -1:
            # Política de Gravação Write Through
            if self.write_policy == 'WT':
                # Realização da escrita na Cache L1
                stats.stats['memtime'] += 2
                self.cacheM[index] = 1
                # Realiza escrita no nível inferior também
                l2.write(address)
            # Política de Gravação Write Back
            elif self.write_policy == 'WB':
                # Realização da escrita na Cache L1
                stats.stats['memtime'] += 2
                self.cacheM[index] = 1
        else:
            # Política de Gravação Write Through
            if self.write_policy == 'WT':
                # Faz a gravação no nível inferior
                l2.write(address)
                # Traz o bloco para a Cache L1
                self.substitute(address)
                # Realização da escrita na Cache L1
                stats.stats['memtime'] += 2
                self.cacheM[index] = 1
            # Política de Gravação Write Back
            elif self.write_policy == 'WB':
                # Traz o bloco do nível inferior
                l2.read(address)
                # Traz o bloco para a Cache L1
                self.substitute(address)
                # Realização da escrita na Cache L1
                stats.stats['memtime'] += 2
                self.cacheM[index] = 1


class L2cache (object):
    u"""Cache L1."""

    cache = []
    cacheM = []
    LRU = Queue()
    write_policy = 'WB'
    subst_policy = 'FIFO'
    write_fail_policy = 'WNA'

    def __init__(self):
        u"""Inicialização da Cache L1."""
        for i in range(64):
            self.cache.append(-1)
            self.cacheM.append(0)
            self.LRU.insert(i)

    def search(self, address):
        u"""Procura endereço na cache L2."""
        stats.stats['memtime'] += 2
        if address in self.cache:
            stats.stats['l2hits'] += 1
            return self.cache.index(address)
        else:
            return -1

    def substitute(self, address):
        u"""Substituição de bloco na Cache L2."""
        if self.subst_policy == 'FIFO':
            slot = self.LRU.remove()
            self.cache[slot] = address
            self.cacheM[slot] = 0
            self.LRU.insert(slot)

    def available(self):
        u"""Procura slot disponível na Cache L1."""
        if -1 in self.cache:
            slot = self.cache.index(-1)
            self.cache[slot] = 0
            return slot
        else:
            return -1

    def read(self, address):
        u"""Operação de leitura na Cache L2."""
        # Busca endereço na Cache L2
        index = self.search(address)
        if index != -1:
            # Realização da leitura na Cache L2
            stats.stats['memtime'] += 4
        else:
            # Continua a busca no nível inferior
            mem.read(address)
            # Traz o bloco para a Cache L2
            self.substitute(address)

    def write(self, address):
        u"""Operação de escrita na Cache L2."""
        # Busca endereço na Cache L2
        index = self.search(address)
        if index != -1:
            # Política de Gravação Write Through
            if self.write_policy == 'WT':
                # Realização da escrita na Cache L2
                stats.stats['memtime'] += 4
                self.cacheM[index] = 1
                # Realiza escrita no nível inferior também
                mem.write(address)
            # Política de Gravação Write Back
            elif self.write_policy == 'WB':
                # Realização da escrita na Cache L2
                stats.stats['memtime'] += 4
                self.cacheM[index] = 1
        else:
            # Política de Gravação Write Through
            if self.write_policy == 'WT':
                # Faz a gravação no nível inferior
                mem.write(address)
                # Traz o bloco para a Cache L2
                self.substitute(address)
                # Realização da escrita na Cache L2
                stats.stats['memtime'] += 4
                self.cacheM[index] = 1
            # Política de Gravação Write Back
            elif self.write_policy == 'WB':
                # Traz o bloco do nível inferior
                mem.read(address)
                # Traz o bloco para a Cache L2
                self.substitute(address)
                # Realização da escrita na Cache L2
                stats.stats['memtime'] += 4
                self.cacheM[index] = 1


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

    def read(self, address):
        u"""Operação de leitura na memória."""
        # Busca endereço na memória
        self.search(address)

    def write(self, address):
        u"""Operação de escrita na memória."""
        return


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
    operation = line[(line.find(' ') + 1):]
    stats.stats['total'] += 1
    return [address, operation]


def perform_operation(address, operation):
    u"""Executa a tarefa solicitada."""
    if operation == 'R':
        l1.read(address)
    elif operation == 'W':
        l1.write(address)


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
        line = line.strip('\n')
        if not line:
            continue

        # Parsing read line into Address and Operation
        [address, operation] = parse_line(line)

        # Performing selected operation
        perform_operation(address, operation)

    # Closing the input files
    file.close()

    # Printing Statistics
    stats.print_stats()

u"""Escopo global para chamada da main."""
fila = Queue()
stats = Statistics()
l1 = L1cache()
l2 = L2cache()
mem = Memory()

main()
