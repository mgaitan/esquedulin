import matplotlib.pyplot as plt
import numpy as np
import sys
#from helpers import Singleton, logger

class Clock():
    # __metaclass__ = Singleton
    def __init__(self):
        self.time = 0 #initial time
    def inc(self):
        self.time += 1

    def reset(self):
        self.time = 0

    def __repr__(self):
        return "Time: %i" % self.time

class Cpu(object):
    """A processor unit object"""

    def __init__(self, name="", cores=1):
        self.name = name
        self.cores = cores

        self.reset()
        

    def set_process(self, process):
        self.process.append(process)

    def get_process(self):
        return self.process.pop()

    #@logger("Processor")
    def step(self, cycles=1):
        if not self.is_empty():
            self.life.append(self.process[0].name)
            self.process[0].run(cycles)
            self.elapsed_time += cycles
            self.partial_counter += cycles
            #process end?
            if self.process[0].status == 'finished':
                return self.get_process()
        else:
            self.life.append('idle')

    def count_idle_time(self):
        return self.life.count('idle')

    def reset(self):
        self.elapsed_time = 0
        self.process = []
        self.life = []
        self.partial_counter = 0       

    def is_empty(self):
        if len(self.process) != 0:
            return False
        else:
            return True
    
    def __repr__(self):
        return  "CPU running %s...(time elapsed: %i | partial: %i)" % (self.process, self.elapsed_time, self.partial_counter)   


class Process():
    """Create a process in the system
    
    name is the name of the process, 
    duration is the given estimated processor time. If it's None, the process 
    run until the method finish() is given. 
    """ 

    status_codes = ('new', 'ready', 'running', 'blocked', 'finished')
    INFINITE = 5000
    
    def __init__(self, name="", init_time=0, estimated_duration=INFINITE, status='new', order=None):

        self.name = name or random.choice(range(1000)) 
        self.init_time = init_time
        self.end_time = -1

        self.cpu_time = 0 #no processor time yet
        self.estimated_duration = estimated_duration
        self.waiting_time = 0
        self.life = []  #log status of the process during its life. 
        self.status = status 
        self.remaining_time = self.estimated_duration
        
        self.order = order 
        self.nice = 0

    def response_rate(self):
        "calcules and returns the Response Rate"
        r = float(self.waiting_time + self.estimated_duration) / float(self.estimated_duration)
        return r

               
    def __len__(self):
        return len(self.life)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Process %s (%s). CPU = %i | WT = %i | INIT = %i | END = %i | ET = %i | RT = %i | N = %i  " % (self.name, 
                self.status, self.cpu_time, self.waiting_time, self.init_time, self.end_time, self.estimated_duration, 
                self.remaining_time, self.nice)



    #@logger("Process")        
    def run(self,cycles=1):
        """Run the process during 'cycles' cpu  and update its values"""
        
        if self.status != 'finished':
            self.status = "running"                    
            if self.remaining_time > cycles:
                self.cpu_time += cycles
                #update life
                self.life +=  [self.status] * cycles
            else:
                self.cpu_time += self.remaining_time
                self.life += [self.status] * self.remaining_time
                self.finish()
            
            self.remaining_time = self.estimated_duration - self.cpu_time
            

    def wait(self, status="ready", cycles=1):
        """wait in 'status' queue over 'cycles' CPU periods"""
        self.status = status
        self.waiting_time += cycles
        self.life += [self.status] * cycles
                 

    def finish(self):
        "Finish the process and set status"
        self.status = "finished"
        self.life += [self.status]
    
    def block(self):
        self.status = "blocked"
        self.life += [self.status]

    


class ProcessFactory():
    """a factory of processes. 
        Feeds ReadyQueue with new process when
        the schedule of process list determine it.  
    """

    def __init__(self, process_table, process_list):
        self.process_table = process_table
        
    #@logger("ProcessFactory")
    def get_new_process(self, time):
        """add new process if it's born time"""
        new_processes = [Process(**p) for p in self.process_table if p['init_time'] == time]
        return new_processes

class Algorithm():
    "general class for scheduling algorithm"
    
    #@logger("Algorithm")
    def __init__(self, process_table=None):        
        self.cpu = Cpu()
        self.clock = Clock()
        self.long_name = self.short_name = "Generic Algorithm"
        
        self.reset()
        
        self.preferent = False #if False never a running process is taking off from CPU
        
        self.factory = None
        if process_table:
            self.set_process_table(process_table)
        


    def set_process_table(self, process_table):
        """ Function doc """
        

        if self.factory is None or process_table is not self.factory.process_table:        
            self.factory = ProcessFactory(process_table, self.clock)
            for process in process_table:
                #TODO hay que considerar el idle time
                self.total_estimated_duration += process['estimated_duration']

    


    def __repr__(self):
        sal = "%s (%s) " % (self.long_name, self.short_name)
        sal += "\nSystem time: %i" % self.clock.time
        sal += "\nEstimated duration: " + str(self.total_estimated_duration) 
        sal += "\n%s\n" % self.cpu
        sal += "QUEUE\n"
        for process in self.process_list:
            sal += process.__str__() + "\n"
        return sal
    


    #@logger("Algorithm")
    def step(self):
        """rutine executed on every clock signal"""
        if self.factory is None:
            sys.stderr.write('%s: No hay tabla de procesos asignadas para esta instancia' % self.short_name)
    
        self.process_list.extend(self.factory.get_new_process(self.clock.time)) #time to a new processes?
        self.recalculate() #reorder list applying selection function

        self.clock.inc() #increment global clock
        p = self.cpu.step() #if finish return the process
        if p:
            p.end_time = self.clock.time
            self.finished.append(p)

        for p2 in self.process_list:
            p2.wait()

    #@logger("Algorithm")
    def recalculate(self):
        """reorder the queue and set new process on CPU"""
        
        
        if self.preferent and not self.cpu.is_empty():
            #may be a running process could go back to the queue
            self.process_list.append(self.cpu.get_process())
        
        
        self.process_list.sort(cmp = self.selection_function)
        

        #set first on CPU
        if self.cpu.is_empty() and len(self.process_list) > 0:
            self.cpu.set_process(self.process_list.pop(0)) 


    def reset(self):
        self.process_list = []
        self.finished = []
        self.total_estimated_duration = 0
        self.total_time_running = 0
        self.clock.reset()
        self.cpu.reset()
        
        
    def set_ax(self, fig, order='111'):
        def cmp_by_order(x, y):
            if x.order < y.order:
                return -1
            if x.order == y.order:
                return 0
            if x.order > y.order:
                return 1
        
        all_process = self.finished + self.process_list + self.cpu.process
        all_process.sort(cmp = cmp_by_order)

        vspace = 1.5
        #x = np.arange((self.clock.time if self.clock.time < self.total_estimated_duration else self.total_estimated_duration) + 1 )
        x = np.arange(self.clock.time + 1)

        ax = fig.add_subplot(order)
        ax.clear()
        for i,p in enumerate(all_process):            
            life_in_binary = [1 if state=='running' else 0 for state in p.life]
            x_range = range(p.init_time,(p.end_time + 1 if p.end_time !=-1 else self.clock.time))
            #print x_range, life_in_binary
            ax.plot(x_range, np.array(life_in_binary)-vspace*(i+1),  linestyle="steps", drawstyle='steps-post', label=p.name,lw=2)


        

        ax.set_xticks(np.arange(self.clock.time, step=(self.clock.time)/20 + 1))

        ax.set_yticks(np.arange(-vspace,-(1+len(all_process))*vspace, -vspace))
        ax.set_yticklabels([p.name for p in all_process])
        #ax.set_title(self.long_name)
        #ax.set_ylabel(self.long_name, rotation='horizontal')
        ax.set_ylabel(self.short_name)
        ax.grid(True)


    def plot(self):
        fig = plt.figure()
        self.set_ax(fig, '111')
        #self.set_ax(fig, '212')
        plt.show()
