import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.resume_parser import ResumeParser
from utils.ai_analyzer import AIAnalyzer
from utils.job_matcher import JobMatcher
import os
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
    }
    .skill-tag {
        display: inline-block;
        background: #e8f4fd;
        color: #2980b9;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
    .missing-skill-tag {
        display: inline-block;
        background: #fde8e8;
        color: #c0392b;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
    .score-high {
        color: #27ae60;
        font-weight: 700;
    }
    .score-medium {
        color: #f39c12;
        font-weight: 700;
    }
    .score-low {
        color: #e74c3c;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

def get_score_color(score):
    """Return color class based on score"""
    if score >= 70:
        return "score-high"
    elif score >= 50:
        return "score-medium"
    else:
        return "score-low"

def create_match_chart(matches):
    """Create a bar chart showing match scores"""
    titles = [m["title"] for m in matches]
    scores = [m["match_score"] for m in matches]
    
    fig = go.Figure(data=[
        go.Bar(
            x=titles,
            y=scores,
            marker_color=['#27ae60' if s >= 70 else '#f39c12' if s >= 50 else '#e74c3c' for s in scores],
            text=[f"{s}%" for s in scores],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Job Role Match Scores",
        xaxis_title="Job Roles",
        yaxis_title="Match Score (%)",
        yaxis_range=[0, 100],
        height=400,
        showlegend=False
    )
    
    return fig

def main():
    # Header
    st.markdown('<p class="main-header">📄 AI Resume Screening & Job Recommendation</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your resume to get AI-powered job recommendations and skill analysis</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📤 Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF or DOCX)",
            type=["pdf", "docx"],
            help="Supported formats: PDF, DOCX"
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        use_ai = st.checkbox("Use AI Analysis", value=True, 
                            help="Enable AI-powered resume analysis for better results")
        top_n = st.slider("Number of job recommendations", 1, 5, 3)
        
        st.markdown("---")
        st.markdown("### 📊 About")
        st.info(
            "This AI-powered system analyzes your resume, extracts skills, "
            "and recommends the most suitable job roles based on your profile."
        )
    
    # Main content area
    if uploaded_file is not None:
        try:
            # Read file
            file_bytes = uploaded_file.read()
            file_type = uploaded_file.type
            
            with st.spinner("📝 Processing resume..."):
                # Parse resume
                parser = ResumeParser()
                resume_text = parser.parse_resume(file_bytes, file_type)
                
                # Analyze resume
                if use_ai:
                    with st.spinner("🧠 AI analyzing your resume..."):
                        analyzer = AIAnalyzer()
                        analysis = analyzer.analyze_resume(resume_text)
                else:
                    # Basic analysis
                    analysis = {
                        "skills": {
                            "technical": ["Python", "JavaScript", "SQL", "React"],
                            "soft": ["Communication", "Teamwork", "Problem Solving"]
                        },
                        "experience": "3 years",
                        "education": "Bachelor's in Computer Science",
                        "profile_summary": "Experienced developer with a focus on web technologies."
                    }
                
                # Match job roles
                matcher = JobMatcher()
                all_skills = analysis.get("skills", {}).get("technical", []) + analysis.get("skills", {}).get("soft", [])
                matches = matcher.find_best_matches(all_skills, top_n)
            
            # Display results in columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 🎯 Job Recommendations")
                
                # Create match chart
                fig = create_match_chart(matches)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display detailed recommendations
                for i, match in enumerate(matches, 1):
                    score = match["match_score"]
                    score_class = get_score_color(score)
                    
                    with st.expander(f"#{i} {match['title']} - Match: {score}%", expanded=(i==1)):
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown(f"**Match Score:** <span class='{score_class}'>{score}%</span>", unsafe_allow_html=True)
                            st.markdown(f"**Experience:** {match['experience']}")
                            st.markdown(f"**Education:** {match['education']}")
                        
                        with col_b:
                            st.markdown("**Required Skills:**")
                            for skill in match["required_skills"][:6]:
                                st.markdown(f"<span class='skill-tag'>{skill}</span>", unsafe_allow_html=True)
                            
                            if match["missing_skills"]:
                                st.markdown("**Skills to Develop:**")
                                for skill in match["missing_skills"][:3]:
                                    st.markdown(f"<span class='missing-skill-tag'>⚠️ {skill}</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 👤 Profile Summary")
                st.markdown(f"**Experience:** {analysis.get('experience', 'Not specified')}")
                st.markdown(f"**Education:** {analysis.get('education', 'Not specified')}")
                st.markdown("---")
                
                st.markdown("**Technical Skills:**")
                tech_skills = analysis.get("skills", {}).get("technical", [])
                if tech_skills:
                    for skill in tech_skills[:8]:
                        st.markdown(f"<span class='skill-tag'>✓ {skill}</span>", unsafe_allow_html=True)
                else:
                    st.info("No technical skills identified")
                
                st.markdown("---")
                st.markdown("**Soft Skills:**")
                soft_skills = analysis.get("skills", {}).get("soft", [])
                if soft_skills:
                    for skill in soft_skills[:5]:
                        st.markdown(f"<span class='skill-tag'>✓ {skill}</span>", unsafe_allow_html=True)
                else:
                    st.info("No soft skills identified")
                
                st.markdown("---")
                st.markdown("**📝 Profile Summary:**")
                st.markdown(analysis.get("profile_summary", "No summary available"))
            
            # Additional analysis section
            st.markdown("---")
            st.markdown("### 📊 Detailed Analysis")
            
            tab1, tab2, tab3 = st.tabs(["Skills Analysis", "Job Market Fit", "Recommendations"])
            
            with tab1:
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("#### 🛠️ Technical Skills")
                    if tech_skills:
                        df_tech = pd.DataFrame({
                            "Skill": tech_skills,
                            "Category": ["Technical"] * len(tech_skills)
                        })
                        st.dataframe(df_tech, hide_index=True)
                    else:
                        st.info("No technical skills found")
                
                with col_b:
                    st.markdown("#### 🤝 Soft Skills")
                    if soft_skills:
                        df_soft = pd.DataFrame({
                            "Skill": soft_skills,
                            "Category": ["Soft"] * len(soft_skills)
                        })
                        st.dataframe(df_soft, hide_index=True)
                    else:
                        st.info("No soft skills found")
            
            with tab2:
                st.markdown("#### 💼 Job Market Insights")
                
                # Show top matches in a table
                match_data = []
                for match in matches:
                    match_data.append({
                        "Job Role": match["title"],
                        "Match Score": f"{match['match_score']}%",
                        "Missing Skills": ", ".join(match["missing_skills"][:3]) if match["missing_skills"] else "None",
                        "Experience Required": match["experience"]
                    })
                
                df_matches = pd.DataFrame(match_data)
                st.dataframe(df_matches, hide_index=True, use_container_width=True)
            
            with tab3:
                st.markdown("#### 🚀 Career Recommendations")
                if matches:
                    best_match = matches[0]
                    st.success(f"""
                    **Top Recommendation: {best_match['title']}**
                    
                    *Match Score: {best_match['match_score']}%*
                    
                    **Why this role?**
                    Your skill set aligns well with the requirements for this position.
                    
                    **Suggested Next Steps:**
                    {f"1. Develop these skills: {', '.join(best_match['missing_skills'][:3])}" if best_match['missing_skills'] else "1. You already meet the skill requirements!"}
                    2. Update your LinkedIn profile with relevant keywords
                    3. Network with professionals in this field
                    """)
                    
                    if len(matches) > 1:
                        st.markdown("**Alternative Roles to Consider:**")
                        for match in matches[1:]:
                            st.markdown(f"- **{match['title']}** ({match['match_score']}% match)")
                else:
                    st.warning("No matching job roles found. Consider updating your resume with more relevant skills.")
        
        except Exception as e:
            st.error(f"❌ Error processing resume: {str(e)}")
            st.info("Please try again with a different file or contact support.")
    
    else:
        # Display placeholder when no file is uploaded
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
                <h2 style="font-size: 3rem;">📄</h2>
                <h3>Upload Resume</h3>
                <p style="color: #7f8c8d;">Upload your resume to get started</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
                <h2 style="font-size: 3rem;">🤖</h2>
                <h3>AI Analysis</h3>
                <p style="color: #7f8c8d;">AI extracts skills and experience</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px;">
                <h2 style="font-size: 3rem;">🎯</h2>
                <h3>Get Matched</h3>
                <p style="color: #7f8c8d;">Find the best job roles for you</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("👆 Upload your resume using the sidebar to start the analysis!")

if __name__ == "__main__":
    main()