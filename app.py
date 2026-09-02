import time
import streamlit as st
from google import genai
from weasyprint import HTML

# Page Config
st.set_page_config(page_title="CTE Sub Plan Generator", page_icon="📝", layout="centered")

st.title("📝 CTE Sub Plan & Worksheet Generator")
st.write("Select your class details below to generate ready-to-print PDF lesson plans and worksheets.")

# Initialize Session State memory for persistent downloads
if "pdf_sub" not in st.session_state:
    st.session_state.pdf_sub = None
if "pdf_student" not in st.session_state:
    st.session_state.pdf_student = None
if "file_prefix" not in st.session_state:
    st.session_state.file_prefix = "CTE_Lesson"

# Sidebar for API Key
st.sidebar.header("Configuration")

# Check Streamlit Secrets first, otherwise fallback to text input
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success("🔑 API Key loaded from Secrets!")
else:
    api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Get your free API key at aistudio.google.com")

st.subheader("Lesson Parameters")
col1, col2 = st.columns(2)

with col1:
    cte_course = st.selectbox(
        "CTE Course / Trade",
        [
            "Auto Technology",
            "Culinary Arts",
            "Construction / Carpentry",
            "Welding & Fabrication",
            "Graphic Design & Digital Media",
            "Health Sciences / Nursing",
            "Cosmetology",
            "Agriculture / Vet Tech",
            "Business & Marketing",
            "Custom Trade..."
        ]
    )
    if cte_course == "Custom Trade...":
        cte_course = st.text_input("Specify Custom Trade:")

    wrs_skill = st.selectbox(
        "Workplace Readiness Skill (WRS)",
        [
            "Integrity & Ethics",
            "Workplace Safety & OSHA",
            "Teamwork & Collaboration",
            "Critical Thinking & Problem Solving",
            "Customer Service & Communication",
            "Time Management & Work Ethic",
            "Conflict Resolution"
        ]
    )

with col2:
    duration = st.number_input("Class Duration (Minutes)", min_value=15, max_value=180, value=50, step=5)
    custom_scenario = st.text_input("Optional Scenario Focus", placeholder="e.g., Hydraulic lift safety, knife safety")

generate_btn = st.button("🚀 Generate PDF Sub Package", use_container_width=True)

if generate_btn:
    if not api_key:
        st.error("Please enter your Gemini API key in the left sidebar to generate plans.")
    elif not cte_course:
        st.error("Please select or enter a CTE course.")
    else:
        try:
            with st.spinner("Writing lesson content & compiling PDF printables..."):
                client = genai.Client(api_key=api_key)

                prompt = f"""
                You are an expert high school CTE curriculum writer. Generate TWO separate, production-ready HTML documents for a lesson.

                COURSE: {cte_course}
                WRS SKILL: {wrs_skill}
                CLASS DURATION: {duration} minutes
                SPECIFIC SCENARIO: {custom_scenario if custom_scenario else "Create a realistic, trade-specific high-stakes ethical/safety scenario."}

                IMPORTANT QUESTION GRADE LEVEL REQUIREMENT:
                Write all four (4) written response questions strictly at an 8TH-GRADE READING LEVEL. Use clear, direct, concise sentences. Avoid complex academic jargon in the questions while still requiring students to think critically about trade safety and decision-making.

                FORMAT REQUIREMENT: Output EXACTLY two raw HTML code blocks separated by the exact delimiter text `===SPLIT_HERE===`. Do not include conversational text or Markdown outside these blocks.

                --- HTML DOCUMENT 1 (SUB PLAN) BLUEPRINT ---
                <!DOCTYPE html>
                <html><head><style>
                    @page {{ size: A4; margin: 20mm 15mm; background-color: #f4f6f9; }}
                    body {{ font-family: Helvetica, Arial, sans-serif; color: #333; line-height: 1.6; }}
                    .header {{ background-color: #1e3a8a; color: white; padding: 20px; margin: -20mm -15mm 20px -15mm; text-align: center; }}
                    h1 {{ margin: 0; font-size: 22pt; }}
                    h2 {{ color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 5px; margin-top: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; background-color: white; }}
                    th, td {{ border: 1px solid #cdd5e0; padding: 10px; text-align: left; }}
                    th {{ background-color: #e2e8f0; color: #1e3a8a; }}
                    .script-box {{ background-color: #eef2ff; border: 1px dashed #1e3a8a; padding: 15px; font-style: italic; }}
                </style></head><body>
                    <div class="header"><h1>Substitute Teacher Lesson Plan</h1><p>CTE - Grades 10-12 | {cte_course} - {wrs_skill}</p></div>
                    <h2>1. Schedule Overview ({duration}-Minute Period)</h2>
                    <table><tr><th>Time</th><th>Activity</th><th>Instructions</th></tr>
                    <tr><td>0-5 min</td><td>Attendance & Intro</td><td>Read the script below.</td></tr>
                    <tr><td>5-10 min</td><td>Distribute</td><td>Hand out worksheets (no computers needed).</td></tr>
                    <tr><td>10-25 min</td><td>Silent Reading</td><td>Students read independently.</td></tr>
                    <tr><td>25-45 min</td><td>Written Responses</td><td>Students answer questions on paper.</td></tr>
                    <tr><td>45-{duration} min</td><td>Collection</td><td>Collect worksheets at the bell.</td></tr></table>
                    <h2>2. Substitute Script (Read Aloud)</h2>
                    <div class="script-box">[Generate 2-minute cognitive science read-aloud script framing high-stress decisions]</div>
                    <h2>3. Classroom Management</h2>
                    <p>Paper-based lesson. No student tech required. Collect all completed worksheets at the bell.</p>
                </body></html>

                ===SPLIT_HERE===

                --- HTML DOCUMENT 2 (STUDENT WORKSHEET) BLUEPRINT ---
                <!DOCTYPE html>
                <html><head><style>
                    @page {{ size: A4; margin: 15mm; }}
                    body {{ font-family: Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.6; font-size: 10pt; }}
                    .header-table {{ width: 100%; border-bottom: 2px solid #1e3a8a; margin-bottom: 12px; padding-bottom: 6px; }}
                    .title {{ text-align: center; font-size: 16pt; font-weight: bold; color: #0f172a; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.5px; }}
                    .instructions {{ background-color: #f1f5f9; border-left: 4px solid #1e3a8a; padding: 10px 14px; margin-bottom: 14px; font-style: italic; font-size: 9.5pt; color: #334155; border-radius: 0 4px 4px 0; }}
                    .version-card {{ background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px 14px; margin-bottom: 14px; }}
                    .version-title {{ font-size: 10.5pt; font-weight: bold; color: #1e3a8a; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
                    .version-card p {{ margin: 0; line-height: 1.55; text-align: justify; }}
                    h2 {{ font-size: 14pt; color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 4px; margin-top: 10px; margin-bottom: 14px; text-transform: uppercase; }}
                    .q-box {{ margin-bottom: 14px; }}
                    .q-title {{ font-weight: bold; color: #0f172a; margin-bottom: 4px; font-size: 10pt; }}
                    .line {{ border-bottom: 1px solid #94a3b8; height: 23px; width: 100%; }}
                </style></head><body>
                    <table class="header-table"><tr>
                        <td style="width: 60%;"><strong>Name:</strong> ___________________<br><strong>Date:</strong> _______ <strong>Period:</strong> ___</td>
                        <td style="text-align: right;"><strong>{cte_course}</strong><br>{wrs_skill}</td>
                    </tr></table>
                    <div class="title">[Insert Creative Case Study Title]</div>
                    <div class="instructions">Following are two versions of the same scenario. Choose one to read, then proceed to the back page to answer all four analytical questions in full sentences.</div>
                    
                    <div class="version-card">
                        <div class="version-title">Version A: Standard Level</div>
                        <p>[Write 350-word, 7th-8th grade reading level scenario contextualized to {cte_course}]</p>
                    </div>

                    <div class="version-card">
                        <div class="version-title">Version B: Enrichment Level</div>
                        <p>[Write 450-word, 11th-12th grade reading level scenario contextualized to {cte_course}]</p>
                    </div>

                    <div style="page-break-before: always;"></div>
                    <h2>Written Responses</h2>
                    
                    <div class="q-box">
                        <p class="q-title">1. Identify the Main Problem:</p>
                        <p style="margin:0 0 6px 0; font-size: 9.5pt; color: #475569;">[Write an 8th-grade level trade-specific question asking students to explain what went wrong and why it was dangerous]</p>
                        <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    </div>

                    <div class="q-box">
                        <p class="q-title">2. Better Choices:</p>
                        <p style="margin:0 0 6px 0; font-size: 9.5pt; color: #475569;">[Write an 8th-grade level question asking what safe choices the worker should have made instead of rushing]</p>
                        <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    </div>

                    <div class="q-box">
                        <p class="q-title">3. Handling Workplace Pressure:</p>
                        <p style="margin:0 0 6px 0; font-size: 9.5pt; color: #475569;">[Write an 8th-grade level question asking how pressure from time or coworkers affected the decision]</p>
                        <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    </div>

                    <div class="q-box">
                        <p class="q-title">4. Speak Up (Script Your Answer):</p>
                        <p style="margin:0 0 6px 0; font-size: 9.5pt; color: #475569;">[Write an 8th-grade level prompt asking students to write two respectful sentences refusing to do something unsafe]</p>
                        <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    </div>
                </body></html>
                """

                # Retry loop with fallbacks for high-traffic server errors (503)
                models_to_try = ['gemini-3.6-flash', 'gemini-2.5-flash']
                response = None
                last_exception = None

                for model_name in models_to_try:
                    for attempt in range(2):
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt
                            )
                            if response and response.text:
                                break
                        except Exception as err:
                            last_exception = err
                            if "503" in str(err) or "UNAVAILABLE" in str(err):
                                time.sleep(3)
                                continue
                            else:
                                raise err
                    if response and response.text:
                        break

                if not response or not response.text:
                    raise last_exception or Exception("Server busy. Please try again in a few moments.")

                raw_text = response.text
                if "===SPLIT_HERE===" in raw_text:
                    parts = raw_text.split("===SPLIT_HERE===")
                    html_sub = parts[0].replace("```html", "").replace("```", "").strip()
                    html_student = parts[1].replace("```html", "").replace("```", "").strip()

                    # Save PDFs into persistent session state memory
                    st.session_state.pdf_sub = HTML(string=html_sub).write_pdf()
                    st.session_state.pdf_student = HTML(string=html_student).write_pdf()
                    st.session_state.file_prefix = cte_course.replace(' ', '_')

                else:
                    st.error("Error formatting documents. Please try clicking generate again.")
        except Exception as e:
            st.error(f"Google API is currently experiencing heavy traffic (503). Please wait 10 seconds and try again. Full log: {str(e)}")

# Always display the download buttons if PDFs are saved in memory
if st.session_state.pdf_sub and st.session_state.pdf_student:
    st.success("✨ Lesson Package Ready!")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="📄 Download Sub Plan (PDF)",
            data=st.session_state.pdf_sub,
            file_name=f"Sub_Plan_{st.session_state.file_prefix}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            label="📄 Download Student Worksheet (PDF)",
            data=st.session_state.pdf_student,
            file_name=f"Student_Worksheet_{st.session_state.file_prefix}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
