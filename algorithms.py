from schedulers import Algorithm, logger

#TODO chequear si el generador de procesos FCFS puede crear los procesos en el tiempo que corresponde



class FCFS(Algorithm):
    """First Came First Serve is a very simple algoritm"""

    #@logger("FCFS")
    def __init__(self,procesos):
        Algorithm.__init__(self,procesos)
        self.short_name = u'FCFS'
        self.long_name = u'First-Come, First-Serve'
        self.preferent = False
        self.description = self.__doc__
            


    def cmp_by_init(self, x, y):
        """Auxiliar method to sort by arrive order. Return -1 0 1"""
        if x.init_time < y.init_time:
            return -1
        if x.init_time == y.init_time:
            return 0
        if x.init_time > y.init_time:
            return 1
        
    #@logger("FCFS")
    def recalculate(self):
        Algorithm.recalculate(self)
        #order process by arrive order
        self.process_list.sort(cmp = self.cmp_by_init)
        
        if self.cpu.is_empty() and len(self.process_list) > 0:
            self.cpu.set_process(self.process_list.pop(0)) #set first of queue
    
    #@logger("FCFS")
    def step(self):
        Algorithm.step(self)

        p = self.cpu.step() #if finish return the process
        if p:
            p.end_time = self.clock.time
            self.finished.append(p)

        for p2 in self.process_list:
            if p2.status in ('new','blocked', 'ready'): p2.wait() 



class SPN(Algorithm):
    """Short process next"""

    def __init__(self, procesos):
        Algorithm.__init__(self,procesos)
        self.short_name = u'SPN'
        self.long_name = u'Short process next'
        self.description = self.__doc__
            
        self.calc()

    def cmp_by_shortness(self, x, y):
        """Auxiliar method to sort by arrive order. Return -1 0 1"""
        if x.estimated_duration < y.estimated_duration:
            return -1
        if x.estimated_duration == y.estimated_duration:
            return 0
        if x.estimated_duration > y.estimated_duration:
            return 1
        
    def calc(self):
        #order process by arrive order
        self.process_list.sort(cmp = self.cmp_by_shortness)
     
    def run(self, cycles=1):
        for p in self.process_list:
            while p.status != 'finished':
                #running the first one
                p.run(cycles)
                #wait the rest
                for p2 in self.process_list:
                    if p2.status in ('new','blocked', 'ready'): p2.wait(cycles=cycles) 


        
if __name__=="__main__":
    table = [{'name':"A",'init_time':0, 'estimated_duration':3, 'order':0},
               { 'name':"B",'init_time':2, 'estimated_duration':6, 'order':1},
                { 'name':"C",'init_time':4, 'estimated_duration':4, 'order':2},
                { 'name':"D",'init_time':6, 'estimated_duration':5, 'order':3},
                { 'name':"E",'init_time':8, 'estimated_duration':2, 'order':4}]
                
    prueba = FCFS(table)
    for i in range(prueba.total_estimated_duration):
        prueba.step()
    for p in prueba.finished:
        print p.name, p.init_time, p.end_time, p.life
    
    prueba.plot()
   
