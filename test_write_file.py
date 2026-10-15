# test_write_file.py
from functions.get_files_info import write_file

def main():
    # Test case 1: Scrittura di un file nella directory corrente
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result1)
    print()

    # Test case 2: Scrittura di un file in una sottodirectory
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result2)
    print()

    # Test case 3: Scrittura di un file fuori dalla working_directory (errore)
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result3)

if __name__ == "__main__":
    main()
