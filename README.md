# Something is here

## Project Setup Script

A user-friendly Python script that handles the installation of all required packages for this project. The script features a clean progress tracking interface and automated NLTK data downloads.

### Prerequisites

- Python 3.7+
- pip package manager

### Quick Start

1. Clone the repository:

    ```bash
    git clone https://github.com/XenosWarlocks/Video-Processing-Tool.git
    cd Video-Processing-Tool
    ```

2. Create and activate a virtual environment (recommended):

    ```bash
    python -m venv venv

    # Windows
    .\venv\Scripts\activate

    # macOS/Linux
    source venv/bin/activate
    ```

3. Run the setup script:

    ```bash
    python setup.py
    ```

The script will:

- Automatically install required base packages (tqdm, colorama, nltk)
- Install all project dependencies from requirements.txt
- Download necessary NLTK data packages
- Show installation progress with status updates

### Notes

- Make sure your requirements.txt is in the same directory as setup.py
- For development setup, add your development dependencies to requirements.txt
- If you encounter any permission errors, try running your terminal as administrator

## Project structure

```bash
video-processing-tool/
│
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── base_processor.py        # Base abstract class for processors
│   │   ├── token_counter.py         # AI Token counter
│   │   └── config_manager.py        # Centralized configuration management 
│   │
│   ├── video_processing/
│   │   ├── __init__.py
│   │   ├── video_handler.py         # Enhanced video handling
│   │   ├── frame_extractor.py       # Advanced frame extraction
│   │   ├── ocr_processor.py         # Improved OCR processing
│   │   └── text_analyzer.py         # Text analysis and deduplication
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── vid_api.py
│   │   ├── chunk_api.py
│   │
│   ├── ai_integration/
│   │   ├── __init__.py
│   │   ├── gemini_processor.py      # Gemini AI integration
│   │   └── text_enrichment.py       # AI-powered text enhancement
│   │
│   └── ui/
│       ├── __init__.py
│       └── streamlit.py             # Advanced Streamlit UI
│
├── tests/
│   ├── sample/
│   │   ├── __init__.py
│   │   ├── test_vid.mp4
│   ├── test_video_processing.py
│   └── test_ai_integration.py
│
├── configs/
│   ├── app_config.yaml
│   └── ai_config.yaml
│
├── logs/
│   └── app.log
│
├── requirements.txt
├── Dockerfile
├── docker-composer.yml
├── .env.example
├── .env
├── setup.py
└── README.md
```
