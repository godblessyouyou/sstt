import Queue
import threading
import time
import robot
import os


class TaskManager(object):
    def __init__(self, tasks, thread_max=10):
        self.task_queue = Queue.Queue()
        self.threads = []
        self.__init_task_queue(tasks)
        self.__init_thread_pool(thread_max)

    # init task queue, add all tasks
    def __init_task_queue(self, tasks):
        for task in tasks:
            self.add_task(do_task, task)
    
    # init thread pool
    def __init_thread_pool(self, threads_num):
        for i in range(threads_num):
            self.threads.append(Task(self.task_queue))
        
    def add_task(self, func, *args):
        print args
        self.task_queue.put((func, args))

    # wait all thread running completly
    def wait_all_complete(self):
        for item in self.threads:
            if item.isAlive():
                item.join()

class Task(threading.Thread):
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.task_queue.get(block=False)
                do(args)
                self.task_queue.task_done()
            except:
                break

def do_task(args):
    # each case on thread, args is the case path
    # here may be an error that need to handle
    # the environment might be busy, we should run it later
    robot.run(args[0])

if __name__ == '__main__':
    cases = []
    files = os.listdir('/root/test')
    for i in files:
        cases.append(os.path.join('/root/test', i))
    task_manager = TaskManager(cases, thread_max=1)
    task_manager.wait_all_complete()

