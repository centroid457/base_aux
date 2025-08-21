from playwright.sync_api import sync_playwright
import re
from urllib.parse import urljoin


def get_jpg_links_sync():
    url = "https://potashov-photo.ru/disk/sadovoe-kolco"
    jpg_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print(f"Открываем страницу: {url}")
            page.goto(url, wait_until='networkidle')
            page.wait_for_timeout(3000)

            html_content = page.content()

            jpg_pattern = r'href=["\']([^"\']*\.jpg)["\']'
            found_links = re.findall(jpg_pattern, html_content, re.IGNORECASE)

            for link in found_links:
                absolute_link = urljoin(url, link)
                jpg_links.append(absolute_link)

            jpg_links = list(set(jpg_links))

            print(f"\nНайдено {len(jpg_links)} ссылок на JPG файлы:")
            for i, link in enumerate(jpg_links, 1):
                print(f"{i}. {link}")

            with open('jpg_links.txt', 'w', encoding='utf-8') as f:
                for link in jpg_links:
                    f.write(link + '\n')

            print(f"\nСписок ссылок сохранен в файл 'jpg_links.txt'")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        finally:
            browser.close()

    return jpg_links


if __name__ == "__main__":
    links = get_jpg_links_sync()