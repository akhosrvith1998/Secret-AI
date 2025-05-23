import configparser
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('config.ini')

def charge_command_handler(message):
    if message.text.startswith("شارژ"):
        try:
            days = int(message.text.split()[1])
            expiry_date = datetime.now() + timedelta(days=days)
            config['SUBSCRIPTION'] = {
                'active': 'True',
                'expiry': expiry_date.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            return f"✅ شارژ با موفقیت برای {days} روز فعال شد."
        except:
            return "❌ خطا! فرمت صحیح: «شارژ عدد»"

def is_subscription_active():
    config.read('config.ini')
    if 'SUBSCRIPTION' not in config:
        return False
    expiry_str = config['SUBSCRIPTION'].get('expiry', '')
    if not expiry_str:
        return False
    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
    return datetime.now() < expiry_date