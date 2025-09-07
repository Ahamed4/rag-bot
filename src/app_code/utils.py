import os
from dotenv import load_dotenv
import yaml
from pathlib import Path
from typing import Union
import json
from paths import ENV_FPATH, SOURCE_DATA_DIR, DATA_DIR

def load_env(api_key_type="GROQ_API_KEY") -> None:
    """Loads environment variables from a .env file and checks for required keys.

    Raises:
        AssertionError: If required keys are missing.
    """
    # Load environment variables from .env file
    load_dotenv(ENV_FPATH, override=True)
   

    # Check if 'XYZ' has been loaded
    api_key = os.getenv(api_key_type)

    assert (
        api_key
    ), f"Environment variable '{api_key_type}' has not been loaded or is not set in the .env file."

def load_yaml_config(file_path: Union[str, Path]) -> dict:
    """Loads a YAML configuration file.

    Args:
        file_path: Path to the YAML file.

    Returns:
        Parsed YAML content as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there's an error parsing YAML.
        IOError: If there's an error reading the file.
    """
    file_path = Path(file_path)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"YAML config file not found: {file_path}")

    # Read and parse the YAML file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}") from e
    except IOError as e:
        raise IOError(f"Error reading YAML file: {e}") from e

def json_to_markdown(json_path=os.path.join(SOURCE_DATA_DIR, "project_1_publications.json"), output_dir= DATA_DIR, num_entries_to_process=5):
    # Load JSON
    """
    Converts a JSON file of publication entries to markdown files.

    Args:
        json_path (str): Path to the JSON file of publication entries.
        output_dir (str): Directory to write the markdown files to.
        num_entries_to_process (int): Number of JSON entries to process.

    Returns:
        None
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in range(min(num_entries_to_process, len(data))):
        entry = data[i]
        output_filename = f"publication_{i+1}.md"
        create_markdown_from_json(entry, output_dir, output_filename)

def create_markdown_from_json(entry, output_dir, output_filename):
    # Ensure output directory exists
    """
    Creates a markdown file from a JSON publication entry.

    Args:
        entry (dict): A JSON publication entry.
        output_dir (str): The directory to write the markdown file to.
        output_filename (str): The filename to use for the markdown file.

    """
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"{entry.get('id', output_filename)}.md"

    # Create markdown content
    md_content = f"# Title\n\n{entry.get('title', 'No Title')}\n\n---\n\n"
    md_content += f"**Authors:** {', '.join(author for author in entry.get('authors', []))}\n\n---\n\n"
    md_content += f"**Tags:** {', '.join(tag for tag in entry.get('tags', []))}\n\n---\n\n"
    md_content += f"**License:** {entry.get('license', 'No License')}\n\n---\n\n"
    md_content += f"**Publication Date:** {entry.get('publication_date', 'No Date')}\n\n---\n\n"
    md_content += f"**Link:** {entry.get('link', 'No Link')}\n\n---\n\n"
    md_content += entry.get('publication_description', 'No Description')

    # Write to markdown file
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"Created markdown file: {output_path}")

def load_publication(publication_external_id="0CBAR8U8FakE"):
    """Loads the publication markdown file.

    Returns:
        Content of the publication as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there's an error reading the file.
    """
    publication_fpath = Path(os.path.join(DATA_DIR, f"{publication_external_id}.md"))

    # Check if file exists
    if not publication_fpath.exists():
        raise FileNotFoundError(f"Publication file not found: {publication_fpath}")

    # Read and return the file content
    try:
        with open(publication_fpath, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading publication file: {e}") from e


def load_all_publications(publication_dir: str = DATA_DIR) -> list[str]:
    """Loads all the publication markdown files in the given directory.

    Returns:
        List of publication contents.
    """
    publications = []
    for pub_id in os.listdir(publication_dir):
        if pub_id.endswith(".md"):
            publications.append(load_publication(pub_id.replace(".md", "")))
    return publications

if __name__ == "__main__":
    json_to_markdown()