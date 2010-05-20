#!/usr/bin/env python
# -*- coding: utf-8 -*-

from algorithms import FCFS, SPN, SRT, HRRN, RR, FB
import matplotlib.pyplot as plt


def main():

    table = [{'name':"A",'init_time':0, 'estimated_duration':3, 'order':0},
               { 'name':"B",'init_time':2, 'estimated_duration':6, 'order':1},
                { 'name':"C",'init_time':4, 'estimated_duration':4, 'order':2},
                { 'name':"D",'init_time':6, 'estimated_duration':5, 'order':3},
                { 'name':"E",'init_time':8, 'estimated_duration':2, 'order':4}]
                
    #prueba = FCFS(table)
    #prueba = SPN(table)
    #prueba = SRT(table)
    #prueba = HRRN(table)

    
        
        #self.set_ax(fig, '212')


    all = [FCFS(table), SPN(table), SRT(table), HRRN(table), RR(table, q=1), 
            RR(table, q=4), FB(table, q=1), FB(table, q=2, exp=True)]



    fig = plt.figure()

    for num, alg in enumerate(all):
        time = alg.total_estimated_duration  #10
        for i in range(time):
            alg.step()
        alg.set_ax(fig, '%i1%i' % (len(all), num+1))
        
    plt.show()


if __name__ == '__main__':
    main()
