import pychrome
from bs4 import BeautifulSoup
import time

r = {}#RESI
##можете запустить этот файл чисто для теста как работает у вас данные либы


def parse_results(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    rows = table.find_all("tr")[1:]
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 3:
                subject = cells[1].get_text(strip=True)
                score = cells[2].get_text(strip=True)
                r[subject] = score
    return r


browser = pychrome.Browser(url="http://127.0.0.1:9222")
tab  = browser.list_tab()[0]

tab.start()
tab.call_method("Page.enable")
tab.call_method("Runtime.enable")

def reload_and_parse():
    loaded = False

    def on_load_fired(**kwargs):
        nonlocal loaded
        loaded = True

    tab.set_listener("Page.loadEventFired", on_load_fired)
    tab.call_method("Page.reload", ignoreCache=True)

    # Ждем полной загрузки страницы
    timeout = 30
    waited = 0
    while not loaded and waited < timeout:
        time.sleep(0.1)
        waited += 0.1

    if not loaded:
        print("Не дождались загрузки страницы")
        return

    # Ждем появления таблицы в DOM
    max_wait = 15
    waited = 0
    while waited < max_wait:
        has_table = tab.call_method(
            "Runtime.evaluate",
            expression="document.querySelector('table') !== null"
        )["result"]["value"]
        if has_table:
            break
        time.sleep(0.5)
        waited += 0.5
    else:
        print("Не появилась таблица")
        return

    # Получаем HTML и парсим
    result = tab.call_method(
        "Runtime.evaluate",
        expression="document.documentElement.outerHTML"
    )
    html = result["result"]["value"]
    return parse_results(html)

print(reload_and_parse())


