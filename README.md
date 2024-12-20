# Something is here

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
