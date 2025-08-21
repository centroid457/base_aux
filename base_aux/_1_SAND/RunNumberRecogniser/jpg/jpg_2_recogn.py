import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import re
from enum import Enum


class PreprocessingMethod(Enum):
    NONE = "none"
    MORPHOLOGICAL = "morphological"
    ADAPTIVE_THRESHOLD = "adaptive_threshold"
    CANNY_EDGES = "canny_edges"
    GAUSSIAN_BLUR = "gaussian_blur"
    HISTOGRAM_EQUALIZATION = "histogram_equalization"
    COMBINED = "combined"


# Настраиваемые параметры для поиска контуров
CONTOUR_PARAMS = {
    'min_area': 500,
    'max_area': 10000,
    'min_aspect_ratio': 1.5,
    'max_aspect_ratio': 5.0,
    'epsilon_factor': 0.02,
    'min_vertices': 4,
    'max_vertices': 6,
    'contour_color': (0, 255, 0),
    'rejected_color': (0, 0, 255),
}

# Параметры предобработки
PREPROCESS_PARAMS = {
    'morph_kernel_size': 3,
    'adaptive_block_size': 11,
    'adaptive_c': 2,
    'canny_low_threshold': 50,
    'canny_high_threshold': 150,
    'gaussian_kernel_size': 5,
    'gaussian_sigma': 1.0,
    'cliplimit': 2.0,
    'tile_grid_size': (8, 8)
}


def apply_preprocessing(image, method=PreprocessingMethod.MORPHOLOGICAL):
    """Применение различных методов предобработки"""
    if method == PreprocessingMethod.NONE:
        return image.copy()

    elif method == PreprocessingMethod.MORPHOLOGICAL:
        # Морфологические операции для улучшения текста
        kernel = np.ones((PREPROCESS_PARAMS['morph_kernel_size'],
                          PREPROCESS_PARAMS['morph_kernel_size']), np.uint8)
        processed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
        return processed

    elif method == PreprocessingMethod.ADAPTIVE_THRESHOLD:
        # Адаптивная бинаризация
        return cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, PREPROCESS_PARAMS['adaptive_block_size'],
            PREPROCESS_PARAMS['adaptive_c']
        )

    elif method == PreprocessingMethod.CANNY_EDGES:
        # Детектор краев Canny
        edges = cv2.Canny(image, PREPROCESS_PARAMS['canny_low_threshold'],
                          PREPROCESS_PARAMS['canny_high_threshold'])
        # Заполняем контуры
        kernel = np.ones((3, 3), np.uint8)
        return cv2.dilate(edges, kernel, iterations=1)

    elif method == PreprocessingMethod.GAUSSIAN_BLUR:
        # Размытие по Гауссу для уменьшения шума
        return cv2.GaussianBlur(
            image,
            (PREPROCESS_PARAMS['gaussian_kernel_size'],
             PREPROCESS_PARAMS['gaussian_kernel_size']),
            PREPROCESS_PARAMS['gaussian_sigma']
        )

    elif method == PreprocessingMethod.HISTOGRAM_EQUALIZATION:
        # Выравнивание гистограммы для улучшения контраста
        if len(image.shape) == 2:
            return cv2.equalizeHist(image)
        else:
            # Для цветных изображений
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    elif method == PreprocessingMethod.COMBINED:
        # Комбинированный метод
        # 1. Размытие для уменьшения шума
        blurred = cv2.GaussianBlur(image, (5, 5), 1.5)
        # 2. Адаптивная бинаризация
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        # 3. Морфологические операции
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
        return processed

    return image.copy()


def compare_preprocessing_methods(image_path, output_folder="preprocessing_comparison"):
    """Сравнение различных методов предобработки"""
    os.makedirs(output_folder, exist_ok=True)

    original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original is None:
        return

    results = {}

    for method in PreprocessingMethod:
        processed = apply_preprocessing(original, method)

        # Сохраняем результат
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, f"{method.value}_{filename}")
        cv2.imwrite(output_path, processed)

        # Считаем контуры для оценки эффективности
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        suitable_contours = []

        for contour in contours:
            epsilon = CONTOUR_PARAMS['epsilon_factor'] * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0
            vertices = len(approx)

            area_ok = CONTOUR_PARAMS['min_area'] <= area <= CONTOUR_PARAMS['max_area']
            aspect_ok = CONTOUR_PARAMS['min_aspect_ratio'] <= aspect_ratio <= CONTOUR_PARAMS['max_aspect_ratio']
            vertices_ok = CONTOUR_PARAMS['min_vertices'] <= vertices <= CONTOUR_PARAMS['max_vertices']

            if area_ok and aspect_ok and vertices_ok:
                suitable_contours.append(contour)

        results[method.value] = {
            'total_contours': len(contours),
            'suitable_contours': len(suitable_contours),
            'image': processed
        }

    return results


def find_best_preprocessing_method(image_path):
    """Автоматический подбор лучшего метода предобработки"""
    comparison = compare_preprocessing_methods(image_path)

    best_method = None
    best_score = -1

    for method, data in comparison.items():
        if data['suitable_contours'] > 0:
            # Оценка: количество подходящих контуров / общее количество контуров
            score = data['suitable_contours'] / max(1, data['total_contours'])
            if score > best_score:
                best_score = score
                best_method = method

    return best_method, comparison


def visualize_contours_with_preprocessing(image_path, method=PreprocessingMethod.MORPHOLOGICAL,
                                          output_folder="visualized_results"):
    """Визуализация контуров с предобработкой"""
    os.makedirs(output_folder, exist_ok=True)

    # Загрузка и предобработка
    original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original is None:
        return None, None

    processed = apply_preprocessing(original, method)

    # Создаем цветную копию для визуализации
    color_original = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    color_processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

    # Поиск контуров на обработанном изображении
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    suitable_contours = []
    rejected_contours = []

    for i, contour in enumerate(contours):
        epsilon = CONTOUR_PARAMS['epsilon_factor'] * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h if h > 0 else 0
        vertices = len(approx)

        area_ok = CONTOUR_PARAMS['min_area'] <= area <= CONTOUR_PARAMS['max_area']
        aspect_ok = CONTOUR_PARAMS['min_aspect_ratio'] <= aspect_ratio <= CONTOUR_PARAMS['max_aspect_ratio']
        vertices_ok = CONTOUR_PARAMS['min_vertices'] <= vertices <= CONTOUR_PARAMS['max_vertices']

        is_suitable = area_ok and aspect_ok and vertices_ok

        if is_suitable:
            suitable_contours.append(contour)
            cv2.drawContours(color_processed, [contour], -1, CONTOUR_PARAMS['contour_color'], 2)
            cv2.drawContours(color_original, [contour], -1, CONTOUR_PARAMS['contour_color'], 2)
            cv2.putText(color_processed, f"A:{area:.0f}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, CONTOUR_PARAMS['contour_color'], 1)
        else:
            rejected_contours.append(contour)
            cv2.drawContours(color_processed, [contour], -1, CONTOUR_PARAMS['rejected_color'], 1)

    # Сохраняем результаты
    filename = os.path.basename(image_path)
    original_output = os.path.join(output_folder, f"original_{filename}")
    processed_output = os.path.join(output_folder, f"processed_{method.value}_{filename}")

    cv2.imwrite(original_output, color_original)
    cv2.imwrite(processed_output, color_processed)

    print(f"Метод: {method.value}")
    print(f"  Всего контуров: {len(contours)}")
    print(f"  Подходящих: {len(suitable_contours)}")
    print(f"  Отклоненных: {len(rejected_contours)}")

    return suitable_contours, processed


def process_with_optimal_preprocessing(image_path):
    """Обработка с автоматическим выбором лучшего метода предобработки"""
    print(f"\nПоиск оптимального метода предобработки для: {os.path.basename(image_path)}")

    best_method, comparison = find_best_preprocessing_method(image_path)

    if best_method:
        print(f"Лучший метод: {best_method}")

        # Применяем лучший метод
        method_enum = PreprocessingMethod(best_method)
        suitable_contours, processed_img = visualize_contours_with_preprocessing(
            image_path, method_enum
        )

        if suitable_contours:
            # Распознаем числа с найденных областей
            all_numbers = []
            img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            for contour in suitable_contours:
                x, y, w, h = cv2.boundingRect(contour)
                roi = img_gray[y:y + h, x:x + w]

                # Дополнительная обработка ROI для лучшего распознавания
                roi_processed = apply_preprocessing(roi, PreprocessingMethod.MORPHOLOGICAL)
                numbers = recognize_numbers_from_plate(roi_processed)

                if numbers:
                    all_numbers.extend(numbers)

            return all_numbers, processed_img, best_method

    print("Не удалось найти подходящий метод предобработки")
    return None, None, None


def recognize_numbers_from_plate(plate_image):
    """Распознавание чисел с таблички"""
    # Улучшаем изображение для OCR
    enhanced = cv2.convertScaleAbs(plate_image, alpha=1.5, beta=0)

    # Преобразуем в PIL Image
    pil_img = Image.fromarray(enhanced)

    # Пробуем разные конфигурации Tesseract
    configs = [
        r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789',
        r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789',
        r'--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789'  # Для выровненного текста
    ]

    all_numbers = []
    for config in configs:
        text = pytesseract.image_to_string(pil_img, config=config)
        numbers = re.findall(r'\d{3,5}', text)
        all_numbers.extend(numbers)

    # Убираем дубликаты
    return list(set(all_numbers))


def batch_process_with_preprocessing(folder_path="JPGS"):
    """Пакетная обработка всех изображений с предобработкой"""
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не существует!")
        return {}

    jpg_files = [f for f in os.listdir(folder_path)
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    results = {}
    methods_used = {}

    for filename in jpg_files:
        image_path = os.path.join(folder_path, filename)
        print(f"\nОбработка: {filename}")

        numbers, processed_img, method = process_with_optimal_preprocessing(image_path)

        if numbers:
            results[filename] = numbers
            methods_used[filename] = method
            print(f"  Распознанные номера: {numbers}")
        else:
            print("  Номера не найдены")

    # Статистика использования методов
    print("\nСтатистика методов предобработки:")
    method_counts = {}
    for method in methods_used.values():
        method_counts[method] = method_counts.get(method, 0) + 1

    for method, count in method_counts.items():
        print(f"  {method}: {count} изображений")

    return results


def update_preprocess_params(new_params):
    """Обновление параметров предобработки"""
    global PREPROCESS_PARAMS
    PREPROCESS_PARAMS.update(new_params)
    print("Параметры предобработки обновлены:")


def main():
    # Проверяем наличие Tesseract
    try:
        pytesseract.get_tesseract_version()
    except:
        print("Tesseract не установлен или не найден в PATH")
        return

    # Настраиваем параметры предобработки
    custom_preprocess_params = {
        'morph_kernel_size': 3,
        'adaptive_block_size': 15,  # Больший размер блока для крупного текста
        'adaptive_c': 3,
        'canny_low_threshold': 30,  # Более чувствительный детектор краев
        'canny_high_threshold': 100,
    }
    update_preprocess_params(custom_preprocess_params)

    print("Доступные методы предобработки:")
    for method in PreprocessingMethod:
        print(f"  - {method.value}")

    print("\nНачинаем обработку с автоматическим подбором предобработки...")
    results = batch_process_with_preprocessing("JPGS")

    print("\n" + "=" * 60)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 60)

    if results:
        for filename, numbers in results.items():
            print(f"{filename}: {numbers}")
    else:
        print("Не удалось распознать номера ни на одном изображении")


if __name__ == "__main__":
    main()