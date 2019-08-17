# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import scrp
import _thread

import os



os.system('wget https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz')
os.system('tar -zxvf geckodriver-v0.11.1-linux64.tar.gz')
os.system('wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2')
os.system('tar xjf phantomjs-2.1.1-linux-x86_64.tar.bz2')
cwd = os.getcwd()
path = cwd + '/phantomjs-2.1.1-linux-x86_64/bin'
os.environ["PATH"] += os.pathsep + path
os.environ["PATH"] += os.pathsep + cwd





CHOOSING, TYPING_REPLY, TYPING_CHOICE, USERPASS, START_TIME, FINISH_TIME, COMMENTS, LESSON, PROFESSOR, CHOOSING_NOMRE, DATE = range(
    11)





reply_keyboard = [['فرستادن نام کاربری و کلمه عبور (username, password)'],
                  ['شروع']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(bot, update):
    update.message.reply_text(
        'سلام! کار من اینه که با استفاده از یوزرنیم و پسورد erp وارد سامانه بشم'
        ' و فرم ارزشیابی و انجام بدم! *فقط یه نکته مهم واسه هر دفعه که باید نمره بدی ۲۰ ثانیه وقت داری*',
        reply_markup=markup
    )
    return CHOOSING


def user_pass(bot, update, user_data):
    user_data['choice'] = 'username'
    update.message.reply_text('خب {} خودتو بده:'.format('نام کاربری'))
    return USERPASS


def received_userpass(bot, update, user_data):
    user_data['nomre'] = -1
    with open('n.txt', 'r') as f:
        NUM = int(f.read())
    print(NUM)
    if NUM == 1:
        update.message.reply_text('الان یه نفر دیگه داره از بات استفاده میکنه بعدا دوباره امتحان کن',
                                  reply_markup=markup)
        return CHOOSING
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    if category == 'username':
        update.message.reply_text('خب {} خودتو بده:'.format('کلمه عبور'))
        user_data['choice'] = 'password'
        return USERPASS
    del user_data['choice']
    if 'time_table' in user_data:
        update.message.reply_text('خب الان شروع میکنم!')
        _thread.start_new_thread(scrp.main, (user_data, bot, update))
        del user_data['time_table']
        bot.send_message(chat_id=update.message.chat.id, text='یه ذره صبر کن!')
        return CHOOSING
    update.message.reply_text('خب اطلاعات گرفته شد! الان میتونی شروع کنی!',
                              reply_markup=markup)
    return CHOOSING


def start_scrp(bot, update, user_data):
    if 'username' not in user_data:

        update.message.reply_text('اول باید نام کاربری و کلمه عبور رو بفرستی!')
        bot.send_message(chat_id=update.message.chat_id, text='خب {} خودتو بده:'.format('نام کاربری'))
        user_data['choice'] = 'username'
        return USERPASS

    with open('n.txt', 'r') as f:
        NUM = int(f.read())
    print(NUM)
    if NUM == 1:
        update.message.reply_text('الان یه نفر دیگه داره از بات استفاده میکنه بعدا دوباره امتحان کن',
                                  reply_markup=markup)
        return CHOOSING
    _thread.start_new_thread(scrp.main, (user_data, bot, update))
    bot.send_message(chat_id=update.message.chat.id, text='یه ذره صبر کن!')
    return CHOOSING


def received_nomre(bot, update, user_data):
    nomre = update.message.text
    nomre = 20 - int(nomre)
    user_data['nomre'] = nomre

    return CHOOSING


def restart(bot, update, user_data):
    user_data.clear()
    update.message.reply_text('اطلاعاتت پاک شد.', reply_markup=markup)


def unknown(bot, update):
    update.message.reply_text('ورودی یا دستور نامعتبر!', reply_markup=markup)
    return CHOOSING


def main():
    updater = Updater('')

    dp = updater.dispatcher
    restart_command_handler = CommandHandler('stop', restart, pass_user_data=True)
    dp.add_handler(restart_command_handler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), MessageHandler(Filters.text, start)],

        states={
            CHOOSING: [RegexHandler('^.*\(username\, password\)$',
                                    user_pass,
                                    pass_user_data=True),
                       
                       
                       RegexHandler('^شروع$',
                                    start_scrp,
                                    pass_user_data=True),
                       
                       CommandHandler('start',
                                      start),
                       
                       RegexHandler('12|13|14|20|12|15|16|17|18|19|20',
                                      received_nomre,
                                      pass_user_data=True),
                       
                       MessageHandler(Filters.all,
                                      unknown),
                       ],
            USERPASS: [MessageHandler(Filters.text,
                                      received_userpass,
                                      pass_user_data=True)],

        },

        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

# '517255695:AAFSQ549HEYNGhDCT3iC2dLgst1w5YPLOOA'
