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
                You are an expert CTE Curriculum Developer & Technical Writer. Generate TWO separate, production-ready HTML documents for a lesson package.

                COURSE: {cte_course}
                WRS SKILL: {wrs_skill}
                CLASS DURATION: {duration} minutes
                SPECIFIC SCENARIO: {custom_scenario if custom_scenario else "Create a realistic, trade-specific high-stakes ethical/safety scenario."}

                === MANDATORY WORKSHEET READABILITY & FORMATTING REQUIREMENTS ===

                1. SECTION LABELS:
                   - Label the two reading options exactly as:
                     • `Standard Reading`
                     • `Enrichment Reading`

                2. READABILITY & LANGUAGE TARGETS:
                   - Standard Reading: Write strictly at a 5TH-GRADE READING LEVEL. Use simple, direct, plain English words and short sentences. DO NOT use administrative numbers (e.g., no OSHA code citations like 1910.242), legal terms (e.g., no "tort liability"), or heavy corporate jargon.
                   - Enrichment Reading: Write at a high school technical level. Focus on real trade mechanics, equipment specs, and material science, but avoid dry legal citations or academic bureaucracy. Keep it scannable, engaging, and practical.

                3. STRUCTURAL CHUNKING:
                   - Break continuous narrative paragraphs into logical, short sections using bold subheadings (e.g., ### Context & Time Crunch, ### The Technical Dilemma, ### Supervisor Pressure & Failure).
                   - Strictly limit each narrative section paragraph to a MAXIMUM of 2-3 sentences.

                4. TECHNICAL CALLOUT BOX:
                   - Position a summary callout block (<div class="callout-box">) at the top of EACH version detailing:
                     • Job & Equipment: [e.g., Roof Truss Installation / Vehicle Service]
                     • Key Hardware: [e.g., Structural Screws vs. Framing Nails]
                     • Critical Failure: [e.g., Fastener snapping under heavy load]
                     • Safety Hazard: [e.g., Structural collapse, serious injury]

                5. VISUAL SCAFFOLDING & BOLDING:
                   - Bold all critical trade tools, mechanical parts, spec values, and ethical choices (e.g., <b>structural screws</b>, <b>framing nails</b>, <b>500 lbs</b>, <b>impact driver</b>).

                6. QUESTION GRADE LEVEL:
                   - Write all four (4) written response questions strictly at a clear, direct 8TH-GRADE READING LEVEL.

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
                    @page {{ size: A4; margin: 12mm 15mm; }}
                    body {{ font-family: Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.45; font-size: 9.5pt; }}
                    .header-table {{ width: 100%; border-bottom: 2px solid #1e3a8a; margin-bottom: 8px; padding-bottom: 4px; }}
                    .title {{ text-align: center; font-size: 14pt; font-weight: bold; color: #0f172a; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px; }}
                    .instructions {{ background-color: #f1f5f9; border-left: 4px solid #1e3a8a; padding: 6px 10px; margin-bottom: 10px; font-style: italic; font-size: 8.5pt; color: #334155; border-radius: 0 4px 4px 0; }}
                    
                    .version-card {{ background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px 12px; margin-bottom: 12px; }}
                    .version-title {{ font-size: 10pt; font-weight: bold; color: #1e3a8a; border-bottom: 1.5px solid #cbd5e1; padding-bottom: 3px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
                    
                    .callout-box {{ background-color: #f0f9ff; border: 1px solid #bae6fd; border-left: 3.5px solid #0284c7; padding: 6px 8px; margin-bottom: 8px; font-size: 8.5pt; border-radius: 3px; color: #0369a1; line-height: 1.35; }}
                    .callout-box strong {{ color: #0c4a6e; }}
                    
                    .subheading {{ font-size: 8.5pt; font-weight: bold; color: #0f172a; margin-top: 6px; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 0.3px; }}
                    .version-card p {{ margin: 0 0 4px 0; line-height: 1.4; text-align: left; }}
                    
                    h2 {{ font-size: 12pt; color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 3px; margin-top: 8px; margin-bottom: 10px; text-transform: uppercase; }}
                    .q-box {{ margin-bottom: 10px; }}
                    .q-title {{ font-weight: bold; color: #0f172a; margin-bottom: 2px; font-size: 9pt; }}
                    .line {{ border-bottom: 1px solid #94a3b8; height: 21px; width: 100%; }}
                </style></head><body>
                    <table class="header-table"><tr>
                        <td style="width: 60%;"><strong>Name:</strong> ___________________<br><strong>Date:</strong> _______ <strong>Period:</strong> ___</td>
                        <td style="text-align: right;"><strong>{cte_course}</strong><br>{wrs_skill}</td>
                    </tr></table>
                    <div class="title">[Insert Creative Case Study Title]</div>
                    <div class="instructions">Following are two versions of the same scenario. Choose one to read, then proceed to the back page to answer all four analytical questions in full sentences.</div>
                    
                    <div class="version-card">
                        <div class="version-title">Standard Reading</div>
                        <div class="callout-box">
                            <strong>Job & Equipment:</strong> [Insert Simple Details]<br>
                            <strong>Key Hardware:</strong> [Insert Simple Details]<br>
                            <strong>Critical Failure:</strong> [Insert Simple Details]<br>
                            <strong>Safety Hazard:</strong> [Insert Simple Details]
                        </div>
                        <div class="subheading">Context & Time Crunch</div>
                        <p>[2-3 short, simple 5th-grade sentences. Bold key tools, specs, and parts.]</p>
                        <div class="subheading">The Technical Dilemma</div>
                        <p>[2-3 short, simple 5th-grade sentences explaining the problem and shortcut.]</p>
                        <div class="subheading">Supervisor Pressure & Failure</div>
                        <p>[2-3 short, simple 5th-grade sentences detailing the rush, wrong choice, and safety result.]</p>
                    </div>

                    <div class="version-card">
                        <div class="version-title">Enrichment Reading</div>
                        <div class="callout-box">
                            <strong>Job & Equipment:</strong> [Insert Technical Details]<br>
                            <strong>Key Hardware:</strong> [Insert Hardware Specs]<br>
                            <strong>Critical Failure:</strong> [Insert Mechanical Failure]<br>
                            <strong>Safety Hazard:</strong> [Insert Hazard Details]
                        </div>
                        <div class="subheading">Operational Context & Pressure</div>
                        <p>[2-3 short sentences using clear trade vocabulary with bolding.]</p>
                        <div class="subheading">Material Mechanics & Shortcut</div>
                        <p>[2-3 short sentences explaining tool limits and material specs.]</p>
                        <div class="subheading">Boss Pressure & System Failure</div>
                        <p>[2-3 short sentences detailing time pressure, shortcut decision, and catastrophic failure.]</p>
                    </div>

                    <div style="page-break-before: always;"></div>
                    <h2>Written Responses</h2>
                    
                    <div class="q-box">
                        <p class="q-title">1. Identify the Main Hazard:</p>
                        <p style="margin:0 0 4px 0; font-size: 8.5pt; color: #475569;">[Write an 8th-grade level trade question asking what went wrong mechanically and why it was dangerous]</p>
                        <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    </div>

                    <div class="q-box">
                        <p class="q-title">2. Safe Alternatives:</p>
                        <p style="margin:0 0 4px 0; font-size: 8.5pt; color: #475569;">[Write an 8th-grade level question asking what safe choices the worker should have made instead of taking a shortcut]</p>
                        <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    </div>

                    <div class="q-box">
                        <p class="q-title">3. Workplace Culture & Pressure:</p>
                        <p style="margin:0 0 4px 0; font-size: 8.5pt; color: #475569;">[Write an 8th-grade level question asking how rush deadlines or supervisor pressure changed their choices]</p>
                        <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    </div>

                    <div class="q-box">
                        <p class="q-title">4. Professional Scripting:</p>
                        <p style="margin:0 0 4px 0; font-size: 8.5pt; color: #475569;">[Write an 8th-grade level prompt asking students to write a two-sentence polite refusal to perform an unsafe task]</p>
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
