from operator import itemgetter 
import random
from Queue import Queue

class Processor(object):
    """A processor object"""

    def __init__(self, name="", cores=1):
        self.name = name
        self.elapsed_time = 0
        self.cores = cores


    def set_process(self, process):
        self.process = process
        print "process assigned %s" % self.process.name

    def get_process(self):
        ret = self.process 
        self.process = None
        return ret

    def run(self, cycles=1):
        self.elapsed_time += cycles
        if not self.is_empty:
            ret = self.process.run(cycles)
            print ret + " <---"
            return ret

    def is_empty(self):
        if self.process is None:
            return True
        else:
            return False
    
    def __unicode__(self):
        return  "CPU %s running %s... (time elapsed: %i)" % (self.name, self.process, self.elapsed_time)   



class Process(object):
    """Create a process in the system
    
    name is the name of the process, 
    duration is the given estimated processor time. If it's None, the process 
    run until the method finish() is given. 
    
    """ 
    

    INFINITE = 5000
    
    def __init__(self, name="", init_time=0, estimated_duration=INFINITE, status='new', order=None):
        if status not in ('new', 'ready', 'running', 'blocked', 'finished'): 
            print "status not valid. Using 'new' instead"
            status = 'new'

        self.name = name or random.choice(range(1000)) 
        self.init_time = init_time
        self.cpu_time = 0 #no processor time yet
        self.estimated_duration = estimated_duration
        self.waiting_time = 0
        self.life = []
        self.status = status
        self.remaining_time = self.estimated_duration
        
        self.order = order
               
            
    def run(self,cycles=1):
        "Run the process during 'cycles' cpu  and update its values" 
        
        if self.status != 'finished':
            self.status = "running"                    
            if self.remaining_time > cycles:
                self.cpu_time  = self.cpu_time + cycles
                #update life
                self.life = self.life + [1] * cycles
            else:
                self.cpu_time = self.cpu_time + self.remaining_time
                self.life = self.life + [1] * self.remaining_time + [0]*(cycles - self.remaining_time)
                self.finish()
            
            self.remaining_time = self.estimated_duration - self.cpu_time
        return self.status
            

    def wait(self, status="ready", cycles=1):
        "wait in 'status' queue over 'cycles' CPU periods"
        self.status = status
        self.waiting_time = self.waiting_time + cycles
        self.life = self.life + [0]*cycles
        

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "Process %s (%s). CPU = %i | WT = %i | INIT = %i | ET = %i | RT = %i  " % (self.name, 
                self.status, self.cpu_time, self.waiting_time, self.init_time, self.estimated_duration, 
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
        
        self.processor = Processor()

        self.process_list = []
        for p in process_table:
            self.process_list.append(Process(**p))
        
        
        self.total_estimated_duration = 0
        self.total_time_running = 0

        for process in self.process_list:
            self.total_estimated_duration += process.estimated_duration
        
    def __repr__(self):
        sal = "%s (%s) " % (self.long_name, self.short_name)
        sal += "\nTotal " + str(self.total_estimated_duration) + "\n\n"
        for process in self.process_list:
            sal = sal + process.__str__() + "\n"
        return sal





class FCFS(Algorithm):
    """First Came First Serve is a very simple algoritm"""

    def __init__(self,procesos):
        Algorithm.__init__(self,procesos)
        self.short_name = u'FCFS'
        self.long_name = u'First Came-First Serve'
        self.description = self.__doc__
            
        self.calc()


    def cmp_by_init(self, x, y):
        """Auxiliar method to sort by arrive order. Return -1 0 1"""
        if x.init_time < y.init_time:
            return -1
        if x.init_time == y.init_time:
            return 0
        if x.init_time > y.init_time:
            return 1
        

    def calc(self):
        #order process by arrive order
        self.process_list.sort(cmp = self.cmp_by_init)
        


    def run(self):
        for i,p in enumerate(self.process_list):
            self.processor.set_process(p)
            for i in range(10):
                state = self.processor.run()
                print state, self.processor.elapsed_time
                for p2 in self.process_list[i+1:]: p2.wait()
                if state == 'finished': break
                

            
        
        
                
        
         
if __name__=="__main__":
    process = [{'name':"A",'init_time':2, 'estimated_duration':3, 'order':0},
               { 'name':"B",'init_time':0, 'estimated_duration':6, 'order':1},
                { 'name':"C",'init_time':4, 'estimated_duration':4, 'order':2},
                { 'name':"D",'init_time':6, 'estimated_duration':5, 'order':3},
                { 'name':"E",'init_time':8, 'estimated_duration':2, 'order':4}]
                
    prueba = FCFS(process)
    print prueba
    prueba.run()
    print prueba
    for p in prueba.process_list:
        print p.life
    #print prueba.process_list
