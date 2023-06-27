import argparse
import concurrent.futures
import logging
from pathlib import Path
from shutil import copyfile
from time import time


"""
--source [-s] 
--threads [-t] default folder = 1
--output [-o] default folder = dist

"""


parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--threads", "-t", help="Number of threads", default=1)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())
print(args)

source = Path(args.get("source"))
num_th = int(args.get("threads"))
output = Path(args.get("output"))

folders = [source]


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path) -> None:
    #logging.error(f'Got semaphore')
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            new_folder = output / ext
            try:
                new_folder.mkdir(parents=True, exist_ok=True)
                copyfile(el, new_folder / el.name)
            except OSError as err:
                logging.error(err)
    #logging.error(f'finished')


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    grabs_folder(source)
    timer = time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_th) as executor:
        results = list(executor.map(copy_file, folders))
    print(f'Done by {num_th} threads: {round(time() - timer, 4)}')
