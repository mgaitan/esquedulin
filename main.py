#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithms import FCFS, SPN, SRT, HRRN, RR, FB
import matplotlib.pyplot as plt


def main():
    from settings import TABLE_PROC

    all = [FCFS(TABLE_PROC),]# SPN(TABLE_PROC), SRT(TABLE_PROC), HRRN(TABLE_PROC), RR(TABLE_PROC, q=1), 
            #RR(TABLE_PROC, q=4), FB(TABLE_PROC, q=1), FB(TABLE_PROC, q=2, exp=True)]



    fig = plt.figure()

    for num, alg in enumerate(all):
        time = alg.total_estimated_duration #10
        for i in range(time) :
            alg.step()
    

        alg.set_ax(fig, '%i1%i' % (len(all), num+1))
    
    plt.show()


if __name__ == '__main__':
    main()
