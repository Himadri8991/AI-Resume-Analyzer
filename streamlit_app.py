import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import requests
from streamlit_lottie import st_lottie
from analyzer import analyze_resume

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# CONFIG
st.set_page_config(
    page_title="PI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS (Glassmorphism & Gradients & Animations)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

body {
    background: linear-gradient(-45deg, #090B10, #161B22, #0D162B, #110B17);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #e5e7eb;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background-color: transparent;
}

/* Glassmorphism Card Style */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(0, 255, 213, 0.3);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #00FFD5, #00A3FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    font-size: 1rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.header-title {
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    background: -webkit-linear-gradient(45deg, #FF007A, #7000FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}

.header-subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 1.2rem;
    margin-top: 5px;
    margin-bottom: 40px;
}

/* Fix for streamlittables */
.dataframe {
    background: rgba(0, 0, 0, 0.2) !important;
}

/* Radar & Gauge Fixes */
.js-plotly-plot .plotly .main-svg {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### PI (Pentaverse India) 🌌")
    st.markdown("#### Enterprise AI Hiring Core")
    
    st.markdown("---")
    st.markdown("### 🛠 Options")
    
    mode = st.radio("Pipeline Mode", ["Standard Search", "Candidate Comparison Mode"])
    
    st.markdown("---")
    st.markdown("### 📌 Batch Scale")
    st.caption("Engine supports up to 1000 resumes concurrently via SBERT.")
    
    st.markdown("---")
    st.caption("© 2026 PI | Built locally")

# HEADER
st.markdown('<div class="header-title">PI Resume Analyzer Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Scan, Match, and Hire. Powered by O*NET AI & SBERT.</div>', unsafe_allow_html=True)

# Lottie Animation
lottie_ai = load_lottieurl("https://lottie.host/8e1f5869-d464-42b3-9eb4-6e690f055a40/5s15lV5oUv.json")
if lottie_ai:
    st_lottie(lottie_ai, height=200, key="ai_animation")
else:
    # Fallback to a different cool space tech lottie if the first fails
    lottie_fallback = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_tno6cg2w.json")
    if lottie_fallback:
        st_lottie(lottie_fallback, height=200, key="ai_fallback")

# INPUT SECTION
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📂 1. Upload Candidates")
    resume_files = st.file_uploader(
        "Supports PDF & DOCX formats (Up to 1000 files)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

with col2:
    st.markdown("### 📄 2. Define Requirements (Optional)")
    job_desc = st.text_area("Paste Job Description (If left blank, AI auto-detects best jobs from Resumes)", height=150)

# ANIMATED PROCESSING
if st.button("🚀 INITIATE SCAN", use_container_width=True, type="primary"):

    if not resume_files:
        st.error("⚠️ Please upload at least one candidate resume.")
    else:
        results = []
        
        # UI Element for Progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # SBERT cache for JD to speed up batch processing of 1000 resumes
        cached_job_emb = None
        
        start_time = time.time()
        
        for i, file in enumerate(resume_files):
            status_text.write(f"🧬 Scanning structure for: {file.name} ({i+1}/{len(resume_files)})")
            
            # For the first run, job_emb gets generated and we cache it
            result = analyze_resume(file, file.name, job_description=job_desc, job_emb=cached_job_emb)
            
            if "error" in result:
                st.error(f"Error in {file.name}: {result['error']}")
                continue
                
            if i == 0 and "job_emb_cache" in result:
                cached_job_emb = result["job_emb_cache"]
                
            results.append(result)
            progress_bar.progress((i + 1) / len(resume_files))
            
        end_time = time.time()
        status_text.empty()
        st.success(f"✅ AI Analysis Complete! Processed {len(results)} resumes in {round(end_time - start_time, 2)}s")
        st.markdown("---")
        
        # ---------------------------------------------
        # UI DASHBOARD
        # ---------------------------------------------
        
        # Candidate Leaderboard
        st.markdown("### 🏆 Recruitment Leaderboard")
        ranked = sorted([r for r in results if not r.get('error')], key=lambda x: x["ats_score"], reverse=True)
        
        # Dataframe View
        df_display = pd.DataFrame([{
            "Rank": idx + 1,
            "Name / File": r['name'][:30],
            "ATS Score": f"{r['ats_score']}%",
            "Similarity": f"{r['similarity_score']}%",
            "Experience": f"{r['experience']} yrs",
            "Top Job Match": r['matched_roles'][0]['job_title'] if r['matched_roles'] else "Unknown"
        } for idx, r in enumerate(ranked)])
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        if mode == "Candidate Comparison Mode" and len(ranked) > 1:
            st.markdown("---")
            st.markdown("### ⚖️ Head-to-Head Comparison")
            
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='glass-card'><h4>🥇 #1 {ranked[0]['name']}</h4><b>ATS Score:</b> {ranked[0]['ats_score']}%<br><b>Exp:</b> {ranked[0]['experience']}y<br><b>Skills:</b> {len(ranked[0]['skills'])}</div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='glass-card'><h4>🥈 #2 {ranked[1]['name']}</h4><b>ATS Score:</b> {ranked[1]['ats_score']}%<br><b>Exp:</b> {ranked[1]['experience']}y<br><b>Skills:</b> {len(ranked[1]['skills'])}</div>", unsafe_allow_html=True)

            # Comparative Radar Chart
            fig = go.Figure()
            
            categories = ['ATS Score', 'Similarity Match', 'Experience Factor', 'Skill Volume', 'Education Tier']
            
            for idx in [0, 1]:
                vol = min(len(ranked[idx]['skills']) * 4, 100) # Arbitrary scale for chart
                exp = min(ranked[idx]['experience'] * 10, 100)
                edu = 80 if ranked[idx]['education'] else 40
                
                fig.add_trace(go.Scatterpolar(
                      r=[ranked[idx]['ats_score'], ranked[idx]['similarity_score'], exp, vol, edu],
                      theta=categories,
                      fill='toself',
                      name=f"Rank {idx+1}: {ranked[idx]['name']}"
                ))

            fig.update_layout(
              polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
              showlegend=True,
              paper_bgcolor='rgba(0,0,0,0)',
              plot_bgcolor='rgba(0,0,0,0)',
              font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("### 👤 Detailed Deep-Dives")

        cats = [r['name'] for r in ranked]
        selected_cand = st.selectbox("Select Candidate to view full profile:", cats)
        
        for r in ranked:
            if r['name'] == selected_cand:
                
                # Top Metrics Card
                colA, colB, colC = st.columns(3)
                with colA:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <div class="metric-label">ATS Optimization</div>
                        <div class="metric-value">{r['ats_score']}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with colB:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <div class="metric-label">Domain Match</div>
                        <div class="metric-value">{r['similarity_score']}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with colC:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <div class="metric-label">Detected Experience</div>
                        <div class="metric-value">{r['experience']} <span style='font-size:1rem;color:#ccc;'>Yrs</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                
                c_info, c_jobs = st.columns([1, 1])
                
                with c_info:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown("#### 🧬 Verified Entity Data")
                    st.write(f"**Email:** {r['email'] or 'Not detected'}")
                    st.write(f"**Phone:** {r['phone'] or 'Not detected'}")
                    st.write(f"**Degrees:** {', '.join(r['education']) or 'Not explicitly detected'}")
                    
                    st.markdown("#### 💡 Missing Core Skills")
                    if r['missing_skills']:
                        st.caption(", ".join(r['missing_skills'][:10]))
                    else:
                        st.success("None! 100% Core Skill Coverage.")
                        
                    st.markdown("#### 🎯 AI Recommendations")
                    for s in r['suggestions']:
                        st.info(s)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                with c_jobs:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown("#### 🔍 Best O*NET Framework Matches (Local Inference)")
                    
                    if r['matched_roles']:
                        for match in r['matched_roles'][:3]:
                            st.write(f"- **{match['job_title']}** ({match['sub_category']}) — Match Rate: {match['match_score']}%")
                            
                        # Bullet chart for best match
                        best_match = r['matched_roles'][0]
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = best_match['match_score'],
                            title = {'text': f"Affinity: {best_match['job_title']}"},
                            gauge = {
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "#00FFD5"},
                                'steps': [
                                    {'range': [0, 50], 'color': "rgba(255,255,255,0.05)"},
                                    {'range': [50, 80], 'color': "rgba(255,255,255,0.1)"}]
                            }))
                        fig.update_layout(height=250, margin=dict(l=20, r=20, b=20, t=50), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.write("Insufficient data for O*NET mapping.")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Skill Pills
                st.markdown('<div class="glass-card"><h4>🧠 Discovered Skills Ecosystem</h4>', unsafe_allow_html=True)
                skills_html = ""
                for skill in r['skills']:
                    skills_html += f"<span style='background:#1f2937; padding: 5px 12px; margin: 4px; border-radius: 15px; border: 1px solid #374151; display: inline-block;'>{skill}</span>"
                st.markdown(skills_html, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
        # Export logic
        st.markdown("### 📥 Download Reports")
        csv = df_display.to_csv(index=False)
        st.download_button(
            label="Download Complete Results (CSV)",
            data=csv,
            file_name="PI_Recruitment_Report.csv",
            mime="text/csv",
        )