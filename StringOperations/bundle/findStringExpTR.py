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

    with open("output_stringsTR.txt", "w", encoding="utf-8") as output_file:
        for string_expression in unique_strings:
            transformed_string = transform_string(string_expression)
            output_file.write(transformed_string + "=\n")

def is_valid_string(string):
    # Filtreleri uygula
    invalid_keywords = ["JPG","   ","',","(",")","%","=","ZIP","XML","YYYY","ENCODE","HTTP","XMLN","PNG","+","STRING","GIF","THEN","ADMIN","TSL","FORMAT",">","<","WHEN","IS NULL", "OR ", "T_", "V_", "LEFT", "CASE", "TO_STRING", "GUNLE", "CURRENCY", "FIELD", "LABEL", "FORMATTED", "TO_CHAR", "AND", "##", "BOX", "PIE", "SELECT", "ORDER BY", "JASPER", "PANE", "BLS", "GNL", "TR.", "FROM", "WHERE", "A."]
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
    invalid_line_keywords = ["ATTRIBUTE","CONTAINS","FILE","CONTENT",".SETVALUEOFCUSTOMFIELD",".GETVALUEOFCUSTOMFIELD","PRIVATE", "PUBLIC", "COMBOBOX","PARAMKOD","SYSTEM.OUT", ".SETRAPOR", "SETTABLO"]
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

def transform_string(input_string):
    # Dönüşümü uygula
    transformed_string = (
        input_string.replace("Ğ", "\\u011e").
        replace("Ü", "\\u00dc").
        replace("Ş", "\\u015e").
        replace("İ", "\\u0130").
        replace("Ç", "\\u00c7").
        replace("Ö", "\\u00d6").
        replace("ı", "\\u0131").
        replace("ğ", "\\u011f").
        replace("ü", "\\u00fc").
        replace("ş", "\\u015f").
        replace("ç", "\\u00e7").
        replace(" ", "_").
        replace("ö", "\\u00f6")
    )
    return transformed_string

# Kullanım örneği:
java_project_directory = "C:/JAVAKAYNAK/workspaceTekJ8/ErpGUI"
find_strings_in_java_files(java_project_directory)
