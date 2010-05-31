from schedulers import Algorithm 
#from helpers import logger

class FCFS(Algorithm):
    """First Came First Serve is the most simple algorithm"""

    #@logger("FCFS")
    def __init__(self,procesos=None):
        Algorithm.__init__(self,procesos)
        self.short_name = u'FCFS'
        self.long_name = u'First-Come, First-Serve'
        self.preferent = False
        self.description = self.__doc__
            


    def selection_function(self, x, y):
        """Doesn't alter the order of process in the queue"""
        return 0

        #if x.init_time < y.init_time:
            #return -1
        #if x.init_time == y.init_time:
            #return 0
        #if x.init_time > y.init_time:
            #return 1
        
    #@logger("FCFS")
    def recalculate(self):
        Algorithm.recalculate(self)
        #order process by arrive order
     

class SPN(Algorithm):
    """Short process next"""

    def __init__(self, procesos=None):
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

    def __init__(self, procesos=None):
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


class HRRN(Algorithm):
    """Highest Response Rate Next"""

    def __init__(self, procesos=None):
        Algorithm.__init__(self,procesos)
        self.short_name = u'HRRN'
        self.long_name = u'Highest Response Rate Next'
        self.description = self.__doc__
        self.preferent = False # True  # es preferente o no preferente? 
        

    def selection_function(self, x, y):
        """Order by higher response rate"""
        if x.response_rate() > y.response_rate():
            return -1
        if x.response_rate() == y.response_rate():
            return 0
        if x.response_rate() < y.response_rate():
            return 1



   

class RR(Algorithm):
    """Round Robin"""

    def __init__(self, procesos=None, q=1):
        try:
            q = int(q)
        except ValueError:
            return

        Algorithm.__init__(self,procesos)
        self.short_name = u'RR'
        self.q = q

        self.long_name = u'Round Robin (Q=%i)' % self.q
        self.description = self.__doc__
        #self.preferent = True
            

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
            self.cpu.partial_counter = 0       #reset the counter
            self.cpu.set_process(self.process_list.pop(0)) 
        

class FB(Algorithm):
    """FeedBack"""
    def __init__(self, procesos=None, q=1, nq=3, exp=False ):
        """
        q = lenght (in time) of base turn
        nq = number of queues
        exp = if lenght grew up expononetially q=q**i (i==nice)
        """
        try:
            q = int(q)
            nq = int(nq)
            exp = False if not exp or exp=='False' else True
        except ValueError:
            return

        Algorithm.__init__(self,procesos)
        self.short_name = u'FB'
        self.q_base = q
        self.q = 1 if exp else q     #lenght of initial turn
        self.exp = exp
        self.nq = nq #number of queues + 1 
        

        self.long_name = u'Feedback (Q=%i%s)' % (self.q_base, '^i' if exp else '')
        self.description = self.__doc__
        #self.preferent = True

    def set_q(self, p):
        if self.exp:
            self.q = self.q_base**p.nice
        else:
            self.q = self.q_base

    def step(self):
        """rutine executed on every clock signal"""
        self.process_list.extend(self.factory.get_new_process(self.clock.time)) #time to a new processes?
        
        #end turn?
        if self.cpu.partial_counter >= self.q and not self.cpu.is_empty():
            p = self.cpu.get_process()
            stalling_condition = len([pr for pr in self.process_list])>0  #global queue empty?
            if p.nice < self.nq - 1  and stalling_condition :#last queue? 
                p.nice += 1             #inc nice => drecrement priority

            self.process_list.append(p)
        
       
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
        self.process_list.sort(cmp = self.selection_function)
        
        #set first process on CPU
        if self.cpu.is_empty() and len(self.process_list) > 0:
                p = self.process_list.pop(0)
                self.cpu.partial_counter = 0       #reset the counter
                self.set_q(p)
                self.cpu.set_process(p)

    def selection_function(self, x, y):
        """Order by lower nice"""
        if x.nice < y.nice:
            return -1
        if x.nice == y.nice:
            return 0
        if x.nice > y.nice:
            return 1


    

                
    def __repr__(self):
        return Algorithm.__repr__(self) + '\n Q actual=%i' % self.q
        

        
   

