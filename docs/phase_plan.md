# **Project Kickoff Prompt for Scalable Educational Video Processing Tool**

## **Objective:**

The goal of this project is to develop a **highly scalable and modular tool** that processes educational videos to provide summaries, key points, and transcriptions. The project will be structured into **three phases**, with each phase adding more advanced features, enhancing modularity, and ensuring scalability. This tool will support seamless integration of different technologies and APIs to ensure long-term sustainability and scalability.

### **Phase 1: Foundation - Core Functionality and Modular Architecture**

The first phase will focus on building the foundational components of the system with a modular approach, ensuring that all parts of the code are reusable, extensible, and easy to maintain.

#### 1. **Streamlit Web App Interface:**

   - **Objective:** Create a user-friendly **Streamlit web application** to provide an intuitive interface for uploading videos, processing frames, and displaying transcriptions and summaries.
   
   - **Tasks:** 
   
     - Build a clean UI with user-friendly navigation and input fields for uploading videos.
     - Implement a **file upload function** with the capability to handle large video files (up to 1GB or more).
     - Display progress indicators for video upload, processing, and text extraction.
     - Provide an option for users to download results (e.g., transcriptions, summaries, and key points).

#### 2. **Backend API for Video Handling:**

   - **Objective:** Build a **scalable backend API** to handle video uploads and storage, ensuring that video files are processed efficiently.
   
   - **Tasks:**
   
     - Develop an API endpoint that listens for video uploads and stores the files in a dedicated `temp_vid_file` directory.
     - Implement file type validation (only allow video formats like MP4, MOV, etc.).
     - Ensure that the backend API can handle concurrent video uploads without performance degradation.
     - Organize the directory structure to store files efficiently, especially when handling multiple uploads.

#### 3. **Modular Video Frame Sampling:**

   - **Objective:** Slice the uploaded video into frames at regular intervals to enable text extraction and later processing.
   
   - **Tasks:**
   
     - Develop a **frame sampling module** that slices the video into frames at configurable time intervals (e.g., every 30 seconds).
     - Store the frames sequentially with unique names for later processing (e.g., `frame_1.png`, `frame_2.png`, etc.).
     - Ensure that the frame extraction process can be parallelized for scalability and efficiency.

#### 4. **Text Extraction with OCR (Tesseract or EasyOCR):**

   - **Objective:** Extract textual content from the sampled frames using advanced OCR technology.

   - **Tasks:**
   
     - Integrate **Tesseract** or **EasyOCR** to extract text from each frame.
     - Preprocess frames for optimal OCR performance (e.g., grayscale conversion, thresholding, noise removal).
     - Ensure that the OCR extraction is robust by handling various text styles, fonts, and video resolutions.
     - Implement logic to remove **duplicate text** between consecutive frames, ensuring that the extracted data is clean and non-redundant.

#### 5. **Text Deduplication and Storage:**

   - **Objective:** Clean the extracted text by removing duplicates and storing the final output in a structured format.
   
   - **Tasks:**
   
     - Implement a **deduplication algorithm** that compares extracted text and removes repeated phrases.
     - Store the deduplicated text in a structured format (e.g., JSON, CSV, or database) to facilitate future processing in later phases.
     - Ensure that text is stored in a way that allows easy retrieval, searching, and manipulation for further analysis.

**Deliverable for Phase 1:**
- A functional, scalable web application with video upload and processing functionality.
- A modular backend with file handling, frame sampling, and text extraction capabilities.
- A clean text output with deduplication and storage, ready for AI-enhanced analysis in Phase 2.

---

### **Phase 2: AI-Based Frame Analysis and Enhanced Text Understanding**
In Phase 2, we’ll enhance the functionality by integrating **AI-based analysis** to improve text understanding and generate more meaningful insights, such as sentiment analysis and topic segmentation.

#### 1. **Gemini AI API Integration:**
   - **Objective:** Leverage AI models to enhance the analysis of video frames and extract richer contextual information.
   - **Tasks:**
     - Integrate **Gemini AI API** for advanced frame analysis, extracting contextual understanding, sentiment weight, and topic segmentation.
     - Implement AI models to analyze frames not only for text extraction but also for visual context, scene recognition, and emotional sentiment.

#### 2. **Audio-Visual Data Fusion with ASR (Whisper Model):**
   - **Objective:** Combine both **audio and visual data** to provide a richer understanding of the video content.
   - **Tasks:**
     - Use **Whisper ASR model** to extract audio transcriptions from the video.
     - Synchronize the text extracted from OCR with the audio transcription, enriching the analysis.
     - Implement an algorithm to combine these data sources in a modular way for scalability, enabling future extensions with other ASR models if needed.

#### 3. **LangChain Integration for Text Chunking and Prompt Tuning:**
   - **Objective:** Use **LangChain** for **text chunking**, prompt optimization, and fine-tuning for specific tasks (summarization, transcription, key point extraction).
   - **Tasks:**
     - Implement LangChain to process large chunks of text from the frames and audio transcriptions.
     - Fine-tune LangChain prompts for various tasks, ensuring that summaries and key points are relevant and accurate.
     - Develop a modular chunking system that breaks down long transcriptions into manageable pieces based on context or time duration.

**Deliverable for Phase 2:**
- An AI-enhanced tool that analyzes video frames and audio to provide richer insights (e.g., sentiment analysis, scene understanding, and topic segmentation).
- A modular approach to combining audio and visual data, creating a more thorough understanding of the content.
- A LangChain-based system for summarization, transcription, and key point extraction.

---

### **Phase 3: Advanced Features and User Interactivity**
The final phase will focus on improving the user experience, adding interactivity, and providing a fully-featured platform that allows users to interact with and explore video transcriptions, summaries, and keywords.

#### 1. **Summaries with Visual Context and Timestamps:**
   - **Objective:** Create **interactive summaries** that are not only textual but also include associated visual context (e.g., frame snapshots, timestamps).
   - **Tasks:**
     - Generate **summaries** of the video content, combining extracted text with corresponding visual frames or scenes.
     - Include **timestamps** in the summaries, allowing users to quickly jump to specific parts of the video.

#### 2. **Interactive Keyword Highlights:**
   - **Objective:** Enable users to interact with keywords in the transcriptions to navigate specific video sections.
   - **Tasks:**
     - Implement clickable **keywords or key phrases** in the transcription output, allowing users to navigate to relevant sections of the video.
     - Use AI-based keyword extraction to identify significant phrases that can serve as navigation points.

#### 3. **Searchable Transcriptions by Keyword, Timestamp, and Sentiment:**
   - **Objective:** Allow users to **search and filter** transcriptions based on specific criteria (e.g., keywords, timestamps, sentiment).
   - **Tasks:**
   
     - Build a **search engine** that enables users to search for specific words, phrases, or sentiments within the transcriptions.
     - Implement filters for **timestamp-based** search, so users can jump to specific parts of the video.
     - Integrate sentiment-based filtering, allowing users to find specific emotional or contextual moments in the video.

**Deliverable for Phase 3:**

- A fully-featured video analysis tool with interactive features like **summaries with visuals**, **keyword highlights**, and **searchable transcriptions**.
- A robust and scalable user experience that enables users to interact deeply with the video content.

---

### **General Considerations for Scalability and Modularity:**

- **Modular Codebase:** Each component (file upload, text extraction, AI analysis, etc.) should be implemented as an independent module to facilitate testing, debugging, and future feature expansion.
- **Scalability:** The architecture should be designed to handle large video files, concurrent user requests, and large-scale text and data processing efficiently.
- **Error Handling & Logging:** Ensure that error handling is robust, with proper logging and notification systems in place for better debugging and user feedback.
- **Cloud Integration:** For scalability, consider integrating cloud services (e.g., AWS S3 for storage, AWS Lambda for processing) to handle large video files and heavy processing loads.
