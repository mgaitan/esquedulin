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
        
    
     
#    def step(self):
#        Algorithm.step(self)

        

        
if __name__=="__main__":
    table = [{'name':"A",'init_time':0, 'estimated_duration':3, 'order':0},
               { 'name':"B",'init_time':2, 'estimated_duration':6, 'order':1},
                { 'name':"C",'init_time':4, 'estimated_duration':4, 'order':2},
                { 'name':"D",'init_time':6, 'estimated_duration':5, 'order':3},
                { 'name':"E",'init_time':8, 'estimated_duration':2, 'order':4}]
                
    #prueba = FCFS(table)
    prueba = SPN(table)

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
   
