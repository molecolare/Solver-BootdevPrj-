from functions.run_python_file import run_python_file

def test_run_python_file():
    print("Test 1: Esecuzione di un file Python con istruzioni di utilizzo")
    risultato = run_python_file("calculator", "main.py")
    print(risultato)
    print("-" * 80)

    print("Test 2: Esecuzione di un file Python con argomenti")
    risultato = run_python_file("calculator", "main.py", ["3 + 5"])
    print(risultato)
    print("-" * 80)

    print("Test 3: Esecuzione di un file Python per eseguire test")
    risultato = run_python_file("calculator", "tests.py")
    print(risultato)
    print("-" * 80)

    print("Test 4: file_path fuori dalla working_directory")
    risultato = run_python_file("calculator", "../main.py")
    print(risultato)
    print("-" * 80)

    print("Test 5: file_path inesistente")
    risultato = run_python_file("calculator", "nonexistent.py")
    print(risultato)
    print("-" * 80)

    print("Test 6: file_path non è un file Python")
    risultato = run_python_file("calculator", "lorem.txt")
    print(risultato)
    print("-" * 80)

if __name__ == "__main__":
    test_run_python_file()
