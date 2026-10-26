import streamlit as st
import pandas as pd
import io

# 1. 페이지 기본 설정 (웹 브라우저 탭 설정)
st.set_page_config(page_title="디딤(DIDIM) UDL 3.0 지도안 생성기", layout="wide", page_icon="🏃")

st.title("🏃‍♂️ 디딤(DIDIM) 맞춤형 UDL 3.0 학습지도안 생성 플랫폼")
st.markdown("특수교육 및 일반교육 환경의 학습자 실태를 반영하여, 디딤(DIDIM) 에듀테크 기반의 일관성 있는 UDL 3.0 지도안을 자동 생성합니다.")

# ==========================================
# 사이드바: 학교 구분 및 기본 설정
# ==========================================
st.sidebar.header("⚙️ 기본 설정")
school_type = st.sidebar.radio("학교 구분", ["특수학교", "일반학교"])
grade = st.sidebar.text_input("학년/반", "고등부 3-1")
student_count = st.sidebar.number_input("학생 수 (명)", min_value=1, value=6) # 소규모 학급 기준

# ==========================================
# 섹션 1: 수업 기본 정보 (수정 가능)
# ==========================================
st.header("1. 수업 기본 정보 (수정 가능)")
col1, col2 = st.columns(2)
with col1:
    unit = st.text_input("단원/주제", "체육·사회 융합: 디딤을 활용한 기초 체력 증진 및 안전 규칙")
    topic = st.text_input("제재", "AR 바닥 투사를 활용한 협동 게임 및 횡단보도 건너기")
with col2:
    achievement = st.text_area("성취기준", 
        "[9체01-05] 자신의 체력을 진단하고 적합한 체력 관리 방법을 실천한다.\n"
        "[기본생활/사회] 일상생활의 안전 규칙(횡단보도 이용 등)을 알고 실제 상황에서 안전하게 행동할 수 있다.")

# ==========================================
# 섹션 2: 학습자 실태 및 특성 입력
# ==========================================
st.header("2. 학습자 실태 및 장애 특성")
if school_type == "특수학교":
    disability_type = st.multiselect("주요 장애 영역 (중복 선택 가능)", 
                                     ["지적장애", "자폐성장애", "지체장애", "시각장애", "청각장애", "정서행동장애"])
    support_needs = st.selectbox("신체 가동 범위 및 지원 요구도", 
                                 ["전신 활용 가능 (독립적 수행)", "상체 위주 활용 (부분 지원 필요)", "휠체어 사용 (도구 연계 필요)"])
    learner_profile = st.text_area("학습자 특성 상세 기록 (자유 기재)", 
                               "시청각 자극에 민감한 학생이 포함되어 있어 조도 조절(탈감작) 및 명시적 대기선 훈련이 필요함.")
else:
    disability_type = ["일반 (통합교육 대상자 포함)"]
    support_needs = st.selectbox("전반적 신체 활동 수준", ["우수", "보통", "기초 체력 증진 필요 (저체력)"])
    learner_profile = st.text_area("학습자 특성 상세 기록 (자유 기재)", 
                               "체육 활동에 소극적인 학생이 일부 있어 게이미피케이션 요소를 통한 흥미 유발이 필요함.")

# ==========================================
# 섹션 3: UDL 기반 수준별 학습목표
# ==========================================
st.header("3. UDL 3.0 기반 수준별 학습목표")
st.markdown("입력된 학습자 실태를 반영하여 목표가 자동 세팅됩니다. 상황에 맞게 수정하세요.")

goal_high = st.text_input("상 수준", f"디딤을 활용하여 친구들과 어울리며 {support_needs} 수준에 맞는 운동을 자발적으로 선택하고 수행할 수 있다.")
goal_mid = st.text_input("중 수준", "디딤의 시각적 지시를 이해하고, 친구들과 함께 질서를 지키며 기초적인 체력활동(예: F01 달리기)에 참여할 수 있다.")
goal_low = st.text_input("하 수준", "교사 및 또래의 촉구를 받아 디딤 활동 구역 내에서 안전하게 1가지 이상의 다감각 활동(예: B23 횡단보도 건너기)을 경험할 수 있다.")

# ==========================================
# 섹션 4: 환경, 안전 및 긍정적 행동지원계획(PBIS)
# ==========================================
st.header("4. 수업 환경, 안전 및 긍정적 행동지원계획(PBIS)")
col_env, col_pbis = st.columns(2)

with col_env:
    st.subheader("안전 및 환경 계획")
    env_plan = st.text_area("환경 설정 내용 (자동 설정 및 수정 가능)", 
        "1. 최소 공간 확보: 가로 6m x 세로 4m 확보 및 디딤 기기 수평 조절\n"
        "2. 충돌 방지: 센서 암 주변 및 인터랙션 활동 구역 모서리 안전 매트 설치\n"
        "3. 다감각 환경(Snoezelen) 조성: 프로젝터 가시성 확보 및 심리적 안정을 위한 암막 커튼 활용")

with col_pbis:
    st.subheader("긍정적 행동지원계획 (PBIS)")
    pbis_1 = st.checkbox("시각적 대기선(안전 테이프) 제공으로 순서 지키기 유도", value=True)
    pbis_2 = st.checkbox("빛/소리 리추얼화(점진적 조도 조절 등 탈감작)로 돌발행동 예방", value=True if school_type=="특수학교" else False)
    pbis_3 = st.checkbox("활동 성공 시 토큰(보상) 제공 및 앱 내 하이파이브 유도", value=True)
    pbis_4 = st.checkbox("멀티모드 또는 원격 제어를 통한 즉각적 시스템 중재(독점 방지)", value=True)
    custom_pbis = st.text_input("추가 행동지원 전략 직접 기입", "")

# ==========================================
# 섹션 5: UDL 3.0 설계 도식화 및 기대효과 (인포그래픽)
# ==========================================
st.header("5. UDL 3.0 설계 도식화 및 기대효과")
st.markdown("작성된 지도안의 UDL 균형과 예상 교육 효과를 시각적으로 확인하고 수정 지표로 삼으세요.")

col_udl1, col_udl2, col_udl3 = st.columns(3)
col_udl1.metric("1. 다중 참여 수단 (Engagement)", "85%", delta="흥미 유발 & 동기 부여")
col_udl1.info("적용 앱: H26 점프점프, B20 동물악단 등")
col_udl2.metric("2. 다중 표상 수단 (Representation)", "90%", delta="체화된 인지 & 다감각 제공")
col_udl2.info("적용 앱: B23 횡단보도 건너기, 하단 티커(Ticker) 기능")
col_udl3.metric("3. 다중 행동/표현 (Action)", "75%", delta="신체 움직임 및 대체 도구", delta_color="off")
col_udl3.warning("보완 권장: 휠체어 사용자를 위해 폼롤러나 막대를 이용한 상체 터치 룰 추가 고려")

st.progress(85) 

# ==========================================
# 섹션 6: 수업 관찰 체크리스트 자동 생성
# ==========================================
st.header("6. 수업 관찰 체크리스트 자동 생성")
checklist_data = {
    "관찰 항목 (루브릭)": [
        "시각적 대기선 밖에서 자신의 차례를 기다리며 규칙을 준수하는가?",
        "어두운 환경(암막)과 시청각 자극에 과흥분하지 않고 적절히 반응하는가?",
        "또래와 협동(예: 색 채우기) 혹은 선의의 경쟁을 수행하며 긍정적 유대감을 맺는가?",
        "체육활동 후 쿨다운 시간에 감정 카드 등을 활용해 느낌을 표현할 수 있는가?"
    ],
    "성취 수준(상/중/하)": ["", "", "", ""],
    "비고 (교사 관찰/PBIS 데이터)": ["", "", "", ""]
}
df_checklist = pd.DataFrame(checklist_data)
st.dataframe(df_checklist, use_container_width=True)

# ==========================================
# 섹션 7: 엑셀 데이터 누적 및 다운로드 (웹 환경 호환)
# ==========================================
st.header("7. 학습지도안 및 체크리스트 엑셀 저장")
st.markdown("생성된 지도안 및 체크리스트를 Excel 파일로 다운로드하여 학생 데이터를 누적 관리하세요.")

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # 체크리스트 시트
        df.to_excel(writer, index=False, sheet_name='관찰체크리스트')
        # 지도안 요약 시트
        summary_data = {
            "항목": ["학교구분", "학년", "학생수", "단원", "학습목표(상)", "학습자 실태", "환경/안전계획"],
            "내용": [school_type, grade, student_count, unit, goal_high, learner_profile, env_plan]
        }
        pd.DataFrame(summary_data).to_excel(writer, index=False, sheet_name='학습지도안_요약')
    return output.getvalue()

excel_file = to_excel(df_checklist)

st.download_button(
    label="📥 UDL 3.0 맞춤형 학습지도안 엑셀(.xlsx) 다운로드",
    data=excel_file,
    file_name='DIDIM_UDL3.0_학습지도안.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)