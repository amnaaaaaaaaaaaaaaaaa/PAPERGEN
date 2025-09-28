import io
from datetime import date
import pandas as pd
import streamlit as st

from modules.paraphraser import Paraphraser, ParaphraseConfig
from modules.selector import derive_distribution, select_questions
from modules.pdf_builder import build_pdf

st.set_page_config(page_title="G12 Biology Paper Generator", page_icon="🧬", layout="centered")

@st.cache_resource
def load_paraphraser(enabled: bool, model_name: str):
    cfg = ParaphraseConfig(enabled=enabled, model_name=model_name)
    return Paraphraser(cfg)

@st.cache_data
def load_bank(path: str):
    df = pd.read_excel(path)
    df["chapter"] = df["chapter"].astype(str)
    df["marks"] = df["marks"].astype(int)
    df["question_text"] = df["question_text"].astype(str)
    if "difficulty" not in df.columns:
        df["difficulty"] = "medium"
    if "source" not in df.columns:
        df["source"] = ""
    return df

st.title("Grade 12 Biology — Question Paper Generator")
st.caption("Local, free, school-focused. Upload your bank or use the starter sample.")

df_bank = load_bank("data/questions.xlsx")

with st.sidebar:
    st.header("Paper Settings")
    school_name = st.text_input("School Name", "Your School Name")
    exam_title = st.text_input("Exam Title", "Biology Unit Test")
    class_name = st.text_input("Class", "XII")
    date_str = st.text_input("Date", date.today().isoformat())
    time_allowed = st.text_input("Time Allowed", "3 Hours")
    max_marks = st.number_input("Max Marks", min_value=10, max_value=100, value=70, step=1)
    seed = st.number_input("Random Seed", min_value=0, max_value=999999, value=42, step=1)

        # Always paraphrase in the background (hidden from user)
    df_sel = df_sel.copy()
    paraphraser = load_paraphraser(True, "tuner007/pegasus_paraphrase")
    df_sel["question_text"] = [
        paraphraser.paraphrase(q, level="medium") for q in df_sel["question_text"]
    ]


chapters = sorted(df_bank["chapter"].unique().tolist())
chosen_chapters = st.multiselect("Select chapters", chapters, default=chapters)

st.markdown("### Question Targets")
colA, colB = st.columns(2)
with colA:
    total_q = st.number_input("Total questions", min_value=0, max_value=200, value=10, step=1)
with colB:
    total_m = st.number_input("Total marks", min_value=0, max_value=1000, value=30, step=1)

c1, c2, c3, c5 = st.columns(4)
with c1: n1 = st.number_input("1-mark", min_value=0, max_value=200, value=0)
with c2: n2 = st.number_input("2-mark", min_value=0, max_value=200, value=0)
with c3: n3 = st.number_input("3-mark", min_value=0, max_value=200, value=0)
with c5: n5 = st.number_input("5-mark", min_value=0, max_value=200, value=0)

st.markdown("---")
if st.button(" Generate Question Paper (PDF)"):
    if (n1+n2+n3+n5)==0 and (total_q>0 or total_m>0):
        dist = derive_distribution(total_q, total_m)
    else:
        dist = {1:n1, 2:n2, 3:n3, 5:n5}

    df_sel = select_questions(df_bank, chosen_chapters, dist, seed=int(seed))
    if df_sel.empty:
        st.error("No questions available for chosen filters")
        st.stop()

    if enable_para:
        paraphraser = load_paraphraser(True, model_name)
        df_sel = df_sel.copy()
        df_sel["question_text"] = [paraphraser.paraphrase(q, level=level) for q in df_sel["question_text"]]

    meta = dict(
        school_name=school_name,
        exam_title=exam_title,
        class_name=class_name,
        time_allowed=time_allowed,
        max_marks=int(max_marks),
        date_str=date_str
    )
    pdf_path = f"output/{exam_title.replace(' ','_')}_{date_str}.pdf"
    build_pdf(df_sel, meta, pdf_path)
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button(" Download PDF", data=pdf_bytes, file_name=pdf_path.split("/")[-1], mime="application/pdf")

