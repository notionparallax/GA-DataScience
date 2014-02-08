# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 22:43:25 2014

@author: mohammad
"""

from mrjob.job import MRJob


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        yield "chars", len(line)
        yield "words", len(line.split())
        yield "lines", 1
        
        print "chars", len(line)
        print "words", len(line.split())
        print "lines", 1
        print "---------"
        

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRWordFrequencyCount.run()