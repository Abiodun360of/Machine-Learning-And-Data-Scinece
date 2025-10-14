Usage
Tab 1: Resume Analysis

Upload a resume (PDF or TXT format)
The app will automatically extract and display:

Contact information (email, phone)
Skills organized by category
Educational background
Work experience highlights
Organizations and dates



Tab 2: Job Matching

Upload your resume
Paste the job description
View matching results:

Skill Match Score: Percentage of resume skills found in job
Semantic Similarity: Overall content relevance
Overall Score: Combined metric
Matched Skills: Skills you have that the job requires
Missing Skills: Skills you need to acquire



Tab 3: Batch Comparison

Paste the job description
Upload multiple resumes
Compare candidates:

View ranking table
See score comparisons in charts
Identify top candidate



Data Flow
Resume Upload (PDF/TXT)
        ↓
Text Extraction
        ↓
Text Cleaning
        ↓
NLP Processing (spaCy)
        ↓
Information Extraction:
├── Skills Detection
├── Education Extraction
├── Experience Parsing
├── Entity Recognition
└── Contact Information
        ↓
Skill Database Matching
        ↓
Job Description Comparison
        ↓
Results & Visualization
Project Structure
resume-extractor/
├── app.py                      # Main Streamlit application
├── nlp_processor.py            # NLP pipeline and extraction logic
├── text_extractor.py           # PDF and TXT text extraction
├── matcher.py                  # Job matching and scoring engine
├── skills_database.py          # Skills taxonomy and keywords
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── .streamlit/config.toml      # Streamlit settings
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
Key Components
skills_database.py
Maintains a comprehensive database of skills organized by category:

Programming Languages
Web Development Frameworks
Data & ML Tools
Cloud & DevOps
Soft Skills
Education Keywords

nlp_processor.py
Handles all NLP operations:

Text cleaning and normalization
Skill extraction with regex patterns
Email and phone number detection
Date extraction and validation
Named entity recognition
Experience sentence extraction

matcher.py
Implements matching algorithms:

Skill-based matching
TF-IDF semantic similarity
Match scoring and aggregation
Missing skill identification

app.py
Streamlit UI with:

Beautiful gradient design
Interactive charts and visualizations
Real-time processing
Responsive layout

Model Details
Skills Extraction

Uses regex pattern matching with word boundaries
Case-insensitive search
Supports 200+ predefined skills across 6+ categories
Extensible skill database

Email Detection

Supports standard email formats
Regex: [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}

Phone Detection

Recognizes US format: (XXX) XXX-XXXX
Nigeria format: +234XXXXXXXXXX or 0XXXXXXXXXX
International formats with 10+ digits

Date Extraction

Validates dates against month names and years
Filters out random numbers misidentified as dates
Supports formats: "Jan 2024", "January 2024", "2024-Present"

Job Matching Score
Overall Score = (Skill Match % + Semantic Similarity %) / 2

Where:
- Skill Match % = (Matched Skills / Required Skills) × 100
- Semantic Similarity % = TF-IDF cosine similarity × 100
Limitations & Considerations

Accuracy: Depends on resume formatting and quality
Scanned PDFs: Currently handles text-based PDFs only (not scanned images)
Skill Database: Limited to predefined skills (can be extended)
Context Understanding: May miss context-specific skills or abbreviations
Language: Currently English only

Performance Metrics

Resume processing time: ~2-5 seconds
Batch comparison (10 resumes): ~15-30 seconds
Memory usage: ~500MB per session
Disk space: ~300MB for dependencies

Deployment
Hugging Face Spaces
This project is deployed on Hugging Face Spaces using Docker.
Live at: https://huggingface.co/spaces/YOUR_USERNAME/resume-extractor
Deployment Steps

Create GitHub repository
Create Hugging Face Space (Docker SDK)
Upload all files including Dockerfile
Hugging Face automatically builds and deploys

Environment Requirements

Python 3.10+
Docker support
2GB RAM minimum
500MB free disk space
