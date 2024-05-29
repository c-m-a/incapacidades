from datetime import datetime
import random

def generate_series_with_date():
    current_date = datetime.now().strftime('%Y%m%d')
    random_number = random.randint(10000, 99999)
    return f"{current_date}{random_number}"

