import os
import zipfile

def list_png_in_jars(directory, png_name_filter=None):
    """
    Verilen dizindeki JAR dosyalarını tarar ve PNG dosyalarını listeler.
    
    :param directory: JAR dosyalarının bulunduğu dizin
    :param png_name_filter: PNG dosya isimlerini filtrelemek için bir alt string, None ise tüm PNG'ler listelenir
    """
    # Verilen dizindeki tüm JAR dosyalarını bul
    jar_files = [f for f in os.listdir(directory) if f.endswith('.jar')]

    if not jar_files:
        print("No JAR files found in the directory.")
        return

    for jar_file in jar_files:
        jar_path = os.path.join(directory, jar_file)
        try:
            with zipfile.ZipFile(jar_path, 'r') as jar:
                # print(f"Scanning JAR: {jar_file}")
                # JAR dosyasındaki tüm dosyaları tarar
                found_any = False
                for file_name in jar.namelist():
                    if file_name.endswith('.png') and (png_name_filter is None or png_name_filter in file_name):
                        print(f"{jar_file}  Found PNG: {file_name}")
                        found_any = True
        except zipfile.BadZipFile:
            print(f"Error: {jar_file} is not a valid JAR file.")
        except Exception as e:
            print(f"Error reading {jar_file}: {e}")

# Kullanım
if __name__ == "__main__":
    directory_path = "C:\JAVAKAYNAK\erp-git\ErpWEB\Web Content\GUIJars"  # JAR dosyalarının bulunduğu dizin
    png_filter = "monit"  # PNG isimlerinde aranacak alt string, None ise tümü listelenir

    # Filtre uygulanmadan tüm PNG'ler için
    # png_filter = None

    list_png_in_jars(directory_path, png_name_filter=png_filter)
