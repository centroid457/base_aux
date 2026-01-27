import cv2
import numpy as np
import requests


class NumberRecognizer:
    def __init__(self):
        # Убедитесь, что tesseract установлен и путь указан правильно
        # Для Windows раскомментируйте следующую строку:
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def download_image(self, url, save_path='downloaded_image.jpg'):
        """Скачивание изображения по URL"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Изображение сохранено как: {save_path}")
            return save_path
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
            return None

    def preprocess_image(self, image_path):
        """Предварительная обработка изображения для улучшения распознавания"""
        # Чтение изображения
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Не удалось загрузить изображение")

        # Сохранение оригинала
        original = image.copy()

        # Увеличение разрешения для лучшего распознавания
        scale_factor = 1.5
        height, width = image.shape[:2]
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = cv2.resize(image, (new_width, new_height))

        # Конвертация в grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Уменьшение шума с сохранением краев
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)

        # Адаптивная бинаризация для лучшей работы с неравномерным освещением
        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)

        # Морфологические операции для улучшения текста
        kernel = np.ones((2, 2), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)

        # Сохранение обработанного изображения
        processed_path = 'processed_image.jpg'
        cv2.imwrite(processed_path, processed)

        return original, processed, processed_path

    def process_from_url(self, url):
        """Обработка изображения по URL"""
        try:
            print("Скачиваем изображение...")
            image_path = self.download_image(url)
            if not image_path:
                return []

            print("Обрабатываем изображение...")
            results = self.preprocess_image(image_path)

        except Exception as e:
            print(f"Ошибка в process_from_url: {e}")
            return []


# Пример использования
if __name__ == "__main__":
    # URL изображения с наклоненными номерами
    image_url = "https://i.wfolio.ru/x/Sjpgrm2v20FR6Cth5viRk6Iir5aoqG4h/ZXWGJmu7EQlhnv6D9ELHSMzGOBuFicXp/OGcM34slpvmXTMkbuJagSV1xA4akZdWt/iGTrK_jx2PJdzPpMyVlbGIyR5mAu9UqG/rL-5DUxboiaoOuXyk54XGSc-uy8S4Sid/ndneNsQofN7rDZnJco7E6fIxw7sSkYkK/csDLbsHb1NacHh-TmPWQCsK_M_qdis5a/Z3y8t2bA3Damy0c6yD052k4z03m0hLgz/Nqb6796vYVZ1KQWCTdMQmBv8wmCGA5DQ/Uwp1ENeCBM74hSimeJqecEhkjF-D-Fdd/zzYuadnEVUCDlhtBvPzmwP7RXaIUCWu-/vmwGbl6hv7-xaZ1eSlzn9NPc6g97sukQ/TOQ_ZSYCOXx2jgExAOzL1f2lkHR5AKPC/2t893A2ZuEelsIucVIZdER35DxTBRrpP/y5GSp60oWAF82L0F3ZQCjahGo9bn6jAW/H8coUN5kqFAQESOJpExCmpL1HubnL-ou/mHM2a4OMgMzh36HhvGyH96oqilNVyDjW/dI3iu3g-3og.jpg"
    # Создание экземпляра распознавателя
    recognizer = NumberRecognizer()

    # Обработка изображения
    # print("Начинаем обработку изображения...")
    # detected_numbers = recognizer.process_from_url(image_url)
    #
    # print(f"\nРезультаты распознавания: {detected_numbers}")

    recognizer.preprocess_image("4.jpg")