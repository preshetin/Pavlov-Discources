def remove_specific_lines(input_file, output_file):
    try:
        # Read all lines from the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()
        
        # Keep lines that are not at indices 0, 3, 6, 9, ... (0-based indexing)
        filtered_lines = [line for i, line in enumerate(lines) if i % 3 != 0]
        
        # Write the filtered lines to the output file
        with open(output_file, 'w') as file:
            file.writelines(filtered_lines)
        
        print(f"File processed successfully. Updated file saved as {output_file}")
    
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
input_filename = "240920_Подробнее_о_сатипаттхане_Сатипаттхана_медитация.txt"  # Replace with your input file name
output_filename = "updated.txt"  # Name for the output file

remove_specific_lines(input_filename, output_filename)
