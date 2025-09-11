from pathlib import Path
from typing import Union, Any
import yaml
import json
from docx import Document
import PyPDF2

def load_file(file_path: Union[str, Path], encoding="utf-8") -> Any:
    """Loads files of various types including txt, docx, pdf, and md.

    Args:
        file_path: Path to the file.
        encoding: File encoding (default: utf-8).

    Returns:
        File content as string or parsed content.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is not supported.
        IOError: If there's an error reading the file.
    """
    print(f"Loading file: {file_path}")
    file_path = Path(file_path)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine file type by extension
    suffix = file_path.suffix.lower()
    print("Suffix",suffix)
    
    try:
        # Plain text files
        if suffix == '.txt':
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        
        # Markdown files
        elif suffix == '.md':
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                return content
        
        # Word documents
        elif suffix == '.docx':
            with file_path.open('rb') as file:
                doc = Document(file)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        
        # PDF files
        elif suffix == '.pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
                return text
        
        # YAML files
        elif suffix in ['.yaml', '.yml']:
            with open(file_path, 'r', encoding=encoding) as file:
                return yaml.safe_load(file)
        
        # JSON files
        elif suffix == '.json':
            with open(file_path, 'r', encoding=encoding) as file:
                return json.load(file)
        
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
            
    except Exception as e:
        raise IOError(f"Error reading {suffix} file: {str(e)}") from e
