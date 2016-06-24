# !/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Simulador de Sistema de Memória."""
# Professor: Paulo André (PA)
# Disciplina: CES-25
# Autor: Felipe Tuyama


class Cache (object):
    u"""Classe Cache."""

    def __init__(self, size):
        u"""Inicialização da Cache."""
        self.cache = [-1] * size
        self.cacheM = [0] * size
        self.size = size
        self.LRU = 0

    def search(self, address):
        u"""Procura endereço na cache."""
        if address in self.cache:
            return self.cache.index(address)
        else:
            return -1

    def substitute(self, address):
        u"""Substituição de bloco na Cache."""
        slot = self.LRU
        # Verfica se o bloco está sujo
        if self.cacheM[slot] == 1 and self.write_policy == 'WB':
            # O Bloco deve ser gravado no nível inferior
            # (O tempo será dado pelo nível inferior)
            self.lower_level.write(address)

        # Substituição sem traumas
        self.cache[slot] = address
        self.cacheM[slot] = 0
        self.LRU = (self.LRU + 1) % self.size

    def read(self, address):
        u"""Operação de leitura na Cache."""
        # Busca endereço na Cache
        index = self.search(address)
        if index != -1:
            # Realização da leitura na Cache
            stats.stats[self.stathits] += 1
            stats.stats['memtime'] += self.tag_time + self.access_time
        else:
            # Continua a busca no nível inferior
            # (O tempo será dado pelo nível inferior)
            self.lower_level.read(address)
            # Traz o bloco para a Cache
            self.substitute(address)

    def write(self, address):
        u"""Operação de escrita na Cache."""
        # Busca endereço na Cache
        index = self.search(address)
        if index != -1:
            # Política de Gravação Write Through
            if self.write_policy == 'WT':
                # Realização da escrita na Cache
                # (O tempo será dado pelo nível inferior)
                self.cacheM[index] = 1
                # Realiza escrita no nível inferior também
                self.lower_level.write(address)
            # Política de Gravação Write Back
            elif self.write_policy == 'WB':
                # Realização da escrita na Cache
                stats.stats['memtime'] += self.access_time
                self.cacheM[index] = 1
        else:
            # Política de Gravação Write Through
            if self.write_policy == 'WT':
                # Faz a gravação no nível inferior
                # (O tempo será dado pelo nível inferior)
                self.lower_level.write(address)
                # Traz o bloco para a Cache
                self.substitute(address)
                # Realização da escrita na Cache
                self.cacheM[index] = 1
            # Política de Gravação Write Back
            elif self.write_policy == 'WB':
                # Traz o bloco do nível inferior
                # (O tempo será dado pelo nível inferior)
                self.lower_level.read(address)
                # Traz o bloco para a Cache
                self.substitute(address)
                # Realização da escrita na Cache
                self.cacheM[index] = 1


class Memory (object):
    u"""Memória RAM principal."""

    def __init__(self):
        u"""Inicialização da memória."""
        self.memory = []

    def search(self, address):
        u"""Procura endereço na memória."""
        stats.stats['memtime'] += 60

    def read(self, address):
        u"""Operação de leitura na memória."""
        # Busca endereço na memória
        self.search(address)
        stats.stats['memhits'] += 1

    def write(self, address):
        u"""Operação de escrita na memória."""
        # Busca endereço na memória
        self.search(address)


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
        print "Mem Total Time: " + str(self.stats['memtime'])


def main():
    u"""Rotina main do Simulador de Memória."""
    print "*************************************"
    print "*                                   *"
    print "*  Simulador de Sistema de Memória  *"
    print "*                                   *"
    print "*************************************"

    total = 0
    # For each line on input file:
    with open('gcc.trace') as infile:
        for line in infile:
            if total % 50000 == 0:
                print "#",
            total += 1
            # Parsing read line into Address and Operation
            index = line.find(' ')
            address = line[:index]
            operation = line[index + 1]

            # Performing selected operation
            if operation == 'R':
                l1.read(address)
            elif operation == 'W':
                l1.write(address)

    # Printing Statistics
    stats.stats['total'] = total
    stats.print_stats()

u"""Escopo global para chamada da main."""

# Creating Statistics
stats = Statistics()

# Creating Memory
mem = Memory()

# Creating Cache L2
l2 = Cache(64)
l2.write_policy = 'WB'
l2.write_fail_policy = 'WNA'
l2.stathits = 'l2hits'
l2.access_time = 4
l2.tag_time = 2
l2.lower_level = mem

# Creating Cache L1
l1 = Cache(10)
l1.write_policy = 'WT'
l1.write_fail_policy = 'WA'
l1.stathits = 'l1hits'
l1.access_time = 2
l1.tag_time = 1
l1.lower_level = l2

main()
