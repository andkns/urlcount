#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'andkns'

import sys
import argparse

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-i', '--input', default='kns.txt')
    parser.add_argument ('-o', '--output', default='out.txt')
    parser.add_argument ('-c', '--check', default='check.txt')
    return parser

def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    outfile = namespace.output
    inputfile = namespace.input
    checkfile = namespace.check

    kns = {}

    f = open(inputfile)
    for line in f:
        # разделяем строки на слова разделенные табуляцией
        words = line.strip().split('\t')
        # приводим все строки в нижний регистр, удаляем https, http, www, разделяем на слова по "/"
        ssylka = words[1].lower().replace('https://','').replace('http://','').replace('www.','').split('/')[0]
        # заполняем словарь  kns[ключ]=значение
        if ssylka not in kns:
            kns[ssylka] = 1
        else:
            kns[ssylka] += 1
    f.close()

    # сортируем словарь по значению, получаем отсортированный кортеж knssorted
    knssorted = sorted(kns.items(), key = lambda x: x[1], reverse=True)

    #for ss in sorted(kns):
    #    g.write(ss + ' ' + str(kns[ss]) + '\n')

    g = open(outfile, 'w')
    for ss in knssorted:
         g.write(ss[0] + ' ' + str(ss[1]) + '\n')
    g.close()

    # читаем файл с с сайтами для подсчета ссылок с них (удаляем www.)
    # и записываем список в chk_words

    c = open(checkfile)
    chk_words = c.read().splitlines()
    chk_words = [sss.replace('www.','')  for sss in chk_words]
    c.close()

    g = open("res.txt", 'w')
    for ss in chk_words:
         if ss in kns:
            g.write(ss + ' --- ' + str(kns[ss]) + '\n')
    g.close()


if __name__ == '__main__':
    main()








