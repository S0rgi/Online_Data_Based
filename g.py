#для времени
import datetime
import time
#для телеграма
from pyrogram import Client, filters
#ускорение работы телеграма
import uvloop
# для сайтов
import requests
from bs4 import BeautifulSoup
#для баз данных
import sqlite3

def main ():
    uvloop.install()
    BD()
    print(f' Текущее время  {(datetime.datetime.now()).strftime("%d-%m-%Y %H:%M")}\n')
    print (f' Telegram  -  ')
    conn = sqlite3.connect('/home/sorgi/PycharmProjects/Online_Data_Based/online.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM online;")
    all_results = cursor.fetchall()
    max=-3
    for index,current in enumerate(all_results):
        if current[2]=='Online':
            max = index
    # if max ==-3:
    #     VK_output = (all_results[len(all_results)-1])[4]

    VK_output = 'была в сети сегодня в 0:56'
    function = Vks(VK_output)
    time_online = f'{(all_results[max + 1])[0]} {(all_results[max + 1])[1]}'
    time_online = datetime.datetime.strptime(time_online, "%d-%m-%Y %H:%M")
    if type(function) ==tuple:
        t1 = (function[0]-time_online)
        t2 = (time_online-function[1])
        if ((str(t1))[ 0]!='-') and ((str(t2))[0]!='-'):
            VK_output = time_online
        else:
            VK_output = VK_output
    elif type(function) !=tuple:
        print(function)
    else:
        try:
            if (all_results[max+1])[4]=='заходила 5 минут назад':
                time = f'{(all_results[max+1])[0]} {(all_results[max+1])[1]}'
                time = datetime.datetime.strptime(time, "%d-%m-%Y %H:%M") - datetime.timedelta(minutes=5)
                VK_output = f'в сети {time}'
        except IndexError:
            time = f'{(all_results[max ])[0]} {(all_results[max ])[1]}'
            VK_output = f'в сети {time}'

    try:
        s= (all_results[len(all_results)-1])[5]
        print(f'     {s}')
        now = datetime.datetime.now()
        fow = str(now)[0:-7]
        now = datetime.datetime.strptime(fow, "%Y-%m-%d %H:%M:%S")
        s = s[-19::]
        s = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        f = (now - s)
        print(f'     то есть {timeschet(f,True)} назад')
    except:
        pass
    print(f' Вконтакте - ')
    print(f'     {VK_output}')
    try:
        try:
            s = VK_output
            s = s[-19::]
            s = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            f = (now - s)
            print(f'     то есть {timeschet(f,False)} назад')
        except:
            #vivod = f'в промежутке от {time[1]} до {time[0]}'
            print(f'     то есть {Vks(VK_output)}')
    except:
        pass
def g(s,now):
    low = now.strftime("%d-%m-%Y %H:%M")
    pow = datetime.datetime.strptime(low, "%d-%m-%Y %H:%M")
    fow = pow.strftime("%d-%m-%Y")
    time = datetime.datetime.strptime(f'{fow} {s[-5::]}', '%d-%m-%Y %H:%M')
    now = datetime.datetime.now()
    low = now.strftime("%d-%m-%Y %H:%M")
    pow = datetime.datetime.strptime(low, "%d-%m-%Y %H:%M")
    timeleft = pow - time

    return timeschet(timeleft,True)
def findMonth(s,maxindex):
    mes = ('янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек')
    mon = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '12')

    for index, m in enumerate(mes):
        if s[maxindex:maxindex+3] == m or s[maxindex+1:maxindex+4] == m:
            month = mon[index]
    return month
def Vks(s):

    index = s.find (' назад')
    if index !=-1: #Если есть слово назад
        if s[index-3:index]=='час':
            time  = [datetime.datetime.now() - datetime.timedelta(minutes=60),datetime.datetime.now() - datetime.timedelta(minutes=120)]

        elif s[index-4:index] =='часа':
            if s[index-8:index-5]=='два':
                time = [datetime.datetime.now() - datetime.timedelta(minutes=120),datetime.datetime.now() - datetime.timedelta(minutes=180)]
            else:
                time = [datetime.datetime.now() - datetime.timedelta(minutes=180) , datetime.datetime.now() - datetime.timedelta(minutes=240)]
        else:
            index2=s.find(' минут')

            if s[index2-2]!=' ':
                timeleft =str(s[index2-2:index2])
            else:
                timeleft = str(s[index2-1])
            time = [datetime.datetime.now() - datetime.timedelta(minutes=int(timeleft)-1),datetime.datetime.now() - datetime.timedelta(minutes=int(timeleft)+1)]
        return time[1],time[0]

    else     :#Если указано точное время
        if s.find('сегодня')!=-1:
            dayleft=0
            now=datetime.datetime.now()
            return g(s,now)


        elif s.find(' вчера ')!=-1:
            now = datetime.datetime.now() - datetime.timedelta(days=1)
            return g(s,now)

        elif s.find('в сети')!=-1:
            month= findMonth(s,-11)
            index = s.find('ти ')
            if s[index+4]!=' ':
                day = s[index+3:index+5]
            else:
                day = s[index+3]
            now = datetime.datetime.now()
            low = now.strftime("%d-%m-%Y %H:%M")
            index= low.find('-')
            pow = datetime.datetime.strptime(f'{day}-{month}{low[index+3:index+8]} {s[-5::]}','%d-%m-%Y %H:%M')
            timenow=datetime.datetime.strptime(low, "%d-%m-%Y %H:%M")
            timeleft = timenow - pow
            return timeschet(timeleft,True)

        else:
            index= s.find('л')
            if s[index+1]!=' ':
                index+1

            if s[index+3]==' ': #если день меньше 10
                day = s[index+2]
                month= findMonth(s,-16)
                year = s[index+8:index+12]
                time= s[-5::]
                time= datetime.datetime.strptime(f'{day}-{month}-{year} {time}',"%d-%m-%Y %H:%M")
                now = datetime.datetime.now()
                low = now.strftime("%d-%m-%Y %H:%M")
                timenow = datetime.datetime.strptime(low, "%d-%m-%Y %H:%M")
                timeleft = timenow - time
                return timeschet(timeleft,True)

def timeschet(f,K):#запрашивает разницу во времени

    f=str(f)
    if len(f)<14:#если меньше дня
        if f[1]==':':

            if int(f[0])==1:
                g='час'
            elif 1<int(f[0])<5 :
                g = 'часа'
            else:
                g = 'часов'
            h = f'{f[0]} {g}'
            if int(f[0])==0:
                h=''

            if int(f[3]) == 1 and int(f[2])!=1 :
                g = 'минуту'
            elif (1 < int(f[3]) < 5) and int(f[2])!=1 :
                g = 'минуты'
            else:
                g = 'минут'
            m = f'{f[2:4]} {g}'
            if (f[2:4])=='00':
                m=''
            elif f[2]=='0':
                m=f'{f[3]} {g}'
            if int(f[6]) == 1 and int(f[5])!=1 :
                g = 'секунду'
            elif (1 < int(f[6]) < 5) and int(f[5])!=1 :
                g = 'секунды'
            else:
                g = 'секунд'
            s= f'{f[5::]} {g}'
            if f[5::]=='00':
                s = f''
            elif f[5]=='0':
                s = f'{f[6::]} {g}'
        else:
            if int(f[1])==1 and int(f[0])!=1:
                g='час'
            elif (1<int(f[1])<5) and int(f[0])!=1 :
                g = 'часа'
            else:
                g = 'часов'
            h = f'{f[0:2]} {g}'

            if (f[0:2])=='00':
                h=''
            elif f[0]=='0':
                h=f'{f[1]} {g}'

            if int(f[4]) == 1 and int(f[3])!=1 :
                g = 'минуту'
            elif (1 < int(f[4]) < 5) and int(f[3])!=1 :
                g = 'минуты'
            else:
                g = 'минут'
            m = f'{f[3:5]} {g}'
            if (f[3:5])=='00':
                m=''
            elif f[3]=='0':
                m=f'{f[4]} {g}'
            if int(f[7]) == 1 and int(f[6])!=1 :
                g = 'секунду'
            elif (1 < int(f[7]) < 5) and int(f[6])!=1 :
                g = 'секунды'
            else:
                g = 'секунд'
            s= f'{f[6::]} {g}'
            if f[6::]=='00':
                s = f''
            elif f[7]=='0':
                s = f'{f[7::]} {g}'
        if K:
            vivod =f'{h} {m} {s}'
        else:
            vivod = f'{h} {m}'
    else:#если больше дня
        index= f.find('d')
        if f[1] == ' ':
            if int(f[index-2]) == 1:
                g = 'день'
            elif 1 < int(f[index-2]) < 5:
                g = 'дня'
            else:
                g = 'дней'
        else:

            if int(f[index-2]) == 1 and int(f[index-3]) != 1:
                g = 'день'
            elif 1 < int(f[index-2]) < 5 and int(f[index-3]) != 1:
                g = 'дня'
            else:
                g = 'дней'
        d=f'{f[0:index-1]} {g}'

        index = f.find(',')
        if f[index+3]==':':#если несколько дней и до 10 часов
            if int(f[index+2])==1:
                g='час'
            elif 1<int(f[index+2])<5 :
                g = 'часа'
            else:
                g = 'часов'

            h=f'{f[index+2]} {g}'

            if f[index+2]=='0':
                h=f''
            if int(f[index+5])==1 and int(f[index+4])!=1:
                g='минуту'
            elif 1<int(f[index+5])<5 and int(f[index+4])!=1:
                g = 'минуты'
            else:
                g = 'минут'
            m= f'{f[index+4:index+6]} {g}'
            if (f[index+4:index+6])=='00':
                m=''
            elif f[index+4]=='0':
                m=f'{f[index+5]} {g}'
            if int(f[index+8]) == 1 and int(f[index+7])!=1 :
                g = 'секунду'
            elif (1 < int(f[index+8]) < 5) and int(f[index+7])!=1 :
                g = 'секунды'
            else:
                g = 'секунд'
            s= f'{f[index+7::]} {g}'

            if (f[index+7::])=='00':
                s=''
            elif (f[index+7])=='0':
                s=f'{f[index+8]} {g}'


        else:#если несколько дней и больше 10 часов
            print((f[index+3]))
            if int(f[index+3])==1 and int(f[index+2])!=1:
                g= 'час'
            elif 1<int(f[index+3])<5 and int(f[index+2])!=1:
                g= 'часа'
            else:
                g= 'часов'
            h = f'{f[index + 2:index+4]} {g}'
            if (f[index+2:index+4])=='00':
                h=''
            elif f[index+2]=='0':
                h=f'{f[index+3]} {g}'
            if int(f[index + 2:index+4])==0:
                h=''
            if int(f[index+6])==1 and int(f[index+5])!=1:
                g='минуту'
            elif 1<int(f[index+6])<5 and int(f[index+5])!=1:
                g = 'минуты'
            else:
                g = 'минут'
            m= f'{f[index+5:index+7]} {g}'
            if (f[index+5:index+7])=='00':
                m=''
            elif f[index+5]=='0':
                m=f'{f[index+6]} {g}'
            if int(f[index+9]) == 1 and int(f[index+8])!=1 :
                g = 'секунду'
            elif (1 < int(f[index+9]) < 5) and int(f[index+8])!=1 :
                g = 'секунды'
            else:
                g = 'секунд'
            s= f'{f[index+8::]} {g}'
            if (f[index+8::])=='00':

                s=''
            elif (f[index+8])=='0':
                s = f'{f[index + 9]} {g}'
        if K:
            vivod =f'{d} {h} {m} {s}'
        else:
            vivod = f'{d} {h} {m}'

    return vivod
def FirstSign():
    #Api id из https://my.telegram.org/apps
    try:
        api_id: int = int(input('Введите api ID'))
    except:
        api_id = 10268925

    # Api hash из https://my.telegram.org/apps
    try:
        api_hash = int(input('Введите api hash'))
    except:
        api_hash = "ab2124de1c4e2b9a8bca00364e144c3d"
    #  По дефолту стоят значения с моим Api_if и Api_hash
    uvloop.install()
    app = Client("my_account", api_id=api_id, api_hash=api_hash)

    app.run()
    # Далее выведет
    # Enter phone number: надо ввести свой номер вида +1-123-456-7890
    # На телефон придёт код входа, введи
    # в последующие разы на этом устройстве не придётся использовать api_id, api_hash , номер телефона и код
    # всё будет работать автоматом

def fina(a,b):
    if a.find(b)!=-1:
        return True
    else :
        return False

def pars(f):
    def fina(a,b):
        if a.find(b)!=-1:
            return True
        else :
            return False

    s=''''''
    for a in str(f):
        s+=a
    s=s.split('"user": {')
    for i in s:
        # вместо ' "first_name": "Соня" ' можно вставить любой параметр , главное не забыть про кавычки , захватывающие всю строку
        if fina(i,b='"first_name": "Соня"'):
            index = i.find("status")
            a= (i[index:index+80])
        else:
            pass
    a= (a.replace("}",""))

    return (a.replace("}","")).replace('\n','')
def BD():
    conn = sqlite3.connect('/home/sorgi/PycharmProjects/Online_Data_Based/online.db', check_same_thread=False)
    cursor = conn.cursor()

    def db_table_val(date: str, time: str, VK_online: str, Telegram_online: str,VK_output,TG_output):
        cursor.execute('INSERT OR REPLACE INTO online(date, time, VK_online, Telegram_online,VK_output,TG_output) VALUES (?, ?, ?, ?, ?, ?)',
                       (date, time, VK_online, Telegram_online,VK_output,TG_output))
        conn.commit()

    #8-962-321-4239

    TARGET = -675385072

    # 11 А класс   -756259936
    # 11 параллель -675385072

    app = Client("my_account")

    async def APP():
        async with app:
            async for member in app.get_chat_members(TARGET):
                a=str(pars(member))

                if a[21:28]=="OFFLINE":
                    index1 = a.find('"last_online_date": "')
                    a= a[index1+21:index1+40]
                    VK_v = VK()
                    if VK_v == 'online':
                        vk_online = 'Online'
                    else:
                        vk_online = 'Offline'

                    TG_v= f"Offline {a}"

                    tg_online = TG_v[0:7]
                    datanow = (datetime.datetime.now()).strftime("%d-%m-%Y")
                    timenow = (datetime.datetime.now()).strftime("%H:%M")
                    db_table_val(date=datanow, time=timenow, VK_online=vk_online, Telegram_online=tg_online,VK_output=VK_v,TG_output=TG_v)

                elif a[21:27]=="ONLINE":
                    a=str(datetime.datetime.now())[0:20]

                    VK_v = VK()
                    if VK_v == 'online':
                        vk_online = 'Online'
                    else:
                        vk_online = 'Offline'

                    TG_v= f"Online {a}"

                    tg_online = TG_v[0:6]
                    datanow = (datetime.datetime.now()).strftime("%d-%m-%Y")
                    timenow = (datetime.datetime.now()).strftime("%H:%M")
                    db_table_val(date=datanow, time=timenow, VK_online=vk_online, Telegram_online=tg_online,VK_output=VK_v,TG_output=TG_v)


    app.run(APP())

def VK():
    #просто забить в гугле свой юзер агент
    UserAgent ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.66"
    headers = {"User-Agent": UserAgent}
    # сюда любая ссылка вк
    valueURL = "https://vk.com/t.sonn"
    full_page = requests.get(valueURL, headers=headers)

    soup = BeautifulSoup(full_page.content, 'html.parser')
    #здесь указываем расположение искомой информации
    convert = soup.find_all("div", {"class": "profile_online_lv"})
    # Если информация скрыта, то массив информации останется пустым

    try:
        return (f'{convert[0].text}')

    except IndexError: #Если массив пуст
        return ("     This information is masked ")


if __name__ == '__main__':

    main()