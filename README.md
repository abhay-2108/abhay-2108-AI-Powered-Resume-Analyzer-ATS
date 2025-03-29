# AI-Powered Resume Analyzer (ATS)

The **AI-Powered Resume Analyzer** is an advanced web application designed to assess resumes based on **ATS (Applicant Tracking System) criteria**. It extracts text from resumes, analyzes formatting, identifies key skills, and calculates an ATS score to help candidates improve their resumes for job applications. This system leverages **Google Gemini AI**, **Flask**, and **PyMuPDF** for efficient text extraction and intelligent analysis.

![AT1](https://github.com/user-attachments/assets/d66e4e36-b39b-44db-a5db-b70630c898a0)

![AT2](https://github.com/user-attachments/assets/b55eb4c8-49f0-40e7-910e-cef555ee7e81)


## Features
- **Resume Text Extraction:** Extracts text from PDF resumes.
- **ATS Score Calculation:** Evaluates resume relevance based on job keywords.
- **AI-Powered Keyword Matching:** Uses Google Gemini AI to extract and match job-specific keywords.
- **Resume Formatting Analysis:** Checks for missing sections like experience, skills, and education.
- **Job Role Analysis:** Suggests suitable job roles based on resume content.
- **Web-Based Interface:** Simple UI for uploading resumes and receiving feedback.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/abhay-2108/abhay-2108-AI-Powered-Resume-Analyzer-ATS
   ```
2. Navigate to the project directory:
   ```bash
   cd abhay-2108-AI-Powered-Resume-Analyzer-ATS
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up your **Google Gemini AI API key** in a `.env` file:
   ```bash
   GENAI_API_KEY=your_google_api_key_here
   ```
6. Run the Flask app:
   ```bash
   python app.py
   ```

## Usage
1. Open the application in your browser at `http://localhost:5000`
2. Enter a **job title** to tailor the resume analysis.
3. Upload a **PDF resume** or paste text directly.
4. View feedback, including:
   - **ATS Score**
   - **Matched Keywords**
   - **Formatting Score**
   - **Missing Sections**
   - **Strengths & Weaknesses**

## Technologies Used
- **Flask** - Backend framework
- **Google Gemini AI** - AI-powered resume analysis
- **PyMuPDF** - PDF text extraction
- **Markdown** - Formatting output for analysis

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License
This project is licensed under the [MIT License](LICENSE).

