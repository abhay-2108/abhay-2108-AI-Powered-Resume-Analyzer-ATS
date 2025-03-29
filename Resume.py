import fitz  # PyMuPDF for PDF processing
import os
import google.generativeai as genai
from flask import Flask, render_template, request
from dotenv import load_dotenv
import markdown

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

app = Flask(__name__)

# Upload folder for PDFs
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"


# Function to check resume formatting
def check_resume_formatting(resume_text):
    required_sections = ["summary", "skills", "experience", "education", "certifications", "contact"]
    missing_sections = [section for section in required_sections if section not in resume_text.lower()]

    formatting_score = ((len(required_sections) - len(missing_sections)) / len(required_sections)) * 100
    
    return round(formatting_score, 2), missing_sections


# Function to extract resume keywords using AI
def extract_resume_keywords(text):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = f"""
    Extract the most important technical and industry-specific keywords from the following resume.
    Return them as a comma-separated list.

    Resume Text:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text.strip().split(", ")  


# Function to get job-related keywords using AI
def get_job_keywords(job_title):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    prompt = f"""
    You are an AI job recruitment assistant. 
    List the **top 10 most important keywords** an ATS system looks for in a **{job_title}** resume.
    Focus on **skills, technologies, tools, and industry-specific terms**.
    Output should be a comma-separated list (e.g., Python, React, SQL, Git).
    """

    response = model.generate_content(prompt)
    keywords = response.text.strip().split(",")

    print("🔹 Extracted Job Keywords:", keywords)  

    return [keyword.strip().lower() for keyword in keywords if keyword.strip()]  # Remove empty values


# Function to calculate ATS score
def calculate_ats_score(resume_text, job_title):
    job_keywords = get_job_keywords(job_title)

    # If no keywords are found, return 0 score
    if not job_keywords:
        return 0, []

    resume_words = resume_text.lower().split()
    matched_keywords = [word for word in job_keywords if word in resume_words]

    ats_score = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0

    print(f"✅ ATS Score: {ats_score}/100")  
    print("🔹 Matched Keywords:", matched_keywords)  

    return round(ats_score, 2), matched_keywords


# Function to analyze resume and return feedback
def analyze_resume(resume_text, job_title):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    prompt = f"""
    You are an AI career coach. Analyze the following resume and provide:
    - Strengths
    - Weaknesses
    - Areas of improvement
    - Suggested job roles

    Resume Text:
    {resume_text}

    Provide your response in a clear, structured format.
    """

    response = model.generate_content(prompt)
    analysis = response.text  

    # Calculate ATS score and Formatting score
    ats_score, matched_keywords = calculate_ats_score(resume_text, job_title)
    formatting_score, missing_sections = check_resume_formatting(resume_text)

    # Append scores to the analysis
    analysis += f"\n\n**✅ ATS Score: {ats_score}/100**"
    analysis += f"\n**Matched Keywords:** {', '.join(matched_keywords) if matched_keywords else 'None'}"
    analysis += f"\n\n**📝 Formatting Score: {formatting_score}/100**"
    analysis += f"\n❌ **Missing Sections:** {', '.join(missing_sections) if missing_sections else 'None'}"

    return analysis


# Flask route for handling requests
@app.route('/', methods=['POST', 'GET'])
def index():
    feedback = None

    if request.method == "POST":
        job_title = request.form.get("job_title")  
        uploaded_file = request.files.get("resume")
        resume_text = request.form.get("resume_text")  

        if not job_title or not job_title.strip():
            return render_template("index.html", feedback="❌ Please enter a job title!")

        if uploaded_file and uploaded_file.filename.endswith(".pdf"):
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
            uploaded_file.save(pdf_path)
            resume_text = extract_text_from_pdf(pdf_path)
        
        if resume_text and resume_text.strip():
            feedback = analyze_resume(resume_text, job_title)
            feedback = markdown.markdown(feedback)

    return render_template("index.html", feedback=feedback)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
