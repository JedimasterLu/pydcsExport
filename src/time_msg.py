import time

def get_time()->str:
    return time.strftime('%H:%M:%S',time.localtime(time.time()))

def add_time(msg:str)->str:
    time = get_time()
    return f'{time} {msg}'

def get_date()->str:
    return time.strftime('%Y%m%d',time.localtime(time.time()))