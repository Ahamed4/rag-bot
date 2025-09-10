# RAG-Bot: Interactive LLM Terminal with RAG Capabilities

A powerful Retrieval-Augmented Generation (RAG) system that allows you to query documents using various LLM providers.The project aims to create a reusable and robust chatbot using RAG system. This helps to plug in any data source as knowledge base and creates chatbot grounded to the data to avoid hallucination.

This project provides an interactive terminal interface for document ingestion, vector storage, and natural language querying.

## Features

- **Multiple LLM Provider Support**: OpenAI, Ollama, Google, and Groq
- **Document Processing**: Convert JSON data to markdown files
- **Vector Database**: ChromaDB integration for efficient document retrieval
- **Interactive Terminal**: User-friendly command-line interface
- **Configurable Parameters**: Adjust model, temperature, and other settings
- **Huggingface Embeddings**: High-quality document embeddings

## Installation

### Prerequisites

- Python 3.9+
- Git

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/rag-bot.git
cd rag-bot
```

2. **Create and activate a virtual environment**

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up API keys**

Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

## Usage

### Running the Application

Navigate to the `src` directory and run the main script:

```bash
cd src
python -m main
```

### Interactive Commands

Once the application is running, you'll be presented with an interactive terminal:

1. **Data Ingestion**:

   - Choose whether to convert JSON files to markdown
   - The system will ingest documents into the vector database

2. **LLM Provider Selection**:

   - Choose from OpenAI, Ollama, Google, or Groq
   - Configure model parameters like temperature

3. **Querying**:
   - Enter natural language questions to query your documents
   - Type `config` to change parameters
   - Type `exit` to quit

### JSON File Format for Conversion

The system can convert JSON files to markdown format. Place your JSON files in the `source` directory with the following structure:

```json
[
  {
    "id": "unique_identifier",
    "username": "author_name",
    "license": "license_type",
    "title": "Document Title",
    "publication_description": "The main content of your document. You can use --DIVIDER-- to separate sections."
  },
  {
    "id": "another_identifier",
    "username": "another_author",
    "license": "license_type",
    "title": "Another Document Title",
    "publication_description": "Content of the second document."
  }
]
```

**Required Fields:**

- `id`: A unique identifier for the document
- `username`: Author or creator name
- `license`: License type (e.g., "cc-by", "none")
- `title`: Document title
- `publication_description`: The main content of your document

**Example:**

```json
[
  {
    "id": "0CBAR8U8FakE",
    "username": "3rdson",
    "license": "none",
    "title": "How to Add Memory to RAG Applications and AI Agents",
    "publication_description": "# Introduction\n\nThis document explains how to add memory to RAG applications.\n--DIVIDER--\n## Implementation Details\n\nHere are the technical details..."
  }
]
```

When prompted during application startup, you can specify:

1. The JSON file name (default: `project_1_publications.json`)
2. The number of entries to process (default: 5)

### Example Session

```
INFO: Welcome to the Interactive LLM Terminal!
INFO: Let us first ingest some data.
Do you want to convert a JSON file to markdown files? (y/n) [default: y]: n
INFO: Skipping JSON to markdown conversion.
INFO: Data ingestion completed.
INFO: Let us initialize the LLM.
INFO: Supported LLM Providers:
1. Openai
2. Ollama
3. Google
4. Groq
Choose provider [default: groq]: 4
INFO: Selected provider: groq
Enter model name for 'Groq' llm [default: llama-3.1-8b-instant]:
Enter temperature [default: 0.0]:
INFO: Success! Instantiated 'Groq' LLM with model 'llama-3.1-8b-instant' and temperature 0.0.
Enter a question, 'config' to change the parameters, or 'exit' to quit: what is uv?
INFO: Querying collection...
INFO: LLM response:
UV is a Python package installer and resolver that:
* Offers fast, reliable, and reproducible builds.
* Generates and updates a `uv.lock` file to capture the exact version of all installed dependencies.
* Minimizes the risk of "dependency hell" by maintaining consistent package versions.
* Speeds up installation since UV can use the locked versions instead of solving the dependencies again.
```

## Project Structure

```
rag-bot/
├── data/                  # Source data and processed markdown files
├── outputs/
│   └── vector_db/         # ChromaDB vector database
├── src/
│   ├── app_code/
│   │   ├── chroma_db_ingest.py  # Document ingestion
│   │   ├── chroma_db_rag.py     # RAG functionality
│   │   ├── db_manager.py        # ChromaDB connection management
│   │   ├── logger.py            # Logging utilities
│   │   └── utils.py             # Helper functions
│   ├── main.py                  # Main application entry point
│   └── paths.py                 # Path configurations
├── .env                   # Environment variables (API keys)
├── .gitignore
├── requirements.txt       # Project dependencies
└── README.md
```

## Troubleshooting

### ChromaDB File Access Issues

If you encounter errors like:

```
ERROR: Failed to delete vector_db directory. Make sure no process is using chroma.sqlite3.
ERROR: [WinError 32] The process cannot access the file because it is being used by another process
```

Try these solutions:

1. Restart your terminal/IDE
2. Make sure no other instances of the application are running
3. If on Windows, you may need to manually delete the `outputs/vector_db` directory

### Embedding Model Errors

If you see errors related to the sentence transformer model:

```
KeyError: 'sentence-transformers/all-MiniLM-L6-v2'
```

Make sure you have internet access for the initial model download and that you're using the correct embedding method for your model type.

## Dependencies

- `chromadb`: Vector database for document storage and retrieval
- `langchain`: Framework for LLM applications
- `huggingface`: Document embedding models
- `openai`, `groq`: API clients for LLM providers
- `python-dotenv`: Environment variable management
- `psutil`: Process management for ChromaDB cleanup

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [ChromaDB](https://docs.trychroma.com/) for vector database functionality
- [LangChain](https://www.langchain.com/) for LLM application framework
- [Sentence Transformers](https://www.sbert.net/) for document embeddings
- All the LLM providers (OpenAI, Groq, Google, Ollama) for their APIs

---

_Note: This project is for educational and research purposes only. Use responsibly and in accordance with the terms of service of the LLM providers._
