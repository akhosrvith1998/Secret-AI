from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.subscription import is_subscription_active, charge_command_handler

app = Client(
    "bot",
)

admin = 7824772776

# -------- سیستم بررسی اشتراک --------
@app.on_message(filters.group)
async def check_subscription(client, message: Message):
    if not is_subscription_active():
        await message.reply("⚠️ ربات غیرفعال است! برای شارژ با صاحب ربات تماس بگیرید.")
        return
    message.continue_propagation()

# -------- دستور شارژ (فقط برای مالک) --------
@app.on_message(filters.command("شارژ") & filters.user(int("7824772776")) & filters.group)
async def handle_charge(client, message: Message):
    response = charge_command_handler(message)
    await message.reply(response)

# -------- دستور استارت (بدون تغییر) --------
@app.on_message(filters.command("start") & filters.user(admin) & filters.group)
async def start(client, message: Message):
    await message.reply_text("""
    سلام، ربات با موفقیت نصب شد.
    برای دیدن دستور های ربات /help را بفرستید.
    
    Secret AI
    """)
    await app.send_message("258564057", "ربات توسط کاربر @" + str(message.from_user.username) + " فعال شد.")

# -------- دستور کمک (آپدیت شده) --------
@app.on_message(filters.command("help"))
async def help_menu(c, m: Message):
    await m.reply_text("""
    🛠️ دستورات ربات:
    
    • حذف پیام ها: 
      /del [تعداد] یا 'حذف [تعداد]'
    
    • اخطار به کاربر: 
      ریپلای + ارسال 'اخطار' یا /warn
    
    • حذف اخطار: 
      ریپلای + ارسال 'حذف اخطار'
    
    • اسپم: 
      /spam [تعداد] [متن] (حداکثر ۲۰ پیام)
    
    • شارژ ربات: 
      'شارژ [عدد]' (فقط برای صاحب ربات)
    """)

# -------- اجرای ربات --------
app.run()