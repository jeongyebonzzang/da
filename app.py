import streamlit as st
import json
import uuid
from datetime import date
from pathlib import Path

st.set_page_config(
    page_title="2026년 다이어리 기록 모음.zip",
    page_icon="🎀",
    layout="wide"
)

DATA_DIR = Path("gallery_data")
IMAGE_DIR = DATA_DIR / "images"
DATA_FILE = DATA_DIR / "works.json"
DATA_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(exist_ok=True)

def load_works():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [
        {
            "id": "sample1",
            "title": "딸기 우유의 하루",
            "date": "2026-09-01",
            "category": "핑크 다꾸",
            "description": "핑크빛으로 채워 본 오늘의 기록 ♡",
            "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=900"
        },
        {
            "id": "sample2",
            "title": "소녀의 작은 취향",
            "date": "2026-09-05",
            "category": "인물 다꾸",
            "description": "좋아하는 스티커를 한가득 모아서.",
            "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?w=900"
        },
        {
            "id": "sample3",
            "title": "파스텔 메모리",
            "date": "2026-09-12",
            "category": "감성 다꾸",
            "description": "그날의 분위기를 담아 두기.",
            "image": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=900"
        }
    ]

def save_works(works):
    DATA_FILE.write_text(
        json.dumps(works, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

if "works" not in st.session_state:
    st.session_state.works = load_works()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
html, body, [class*="css"] { font-family: 'Gowun Dodum', sans-serif; }
.stApp { background: #FFF8FA; }
.block-container { max-width: 1200px; padding-top: 2rem; }
.hero {
    background: linear-gradient(135deg, #FFD1DC, #FFF0F4, #E5DDFB);
    border: 1px solid #F8DCE5; border-radius: 28px;
    padding: 55px 20px; text-align: center; margin-bottom: 30px;
}
.hero h1 { color: #A94F72; font-size: clamp(28px, 5vw, 48px); font-weight: 700; }
.hero p { color: #98677D; font-size: 16px; }
.tag {
    display: inline-block; background: white; color: #B75B7C;
    padding: 7px 15px; border-radius: 30px; margin: 5px; font-size: 13px;
}
div.stButton > button {
    background: #FFD1DC; color: #9D4D6C; border: none; border-radius: 20px;
    font-weight: bold;
}
div.stButton > button:hover { background: #F8BBD0; color: #8A3D5B; border: none; }
h2, h3 { color: #A94F72; }
@media (max-width: 640px) {
    .block-container { padding: 1rem; }
    .hero { padding: 35px 12px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <p>♡ A LITTLE COLLECTION OF MY DAYS ♡</p>
    <h1>2026년 다이어리<br>기록 모음.zip</h1>
    <p>하루하루 모아 둔 작은 취향과 미소녀의 기록들.</p>
    <span class="tag">#핑크다꾸</span>
    <span class="tag">#미소녀다꾸</span>
    <span class="tag">#다이어리아카이브</span>
    <p style="margin-top:20px;">୨୧ ─────── ୨୧</p>
</div>
""", unsafe_allow_html=True)

works = st.session_state.works
c1, c2, c3 = st.columns(3)
c1.metric("COLLECTION", f"{len(works):02d}")
c2.metric("YEAR", "2026")
c3.metric("MOOD", "♡ PINK ♡")
st.divider()

with st.expander("＋ 새로운 작품 등록하기"):
    with st.form("add_work", clear_on_submit=True):
        title = st.text_input("작품 제목", placeholder="예: 딸기 우유의 하루")
        work_date = st.date_input("제작 날짜", value=date.today())
        category = st.selectbox(
            "카테고리",
            ["핑크 다꾸", "인물 다꾸", "감성 다꾸", "계절 다꾸", "서포터즈", "기타"]
        )
        description = st.text_area("작품 소개", placeholder="오늘의 다꾸 기록을 남겨 주세요 ♡")
        uploaded = st.file_uploader("작품 사진", type=["jpg", "jpeg", "png", "webp"])
        submitted = st.form_submit_button("♡ 작품 전시하기")

        if submitted:
            if not title or uploaded is None:
                st.warning("작품 제목과 사진을 모두 입력해 주세요!")
            else:
                filename = f"{uuid.uuid4().hex}_{Path(uploaded.name).name}"
                filepath = IMAGE_DIR / filename
                filepath.write_bytes(uploaded.getvalue())
                new_work = {
                    "id": uuid.uuid4().hex,
                    "title": title,
                    "date": str(work_date),
                    "category": category,
                    "description": description,
                    "image": str(filepath)
                }
                works.insert(0, new_work)
                save_works(works)
                st.session_state.works = works
                st.success("새로운 작품이 전시되었어요! 🎀")
                st.rerun()

categories = ["전체 작품"] + sorted(set(w["category"] for w in works))
selected = st.selectbox("작품 모아보기", categories)
filtered = [w for w in works if selected == "전체 작품" or w["category"] == selected]
st.markdown(f"#### ୨୧ {selected} · {len(filtered)} works")

columns = st.columns(3)
for i, work in enumerate(filtered):
    with columns[i % 3]:
        with st.container(border=True):
            st.image(work["image"], use_container_width=True)
            st.caption(f"♡ {work['category']} · {work['date']}")
            st.markdown(f"### {work['title']}")
            st.write(work["description"])
            with st.expander("작품 자세히 보기"):
                st.image(work["image"], use_container_width=True)
                st.write(work["description"])
                st.caption("A little piece of my diary ♡")

st.divider()
st.markdown("""
<div style="text-align:center; color:#B77C91; padding:25px;">
    ♡ made with love ♡<br>
    My little diary archive · 2026
</div>
""", unsafe_allow_html=True)
