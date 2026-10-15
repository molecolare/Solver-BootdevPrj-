# test_get_files_info.py
from functions.get_files_info import get_files_info

def main():
    # Test case 1: Directory valida (successo)
    result1 = get_files_info("calculator", ".")
    print(result1)
    print()

    # Test case 2: Sottodirectory "pkg" (successo)
    result2 = get_files_info("calculator", "pkg")
    print(result2)
    print()

    # Test case 3: Directory fuori dai limiti (errore)
    result3 = get_files_info("calculator", "/bin")
    print(result3)
    print()

    # Test case 4: Directory con ".." (errore)
    result4 = get_files_info("calculator", "../")
    print(result4)

if __name__ == "__main__":
    main()
