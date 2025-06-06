import os
import json
import pandas as pd
from pathlib import Path

def find_excel_files(directory):
    """Find all Excel files in directory and subdirectories"""
    excel_files = []
    directory_path = Path(directory)
    
    # Search for Excel files with common extensions
    for pattern in ['*.xlsx', '*.xls', '*.xlsm']:
        excel_files.extend(directory_path.rglob(pattern))
    
    return excel_files

def process_excel_file(file_path):
    """Process a single Excel file and extract data"""
    data_entries = []
    
    try:
        # Read Excel file - try all sheets
        excel_file = pd.ExcelFile(file_path)
        
        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Look for the required columns (case-insensitive)
                soru_col = None
                yanit_col = None
                
                for col in df.columns:
                    col_upper = str(col).upper()
                    if 'SORU' in col_upper or 'SORUN' in col_upper:
                        soru_col = col
                    elif 'YANIT' in col_upper or 'ÇÖZÜM' in col_upper:
                        yanit_col = col
                
                if soru_col is not None and yanit_col is not None:
                    # Process each row
                    for index, row in df.iterrows():
                        soru_value = row[soru_col]
                        yanit_value = row[yanit_col]
                        
                        # Skip empty rows
                        if pd.isna(soru_value) or pd.isna(yanit_value):
                            continue
                        if str(soru_value).strip() == '' or str(yanit_value).strip() == '':
                            continue
                        
                        # Create JSON entry
                        entry = {
                            "instruction": str(soru_value).strip(),
                            "input": "",
                            "output": str(yanit_value).strip()
                        }
                        
                        data_entries.append(entry)
                        
                else:
                    print(f"Warning: Required columns not found in {file_path} - Sheet: {sheet_name}")
                    print(f"Available columns: {list(df.columns)}")
                    
            except Exception as e:
                print(f"Error processing sheet '{sheet_name}' in {file_path}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
    
    return data_entries

def excel_to_json(input_directory, output_file="converted_data.json"):
    """Main function to convert Excel files to JSON"""
    
    # Check if input directory exists
    if not os.path.exists(input_directory):
        print(f"Error: Directory '{input_directory}' does not exist!")
        return
    
    print(f"Searching for Excel files in: {input_directory}")
    
    # Find all Excel files
    excel_files = find_excel_files(input_directory)
    
    if not excel_files:
        print("No Excel files found in the specified directory!")
        return
    
    print(f"Found {len(excel_files)} Excel files")
    
    all_data = []
    
    # Process each Excel file
    for file_path in excel_files:
        print(f"Processing: {file_path}")
        file_data = process_excel_file(file_path)
        all_data.extend(file_data)
        print(f"  -> Extracted {len(file_data)} entries")
    
    # Save to JSON file
    if all_data:
        # Save as JSON Lines format (one JSON object per line)
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in all_data:
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')
        
        print(f"\nSuccess! Converted {len(all_data)} entries to '{output_file}'")
        print(f"Output file saved in JSON Lines format (one JSON object per line)")
        
        # Also create a regular JSON array format
        array_output_file = output_file.replace('.json', '_array.json')
        with open(array_output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"Also created array format: '{array_output_file}'")
        
    else:
        print("No data was extracted from the Excel files!")

# Main execution
if __name__ == "__main__":
    # Configuration
    BASE_DIR = r"C:\CODE-BASE\PYTON"
    EXCEL_DIR = r"C:\CODE-BASE\PYTON\AKADEMİ"
    OUTPUT_FILE = os.path.join(BASE_DIR, "training_data.json")
    
    # Run the conversion
    excel_to_json(EXCEL_DIR, OUTPUT_FILE)
    
    print(f"\nConversion completed!")
    print(f"Check the output file: {OUTPUT_FILE}")