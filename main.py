# https://github.com/watermelon46/CCReborn

import time, os, json, getpass
from platform import uname

try:
    from colorama import Fore, Style, init
except ModuleNotFoundError:
    print('Colorama отсутствует. Попытка установки из PyPi...')
    os.system('pip install colorama')
    from colorama import Fore, Style, init

init()

clickerActive = False
clickerActiveTime = 0
clickerLastClick = 0

config = {
    "autoLoadGame": False, # Автоматическая загрузка сохранения.
    "cfgDir": "ToBeFilled", # Папка для хранения сохранений. Обычно, заполняется автоматически используя SysCompat. Уберите ToBeFilled, чтобы не заполнять автоматически
    "clearCmd": "ToBeFilled", # Команда, используемая функцией clear(). Обычно, заполняется автоматически используя SysCompat. Уберите ToBeFilled, чтобы не заполнять автоматически.
    "system": "ToBeFilled", # Тип системы. Влияет на принцип работы clear()
}

if config['system'] == 'ToBeFilled':
    config['system'] = uname()[0]

def SysCompat(): # Функция, которая обеспечивает совместимость CC Reborn с Windows, Linux и MacOS
    if config['system'] == 'Windows':
        if config['clearCmd'] == "ToBeFilled":
            config['clearCmd'] = 'cls'
        if config['cfgDir'] == "ToBeFilled":
            config['cfgDir'] = 'C://CookieClicker//'
    elif (config['system'] == 'Linux') and ('aarch' in uname()[4]):
        if config['clearCmd'] == "ToBeFilled":
            config['clearCmd'] = 'clear'
        if config['cfgDir'] == "ToBeFilled":
            isAndroid = input(f"{Fore.GREEN}🤖 • Кажется, что вы используете Android.\nИспользовать Android'овский путь к папке сохранения (рекомендуется, если у вас Android)\n[Y/N]\n> {Style.RESET_ALL}")
            if isAndroid == 'Y' or isAndroid == 'y':
                config['cfgDir'] = '//storage//emulated//0//CookieClicker//'
    else:
        if config['clearCmd'] == "ToBeFilled":
            config['clearCmd'] = 'clear'
        if config['cfgDir'] == "ToBeFilled":
            config['cfgDir'] = f'//home//{getpass.getuser()}CookieClicker//'

def clear():
    os.system(config['clearCmd'])

SysCompat()
clear()

player = {
    "cookies" : 0,
    "coins" : 0,
    "boosters" : 0,
    "clickers" : 0,
    "watermelons" : 0
}

def save(showSuccessSave = True):
    prepared_data = json.dumps(player, indent = 4)
    dir = config['cfgDir']
    try:
        save_file = open(f'{dir}ccsave.json', 'w')
    except FileNotFoundError:
        os.mkdir(dir)
        save_file = open(f'{dir}ccsave.json', 'w')
    save_file.truncate(0)
    save_file.write(prepared_data)
    save_file.close()
    if showSuccessSave == True:
        print(f'{Style.RESET_ALL + Fore.GREEN}Игра сохранена!{Style.RESET_ALL}')

def load():
    global clickerActive
    clickerActive = False
    dir = config['cfgDir']
    try:
        save_file = open(f'{dir}ccsave.json')
    except FileNotFoundError:
        print(f'{Style.RESET_ALL}{Fore.RED}Файл сохранения не найден, создаем при помощи save...{Style.RESET_ALL}')
        save(False)
        save_file = open(f'{dir}ccsave.json')
    global player
    save_data = save_file.read()
    player = json.loads(save_data)
    save_file.close()
    print(f'{Style.RESET_ALL + Fore.GREEN}Игра загружена!{Style.RESET_ALL}')

if config['autoLoadGame'] == True:
    load()

def reInput():
    return input(f'{Style.RESET_ALL + Style.BRIGHT}\n> {Style.RESET_ALL}')

cache = None # Переменная для хранения всякой фигни
clear()
print(f'{Fore.YELLOW + Style.BRIGHT}CookieClicker {Style.RESET_ALL + Fore.YELLOW}Reborn {Fore.RESET}v1.1 beta\n{Style.RESET_ALL}Пропиши help для просмотра списка команд\n{Style.BRIGHT}Нажми Enter, чтобы начать{Style.RESET_ALL}')

# Переменные античита

ACLastClick = int(round(time.time() * 1000))
ACCheatClicks = 0

# Кликер

while True:
    try:
        command = input(f'{Style.RESET_ALL + Style.BRIGHT}\n> {Style.RESET_ALL}')
    except KeyboardInterrupt:
        print('Тебе трудно прописать exit?')
        if config['system'] != 'Windows':
            input('Нажмите Enter для продолжения\n')
        else:
            os.system('pause')
    clear()
    if command == '':
        summaryClick = player['boosters'] + 1
        if clickerActive == True:
            clickerActiveAgo = int(time.time() - clickerActiveTime)
            clickSecondsNeed = int(time.time() - clickerLastClick)
            if clickerActiveAgo > 300:
                player['cookies'] += summaryClick * 300
                clickerActive = False
            else:
                player['cookies'] += summaryClick * clickSecondsNeed
            clickerLastClick = time.time()
            toClickerEnd = 300 - clickerActiveAgo

        diff = int(round(time.time() * 1000)) - ACLastClick

        if diff < 450:
            if ACCheatClicks < 4:
                print(f'{Fore.GREEN + Style.BRIGHT}⚠️  •  Кликать можно раз в 450мсек! Не читери!{Style.RESET_ALL}')
                ACCheatClicks += 1
            else:
                print(f'{Fore.RED + Style.BRIGHT}⚠️  •  Перестань спамить Enter! Игра таймаутнула тебя на 10 секунд, чтобы ты подумал о своем поведении.{Style.RESET_ALL}')
                time.sleep(10)
                ACCheatClicks = 0
        else:
            player['cookies'] += summaryClick
            ACLastClick = int(round(time.time() * 1000))
            ACCheatClicks = 0
            print(f'{Fore.GREEN + Style.BRIGHT}🍪 • Клик!\n\nВаш баланс:\n {Style.RESET_ALL + Fore.YELLOW}Печеньки: {Style.RESET_ALL}{player["cookies"]}\n {Fore.YELLOW}Монетки: {Style.RESET_ALL}{player["coins"]}\n {Fore.YELLOW}Арбузы: {Style.RESET_ALL}{player["watermelons"]}\n {Fore.YELLOW}Бустеры: {Style.RESET_ALL}{player["boosters"]}\n {Fore.YELLOW}Кликеры: {Style.RESET_ALL}{player["clickers"]}')
        if clickerActive:
            print(f'{Fore.GREEN + Style.BRIGHT}ℹ • До конца кликера осталось {toClickerEnd} сек.')
        
    elif command == 'exit':
        print(f'{Fore.RED + Style.BRIGHT}Сохранить игру перед выходом? [Y/N]')
        if reInput() == 'Y':
            save()
        break
    elif command == 'exchange':
        cache = player['cookies'] / 100
        player['coins'] = player['coins'] + player['cookies'] / 100 + player['watermelons'] / 10
        player['cookies'] = 0
        print(f'{Fore.GREEN + Style.BRIGHT}💱 • Ваши печеньки были обменены на монетки ({cache})')
    elif command == 'save':
        save()
    elif command == 'load':
        load()
    elif command == 'help':
        print(f"{Fore.GREEN + Style.BRIGHT}ℹ • Команды CookieClicker'а\n\n{Style.RESET_ALL + Fore.YELLOW}пустая команда - {Style.RESET_ALL}клик\n{ Fore.YELLOW}help - {Style.RESET_ALL}это меню\n{Fore.YELLOW}exchange - {Style.RESET_ALL}обменять печеньки на монетки с курсом 100 печенек к 1 монетке\n{Fore.YELLOW}shop - {Style.RESET_ALL}магазин\n{Fore.YELLOW}clicker - {Style.RESET_ALL}запустить автокликер\n{Fore.YELLOW}save - {Style.RESET_ALL}сохранить игру\n{Fore.YELLOW}load - {Style.RESET_ALL}загрузить игру\n{Fore.YELLOW}exit - {Style.RESET_ALL}покинуть игру")
    elif command == 'reloadSysCompat':
        print(f"{Fore.GREEN + Style.BRIGHT}⏳ • Перезагружаем SysCompat...{Style.RESET_ALL}")
        SysCompat()
        clear()
        print(f"{Fore.GREEN + Style.BRIGHT}✔ • SysCompat успешно перезагружен, но зачем?{Style.RESET_ALL}")
    elif command == 'shop':
        shopcancel = 0
        print(f"{Fore.GREEN + Style.BRIGHT}ℹ • Магазин\nДля покупки введите код продукта\n{Style.RESET_ALL + Fore.YELLOW}Бустер (1) - {Style.RESET_ALL}5 монет\n{Style.RESET_ALL + Fore.YELLOW}Кликер (2) - {Style.RESET_ALL}10 монет\n{Style.RESET_ALL + Fore.YELLOW}Арбуз (3) - {Style.RESET_ALL}20 монет\n{Style.RESET_ALL}")
        shopinput = reInput()
        if shopinput == '1':
            if player['coins'] >= 5:
                player['coins'] -= 5
                player['boosters'] += 1
                print(f"{Fore.GREEN + Style.BRIGHT}✔ • Вы успешно купили 1 бустер!{Style.RESET_ALL}")
            else:
                shopcancel = 1
        elif shopinput == '2':
            if player['coins'] >= 10:
                player['coins'] -= 10
                player['clickers'] += 1
                print(f"{Fore.GREEN + Style.BRIGHT}✔ • Вы успешно купили 1 кликер! Он работает 5 минут, для его включения напишите clicker{Style.RESET_ALL}")
            else:
                shopcancel = 1
        elif shopinput == '3':
            if player['coins'] >= 20:
                player['coins'] -= 20
                player['watermelons'] += 1
                print(f"{Fore.GREEN + Style.BRIGHT}✔ • Вы успешно купили 1 арбуз!{Style.RESET_ALL}")
            else:
                shopcancel = 1
        if shopcancel == 1:
            print(f"{Fore.YELLOW + Style.BRIGHT}❌ • Неверный код продукта или недостаточно монет!{Style.RESET_ALL}")
    elif command == 'clicker':
        if player['clickers'] < 1:
            print(f"{Fore.YELLOW + Style.BRIGHT}❌ • У вас нет кликеров!{Style.RESET_ALL}")
        else:
            player['clickers'] -= 1
            clickerActive = True
            clickerActiveTime = time.time()
            clickerLastClick = clickerActiveTime
            print(f"{Fore.GREEN + Style.BRIGHT}✔ • Кликер запущен!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW + Style.BRIGHT}❌ • Неизвестная команда. Пропишите help для получения списка команд!{Style.RESET_ALL}")
