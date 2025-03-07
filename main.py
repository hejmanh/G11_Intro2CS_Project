import time
from scheduler import *
from task1 import *
from task2 import *
from task3 import *


scheduler = Scheduler()
scheduler.SCH_Init()

task3 = Task3()
task2 = Task2()
task1 = Task1()

scheduler.SCH_Add_Task(task3.update_result_text, 40000 ,0)
scheduler.SCH_Add_Task(task2.analyze_weather("d:\Downloads\VGU\Intro to CS\RTOS\BerlinGermany.csv"), 20000 ,0)
scheduler.SCH_Add_Task(task1.Task1_Run, 0,0)

while True:
    scheduler.SCH_Update()
    scheduler.SCH_Dispatch_Tasks()
    time.sleep(0.1)