import configparser
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('config.ini')

def charge_command_handler(message):
    try:
        # بررسی مالکیت کاربر
        owner_id = int(config['OWNER']['user_id'])
        if message.from_user.id != owner_id:
            return "❌ فقط صاحب ربات مجاز به اجرای این دستور است!"

        # پردازش دستور شارژ
        if message.text.startswith("شارژ"):
            parts = message.text.split()
            if len(parts) != 2:
                return "❌ فرمت صحیح: «شارژ عدد» (مثال: شارژ 30)"
            
            days = int(parts[1])
            expiry_date = datetime.now() + timedelta(days=days)
            
            # به‌روزرسانی config
            config.read('config.ini')
            config['SUBSCRIPTION'] = {
                'active': 'True',
                'expiry': expiry_date.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            
            return f"✅ شارژ برای {days} روز با موفقیت فعال شد!"
            
    except ValueError:
        return "❌ عدد وارد شده نامعتبر است!"
    except KeyError:
        return "❌ تنظیمات مالک یافت نشد!"
    except Exception as e:
        return f"❌ خطای سیستمی: {str(e)}"

def is_subscription_active():
    try:
        config.read('config.ini')
        
        # بررسی وجود بخش اشتراک
        if not config.has_section('SUBSCRIPTION'):
            return False
            
        # بررسی وضعیت فعال/غیرفعال
        if not config.getboolean('SUBSCRIPTION', 'active'):
            return False
            
        # بررسی تاریخ انقضا
        expiry_str = config['SUBSCRIPTION'].get('expiry', '')
        if not expiry_str:
            return False
            
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
        return datetime.now() < expiry_date
        
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False