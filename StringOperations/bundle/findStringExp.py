import os
import re

def find_strings_in_java_files(directory):
    unique_strings = set()

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".java"):
                file_path = os.path.join(root, file_name)
                file_strings = extract_strings_from_file(file_path)
                unique_strings.update(file_strings)

    with open("output_strings.txt", "w", encoding="utf-8") as output_file:
        for string_expression in unique_strings:
            output_file.write(string_expression + "\n")

def is_valid_string(string):
    # Filtreleri uygula
    invalid_keywords = ["IS NULL", "OR ", "T_", "V_", "LEFT", "CASE", "TO_STRING", "GUNLE", "CURRENCY", "FIELD", "LABEL", "FORMATTED", "TO_CHAR", "AND", "##", "BOX", "PIE", "SELECT", "ORDER BY", "JASPER", "PANE", "BLS", "GNL", "TR.", "FROM", "WHERE", "A."]
    invalid_start_keywords = ["GET", "SET", " - "]
    
    return (
        bool(string) and 
        len(string) > 2 and  # Tek karakter ve iki karakteri kontrol et
        not string[0].isdigit() and 
        not any(keyword.upper() in string.upper() for keyword in invalid_keywords) and
        not any(string.upper().startswith(keyword.upper()) for keyword in invalid_start_keywords) and
        not string.isupper()  # Büyük harf içermemeli
    )


def is_valid_line(line):
    # Full Line için filtre uygula
    invalid_line_keywords = ["FILE", "CONTENT", ".SETVALUEOFCUSTOMFIELD", ".GETVALUEOFCUSTOMFIELD", "PRIVATE", "PUBLIC", "COMBOBOX", "PARAMKOD", "SYSTEM.OUT", ".SETRAPOR", "SETTABLO"]
    return not any(keyword.upper() in line.upper() for keyword in invalid_line_keywords)

def extract_strings_from_file(file_path):
    file_strings = set()
    with open(file_path, "r", encoding="cp1254", errors="ignore") as java_file:
        lines = java_file.readlines()
        for line in lines:
            strings = re.findall(r'"(.*?)"', line)
            if strings:
                for string in strings:
                    if is_valid_string(string) and is_valid_line(line):
                        file_strings.add(string)
    return file_strings

# Kullanım örneği:
java_project_directory = "C:/JAVAKAYNAK/workspaceTekJ8/ErpGUI"
find_strings_in_java_files(java_project_directory)
