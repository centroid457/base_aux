import cv2
import numpy as np
import pytesseract
from PIL import Image
import requests
import os
import glob


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

    def find_number_plates(self, processed_image):
        """Поиск номерных пластин (белые области с черным текстом)"""
        # Используем само обработанное изображение для поиска контуров
        # Инвертируем изображение для поиска белых областей
        inverted = cv2.bitwise_not(processed_image)

        # Поиск контуров на инвертированном изображении
        contours, _ = cv2.findContours(inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Фильтрация контуров для поиска номерных пластин
        number_plates = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if 2000 < area < 50000:  # Подходящий размер для номера
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h

                # Номерные пластины обычно имеют прямоугольную формацию
                if 2.0 < aspect_ratio < 6.0:
                    # Проверяем, что это действительно белая область с текстом
                    roi = processed_image[y:y + h, x:x + w]
                    if roi.size > 0:
                        # Вычисляем соотношение белого/черного
                        white_pixels = np.sum(roi == 255)
                        black_pixels = np.sum(roi == 0)
                        total_pixels = white_pixels + black_pixels

                        if total_pixels > 0:
                            white_ratio = white_pixels / total_pixels
                            # Белая пластина должна иметь много белого фона
                            if white_ratio > 0.6:
                                number_plates.append((x, y, w, h))

        return number_plates

    def extract_roi_from_plate(self, original, plate_coords):
        """Извлечение ROI из координат номерной пластины"""
        x, y, w, h = plate_coords

        # Добавляем небольшие отступы
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(original.shape[1] - x, w + 2 * padding)
        h = min(original.shape[0] - y, h + 2 * padding)

        roi = original[y:y + h, x:x + w]
        return roi

    def enhance_number_contrast(self, roi):
        """Улучшение контраста номера"""
        if roi is None or roi.size == 0:
            return None

        # Конвертация в grayscale если нужно
        if len(roi.shape) == 3:
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        else:
            gray = roi

        # Увеличение контраста
        gray = cv2.convertScaleAbs(gray, alpha=1.8, beta=0)

        # Резкость
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        # Бинаризация
        _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binary

    def recognize_numbers(self, enhanced_roi):
        """Распознавание чисел с улучшенного ROI"""
        if enhanced_roi is None or enhanced_roi.size == 0:
            return None

        try:
            # Конвертация в PIL Image
            pil_image = Image.fromarray(enhanced_roi)

            # Пробуем разные настройки Tesseract
            configs = [
                r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789',
                r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789',
                r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
            ]

            for config in configs:
                try:
                    text = pytesseract.image_to_string(pil_image, config=config)
                    cleaned_text = ''.join(filter(str.isdigit, text))

                    if len(cleaned_text) >= 4:
                        # Берем первые 4-5 цифр
                        if len(cleaned_text) > 5:
                            cleaned_text = cleaned_text[:5]
                        return cleaned_text
                except:
                    continue

            return None

        except Exception as e:
            print(f"Ошибка при распознавании: {e}")
            return None

    def cleanup_temp_files(self):
        """Очистка всех временных файлов"""
        temp_patterns = [
            'downloaded_image.jpg',
            'processed_image.jpg',
            'plate_*.jpg',
            'enhanced_plate_*.jpg',
            'roi_*.jpg'
        ]

        for pattern in temp_patterns:
            for file_path in glob.glob(pattern):
                try:
                    os.remove(file_path)
                    print(f"Удален временный файл: {file_path}")
                except Exception as e:
                    print(f"Не удалось удалить файл {file_path}: {e}")

    def process_image(self, image_path):
        """Основной метод обработки изображения"""
        try:
            print("Начинаем предварительную обработку...")
            original, processed, processed_path = self.preprocess_image(image_path)

            print("Ищем номерные пластины...")
            number_plates = self.find_number_plates(processed)

            if not number_plates:
                print("Не найдено номерных пластин, пробуем альтернативный метод...")
                # Прямая обработка всего изображения
                enhanced = self.enhance_number_contrast(original)
                number = self.recognize_numbers(enhanced)
                if number:
                    return [number]
                return []

            print(f"Найдено {len(number_plates)} номерных пластин, распознаем...")
            results = []

            for i, plate_coords in enumerate(number_plates):
                # Извлекаем ROI
                roi = self.extract_roi_from_plate(original, plate_coords)

                if roi is not None and roi.size > 0:
                    # Сохраняем для отладки
                    cv2.imwrite(f'plate_{i}.jpg', roi)

                    # Улучшаем контраст
                    enhanced_roi = self.enhance_number_contrast(roi)

                    if enhanced_roi is not None:
                        # Сохраняем улучшенную версию
                        cv2.imwrite(f'enhanced_plate_{i}.jpg', enhanced_roi)

                        # Распознаем
                        number = self.recognize_numbers(enhanced_roi)
                        if number:
                            results.append(number)
                            print(f"Найден номер: {number} (пластина {i})")

            return list(set(results))  # Удаляем дубликаты

        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            import traceback
            traceback.print_exc()
            return []

    def process_from_url(self, url):
        """Обработка изображения по URL"""
        try:
            print("Скачиваем изображение...")
            image_path = self.download_image(url)
            if not image_path:
                return []

            print("Обрабатываем изображение...")
            results = self.process_image(image_path)

            print("Очищаем временные файлы...")
            # self.cleanup_temp_files()

            return results
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
    print("Начинаем обработку изображения...")
    detected_numbers = recognizer.process_from_url(image_url)

    print(f"\nРезультаты распознавания: {detected_numbers}")