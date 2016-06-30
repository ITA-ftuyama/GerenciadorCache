# !/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Simulador de Sistema de Memória."""
# Professor: Paulo André (PA)
# Disciplina: CES-25
# Autor: Felipe Tuyama


class Cache (object):
    u"""Classe Cache."""

    def __init__(self, size, associativity):
        u"""Inicialização da Cache."""
        self.size = size
        self.associativity = associativity
        self.groups = size / associativity
        self.cache = [-1] * self.size
        self.cacheM = [0] * self.size
        self.FIFO = [0] * self.groups
        self.LRU = [0] * self.size

    def hash(self, address):
        u"""Cálculo do hash do conjunto do bloco de Cache."""
        hash = i = 1
        while address > 10:
            hash = hash + (address % 10) * i
            address = address / 10
            i = i + 1
        return hash % self.groups

    def search(self, address):
        u"""Procura endereço na cache."""
        stats.stats[self.stattries] += 1

        # Setting the searching range
        group = self.hash(address)
        start = group * self.associativity
        stop = (group + 1) * self.associativity

        for i in range(start, stop):
            if address == self.cache[i]:
                return i
        return -1

    def substitute(self, address):
        u"""Substituição de conjunto de blocos na Cache."""
        group = self.hash(address)
        if self.substitution == 'FIFO':
            slot = group * self.associativity + self.FIFO[group]
            self.FIFO[group] = (self.FIFO[group] + 1) % self.associativity
        elif self.substitution == 'LRU':
            start = group * self.associativity
            stop = (group + 1) * self.associativity
            slot = start
            for i in range(start, stop):
                if self.LRU[slot] < self.LRU[i]:
                    slot = i
                self.LRU[i] = self.LRU[i] + 1
            self.LRU[slot] = 0

        # Verfica se o bloco está sujo
        if self.cacheM[slot] == 1 and self.write_policy == 'WB':
            # Penalidade: Tempo extra para gravação
            stats.stats['memtime'] += max(times)
            del times[:]
            # O Bloco deve ser gravado no nível inferior
            self.lower_level.write(address)

        # Substituição do bloco sem traumas
        self.cache[slot] = address
        self.cacheM[slot] = 0

    def read(self, address):
        u"""Operação de leitura na Cache."""
        # Busca endereço na Cache
        index = self.search(address)
        if index != -1:
            # Realização da leitura na Cache
            stats.stats[self.stathits] += 1
            times.append(self.tag_time + self.access_time)
        else:
            # Continua a busca no nível inferior
            times.append(self.tag_time)
            self.lower_level.read(address)
            # Traz o bloco para a Cache
            self.substitute(address)

    def write(self, address):
        u"""Operação de escrita na Cache."""
        # Busca endereço na Cache
        index = self.search(address)
        if index != -1:
            stats.stats[self.stathits] += 1
            # Política de Gravação Write Through
            if self.write_policy == 'WT':
                # Realização da escrita na Cache
                times.append(self.tag_time + self.access_time)
                self.cacheM[index] = 1
                # Realiza escrita no nível inferior também
                self.lower_level.write(address)
            # Política de Gravação Write Back
            elif self.write_policy == 'WB':
                # Realização da escrita na Cache
                times.append(self.tag_time + self.access_time)
                self.cacheM[index] = 1
        else:
            # Política de Gravação Write Allocate
            if self.write_fail_policy == 'WA':
                # Traz o bloco do nível inferior
                times.append(self.tag_time + self.access_time)
                self.lower_level.read(address)
                # Traz o bloco para a Cache
                self.substitute(address)
                # Realização da escrita na Cache
                self.write(address)
            # Política de Gravação Write Not Allocate
            elif self.write_fail_policy == 'WNA':
                # Não traz o bloco do nível inferior
                times.append(self.tag_time)
                self.lower_level.write(address)


class Memory (object):
    u"""Memória RAM principal."""

    def __init__(self):
        u"""Inicialização da memória."""
        self.memory = []

    def search(self, address):
        u"""Procura endereço na memória."""
        times.append(self.access_time)
        stats.stats['memhits'] += 1

    def read(self, address):
        u"""Operação de leitura na memória."""
        # Busca endereço na memória
        self.search(address)

    def write(self, address):
        u"""Operação de escrita na memória."""
        # Busca endereço na memória
        self.search(address)


class Statistics (object):
    u"""Estatísticas do programa para a sua execução."""

    stats = {
        'l1hits': 0,
        'l2hits': 0,
        'l1tries': 0,
        'l2tries': 0,
        'memhits': 0,
        'memtime': 0,
        'total': 0
    }

    def print_stats(self):
        u"""Exibe as estatísticas da execução do benchmark."""
        print ""
        print "Estatísticas: " + str(stats.stats)

        l1_hit_rate = 1.0 * self.stats['l1hits'] / self.stats['total']
        l2_hit_rate = 1.0 * self.stats['l2hits'] / self.stats['total']
        mem_hit_rate = 1.0 * self.stats['memhits'] / self.stats['total']
        print "L1  hit rate: " + str(l1_hit_rate)
        print "L2  hit rate: " + str(l2_hit_rate)
        print "Mem hit rate: " + str(mem_hit_rate)

        l1_success_rate = 1.0 * self.stats['l1hits'] / self.stats['l1tries']
        l2_success_rate = 1.0 * self.stats['l2hits'] / self.stats['l2tries']
        mem_success_rate = 1.0
        print "L1  success rate: " + str(l1_success_rate)
        print "L2  success rate: " + str(l2_success_rate)
        print "Mem success rate: " + str(mem_success_rate)

        l1time = (l1.tag_time + l1.access_time)
        l2time = (l2.tag_time + l2.access_time)
        effective_time = (
            l1_success_rate * l1time + (1.0 - l1_success_rate) * (
                l2_success_rate * l2time + (1.0 - l2_success_rate) * (
                    mem.access_time
                )))
        print "Effective Time: " + str(effective_time)
        print "Mem Total Time: " + str(self.stats['memtime'] / 1000.0)


def main():
    u"""Rotina main do Simulador de Memória."""
    print "*************************************"
    print "*                                   *"
    print "*  Simulador de Sistema de Memória  *"
    print "*                                   *"
    print "*************************************"

    total = 0
    # Para cada linha do arquivo de entrada:
    with open('../gcc.trace') as infile:
        for line in infile:
            # Barra de progresso
            if total % 50000 == 0:
                print "#",

            total += 1
            # Interpreta endereço e operação
            address = int(line[:8], 16)
            operation = line[9]

            # Realiza operação selecionada
            del times[:]
            if operation == 'R':
                l1.read(address)
            elif operation == 'W':
                l1.write(address)

            # Operações realizads em paralelo
            stats.stats['memtime'] += max(times)

    # Imprime estatísticas
    stats.stats['total'] = total
    stats.print_stats()

u"""Escopo global para chamada da main."""

# Auxiliar times vector
times = []

# Creating Statistics
stats = Statistics()

# Creating Memory
mem = Memory()
mem.access_time = 60

# Creating Cache L2
l2 = Cache(65536, 16)
l2.write_policy = 'WB'
l2.write_fail_policy = 'WNA'
l2.substitution = 'FIFO'
l2.stathits = 'l2hits'
l2.stattries = 'l2tries'
l2.access_time = 4
l2.tag_time = 2
l2.lower_level = mem

# Creating Cache L1
l1 = Cache(1024, 8)
l1.write_policy = 'WT'
l1.write_fail_policy = 'WA'
l1.substitution = 'LRU'
l1.stathits = 'l1hits'
l1.stattries = 'l1tries'
l1.access_time = 2
l1.tag_time = 1
l1.lower_level = l2

main()
