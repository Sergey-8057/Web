import os
import shutil
import sys

# Dict for Hometask
cust_dirs = {'изображения': ['JPEG', 'PNG', 'JPG', 'SVG'],
'видео файлы': ['AVI', 'MP4', 'MOV', 'MKV'],
'документы': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
'музыка': ['MP3', 'OGG', 'WAV', 'AMR'],
'архивы': ['ZIP', 'GZ', 'TAR'],
'неизвестные расширения': 'None'}

# Creation customs DIRs in accordance with HOMETASK guide
def create_custom_dirs(path):
	for cd in cust_dirs:
		if not os.path.exists(os.path.join(path, cd)):
			os.makedirs(os.path.join(path, cd))

# Normalization of the file name
def normalize(path, file):

	CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
	TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
	TRANS = {}
	result = ''
	for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
		TRANS[ord(c)] = l
		TRANS[ord(c.upper())] = l.upper()
	old_name = os.path.join(path, file)
	new_name = os.path.splitext(file)[0].translate(TRANS)
	for word in new_name:
		if word.lower() not in TRANSLATION and not word.isnumeric():
			result = result + '_'
		else:
			result = result + word
	result = result + os.path.splitext(file)[1]
	new_name = os.path.join(path, result)
	if not os.path.exists(new_name):
		os.rename(old_name, new_name)
	return result

# Function to replace the files and delete empty DIRs
def recurse(path):
	files = os.listdir(path)
	for file in files:
		if os.path.isfile(os.path.join(path,file)):
			file = normalize(path, file)
		file_path = os.path.join(path,file)
		if os.path.isfile(file_path):
			for key, value in cust_dirs.items():
				if os.path.splitext(file)[1].lstrip('.') in list(value) or os.path.splitext(file)[1].lstrip('.').upper() in list(value):
					moved_path = os.path.join(path, key)
					os.replace(file_path, os.path.join(moved_path, file))
					print(f'|{file}| replaced in |{key}| folder')
			if os.path.exists(file_path):
				moved_path = os.path.join(sys.argv[1], 'неизвестные расширения')
				os.replace(file_path, os.path.join(moved_path, file))
				print(f'|{file}| replaced in |неизвестные расширения| folder')
		# Condition to recurse the function for each internal Dirs
		elif os.path.isdir(file_path) and file not in cust_dirs.keys():
			recurse(file_path)
			# Condition for Deleting the empty folders
			if not os.listdir(file_path):
				os.rmdir(file_path)

# Function to unpack the archived files
def unpacking(path):
	arch_path = os.path.join(path, 'архивы')
	if os.path.exists(arch_path) and os.listdir(arch_path):
		for file in os.listdir(arch_path):
			if os.path.splitext(file)[1].lstrip('.') in cust_dirs['архивы'] or os.path.splitext(file)[1].lstrip('.').upper() in cust_dirs['архивы']:
				new_path = os.path.join(arch_path, os.path.splitext(file)[0])
				if not os.path.exists(new_path):
					os.makedirs(new_path)
					shutil.unpack_archive(os.path.join(arch_path, file), new_path)
					os.remove(os.path.join(arch_path, file))

def sorting_dir_files(path):
	create_custom_dirs(path)
	recurse(path)
	unpacking(path)
