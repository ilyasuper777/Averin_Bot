import logging
import re
import os
import paramiko
from pathlib import Path
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler,MessageHandler, Filters, ConversationHandler
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('RM_HOST')
port = os.getenv('RM_PORT')
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')
TOKEN = os.getenv('TOKEN')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')

def get_release_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_uname_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /proc/cpuinfo; hostname; uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_uptime_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_df_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df -Th')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_free_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_mpstat_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_w_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /etc/passwd')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_auths_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('tail -n 10 /var/log/auth.log')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_critical_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -p err -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_ps_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_ss_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss -tulpn ')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_apt_list_Command(update: Update, context):
    update.message.reply_text('Введите пакет или all, если хотите получить информацию о всех установленных пакетах')
    return 'get_apt_list'

def get_apt_list(update: Update, context):
    user_input = update.message.text # Получаем текст
    client.connect(hostname=host, username=username, password=password, port=port)
    if user_input=="all":
        stdin, stdout, stderr = client.exec_command('apt list --installed')
        # stdin, stdout, stderr = client.exec_command('dpkg -l')
        data = stdout.read() + stderr.read()
    else:
        stdin, stdout, stderr = client.exec_command(f'dpkg -l {user_input}')
        data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    msgs = [data[i:i + 4096] for i in range(0, len(data), 4096)]
    for text in msgs:
        update.message.reply_text(text=text)
    #update.message.reply_text(data)
    return ConversationHandler.END # Завершаем работу обработчика диалога

def get_services_Command(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('systemctl list-units --type service --state running')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    msgs = [data[i:i + 4096] for i in range(0, len(data), 4096)]
    for text in msgs:
        update.message.reply_text(text=text)
    #update.message.reply_text(data)
    

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'find_phone_number'

def find_phone_number(update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(?:\+7|8)(?: \(\d{3}\) \d{3}-\d{2}-\d{2}|\d{10}|\(\d{3}\)\d{7}| \d{3} \d{3} \d{2} \d{2}| \(\d{3}\) \d{3} \d{2} \d{2}|-\d{3}-\d{3}-\d{2}-\d{2})')

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда email нет
        update.message.reply_text('Телефон(ы) не были найдены')
        return # Завершаем выполнение функции
    
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' # Записываем очередной номер
    
    update.message.reply_text(phoneNumbers) # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога



def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска Email-адресов: ')
    return 'find_Email'

def find_Email(update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) email

    Email = re.compile(r'[a-zA_Z0-9]+[@]{1}[a-zA-Z0-9]+[\.]{1}[a-zA-Z0-9]+', re.IGNORECASE)
    EmailList = Email.findall(user_input) # Ищем email

    if not EmailList: # Обрабатываем случай, когда email нет
        update.message.reply_text('Email-адреса не были найдены')
        return # Завершаем работу обработчика диалога
    
    Email = '' # Создаем строку, в которую будем записывать email
    for i in range(len(EmailList)):
        Email += f'{i+1}. {EmailList[i]}\n'
    
    update.message.reply_text(Email) # Отправляем сообщение пользователю
    return ConversationHandler.END # Завершаем работу обработчика диалога

def verify_passwordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки')
    return 'verify_password'

def verify_password(update: Update, context):
    user_input = update.message.text # Получаем пароль
    password = re.compile(r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()]).*$')
    result = password.search(user_input)

    if result == None: # Обрабатываем случай, когда номер телефона не верен
        update.message.reply_text('Пароль простой')
    else:
        update.message.reply_text('Пароль сложный')
    return ConversationHandler.END # Завершаем работу обработчика диалога

def echo(update: Update, context):
    update.message.reply_text(update.message.text)

def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)]
        },
        fallbacks=[]
    )

    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_Email', findEmailCommand)],
        states={
            'find_Email': [MessageHandler(Filters.text & ~Filters.command, find_Email)]
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verify_passwordCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )
	
    convHandlerget_apt_list = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_list_Command)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )

	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(CommandHandler("get_release", get_release_Command))
    dp.add_handler(CommandHandler("get_uname", get_uname_Command))
    dp.add_handler(CommandHandler("get_uptime", get_uptime_Command))
    dp.add_handler(CommandHandler("get_df", get_df_Command))
    dp.add_handler(CommandHandler("get_free", get_free_Command))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat_Command))
    dp.add_handler(CommandHandler("get_w", get_w_Command))
    dp.add_handler(CommandHandler("get_auths", get_auths_Command))
    dp.add_handler(CommandHandler("get_critical", get_critical_Command))
    dp.add_handler(CommandHandler("get_ps", get_ps_Command))
    dp.add_handler(CommandHandler("get_ss", get_ss_Command))
    dp.add_handler(CommandHandler("get_services", get_services_Command))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(convHandlerget_apt_list)
		
	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()