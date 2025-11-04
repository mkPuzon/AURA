# AURA: AI Understanding, Research, and Analytics glossary for AI education

AURA is a research paper processing pipeline that automates the collection, analysis, and organization of academic papers from arXiv, with a focus on AI-related research. The system extracts key information, processes text, and prepares data for further analysis and display.

## Features

- **Automated Paper Collection**: Fetches latest AI research papers from arXiv
- **Text Extraction**: Extracts and processes full text from PDFs
- **Keyword and Definition Extraction**: Uses Gemma3 and Llama3.3 to identify key terms and their definitions
- **Database Integration**: Stores processed data for analysis and retrieval
- **Modular Design**: Easy to extend with new processing modules or data sources

## Components

1. **`update_db.sh`**: Main script that orchestrates the entire pipeline
2. **`full_scraper.py`**: Handles paper retrieval from arXiv and PDF downloading
3. **`process_text.py`**: Processes paper text to extract keywords and definitions using LLMs
4. **`scrapers.py`**: Contains web scraping utilities and API interactions
5. **`db_functions.py`**: Manages database operations
## Getting Started

### Prerequisites
- Python 3.11.4+
- PostgreSQL (for database functionality)
- Ollama (for local LLM inference)
- Required Python packages (install via `pip install -r requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mkPuzon/AURA.git
   cd AURA
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add required API keys and configurations (see `.env.example` if available)

### Usage

Run the main pipeline:
```bash
./update_db.sh
```

This will:
1. Fetch new papers from arXiv
2. Download and process PDFs
3. Extract text and analyze content
4. Update the database with new findings

## Database Schema

The system uses PostgreSQL to store:
- Paper metadata (title, authors, publication date, etc.)
- Extracted text and processed content
- Identified keywords and their definitions
- Relationships between papers and terms

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thank you to [arXiv](https://arxiv.org/) for use of its open access interoperability.
- The open-source community for various libraries and tools