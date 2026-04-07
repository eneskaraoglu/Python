# Open the original file and read all lines with UTF-8 encoding
with open(r"C:\WORKSPACE\PYTHON\Python\StringOperations\snv-user.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Filter lines that start with 'r'
filtered_lines = [line for line in lines if line.startswith('r')]

# Write only the filtered lines back to the file (overwrite original) with UTF-8 encoding
with open(r"C:\WORKSPACE\PYTHON\Python\StringOperations\snv-user.txt", "w", encoding="utf-8") as file:
    file.writelines(filtered_lines)





# Open the original file and read all lines with UTF-8 encoding
with open(r"C:\WORKSPACE\PYTHON\Python\StringOperations\snv-user.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Process and collect usernames (only from lines starting with 'r')
usernames = set()
for line in lines:
    if line.startswith('r'):
        parts = line.split('|')
        if len(parts) >= 2:
            username = parts[1].strip()
            usernames.add(username)

# Write updated email addresses to the file
with open(r"C:\WORKSPACE\PYTHON\Python\StringOperations\snv-user.txt", "w", encoding="utf-8") as file:
    for username in sorted(usernames):  # Remove sorted() if order is not important
        file.write(f"{username} = {username} <{username}@bilisim.com.tr>\n")
