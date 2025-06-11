from concurrent.futures import ThreadPoolExecutor  
from pathlib import Path   
from colorama import Fore
from tqdm import tqdm            
import argparse            
import logging       
import shutil        
import time


# run code:
# python sort_files.py ./data/file ./data/file_sort


# створення пакету, якщо відсутній, шлях до файлу
log_dir = Path('./logs')
log_dir.mkdir(parents=True, exist_ok=True)
log_file_path = log_dir / 'log.txt'

# налаштування логування
logging.basicConfig(
    level=logging.INFO,  # або DEBUG
    format="%(asctime)s | %(threadName)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
# logging.basicConfig(level=logging.INFO, format="%(threadName)s: %(message)s")


# копіює один файл із вихідної папки в цільову, сортуючи його за розширенням
def copy_file(file_path: Path, source_dir: Path, target_dir: Path):
    try:
        time.sleep(0.5)  # імітація "роботи" - щоб візуально побачити затримку

        relative_path = file_path.relative_to(source_dir) # знаходимо шлях до файлу
        ext = file_path.suffix.lower().lstrip('.')  # розширення маленькими літ., без крапки 
        if not ext:                 # пропускаємо, якщо файл без розширення 
            return
        destination = target_dir / ext    # шлях призначення -> ./data/file_sort -> /ext
        destination.mkdir(parents=True, exist_ok=True)    # створюємо новий пакет
        shutil.copy2(file_path, destination / file_path.name) # копіюємо туди файл

        logging.debug(f"Copied -> {file_path} copied to -> {destination / file_path.name}")
        # logging.info(f"{Fore.BLUE}Copied -> {Fore.RESET}{file_path}{Fore.BLUE} copied to -> {Fore.RESET}{destination / file_path.name}")
    except Exception as e:
        logging.error(f"Error copying {file_path}: {e}")


# обходимо всі файли, каталоги та підкаталоги — повертаємо тільки файли
def find_all_files(directory: Path) -> list[Path]:    
    return [p for p in directory.rglob('*') if p.is_file()] 


def main():
    # створюємо парсер для читання аргументів з командної строки
    parser = argparse.ArgumentParser(description="Sort files by extension using threads")
    parser.add_argument('source', type=str, help='Source directory')
    parser.add_argument('target', nargs='?', default='dist', help='Target directory (default: dist)')

    # перетворюємо строкові шляхи в об'єкти Path
    args = parser.parse_args()
    source_dir = Path(args.source)
    target_dir = Path(args.target)

    # знаходимо всі об'єкти:
    all_files = find_all_files(source_dir)
    logging.info(f"Files found and processed: {len(all_files)}")

    # створюємо багатопоточність, -> для наглядності до 4x потоків: max_workers=4
    with ThreadPoolExecutor(max_workers=4) as executor:
        # for file_path in all_files:
        # executor.submit(copy_file, file_path, source_dir, target_dir)
        list(tqdm(executor.map(lambda f: copy_file(f, source_dir, target_dir), all_files),
              total=len(all_files),
              ncols=150,
              desc=f"{Fore.BLUE}Copying files{Fore.RESET}"))        


if __name__ == '__main__':
    main()
