import os
import shutil

file_exten = {
    "images": [],
    "documents": [],
    "audio": [],
    "video": [],
    "archives": [],
    "other": []
}


def clean(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file in files:
            continue
        elif os.path.isfile(file_path):
            sort_files(folder, file)
        elif file != file_exten.keys():
            subfolder = os.path.join(folder, file)
            clean(subfolder)
    for file in os.listdir(folder):
        if file in files:
            continue
        else:
            del_folder = os.path.join(folder, file)
            shutil.rmtree(del_folder)
    return


def sort_files(folder, file):
    images_path = os.path.join(folder, 'images')
    documents_path = os.path.join(folder, 'documents')
    audio_path = os.path.join(folder, 'audio')
    video_path = os.path.join(folder, 'video')
    archives_path = os.path.join(folder, 'archives')
    other_path = os.path.join(folder, 'other')
    new_name_file = normalize(file)
    old_file_path = os.path.join(folder, file)
    new_file_path = os.path.join(folder, new_name_file)
    os.rename(old_file_path, new_file_path)
    file = new_name_file
    if file.endswith(file_images):
        file_exten["images"].append(file)
        if not os.path.exists(images_path):
            os.makedirs(images_path)
        new_file = os.path.join(folder, file)
        new_location = shutil.move(new_file, images_path)
    elif file.endswith(file_documents):
        file_exten["documents"].append(file)
        if not os.path.exists(documents_path):
            os.makedirs(documents_path)
        new_file = os.path.join(folder, file)
        new_location = shutil.move(new_file, documents_path)
    elif file.endswith(file_video):
        file_exten["video"].append(file)
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        new_file = os.path.join(folder, file)
        new_location = shutil.move(new_file, video_path)
    elif file.endswith(file_audio):
        file_exten["audio"].append(file)
        if not os.path.exists(audio_path):
            os.makedirs(audio_path)
        new_file = os.path.join(folder, file)
        new_location = shutil.move(new_file, audio_path)
    elif file.endswith(file_archives):
        file_exten["archives"].append(file)
        if not os.path.exists(archives_path):
            os.makedirs(archives_path)
        new_file = os.path.join(folder, file)
        new_location = shutil.move(new_file, archives_path)
        new_file = os.path.join(archives_path, file)
        archiv_folder = file.split('.')
        new_file_archiv = os.path.join(archives_path, archiv_folder[0])
        os.mkdir(new_file_archiv)
        shutil.unpack_archive(new_file, new_file_archiv)
        os.remove(new_file)
    else:
        file_exten["other"].append(file)
        if not os.path.exists(other_path):
            os.makedirs(other_path)
        new_file = os.path.join(folder, file)
        new_location = shutil.move(new_file, other_path)


def normalize(name_file):
    word = name_file.split('.')
    norm_name = ""
    for key in translit:
        word[0] = word[0].replace(key, translit[key])
    for i in word[0]:
        if not i.isdigit() and not i.isalpha():
            norm_name = norm_name + "_"
        else:
            norm_name = norm_name + i
    norm_name = norm_name + '.' + word[1]
    return norm_name


translit = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
            'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
            'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
            'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
            'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
            'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
            'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
            'Ю': 'U', 'Я': 'YA', '.': '.'}

files = ("images", "video", "documents", "audio", "archives", "other")
file_images = ('.jpeg', '.png', '.jpg', '.svg')
file_video = ('.avi', '.mp4', '.mov', '.mkv')
file_documents = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
file_audio = ('.mp3', '.ogg', '.wav', '.amr')
file_archives = ('.zip', '.gz', '.tar')

print(file_exten)
