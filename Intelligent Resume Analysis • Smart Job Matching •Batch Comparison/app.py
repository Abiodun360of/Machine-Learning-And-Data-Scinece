import streamlit as st
from text_extractor import extract_text_from_pdf, extract_text_from_txt, clean_text
from nlp_processor import ResumeProcessor
from matcher import JobMatcher
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Resume Extractor AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
        /* Main background gradient */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        }
        
        /* Custom card styling */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        
        /* Header styling */
        .header-text {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 900;
            font-size: 3em;
        }
        
        /* Skill badge styling */
        .skill-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            margin: 5px 5px 5px 0;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 15px 25px;
            background: rgba(255, 255, 255, 0.1);
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        /* Progress bar styling */
        .progress-bar {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Section headers */
        .section-header {
            border-bottom: 3px solid;
            border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1;
            padding-bottom: 10px;
            margin-top: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize processor
processor = ResumeProcessor()

# Header section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5em; font-weight: 900;'>🎯 Resume AI Extractor</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; color: #666; font-size: 1.1em; margin-bottom: 30px;'>
        <p>⚡ Intelligent Resume Analysis • Smart Job Matching • Batch Comparison</p>
        <p style='font-size: 0.9em; color: #999;'>Powered by Advanced NLP & Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs with custom styling
tab1, tab2, tab3 = st.tabs(["📄 Resume Analysis", "💼 Job Matching", "📊 Batch Compare"])

# ============ TAB 1: Resume Analysis ============
with tab1:
    st.markdown("### 📄 Resume Parser & Analyzer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF or TXT)",
            type=["pdf", "txt"],
            help="Drag and drop your resume file here"
        )
    
    with col2:
        st.markdown("""
            **📋 Supported Formats:**
            - 📄 PDF files
            - 📝 Text files
        """)
    
    if uploaded_file:
        # Extract text
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_txt(uploaded_file)
        
        resume_text = clean_text(resume_text)
        
        if resume_text:
            # Show loading animation
            with st.spinner("🔍 Analyzing resume..."):
                results = processor.process_resume(resume_text)
            
            # Success message
            st.success("✅ Resume analyzed successfully!")
            
            # ========== Contact Information ==========
            st.markdown("<div class='section-header'><h3>📧 Contact Information</h3></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if results["email"]:
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; color: white; text-align: center;'>
                            <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>📧 Email</p>
                            <p style='margin: 5px 0 0 0; font-size: 0.85em; word-break: break-all;'>{results['email'][0]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No email found")
            
            with col2:
                if results["phone"]:
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 10px; color: white; text-align: center;'>
                            <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>📱 Phone</p>
                            <p style='margin: 5px 0 0 0; font-size: 0.85em;'>{results['phone'][0]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No phone found")
            
            with col3:
                if results["entities"]["PERSON"]:
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 15px; border-radius: 10px; color: white; text-align: center;'>
                            <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>👤 Name</p>
                            <p style='margin: 5px 0 0 0; font-size: 0.85em;'>{results['entities']['PERSON'][0]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("No name found")
            
            # ========== Skills Section ==========
            st.markdown("<div class='section-header'><h3>🛠️ Skills Extracted</h3></div>", unsafe_allow_html=True)
            
            skill_count = sum(len(skills) for skills in results["skills"].values())
            if skill_count > 0:
                # Skills visualization
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    for category, skills in results["skills"].items():
                        if skills:
                            st.markdown(f"**{category}**")
                            skills_html = ' '.join([f'<span class="skill-badge">{skill}</span>' for skill in skills])
                            st.markdown(f"<div>{skills_html}</div>", unsafe_allow_html=True)
                
                with col2:
                    # Skills pie chart
                    skill_data = {cat: len(skils) for cat, skils in results["skills"].items() if skils}
                    if skill_data:
                        fig = go.Figure(data=[go.Pie(
                            labels=list(skill_data.keys()),
                            values=list(skill_data.values()),
                            marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'])
                        )])
                        fig.update_layout(height=300, showlegend=True)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No skills detected in resume")
            
            # ========== Education Section ==========
            st.markdown("<div class='section-header'><h3>🎓 Education</h3></div>", unsafe_allow_html=True)
            
            if results["education"]:
                for i, edu in enumerate(results["education"][:5], 1):
                    st.markdown(f"""
                        <div style='background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 10px;'>
                            <strong>📚 {edu}</strong>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No education information found")
            
            # ========== Experience Section ==========
            st.markdown("<div class='section-header'><h3>💼 Experience Highlights</h3></div>", unsafe_allow_html=True)
            
            if results["experience"]:
                for i, exp in enumerate(results["experience"], 1):
                    st.markdown(f"""
                        <div style='background: rgba(245, 87, 108, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #f5576c; margin-bottom: 10px;'>
                            <strong>{i}.</strong> {exp}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No experience information found")
            
            # ========== Organizations & Dates ==========
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='section-header'><h3>🏢 Organizations</h3></div>", unsafe_allow_html=True)
                if results["entities"]["ORG"]:
                    for org in results["entities"]["ORG"][:5]:
                        st.markdown(f"🏢 **{org}**")
                else:
                    st.info("No organizations found")
            
            with col2:
                st.markdown("<div class='section-header'><h3>📅 Important Dates</h3></div>", unsafe_allow_html=True)
                if results["dates"]:
                    for date in results["dates"][:5]:
                        st.markdown(f"📅 **{date}**")
                else:
                    st.info("No dates found")
            
            # Raw text expander
            with st.expander("📋 View Raw Resume Text"):
                st.text_area("Resume Content", resume_text, height=200, disabled=True)

# ============ TAB 2: Job Matching ============
with tab2:
    st.markdown("### 💼 Resume to Job Description Matching")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Your Resume")
        resume_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "txt"],
            key="match_resume",
            help="Upload your resume for matching"
        )
    
    with col2:
        st.subheader("📝 Job Description")
        job_desc = st.text_area(
            "Paste Job Description",
            height=250,
            placeholder="Paste the job description here...",
            help="Paste the complete job description"
        )
    
    if resume_file and job_desc:
        with st.spinner("🔄 Matching resume to job description..."):
            # Extract resume text
            if resume_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = extract_text_from_txt(resume_file)
            
            resume_text = clean_text(resume_text)
            
            # Process resume
            results = processor.process_resume(resume_text)
            resume_skills = results["skills"]
            
            # Match
            matcher = JobMatcher(resume_skills, job_desc)
            match_report = matcher.get_match_report()
        
        st.success("✅ Matching complete!")
        
        # Display results in beautiful cards
        st.markdown("### 📊 Match Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);'>
                    <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>Skill Match Score</p>
                    <p style='margin: 10px 0 0 0; font-size: 2.5em; font-weight: 900;'>{match_report["skill_match"]["match_percentage"]}%</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 8px 32px rgba(245, 87, 108, 0.4);'>
                    <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>Semantic Similarity</p>
                    <p style='margin: 10px 0 0 0; font-size: 2.5em; font-weight: 900;'>{match_report["semantic_similarity"]}%</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            score = match_report["overall_score"]
            color = "#667eea" if score >= 70 else "#f5a623" if score >= 50 else "#f5576c"
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, {color} 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);'>
                    <p style='margin: 0; font-size: 0.9em; opacity: 0.9;'>Overall Score</p>
                    <p style='margin: 10px 0 0 0; font-size: 2.5em; font-weight: 900;'>{score}%</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Matched Skills
        st.markdown("### ✅ Matched Skills")
        matched = match_report["skill_match"]["matched_skills"]
        if matched:
            matched_html = ' '.join([f'<span class="skill-badge">{skill}</span>' for skill in matched])
            st.markdown(f"<div>{matched_html}</div>", unsafe_allow_html=True)
            st.success(f"✓ Found {len(matched)} matching skills")
        else:
            st.warning("No matching skills found")
        
        # Missing Skills
        st.markdown("### ❌ Missing Skills")
        missing = match_report["skill_match"]["missing_skills"]
        if missing:
            missing_html = ' '.join([f'<span class="skill-badge" style="background: linear-gradient(135deg, #f5576c 0%, #f5a623 100%)">{skill}</span>' for skill in missing])
            st.markdown(f"<div>{missing_html}</div>", unsafe_allow_html=True)
            st.error(f"✗ Missing {len(missing)} required skills")
        else:
            st.success("🎉 All required skills present!")

# ============ TAB 3: Batch Comparison ============
with tab3:
    st.markdown("### 📊 Compare Multiple Resumes")
    
    job_desc = st.text_area(
        "Job Description",
        height=180,
        placeholder="Paste the job description to compare candidates against...",
        help="This will be used to match all uploaded resumes"
    )
    
    uploaded_files = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload multiple resumes to compare them"
    )
    
    if job_desc and uploaded_files:
        with st.spinner(f"📊 Analyzing {len(uploaded_files)} resumes..."):
            results_list = []
            
            for resume_file in uploaded_files:
                # Extract text
                if resume_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(resume_file)
                else:
                    resume_text = extract_text_from_txt(resume_file)
                
                resume_text = clean_text(resume_text)
                parsed = processor.process_resume(resume_text)
                
                # Match
                matcher = JobMatcher(parsed["skills"], job_desc)
                match_report = matcher.get_match_report()
                
                results_list.append({
                    "Resume": resume_file.name,
                    "Skill Match %": match_report["skill_match"]["match_percentage"],
                    "Semantic Score": match_report["semantic_similarity"],
                    "Overall Score": match_report["overall_score"]
                })
        
        st.success(f"✅ Analyzed {len(uploaded_files)} resumes!")
        
        # Display as table
        df = pd.DataFrame(results_list).sort_values("Overall Score", ascending=False)
        
        # Style dataframe
        st.markdown("### 🏆 Ranking Results")
        st.dataframe(
            df.style.background_gradient(
                subset=['Overall Score', 'Skill Match %', 'Semantic Score'],
                cmap='RdYlGn'
            ),
            use_container_width=True
        )
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                df,
                x='Resume',
                y='Overall Score',
                color='Overall Score',
                color_continuous_scale=['#f5576c', '#f5a623', '#667eea'],
                title='Overall Scores Comparison'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df,
                x='Skill Match %',
                y='Semantic Score',
                size='Overall Score',
                hover_data=['Resume'],
                color='Overall Score',
                color_continuous_scale=['#f5576c', '#f5a623', '#667eea'],
                title='Skill Match vs Semantic Score'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top candidate highlight
        top_candidate = df.iloc[0]
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);'>
                <p style='margin: 0; font-size: 1.2em;'>🏆 Top Candidate</p>
                <p style='margin: 10px 0 0 0; font-size: 1.5em; font-weight: 900;'>{top_candidate['Resume']}</p>
                <p style='margin: 10px 0 0 0; font-size: 1.1em;'>Overall Score: <strong>{top_candidate['Overall Score']}%</strong></p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px; color: #999; border-top: 2px solid rgba(102, 126, 234, 0.3);'>
        <p>🚀 Powered by Advanced NLP & Machine Learning</p>
        <p style='font-size: 0.9em;'>Built with Streamlit • spaCy • scikit-learn</p>
        <p style='margin-top: 20px; font-size: 0.95em;'>
            <strong style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                Created by abbeycity
            </strong>
        </p>
        <p style='font-size: 0.85em; margin-top: 10px;'>
            <a href='https://www.linkedin.com/in/abiodun360of/' target='_blank' style='color: #667eea; text-decoration: none; margin: 0 10px;'>
                💼 LinkedIn
            </a> | 
            <a href='https://github.com/Abiodun360of' target='_blank' style='color: #667eea; text-decoration: none; margin: 0 10px;'>
                💻 GitHub
            </a> | 
            <a href='mailto:abiodun360of@gmail.com' style='color: #667eea; text-decoration: none; margin: 0 10px;'>
                📧 Email
            </a>
        </p>
    </div>
""", unsafe_allow_html=True)