# AI-Powered Video Analysis Platform

## Overview

A user-friendly Python script that handles the installation of all required packages for this project. The script features a clean progress tracking interface and automated NLTK data downloads.

## Features

*   **Chunked Video Upload:** Efficiently upload large video files in smaller chunks, ensuring smooth processing and minimizing upload failures.

*   **AI-Powered Analysis:**
    *   **Frame Extraction:** Extracts keyframes from videos at configurable intervals.
    *   **Gemini AI Integration:** Utilizes the Gemini AI model to generate insightful summaries, identify key concepts, and analyze the content of each frame.
    *   **Sentiment Analysis:** Detects and analyzes the emotional tone of the video content.
*   **Interactive Chat UI:** Engage in a conversation with an AI assistant to ask questions about the video analysis results, fostering a deeper understanding of the content.
*   **Visually Appealing UI:**
    *   **Custom Theme:** A modern and cohesive design with a well-defined color palette and typography.
    *   **Reusable UI Components:** Modular and maintainable UI elements like buttons, cards, and inputs, built using Streamlit and custom CSS.
    *   **Responsive Design:** Ensures optimal viewing experience across different devices and screen sizes.
*   **Payment Integration:** Supports donations through platforms like Buy Me a Coffee and Patreon, allowing users to contribute to the project's development.

## Getting Started

### Prerequisites

*   Python 3.8 or higher
*   pip package manager
*   A Gemini API key (set as the `GEMINI_API_KEY` environment variable)
*   Stripe API keys (if using Stripe for payments)
*   Buy Me a Coffee/Patreon tokens (if applicable)



## Project structure

The project follows a modular and well-organized structure:

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
│   ├── ai_integration/
│       │   ├── inputs.py
│       │   ├── cards.py
│       │   ├── button.py
│       │   └── theme.py
│       ├── __init__.py
│       ├── chat_ui.py
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

## How It Works

1. **Video Upload:** Users upload videos through the Streamlit UI. The `VideoChunkUploader` in `vid_upload.py` splits the video into smaller chunks and uploads them to the server.
2. **Chunk Storage:** The `ChunkedUploadManager` in `chunk_api.py` handles the storage of these chunks in the `uploads/chunks` directory.
3. **Video Assembly:** Once all chunks are uploaded, the `VideoUploadManager` in `vid_api.py` assembles them into a complete video file in the `uploads/videos` directory.
4. **Video Processing:** The `VideoProcessor` in `video_handler.py` extracts frames from the video at specified intervals.
5. **AI Analysis:** The `GeminiProcessor` in `gemini_processor.py` analyzes each frame, generating summaries, identifying key concepts, and performing sentiment analysis.
6. **Results Storage:** The `vid_api.py` stores the analysis results in JSON format in the `uploads/processed` directory.
7. **UI Interaction:** The `streamlit.py` file orchestrates the Streamlit UI, allowing users to upload videos, configure settings, view analysis results, and interact with the AI chat assistant.
8. **Chat Interface:** The `chat_ui.py` file provides the chat interface, powered by the `ChatAPI` in `chat_api.py`, which interacts with the Gemini AI model to answer user questions.
9. **Payment Processing:** The `payment_ui.py` and `payment_processor.py` files handle payment integration, allowing users to support the project through donations.

### Installation

1. Clone the repository:

    ```bash
    https://github.com/XenosWarlocks/Video-Processing-Tool.git
    cd Video-Processing-Tool
    ```

2. Create a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3. Install dependencies:

     ```bash
    python setup.py
    ```

    ### Notes

    - Make sure your requirements.txt is in the same directory as setup.py
    - For development setup, add your development dependencies to requirements.txt
    - If you encounter any permission errors, try running your terminal as administrator
    - Automatically install required base packages (tqdm, colorama, nltk)
    - Install all project dependencies from requirements.txt
    - Download necessary NLTK data packages
    - Show installation progress with status updates

4. Set up environment variables:
    *   Create a `.env` file based on the provided `.env.example`.
    *   Fill in your Gemini API key, Stripe keys, and other relevant tokens.

### Running the Application

1. Navigate to the project root directory:

    ```bash
    cd Video-Processing-Tool
    ```

2. Activate the virtual environment (if you created one):

    ```bash
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3. Run the Streamlit app:

    ```bash
    streamlit run src/ui/streamlit.py
    ```

4. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.
