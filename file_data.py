def load_files_by_section(txt_path='files.txt'):
    files_by_section = {}
    current_section = None

    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('//'):
                    continue  # skip empty lines or comments

                if line.startswith('#'):
                    current_section = line[1:].strip()
                    files_by_section[current_section] = {}
                elif '-' in line and current_section:
                    name, url = line.split('-', 1)
                    files_by_section[current_section][name.strip()] = url.strip()

    except FileNotFoundError:
        print("files.txt not found.")

    return files_by_section

files_by_section = load_files_by_section()
