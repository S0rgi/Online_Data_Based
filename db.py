#из модуля time импортируем функцию sleep
from time import sleep
#ускорение работы телеграма
import uvloop
#импрот модулей мз g.py
from g import   BD
from datetime import datetime
if __name__ == '__main__':
    uvloop.install()
    while True:
        try:
            BD()
            sleep(60)
        except Exception as e:
            sleep(3)
            print(datetime.now)
            print(e)
