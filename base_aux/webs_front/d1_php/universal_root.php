<?php
/**
 * Добавляет к пути файла временную метку последнего изменения (для обхода кеша/cache_buster)
 * @param string $path Относительный путь к файлу (от корня сайта или относительно текущего файла)
 * @return string Путь с добавленным параметром ?v=timestamp
 * ПРИМЕНЕНИЕ
 * <link rel="stylesheet" href="<?= filepath_with_timestamp('css/style.css') ?>">
 */
function filepath_with_timestamp($path) {
    // Преобразуем относительный путь в абсолютный на сервере
    $realPath = $_SERVER['DOCUMENT_ROOT'] . '/' . ltrim($path, '/');
    $timestamp = file_exists($realPath) ? filemtime($realPath) : time();
    return $path . '?v=' . $timestamp;
}
?>