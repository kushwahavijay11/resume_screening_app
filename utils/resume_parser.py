import PyPDF2
import pdfplumber
import docx
import io
from typing import Optional

class ResumeParser:
    """Extract text from resume files (PDF, DOCX)"""
    
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF using pdfplumber (better extraction)"""
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            # Fallback to PyPDF2 if pdfplumber fails
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                return text
            except Exception as e2:
                raise Exception(f"Failed to parse PDF: {str(e2)}")
    
    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")
    
    @staticmethod
    def parse_resume(file_bytes: bytes, file_type: str) -> str:
        """Parse resume based on file type"""
        if file_type == "application/pdf":
            return ResumeParser.parse_pdf(file_bytes)
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            return ResumeParser.parse_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")