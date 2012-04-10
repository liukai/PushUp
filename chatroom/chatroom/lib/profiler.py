import sys
sys.path.append("../utils/")
import usage_reporter
import threading
import time

class SafeCounter():
    def __init__(self):
        self.lock = threading.RLock()
        self.val = 0

    def increase(self):
        self.lock.acquire()
        self.val += 1
        self.lock.release()

    def decrease(self):
        self.lock.acquire()
        self.val -= 1
        self.lock.release()

    def value(self):
        self.lock.acquire()
        value = self.val
        self.lock.release()

        return value

def reportUsage(interval, reporter, safeCounter):
    basicFormatter = " :Memory Usage: %f, CPU Usage: %f\n"
    while True:
        val = safeCounter.value()
        formatter = str(val) + basicFormatter
        reporter.report(0, formatter)
        time.sleep(interval)

def runReportUsage(interval, output, safeCounter):
    reporter = usage_reporter.UsageReporter(output = output)

    thread = threading.Thread(target = reportUsage,
            args = (interval, reporter, safeCounter))
    thread.daemon = True
    thread.start()

