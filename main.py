from statistics import harmonic_mean
from tools_oop import HamrobazarScraper
import pandas as pd
import winsound
import time

hamrobazar_url = "https://hamrobazaar.com/category/baby-childrens-accessories/d4225d8b-1faf-453c-aec3-66ca1c1e2602/05894fc1-ef2e-4788-8e20-9fd9f651b616"


category_name = HamrobazarScraper(hamrobazar_url).category_name()
print(f"Category | {category_name}\n-----------")
hamrobazar = HamrobazarScraper(hamrobazar_url).hamrobazar_automation()

d = {'Names': hamrobazar[0], "Prices": hamrobazar[1], "Links": hamrobazar[-1]}
df = pd.DataFrame(data=d)
df.to_json(f"{category_name}.json", indent=4)
df.to_excel(f"{category_name}.xlsx", index=False)