import requests
import xml.etree.ElementTree as ET
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ==========================
# НАЛАШТУВАННЯ
# ==========================

SHEET_ID = "1ulL_H1YBezBijlUw8LPCe-2Bl9ay3imao_RPKfeQDMA"
XML_URL = "https://raw.githubusercontent.com/vitbadeychyk/xml-processor/refs/heads/main/products.xml"


# ==========================
# ПІДКЛЮЧЕННЯ ДО GOOGLE
# ==========================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", scope
)
client = gspread.authorize(creds)

sheet = client.open_by_key(SHEET_ID).sheet1

print("✅ Підключено до Google Таблиці")

# ==========================
# ЧИТАЄМО XML
# ==========================

response = requests.get(XML_URL)
root = ET.fromstring(response.content)

xml_products = {}

for offer in root.findall(".//offer"):
    sku = offer.get("id")
    quantity = offer.findtext("quantity_in_stock", default="0")

    if sku:
        xml_products[sku.strip()] = int(quantity)

print(f"✅ Знайдено {len(xml_products)} товарів у XML")

# ==========================
# ОНОВЛЕННЯ ТАБЛИЦІ
# ==========================

data = sheet.get_all_records()
headers = sheet.row_values(1)  # отримуємо назви колонок

# шукаємо індекси потрібних колонок
col_sku = headers.index("Артикул")
col_stock = headers.index("Залишки")
col_status = headers.index("Наявність")

all_values = sheet.get_all_values()

for i, row in enumerate(data):
    sku_sheet = str(row["Артикул"]).strip()
    row_index = i + 1  # бо перший рядок заголовок

    if sku_sheet in xml_products:
        quantity = xml_products[sku_sheet]
        availability = "В наявності" if quantity > 0 else "Не в наявності"
    else:
        quantity = 0
        availability = "Не в наявності"

    all_values[row_index][col_stock] = str(quantity)
    all_values[row_index][col_status] = availability

print("🔄 Масове оновлення правильних колонок...")

sheet.update("A1", all_values)

print("🎉 Синхронізація завершена правильно!")