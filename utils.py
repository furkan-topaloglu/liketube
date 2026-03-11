"""
Yardımcı fonksiyonlar
"""
import re
from datetime import datetime, timedelta

def parse_duration(duration_str):
    """
    ISO 8601 duration formatını saniyeye çevir
    Örnek: PT1H2M10S -> 3730 saniye
    """
    if not duration_str:
        return 0
    
    # PT1H2M10S formatı
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration_str)
    
    if not match:
        return 0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 3600 + minutes * 60 + seconds

def format_duration(seconds):
    """Saniyeyi okunabilir formata çevir"""
    if seconds < 60:
        return f"{seconds} sn"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes} dk {secs} sn" if secs > 0 else f"{minutes} dk"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if minutes == 0 and secs == 0:
            return f"{hours} sa"
        elif secs == 0:
            return f"{hours} sa {minutes} dk"
        else:
            return f"{hours} sa {minutes} dk {secs} sn"

def format_number(num):
    """Sayıyı okunabilir formata çevir (1.234.567)"""
    try:
        return f"{int(num):,}".replace(",", ".")
    except:
        return str(num)

