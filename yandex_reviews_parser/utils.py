import time
import shutil
import undetected_chromedriver as uc
from yandex_reviews_parser.parsers import Parser


class YandexParser:
    def __init__(self, id_yandex: int):
        """
        @param id_yandex: ID Яндекс компании
        """
        self.id_yandex = id_yandex

    def __open_page(self):
        url = f'https://yandex.ru/maps/org/{self.id_yandex}/reviews/'

        opts = uc.ChromeOptions()

        chrome_path = shutil.which("google-chrome") or shutil.which("chrome")
        if chrome_path:
            opts.binary_location = chrome_path
        else:
            raise RuntimeError("Google Chrome binary not found!")

        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')

        driver_path = shutil.which("chromedriver")
        if not driver_path:
            raise RuntimeError("ChromeDriver not found!")

        driver = uc.Chrome(options=opts, driver_executable_path=driver_path)

        driver.get(url)
        parser = Parser(driver)
        return parser

    def parse(self, type_parse: str = 'default') -> dict:
        """
        Функция получения данных в виде
        @param type_parse: Тип данных, принимает значения:
            default - получает все данные по аккаунту
            company - получает данные по компании
            reviews - получает данные по отчетам
        @return: Данные по запрошенному типу
        """
        result:dict = {}
        page = self.__open_page()
        time.sleep(4)
        try:
            if type_parse == 'default':
                result = page.parse_all_data()
            if type_parse == 'company':
                result = page.parse_company_info()
            if type_parse == 'reviews':
                result = page.parse_reviews()
        except Exception as e:
            print(e)
            return result
        finally:
            page.driver.close()
            page.driver.quit()
            return result
