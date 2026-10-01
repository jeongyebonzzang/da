import streamlit as st, json, uuid
from pathlib import Path
from datetime import date
st.set_page_config(page_title="2026년 다이어리 기록 모음.zip", page_icon="🎀", layout="wide")
D=Path("gallery_data"); I=D/"images"; W=D/"works.json"; M=D/"monthly.json"
D.mkdir(exist_ok=True); I.mkdir(exist_ok=True)
def load(p, default):
    try: return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
    except: return default
def save(p, data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
samples=[
{"id":"s1","title":"딸기 우유의 하루","date":"2026-09-01","category":"핑크 다꾸","description":"핑크빛으로 채워 본 오늘의 기록 ♡","image":"https://images.unsplash.com/photo-1455390582262-044cdead277a?w=900"},
{"id":"s2","title":"소녀의 작은 취향","date":"2026-09-05","category":"인물 다꾸","description":"좋아하는 스티커를 한가득 모아서.","image":"https://images.unsplash.com/photo-1517842645767-c639042777db?w=900"}]
if "works" not in st.session_state: st.session_state.works=load(W,samples)
if "monthly" not in st.session_state: st.session_state.monthly=load(M,[])
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
html,body,[class*="css"]{font-family:'Gowun Dodum',sans-serif}.stApp{background:#FFF8FA}
.block-container{max-width:1200px;padding-top:1rem}.hero{background:linear-gradient(135deg,#FFD1DC,#FFF0F4,#E5DDFB);border:1px solid #F8DCE5;border-radius:26px;padding:clamp(28px,6vw,55px) 18px;text-align:center;margin-bottom:22px}
.hero h1{color:#A94F72;font-size:clamp(28px,5vw,48px)}.hero p{color:#98677D}.tag{display:inline-block;background:white;color:#B75B7C;padding:7px 13px;border-radius:30px;margin:4px;font-size:13px}
div.stButton>button,div.stFormSubmitButton>button{background:#FFD1DC;color:#934965;border:0;border-radius:18px;min-height:2.7rem}
div.stButton>button:hover,div.stFormSubmitButton>button:hover{background:#F8BBD0;color:#823A58;border:0}
@media(max-width:640px){.block-container{padding:.8rem}.hero{padding:28px 12px}}
</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><p>♡ A LITTLE COLLECTION OF MY DAYS ♡</p><h1>2026년 다이어리<br>기록 모음.zip</h1><p>하루하루 모아 둔 작은 취향과 미소녀의 기록들.</p><span class="tag">#핑크다꾸</span><span class="tag">#미소녀다꾸</span><span class="tag">#다이어리아카이브</span><p>୨୧ ─────── ୨୧</p></div>',unsafe_allow_html=True)
page=st.radio("메뉴",["♡ 작품 갤러리","✿ 나의 먼슬리"],horizontal=True,label_visibility="collapsed")
if page=="♡ 작품 갤러리":
    works=st.session_state.works
    with st.expander("＋ 새로운 작품 등록하기"):
        with st.form("add",clear_on_submit=True):
            title=st.text_input("작품 제목"); dt=st.date_input("제작 날짜",value=date.today())
            cat=st.selectbox("카테고리",["핑크 다꾸","인물 다꾸","감성 다꾸","계절 다꾸","서포터즈","기타"])
            desc=st.text_area("작품 소개"); up=st.file_uploader("작품 사진",type=["jpg","jpeg","png","webp"])
            if st.form_submit_button("♡ 작품 전시하기"):
                if title.strip() and up:
                    f=I/f"{uuid.uuid4().hex}_{Path(up.name).name}"; f.write_bytes(up.getvalue())
                    works.insert(0,{"id":uuid.uuid4().hex,"title":title.strip(),"date":str(dt),"category":cat,"description":desc,"image":str(f)})
                    save(W,works); st.session_state.works=works; st.rerun()
                else: st.warning("제목과 사진을 입력해 주세요.")
    cats=["전체 작품"]+sorted({x.get("category","기타") for x in works})
    filt=st.selectbox("작품 모아보기",cats); items=[x for x in works if filt=="전체 작품" or x.get("category")==filt]
    cols=st.columns(3)
    for n,x in enumerate(items):
        with cols[n%3]:
            with st.container(border=True):
                st.image(x["image"],use_container_width=True); st.caption(f"♡ {x.get('category')} · {x.get('date')}")
                st.markdown("### "+x.get("title","")); st.write(x.get("description",""))
                with st.expander("✎ 작품 수정 / 사진 교체"):
                    with st.form("edit_"+x["id"]):
                        title2=st.text_input("제목",x.get("title",""),key="t"+x["id"])
                        dt2=st.date_input("날짜",date.fromisoformat(x.get("date",str(date.today()))),key="d"+x["id"])
                        opts=["핑크 다꾸","인물 다꾸","감성 다꾸","계절 다꾸","서포터즈","기타"]
                        old=x.get("category","기타")
                        cat2=st.selectbox("카테고리",opts,index=opts.index(old) if old in opts else 5,key="c"+x["id"])
                        desc2=st.text_area("소개",x.get("description",""),key="x"+x["id"])
                        up2=st.file_uploader("새 사진 선택 (선택)",type=["jpg","jpeg","png","webp"],key="u"+x["id"])
                        if st.form_submit_button("변경 사항 저장"):
                            x.update(title=title2,date=str(dt2),category=cat2,description=desc2)
                            if up2:
                                f=I/f"{uuid.uuid4().hex}_{Path(up2.name).name}"; f.write_bytes(up2.getvalue()); x["image"]=str(f)
                            save(W,works); st.session_state.works=works; st.rerun()
                if st.button("🗑 작품 삭제",key="del"+x["id"]):
                    st.session_state.works=[a for a in works if a["id"]!=x["id"]]; save(W,st.session_state.works); st.rerun()
else:
    st.markdown("## ✿ 나의 먼슬리")
    st.write("지난달의 일과 기억하고 싶은 순간을 휴대폰에서도 짧게 남겨 보세요. ♡")
    with st.form("month_add",clear_on_submit=True):
        a,b=st.columns(2)
        month=a.selectbox("기록할 월",[f"2026년 {m:02d}월" for m in range(1,13)],index=date.today().month-1)
        dt=b.date_input("날짜",value=date.today())
        mood=st.selectbox("오늘의 기분",["♡ 행복","☁ 평온","✿ 설렘","☆ 바쁨","☂ 조금 지침","🎀 특별한 날"])
        note=st.text_area("무엇을 했나요?",placeholder="예: 망원에서 다꾸 모임! 키스컷 나눔을 받았다 ♡",height=100)
        if st.form_submit_button("＋ 먼슬리에 기록하기"):
            if note.strip():
                st.session_state.monthly.insert(0,{"id":uuid.uuid4().hex,"month":month,"date":str(dt),"mood":mood,"note":note.strip()})
                save(M,st.session_state.monthly); st.rerun()
            else: st.warning("짧게라도 내용을 적어 주세요.")
    months=sorted({x["month"] for x in st.session_state.monthly},reverse=True)
    if months:
        chosen=st.selectbox("기록 모아보기",months)
        for x in [e for e in st.session_state.monthly if e["month"]==chosen]:
            with st.container(border=True):
                st.caption(f'{x["date"]} · {x["mood"]}'); st.write(x["note"])
                if st.button("기록 삭제",key="md"+x["id"]):
                    st.session_state.monthly=[e for e in st.session_state.monthly if e["id"]!=x["id"]]; save(M,st.session_state.monthly); st.rerun()
    else: st.info("아직 기록이 없어요. 첫 번째 먼슬리를 작성해 보세요! 🎀")
st.markdown('<p style="text-align:center;color:#B77C91;padding:20px">♡ made with love · My little diary archive · 2026 ♡</p>',unsafe_allow_html=True)
