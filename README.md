```markdown
# 📄 AI Resume Screening & Job Recommendation System

An intelligent, interactive application that analyzes resumes and recommends suitable job roles using AI. It provides a complete AI-powered resume screening solution with a polished user interface, helping candidates find their perfect job match while identifying key skill gaps.

---

## ✨ Features

- **📤 Resume Upload**: Supports PDF and DOCX formats with drag-and-drop capability.
- **🔍 Text Extraction**: Automatically extracts text using `PyPDF2`, `pdfplumber`, and `python-docx`.
- **🧠 AI Analysis**: Uses OpenAI GPT-4 to deeply analyze and extract:
  - Technical and Soft skills
  - Experience level and Education background
  - AI-generated Professional Profile Summary
- **🎯 Job Matching & Recommendation**: Advanced match scoring algorithm compares extracted skills with job requirements to find the best fit.
- **🚀 Missing Skills Analysis**: Identifies critical skill gaps needed for recommended roles to help users upskill.
- **📊 Visual Dashboard**: Clean, responsive, and professional UI with interactive Plotly charts.
- **🛡️ Error Handling**: Graceful fallbacks for invalid file formats, large files, API errors, and missing keys.

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI API (GPT-4), LangChain
- **Document Processing**: PyPDF2, pdfplumber, python-docx
- **Data Visualization**: Plotly, Pandas

## 📂 Project Structure

```text
resume_screening_app/
├── app.py                 # Main application script
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables
├── utils/
│   ├── resume_parser.py   # Resume text extraction logic
│   ├── ai_analyzer.py     # AI analysis and OpenAI integration
│   └── job_matcher.py     # Job matching algorithms
└── data/
    └── job_roles.json     # Job role database

```

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Clone the repository

```bash
git clone [https://github.com/KushwahaVijay11/resume_screening_app.git](https://github.com/KushwahaVijay11/resume_screening_app.git)
cd resume_screening_app

```

### 2. Create and Activate Virtual Environment (Windows)

```powershell
# Create the virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

```

*(Note: If you encounter an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first, then try activating again.)*

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

*(Note: If you encounter an httpx proxy error later on, run `pip install "httpx<0.28.0"` to resolve it).*

### 4. Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_actual_api_key_here

```

### 5. Run the Application

```bash
streamlit run app.py

```

The application will automatically open in your default web browser at `http://localhost:8501`.

## 💡 Usage

1. **Upload**: Open the app and upload your resume (PDF or DOCX).
2. **Analyze**: Wait a moment while the AI extracts text, skills, and experience from your document.
3. **Review Matches**: View tailored job recommendations, detailed match scores, and a breakdown of missing skills.
4. **Explore Insights**: Use the interactive dashboard charts to explore your skill gaps and read your AI-generated profile summary.

## ⚙️ Customization

### Adding New Job Roles

You can easily add or modify the roles the AI compares resumes against. Just edit the `data/job_roles.json` file:

```json
{
  "title": "Your Job Title",
  "required_skills": ["Skill 1", "Skill 2"],
  "experience": "1-3 years",
  "education": "Required degree"
}

```

### Configuration Options

* **`use_ai`**: Toggle AI analysis on or off in the sidebar settings.
* **`top_n`**: Adjust the slider to change the number of top job recommendations displayed.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**VIJAY SINGH**

🎓 Computer Science and Engineering

🏛️ Madan Mohan Malaviya University of Technology (MMMUT) - Gorakhpur, Uttar Pradesh, India

* 🐙 **GitHub:** [@KushwahaVijay11](https://github.com/KushwahaVijay11/)
* 💼 **LinkedIn:** [https://www.linkedin.com/in/kushwahavijay11/]
* 📧 **Email:** [vijaysinghtikampar@gmail.com]

Feel free to reach out if you have any questions or want to collaborate on AI and Machine Learning projects!

```

```