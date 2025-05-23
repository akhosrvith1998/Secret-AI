import json
import requests
import datetime
import pytz
import logging
from enum import Enum
from typing import Optional, Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# تنظیمات هندلر برای لاگ‌ها
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class AzanType(Enum):
    MAGHRIB = 'Maghrib'

def get_azan(city: str, timestamp: Optional[int] = None) -> Tuple[Optional[str], Optional[str], Optional[int]]:
    """
    دریافت زمان اذان مغرب از API
    """
    endpoint = "http://api.aladhan.com/v1/timingsByAddress"
    params = {"address": city, "method": 7}
    
    try:
        if timestamp:
            endpoint += f"/{timestamp}"
        
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()['data']
        azan_time = data['timings'][AzanType.MAGHRIB.value]
        timezone = data['meta']['timezone']
        timestamp = int(data['date']['timestamp'])
        
        return azan_time + ":00", timezone, timestamp
    
    except requests.exceptions.RequestException as e:
        logger.error(f"خطا در ارتباط با API: {str(e)}")
    except KeyError as e:
        logger.error(f"فرمت پاسخ API نامعتبر: {str(e)}")
    except Exception as e:
        logger.error(f"خطای ناشناخته: {str(e)}")
    
    return None, None, None

def get_current_time(timezone: str) -> str:
    """
    دریافت زمان فعلی بر اساس منطقه زمانی
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.datetime.now(tz)
        return now.strftime("%H:%M:%S")
    except pytz.UnknownTimeZoneError:
        logger.error(f"منطقه زمانی ناشناخته: {timezone}")
        return datetime.datetime.now().strftime("%H:%M:%S")

def calculate_time_delta(current: str, target: str) -> Tuple[int, int, int]:
    """
    محاسبه تفاوت زمانی بین دو زمان
    """
    c_h, c_m, c_s = map(int, current.split(":"))
    t_h, t_m, t_s = map(int, target.split(":")))

    total_seconds = (t_h * 3600 + t_m * 60 + t_s) - (c_h * 3600 + c_m * 60 + c_s)
    
    if total_seconds < 0:
        total_seconds += 86400  # افزودن 24 ساعت اگر زمان هدف گذشته باشد

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return hours, minutes, seconds

def get_remaining_time(city: str = "Tehran") -> Optional[Tuple[int, int, int]]:
    """
    محاسبه زمان باقیمانده تا اذان مغرب
    """
    azan_time, timezone, _ = get_azan(city)
    if not azan_time:
        return None

    current_time = get_current_time(timezone)
    return calculate_time_delta(current_time, azan_time)

if __name__ == "__main__":
    # تست عملکرد
    ch.setLevel(logging.DEBUG)
    remaining = get_remaining_time("تهران")
    
    if remaining:
        h, m, s = remaining
        print(f"⏳ زمان باقیمانده تا اذان مغرب: {h} ساعت و {m} دقیقه و {s} ثانیه")
    else:
        print("❌ خطا در دریافت اطلاعات اذان")