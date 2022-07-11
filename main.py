from statistics import harmonic_mean
from tools_oop import HamrobazarScraper
import pandas as pd
import winsound
import time

# main URL:
hamrobazar_url = "https://hamrobazaar.com/category/hb-select/00000000-0000-0000-0000-000000000000"

# Track the timer:
start_time = time.time()
time_interval = 0


category_name = HamrobazarScraper(hamrobazar_url).category_name()
print(f"Category | {category_name}\n-----------")
hamrobazar = HamrobazarScraper(hamrobazar_url).hamrobazar_automation()
print(hamrobazar[0])

d = {'Names': hamrobazar[0], "Prices": hamrobazar[1], "Links": hamrobazar[-1]}
df = pd.DataFrame(data=d)
df.to_json(f"{category_name}.json", indent=4)
df.to_excel(f"{category_name}.xlsx", index=False)

# Play the sound after the completion of Scraping process:
winsound.PlaySound('notification.mp3', winsound.SND_FILENAME)

time_took = time.time() - start_time
time_in_seconds = round(time_took, 2)
time_in_minutes = round(time_in_seconds/60, 2)
print(f'Took {time_in_seconds} seconds.....')
print(f"Took {time_in_minutes} minutes.....")