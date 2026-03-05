import os
import importlib


def read_file(filepath: str) -> dict:
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        extension = os.path.splitext(filepath)[1].lower()

        if extension == ".txt":
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
        elif extension == ".docx":
            # Dynamically import docx2txt so static analysis doesn't require it
            docx2txt = importlib.import_module("docx2txt")
            content = docx2txt.process(filepath) or ""
        elif extension == ".pdf":
            # Dynamically import pdfplumber for PDF text extraction
            pdfplumber = importlib.import_module("pdfplumber")
            with pdfplumber.open(filepath) as pdf:
                pages_text = [(page.extract_text() or "") for page in pdf.pages]
            content = "\n".join(pages_text)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return {
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "extension": extension,
            "size_bytes": os.path.getsize(filepath),
            "content": content,
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

def list_files(directory: str, extension: str | None = None) -> list[dict]:
    try:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Not a directory: {directory}")

        norm_ext = extension.lower() if extension else None

        files_metadata: list[dict] = []
        for name in os.listdir(directory):
            full_path = os.path.join(directory, name)
            if not os.path.isfile(full_path):
                continue

            if norm_ext is not None and not name.lower().endswith(norm_ext):
                continue

            stat = os.stat(full_path)
            files_metadata.append(
                {
                    "name": name,
                    "path": full_path,
                    "size_bytes": stat.st_size,
                    "modified_time": stat.st_mtime,
                }
            )

        return files_metadata
    except Exception as e:
        raise Exception(f"Error listing files: {e}")
        
def write_file(filepath: str, content: str) -> dict:
    try:
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        return {
            "status": "success",
            "filepath": filepath,
            "size_bytes": os.path.getsize(filepath),
            "message": "File written successfully",
        }
    except Exception as e:
        return {
            "status": "error",
            "filepath": filepath,
            "message": f"Error writing file: {e}",
        }
    
def search_in_file(filepath: str, keyword: str) -> dict:
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        keyword_lower = keyword.lower()
        matches: list[dict] = []

        for idx, line in enumerate(lines):
            if keyword_lower in line.lower():
                start = max(0, idx - 1)
                end = min(len(lines), idx + 2)  # current line plus one after
                context = "".join(lines[start:end])
                matches.append(
                    {
                        "line_number": idx + 1,
                        "context": context,
                    }
                )

        return {
            "filepath": filepath,
            "keyword": keyword,
            "matches": matches,
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error searching file: {e}")