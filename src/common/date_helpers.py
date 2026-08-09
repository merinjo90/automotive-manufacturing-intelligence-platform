from datetime import date, timedelta
import random

def generate_random_date(start_date,max_days_offset):
    offset = random.randint(0, max_days_offset)
    return start_date+timedelta(days=offset)