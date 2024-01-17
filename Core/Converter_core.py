from natsort import natsorted
from PIL import Image
import os
import shutil


def get_folder_paths(batch_mode_enabled, given_input_folder, given_output_folder):
    """Получает пути ко всем входным и выходным папкам."""
    folder_paths = []
    given_input_folder = os.path.abspath(given_input_folder)
    given_output_folder = os.path.abspath(given_output_folder)
    if batch_mode_enabled == False:
        folder_paths.append((given_input_folder, given_output_folder))
    else:
        # Возвращает абсолютные пути к папкам в пределах заданного пути
        for fileName in os.listdir(given_input_folder):
            filePath = os.path.join(given_input_folder, fileName)
            if os.path.isdir(filePath):
                folder_paths.append((filePath, os.path.join(given_output_folder, fileName + " [Переконвертировано]")))
    return folder_paths


def load_images(foldername):
    """Загружает все изображения из папки в объекты изображений"""
    images = []
    if (foldername == ""):
        return images
    folder = os.path.abspath(str(foldername))
    files = natsorted(os.listdir(folder))
    if len(files) == 0:
        return images
    for imgFile in files:
        if imgFile.lower().endswith(('.png', '.webp', '.jpg', '.jpeg', '.jfif', '.bmp', '.tiff', '.tga')):
            imgPath = os.path.join(folder, imgFile)
            image = Image.open(imgPath)
            images.append(image)
    return images


def convert_psd_to_png(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img.save(output_path, format='PNG')
    except Exception as e:
        return ("Произошла ошибка:", str(e))


def convert_all_psd_to_png(input_folder, output_folder, save_originals=True):
    new_folder = str(output_folder)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    try:
        lisin = []
        lisout = []
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                input_path = os.path.join(root, file)
                output_path = None
                # Является ли файл псд
                if input_path.lower().endswith('.psd'):
                    # Если указан выходной путь:
                    if output_folder:
                        output_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".png")
                    else:
                        # Если выходной путь не указан, выходной путь будет в той же папке
                        output_path = os.path.join(root, os.path.splitext(file)[0] + ".png")
                    lisin.append(input_path)
                    lisout.append(output_path)

                    # Удаляем исходный файл изображения
                    if not save_originals:
                        os.remove(input_path)
                else:
                    # Если это не изображение, просто копируем в выходную папку
                    shutil.copy(input_path, os.path.join(output_folder, file))

                    # Удаляем исходный файл
                    if not save_originals:
                        os.remove(input_path)

        retlis = [lisin, lisout]
        return retlis
    except Exception as e:
        return ("Произошла ошибка:", str(e))


def convert_png_to_gif(input_folder, output_folder, save_originals=True):
    new_folder = str(output_folder) + "[GIF]"
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    try:
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                input_path = os.path.join(root, file)
                output_path = None
                if file.lower().endswith(('.png', '.bmp', '.jpeg', '.jpg')):
                    if new_folder:
                        output_path = os.path.join(new_folder, os.path.splitext(file)[0] + ".gif")
                    else:
                        output_path = os.path.join(root, os.path.splitext(file)[0] + ".gif")

                    img = Image.open(input_path)

                    if not os.path.exists(output_path):
                        img.save(output_path, "JPEG", quality=60)

                else:
                    # Если это не изображение, просто копируем в выходную папку
                    shutil.copy(input_path, os.path.join(output_folder, file))

                    # Удаляем исходный файл
                    if not save_originals:
                        os.remove(input_path)

    except Exception as e:
        return ("Произошла ошибка:", str(e))
