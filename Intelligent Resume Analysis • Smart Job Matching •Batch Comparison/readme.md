# 📄 Resume Extractor

An intelligent resume parsing application that extracts structured information from PDF resumes using advanced NLP and machine learning techniques. Built with Python and deployed on Hugging Face Spaces.

## 🌟 Features

- **PDF Resume Parsing**: Upload and extract text from PDF resumes
- **Structured Data Extraction**: Automatically identifies and extracts key information including:
  - Personal Information (Name, Email, Phone, Address)
  - Education History
  - Work Experience
  - Skills and Competencies
  - Certifications
- **JSON Output**: Converts unstructured resume data into structured JSON format
- **User-Friendly Interface**: Simple and intuitive web interface for easy interaction
- **Fast Processing**: Quick extraction and parsing of resume information

## 🚀 Live Demo

Try out the live application here: [Resume Extractor on Hugging Face](https://huggingface.co/spaces/Abiodun360of/resume-extractor)

## 🛠️ Tech Stack

- **Python**: Core programming language
- **Hugging Face Transformers**: NLP models for text understanding
- **Gradio/Streamlit**: Web interface framework
- **PyPDF2/pdfplumber**: PDF text extraction
- **spaCy/NLTK**: Natural language processing
- **Regular Expressions**: Pattern matching for structured data

## 📋 Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## 💻 Installation

1. Clone the repository:
```bash
git clone https://github.com/Abiodun360of/resume-extractor.git
cd resume-extractor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Local Development

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:7860` (or the port specified)

3. Upload a PDF resume and click "Extract" to parse the information

### API Usage

```python
from resume_extractor import extract_resume_info

# Extract information from a PDF file
result = extract_resume_info("path/to/resume.pdf")

# Access extracted data
print(result['name'])
print(result['email'])
print(result['skills'])
print(result['experience'])
```

## 📊 Output Format

The extractor returns a JSON object with the following structure:

```json
{
  "personal_info": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "address": "123 Main St, City, Country"
  },
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University Name",
      "year": "2020"
    }
  ],
  "experience": [
    {
      "title": "Software Engineer",
      "company": "Tech Company",
      "duration": "2020-2023",
      "description": "Developed and maintained applications..."
    }
  ],
  "skills": ["Python", "JavaScript", "Machine Learning", "React"],
  "certifications": ["AWS Certified Developer", "Google Cloud Professional"]
}
```

## 🔧 Configuration

You can customize the extraction behavior by modifying the configuration file:

```python
# config.py
EXTRACTION_SETTINGS = {
    "confidence_threshold": 0.7,
    "max_file_size_mb": 10,
    "supported_formats": ["pdf"],
    "extract_images": False
}
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for providing the platform and NLP models
- The open-source community for various libraries and tools
- Contributors who have helped improve this project

## 📧 Contact

**Abiodun** - [@Abiodun360of](https://github.com/Abiodun360of)

Project Link: [https://github.com/Abiodun360of/resume-extractor](https://github.com/Abiodun360of/resume-extractor)

## 🐛 Known Issues

- Some complex resume layouts may require manual review
- Non-English resumes may have reduced accuracy
- Large PDF files (>10MB) may take longer to process

## 🗺️ Roadmap

- [ ] Support for multiple languages
- [ ] Integration with ATS systems
- [ ] Batch processing of multiple resumes
- [ ] Resume scoring and ranking
- [ ] Support for DOCX and other formats
- [ ] Advanced skill matching with job descriptions

## ⭐ Show Your Support

If you find this project useful, please consider giving it a star on GitHub!

---

Made with ❤️ by Abiodun
