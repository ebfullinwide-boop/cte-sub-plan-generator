import streamlit as st
from google import genai
from weasyprint import HTML

# Page Config
st.set_page_config(page_title="CTE Sub Plan Generator", page_icon="📝", layout="centered")

st.title("📝 CTE Sub Plan & Worksheet Generator")
st.write("Select your class details below to generate ready-to-print PDF lesson plans and worksheets.")

# Sidebar for API Key
st.sidebar.header("Configuration")
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

                FORMAT REQUIREMENT: Output EXACTLY two raw HTML code blocks separated by the exact delimiter text `===SPLIT_HERE===`. Do not include conversational text or Markdown outside these blocks.

                --- HTML DOCUMENT 1 (SUB PLAN) BLUEPRINT ---
                <!DOCTYPE html>
                <html><head><style>
                    @page {{ size: A4; margin: 20mm 15mm; background-color: #f4f6f9; }}
                    body {{ font-family: Helvetica, sans-serif; color: #333; line-height: 1.6; }}
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
                    body {{ font-family: 'Georgia', serif; color: #222; line-height: 1.5; font-size: 11pt; }}
                    .header-table {{ width: 100%; border-bottom: 2px solid #222; margin-bottom: 20px; }}
                    .title {{ text-align: center; font-size: 18pt; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; }}
                    h2 {{ font-size: 14pt; border-bottom: 1px solid #ccc; margin-top: 15px; }}
                    h3 {{ font-size: 12pt; background-color: #eee; padding: 5px; margin-top: 15px; }}
                    .instructions {{ background-color: #f9f9f9; border: 1px solid #ddd; padding: 10px; font-style: italic; margin-bottom: 15px; }}
                    .line {{ border-bottom: 1px solid #a0aab5; height: 26px; width: 100%; }}
                </style></head><body>
                    <table class="header-table"><tr>
                        <td style="width: 60%;"><strong>Name:</strong> ___________________<br><strong>Date:</strong> _______ <strong>Period:</strong> ___</td>
                        <td style="text-align: right;"><strong>{cte_course}</strong><br>{wrs_skill}</td>
                    </tr></table>
                    <div class="title">[Insert Creative Case Study Title]</div>
                    <div class="instructions">Instructions: Choose one version to read, then answer the questions on the lines provided.</div>
                    <h3>Version A: Standard Level</h3>
                    <p>[Write 350-word, 7th-8th grade reading level scenario contextualized to {cte_course}]</p>
                    <h3>Version B: Enrichment Level</h3>
                    <p>[Write 450-word, 11th-12th grade reading level scenario contextualized to {cte_course}]</p>
                    <div style="page-break-before: always;"></div>
                    <h2>Written Responses</h2>
                    <p><strong>1. Analyze the Conflict:</strong> [Write Trade-specific question 1]</p>
                    <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    <p><strong>2. Evaluate the Options:</strong> [Write Question 2]</p>
                    <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    <p><strong>3. Workplace Psychology:</strong> [Write Question 3]</p>
                    <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                    <p><strong>4. Script the Conversation:</strong> [Write Question 4]</p>
                    <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
                </body></html>
                """

                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )

                raw_text = response.text
                if "===SPLIT_HERE===" in raw_text:
                    parts = raw_text.split("===SPLIT_HERE===")
                    html_sub = parts[0].replace("```html", "").replace("```", "").strip()
                    html_student = parts[1].replace("```html", "").replace("```", "").strip()

                    pdf_sub = HTML(string=html_sub).write_pdf()
                    pdf_student = HTML(string=html_student).write_pdf()

                    st.success("✨ Lesson Package Ready!")
                    col_dl1, col_dl2 = st.columns(2)
                    with col_dl1:
                        st.download_button(
                            label="📄 Download Sub Plan (PDF)",
                            data=pdf_sub,
                            file_name=f"Sub_Plan_{cte_course.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    with col_dl2:
                        st.download_button(
                            label="📄 Download Worksheet (PDF)",
                            data=pdf_student,
                            file_name=f"Student_Worksheet_{cte_course.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.error("Error formatting documents. Please try clicking generate again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
