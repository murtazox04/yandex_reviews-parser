import shutil
import undetected_chromedriver as uc
from yandex_reviews_parser.parsers import Parser
from selenium.webdriver.support.ui import WebDriverWait


class YandexParser:
    def __init__(self, id_yandex: int):
        self.id_yandex = id_yandex

    def __open_page(self):
        url = f"https://yandex.uz/maps/org/{self.id_yandex}/reviews/"
        print(f"Opening URL: {url}")

        opts = uc.ChromeOptions()
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        # Disable headless while debugging
        # opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--lang=ru-RU")

        # ⚡ Add manual hack:
        opts.headless = False

        chrome_path = shutil.which("google-chrome") or shutil.which("chrome")
        if chrome_path:
            opts.binary_location = chrome_path
        else:
            raise RuntimeError("Google Chrome binary not found!")

        driver_path = shutil.which("chromedriver")
        if not driver_path:
            raise RuntimeError("ChromeDriver not found!")

        driver = uc.Chrome(options=opts, driver_executable_path=driver_path)

        driver.get(url)

        try:
            WebDriverWait(driver, 30).until(
                lambda d: "reviews" in d.current_url
                or "review" in d.page_source.lower()
            )
        except Exception:
            raise RuntimeError("Review page did not load properly!")

        parser = Parser(driver)
        return parser

    def parse(self, type_parse: str = "default") -> dict:
        result: dict = {}
        try:
            page = self.__open_page()
            if type_parse == "default":
                result = page.parse_all_data()
            elif type_parse == "company":
                result = page.parse_company_info()
            elif type_parse == "reviews":
                result = page.parse_reviews()
            else:
                raise ValueError(f"Unknown type_parse: {type_parse}")
        except Exception as e:
            print("[ERROR]", e)
            result = {"error": str(e)}
        finally:
            if "page" in locals():
                page.driver.quit()
        return result
