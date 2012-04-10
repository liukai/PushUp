import os, sys, psutil

class UsageReporter:
    def __init__(self, pid = os.getpid(),
                 output = sys.stdout):
        self.output = output
        self.process = psutil.Process(pid)

    def report(self, interval = 0.1,
               formatter = "Memory Usage: %f, CPU Usage: %f\n"):
        memory = self.process.get_memory_percent()
        cpu = self.process.get_cpu_percent(interval)
        self.output.write(formatter % (memory, cpu))
        print formatter % (memory, cpu)

