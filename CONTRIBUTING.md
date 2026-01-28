# 🤝 Contributing to Intelligent OCR

<div align="center">
A guide for contributing to the Intelligent OCR project  
Semi-structured document processing using OCR and semantic extraction
</div>

---

## 📌 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can You Contribute?](#-how-can-you-contribute)
- [Development Setup](#-development-setup)
- [Project Structure](#-project-structure)
- [Coding Guidelines](#-coding-guidelines)
- [Commit Message Guidelines](#-commit-message-guidelines)
- [Submitting Changes](#-submitting-changes)
- [Reporting Issues](#-reporting-issues)
- [Feature Requests](#-feature-requests)
- [Contact](#-contact)

---

## 🧭 Code of Conduct

<div>
This project is open to collaboration and learning.  
All contributors are expected to maintain a respectful and professional environment.
</div>

### We expect contributors to:
- Communicate respectfully
- Accept constructive feedback
- Collaborate in good faith
- Focus on technical quality and clarity

### Unacceptable behavior includes:
- Harassment or discrimination
- Aggressive or disrespectful language
- Spam or irrelevant contributions

---

## 🚀 How Can You Contribute?

<div>
You can contribute to Intelligent OCR in many ways, including but not limited to:
</div>

- 🐞 Bug reports and fixes  
- ✨ New features or enhancements  
- 🧠 OCR preprocessing improvements  
- 📄 Semantic extraction logic (forms, CVs, invoices)  
- 🌍 Multi-language support  
- 🧪 Tests and validation rules  
- 📚 Documentation improvements  

> Even small contributions are welcome.

---

## ⚙️ Development Setup

### Prerequisites

<div>
Make sure you have the following installed:
</div>

- Python **3.8+**
- Tesseract OCR
- Git

---

### Local Installation

```bash
git clone <repository-url>
cd OCR_INTELLIGENT
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
