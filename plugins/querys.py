import sqlite3
from typing import Union, Optional, List, Tuple

# ---------------------- توابع مدیریت کاربران ----------------------
def get_admins(chat_id: Union[str, int], user_id: int) -> bool:
    """بررسی آیا کاربر ادمین است یا خیر"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute("SELECT num_id FROM USERS WHERE is_admin = 1")
            admins = [admin[0] for admin in cur.fetchall()]
            
            # اگر لیست ادمین‌ها خالی باشد، تمام کاربران دسترسی دارند
            return user_id in admins if admins else True
            
    except sqlite3.Error as e:
        print(f"خطای دیتابیس: {str(e)}")
        return False

def new_user(name: str, username: str, user_id: int, status: str, chat_id: Union[str, int]) -> bool:
    """افزودن کاربر جدید به دیتابیس"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                INSERT OR IGNORE INTO USERS 
                VALUES (?,?,?,?,?,?,?)
            ''', (name, username, user_id, False, 0, status, False))
            return True
    except sqlite3.Error as e:
        print(f"خطا در ثبت کاربر: {str(e)}")
        return False

# ---------------------- توابع تغییر وضعیت کاربر ----------------------
def user_rejoined(user_id: int, chat_id: Union[str, int]) -> bool:
    """بازنشانی وضعیت کاربر هنگام پیوستن مجدد"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET status = 'member', is_admin = 0 
                WHERE num_id = ?
            ''', (user_id,))
            return True
    except sqlite3.Error as e:
        print(f"خطا در بازنشانی وضعیت: {str(e)}")
        return False

def verify_user(chat_id: Union[str, int], user_id: int) -> bool:
    """تأیید هویت کاربر"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET is_verified = 1 
                WHERE num_id = ?
            ''', (user_id,))
            return True
    except sqlite3.Error as e:
        print(f"خطا در تأیید کاربر: {str(e)}")
        return False

# ---------------------- توابع مدیریت اخطارها ----------------------
def add_warns(chat_id: Union[str, int], user_id: int) -> bool:
    """افزودن اخطار به کاربر"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET warn = warn + 1 
                WHERE num_id = ?
            ''', (user_id,))
            return True
    except sqlite3.Error as e:
        print(f"خطا در افزودن اخطار: {str(e)}")
        return False

def del_warns(chat_id: Union[str, int], user_id: int) -> bool:
    """کاهش اخطارهای کاربر"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET warn = CASE WHEN warn > 0 THEN warn - 1 ELSE 0 END 
                WHERE num_id = ?
            ''', (user_id,))
            return True
    except sqlite3.Error as e:
        print(f"خطا در کاهش اخطار: {str(e)}")
        return False

# ---------------------- توابع بن/آنبن ----------------------
def ban_user(chat_id: Union[str, int], user_id: int) -> bool:
    """بن کردن کاربر"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET status = 'banned' 
                WHERE num_id = ?
            ''', (user_id,))
            return True
    except sqlite3.Error as e:
        print(f"خطا در بن کاربر: {str(e)}")
        return False

def un_ban(chat_id: Union[str, int], username: str) -> bool:
    """آنبن کردن کاربر"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET status = 'member' 
                WHERE username = ?
            ''', (username,))
            return cur.rowcount > 0
    except sqlite3.Error as e:
        print(f"خطا در آنبن: {str(e)}")
        return False

# ---------------------- توابع مدیریت ادمین‌ها ----------------------
def promote(chat_id: Union[str, int], user_id: int) -> bool:
    """ارتقا کاربر به ادمین"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET status = 'administrator', is_admin = 1 
                WHERE num_id = ?
            ''', (user_id,))
            return True
    except sqlite3.Error as e:
        print(f"خطا در ارتقا کاربر: {str(e)}")
        return False

def demote(chat_id: Union[str, int], user_id: int) -> bool:
    """تنزل کاربر از ادمین"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute('''
                UPDATE USERS 
                SET status = 'member', is_admin = 0 
                WHERE num_id = ?
            ''', (user_id,))
            return True
    except sqlite3.Error as e:
        print(f"خطا در تنزل کاربر: {str(e)}")
        return False

# ---------------------- توابع مدیریت تنظیمات ----------------------
def get_setting(chat_id: Union[str, int]) -> Optional[List[Tuple]]:
    """دریافت تنظیمات گروه"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM SETTING")
            return cur.fetchall()
    except sqlite3.Error as e:
        print(f"خطا در دریافت تنظیمات: {str(e)}")
        return None

def change_answer(chat_id: Union[str, int]) -> Optional[bool]:
    """تغییر وضعیت پاسخ‌دهی خودکار"""
    dbname = f"{chat_id}.db"
    try:
        with sqlite3.connect(f"databases/{dbname}") as con:
            cur = con.cursor()
            cur.execute("SELECT answer_why FROM SETTING")
            current = cur.fetchone()[0]
            new_value = not current
            cur.execute("UPDATE SETTING SET answer_why = ?", (new_value,))
            return new_value
    except sqlite3.Error as e:
        print(f"خطا در تغییر تنظیمات: {str(e)}")
        return None