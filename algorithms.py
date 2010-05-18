from schedulers import Algorithm, logger

class FCFS(Algorithm):
    """First Came First Serve is a very simple algoritm"""

    #@logger("FCFS")
    def __init__(self,procesos):
        Algorithm.__init__(self,procesos)
        self.short_name = u'FCFS'
        self.long_name = u'First-Come, First-Serve'
        self.preferent = False
        self.description = self.__doc__
            


    def selection_function(self, x, y):
        """Order by init_time"""
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
     

class SPN(Algorithm):
    """Short process next"""

    def __init__(self, procesos):
        Algorithm.__init__(self,procesos)
        self.short_name = u'SPN'
        self.long_name = u'Short process next'
        self.description = self.__doc__
        self.preferent = False #True
        

    def selection_function(self, x, y):
        """Order by shortness"""
        if x.estimated_duration < y.estimated_duration:
            return -1
        if x.estimated_duration == y.estimated_duration:
            return 0
        if x.estimated_duration > y.estimated_duration:
            return 1
        

class SRT(Algorithm):
    """Shortest remaining time"""

    def __init__(self, procesos):
        Algorithm.__init__(self,procesos)
        self.short_name = u'SRT'
        self.long_name = u'Shortest remaining time'
        self.description = self.__doc__
        self.preferent = True
        

    def selection_function(self, x, y):
        """Order by remaining time"""
        if x.remaining_time < y.remaining_time:
            return -1
        if x.remaining_time == y.remaining_time:
            return 0
        if x.remaining_time > y.remaining_time:
            return 1



   

class RR(Algorithm):
    """Round Robin"""

    def __init__(self, procesos, q=1):
        Algorithm.__init__(self,procesos)
        self.short_name = u'RR'
        self.q = q

        self.long_name = u'Round Robin (Q=%i)' % self.q
        self.description = self.__doc__
        self.preferent = True
            

    def step(self):
        """rutine executed on every clock signal"""
        self.process_list.extend(self.factory.get_new_process(self.clock.time)) #time to a new processes?
        if self.cpu.partial_counter >= self.q and not self.cpu.is_empty():
            self.process_list.append(self.cpu.get_process())
 
        self.recalculate() #reorder list applying selection function
        self.clock.inc() #increment global clock

        p = self.cpu.step() #if finish return the process
        if p:
            p.end_time = self.clock.time
            self.finished.append(p)
        
        #all other process on ready
        for p2 in self.process_list:
            p2.wait()

                




    def recalculate(self):
        """reorder the queue and set new process on CPU"""
        
        #set first on CPU
        if self.cpu.is_empty() and len(self.process_list) > 0:
            self.cpu.partial_counter = 0                #reset the counter
            self.cpu.set_process(self.process_list.pop(0)) 
        

        
if __name__=="__main__":
    table = [{'name':"A",'init_time':0, 'estimated_duration':3, 'order':0},
               { 'name':"B",'init_time':2, 'estimated_duration':6, 'order':1},
                { 'name':"C",'init_time':4, 'estimated_duration':4, 'order':2},
                { 'name':"D",'init_time':6, 'estimated_duration':5, 'order':3},
                { 'name':"E",'init_time':8, 'estimated_duration':2, 'order':4}]
                
    #prueba = FCFS(table)
    #prueba = SPN(table)
    #prueba = SRT(table)
    prueba = RR(table, q=1)

    def cmp_by_order(x, y):
            if x.order < y.order:
                return -1
            if x.order == y.order:
                return 0
            if x.order > y.order:
                return 1
    
    
    
    for i in range(prueba.total_estimated_duration):
        prueba.step()

    prueba.finished.sort(cmp=cmp_by_order)

    for p in prueba.finished:
        print p.name, p.init_time, p.end_time, p.life
    
    prueba.plot()
   

