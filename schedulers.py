from operator import itemgetter 
import random

class Process():
    """Create a process in the system
    
    name is the name of the process, 
    duration is the given estimated processor time. If it's None, the process 
    run until the method finish() is given. 
    
    status = created || ready || blocked || running || finished
    
    """ 
    
    INFINITE = 5000
    
    def __init__(self, name="", init_time=0, estimated_duration=INFINITE, status="created"):
        self.name = name or random.choice(range(1000)) 
        self.init_time = init_time
        self.cpu_time = 0 #no processor time yet
        self.estimated_duration = estimated_duration
        self.waiting_time = 0
        self.life = []
        self.status = status
        self.remaining_time = self.estimated_duration
        
               
            
    def run(self,cycles=1):
        "Run the process during 'cycles' cpu  and update its values" 
        self.status = "running"
                
        if self.remaining_time > cycles:
            self.cpu_time  = self.cpu_time + cycles
        else:
            self.cpu_time = self.cpu_time + self.remaining_time
            self.finish()
            
        self.remaining_time = self.estimated_duration - self.cpu_time
        
        #update life
        self.life = self.life + [1 for x in range(cycles)]
        return                

    def wait(self, status="ready", cycles=1):
        "wait in 'status' queue over 'cycles' CPU periods"
        self.status = status
        self.waiting_time = self.waiting_time + cycles
        self.life = self.life + [0 for x in range(cycles)]
        
        return                

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "Process %s (%s). CPU = %i | INIT = %i | ET = %i | RT = %i  " % (self.name, 
                self.status, self.cpu_time, self.init_time, self.estimated_duration, 
                self.remaining_time)

    def finish(self):
        "Finish the process and set status"
        self.duration = self.cpu_time
        self.status = "finished"
    
    
    def block(self):
        self.status = "blocked"
    
        


class Algorithm():
    "general class for scheduling algorithm"
    
    def __init__(self, process_table):
        
        self.process_list = []
        for p in process_table:
            new_process = Process(p, process_table[p][0], process_table[p][1])
            self.process_list.append(new_process)
        
        
        self.total_estimated_duration = 0
        for process in self.process_list:
            self.total_estimated_duration = self.total_estimated_duration + process.estimated_duration
        
    def __repr__(self):
        sal = "total " + str(self.total_estimated_duration) + "\n\n"
        for process in self.process_list:
            sal = sal + process.__str__() + "\n"
        return sal

class FCFS(Algorithm):


    def __init__(self,procesos):
        Algorithm.__init__(self,procesos)
    

    def cmp(self, x, y):
        """auxiliar method to sort by arrive order. Return -1 0 1"""
        if x.init_time < y.init_time:
            return -1
        if x.init_time == y.init_time:
            return 0
        if x.init_time > y.init_time:
            return 1
        

    def calc(self):
        #order process by arrive order
        self.process_list.sort(cmp = self.cmp)

        for cycle in range(self.total_estimated_duration):
            
            
            
        
        #each process run until end
        for p in self.process_list:
        
                
        
         
if __name__=="__main__":
    process = {"A":[0,3],"B":[2,6],"C":[4,4],"D":[6,5],"E":[8,2]}
    prueba = FCFS(process)
    print prueba    
