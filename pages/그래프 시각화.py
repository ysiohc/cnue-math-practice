import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정
font_path = '/workspaces/cnue-math-practice/fonts/NanumGothic-Regular.ttf'
korean_font = None

if os.path.exists(font_path):
    try:
        # 폰트 등록 및 설정
        fm.fontManager.addfont(font_path)
        korean_font = fm.FontProperties(fname=font_path)
        
        # matplotlib 전역 설정
        plt.rcParams['font.family'] = [korean_font.get_name()]
        plt.rcParams['axes.unicode_minus'] = False
        
        # 폰트 캐시 클리어 및 재구축
        try:
            fm._rebuild()
        except:
            pass
            
        st.success("🎨 한글 폰트(NanumGothic)가 성공적으로 로드되었습니다!")
        
    except Exception as e:
        st.warning(f"폰트 로딩 중 오류 발생: {e}")
        korean_font = None
else:
    st.error(f"폰트 파일을 찾을 수 없습니다: {font_path}")

# 폰트 설정이 실패한 경우 기본 설정
if korean_font is None:
    plt.rcParams['font.family'] = ['Arial Unicode MS', 'DejaVu Sans', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

plt.style.use('seaborn-v0_8')

# 한글 텍스트 설정 함수
def set_korean_text(ax, title=None, xlabel=None, ylabel=None):
    """차트에 한글 텍스트를 설정하는 함수"""
    if korean_font:
        if title:
            ax.set_title(title, fontproperties=korean_font, fontsize=12, fontweight='bold')
        if xlabel:
            ax.set_xlabel(xlabel, fontproperties=korean_font, fontsize=10)
        if ylabel:
            ax.set_ylabel(ylabel, fontproperties=korean_font, fontsize=10)
    else:
        if title:
            ax.set_title(title, fontsize=12, fontweight='bold')
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=10)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=10)

st.title("📊 Matplotlib 데이터 시각화")
st.write("다양한 차트 타입을 통해 데이터를 시각화하는 예시들을 살펴보세요!")

# 사이드바에서 차트 타입 선택
chart_type = st.sidebar.selectbox(
    "차트 타입을 선택하세요:",
    ["선 그래프", "막대 그래프", "산점도", "히스토그램", "원 그래프", "박스 플롯", "히트맵"]
)

# 데이터 생성 함수들
def generate_line_data():
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(x)
    return x, y1, y2, y3

def generate_bar_data():
    categories = ['사과', '바나나', '체리', '딸기', '포도']
    values = [23, 45, 56, 78, 32]
    return categories, values

def generate_scatter_data():
    np.random.seed(42)
    x = np.random.randn(100)
    y = 2 * x + np.random.randn(100)
    colors = np.random.rand(100)
    return x, y, colors

def generate_hist_data():
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)
    return data

def generate_pie_data():
    labels = ['A', 'B', 'C', 'D', 'E']
    sizes = [30, 25, 20, 15, 10]
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'plum']
    return labels, sizes, colors

def generate_box_data():
    np.random.seed(42)
    data = [np.random.normal(100, 10, 200),
            np.random.normal(80, 20, 200),
            np.random.normal(90, 5, 200),
            np.random.normal(70, 15, 200)]
    return data

def generate_heatmap_data():
    np.random.seed(42)
    data = np.random.rand(10, 12)
    return data

# 차트별 시각화
if chart_type == "선 그래프":
    st.header("📈 선 그래프 (Line Plot)")
    st.write("시간에 따른 데이터 변화나 연속적인 데이터를 표현하는데 적합합니다.")
    
    x, y1, y2, y3 = generate_line_data()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y1, label='sin(x)', linewidth=2)
    ax.plot(x, y2, label='cos(x)', linewidth=2)
    ax.plot(x, y3, label='sin(x)*cos(x)', linewidth=2)
    
    set_korean_text(ax, title='삼각함수 그래프', xlabel='X 값', ylabel='Y 값')
    ax.legend(prop=korean_font if korean_font else None)
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    # 데이터 설명
    st.write("**데이터 설명:**")
    st.write("- 빨간선: sin(x) 함수")
    st.write("- 파란선: cos(x) 함수") 
    st.write("- 초록선: sin(x) × cos(x) 함수")

elif chart_type == "막대 그래프":
    st.header("📊 막대 그래프 (Bar Chart)")
    st.write("범주형 데이터를 비교하는데 효과적입니다.")
    
    categories, values = generate_bar_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 수직 막대 그래프
    bars1 = ax1.bar(categories, values, color=['#ff9999','#66b3ff','#99ff99','#ffcc99','#ff99cc'])
    set_korean_text(ax1, title='세로 막대 그래프', xlabel='과일 종류', ylabel='판매량')
    # x축 라벨 폰트 설정
    if korean_font:
        for label in ax1.get_xticklabels():
            label.set_fontproperties(korean_font)
    
    # 막대 위에 값 표시
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}', ha='center', va='bottom')
    
    # 수평 막대 그래프
    bars2 = ax2.barh(categories, values, color=['#ff9999','#66b3ff','#99ff99','#ffcc99','#ff99cc'])
    set_korean_text(ax2, title='가로 막대 그래프', xlabel='판매량', ylabel='과일 종류')
    # y축 라벨 폰트 설정
    if korean_font:
        for label in ax2.get_yticklabels():
            label.set_fontproperties(korean_font)
    
    # 막대 오른쪽에 값 표시
    for i, bar in enumerate(bars2):
        width = bar.get_width()
        ax2.text(width + 1, bar.get_y() + bar.get_height()/2.,
                f'{values[i]}', ha='left', va='center')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("**데이터 설명:**")
    st.write(f"과일별 판매량 데이터를 막대 그래프로 표현")

elif chart_type == "산점도":
    st.header("🔸 산점도 (Scatter Plot)")
    st.write("두 변수 간의 상관관계를 파악하는데 유용합니다.")
    
    x, y, colors = generate_scatter_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 기본 산점도
    ax1.scatter(x, y, alpha=0.6, s=50)
    set_korean_text(ax1, title='기본 산점도', xlabel='X 값', ylabel='Y 값')
    ax1.grid(True, alpha=0.3)
    
    # 색상과 크기 변화가 있는 산점도
    scatter = ax2.scatter(x, y, c=colors, s=colors*100, alpha=0.6, cmap='viridis')
    set_korean_text(ax2, title='색상 및 크기 변화 산점도', xlabel='X 값', ylabel='Y 값')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax2)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 상관계수 계산
    correlation = np.corrcoef(x, y)[0, 1]
    st.write(f"**상관계수:** {correlation:.3f}")
    st.write("**해석:** 양의 상관관계가 있어 X가 증가하면 Y도 증가하는 경향을 보입니다.")

elif chart_type == "히스토그램":
    st.header("📈 히스토그램 (Histogram)")
    st.write("데이터의 분포를 확인하는데 사용됩니다.")
    
    data = generate_hist_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 기본 히스토그램
    ax1.hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    set_korean_text(ax1, title='히스토그램', xlabel='값', ylabel='빈도')
    ax1.grid(True, alpha=0.3)
    
    # 확률밀도 히스토그램
    ax2.hist(data, bins=30, density=True, alpha=0.7, color='lightcoral', edgecolor='black')
    set_korean_text(ax2, title='확률밀도 히스토그램', xlabel='값', ylabel='밀도')
    ax2.grid(True, alpha=0.3)
    
    # 정규분포 곡선 추가
    x_norm = np.linspace(data.min(), data.max(), 100)
    y_norm = ((1/np.sqrt(2*np.pi*15**2)) * 
              np.exp(-0.5*((x_norm-100)/15)**2))
    ax2.plot(x_norm, y_norm, 'r-', linewidth=2, label='정규분포')
    ax2.legend(prop=korean_font if korean_font else None)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("**통계 정보:**")
    st.write(f"- 평균: {np.mean(data):.2f}")
    st.write(f"- 표준편차: {np.std(data):.2f}")
    st.write(f"- 최솟값: {np.min(data):.2f}")
    st.write(f"- 최댓값: {np.max(data):.2f}")

elif chart_type == "원 그래프":
    st.header("🥧 원 그래프 (Pie Chart)")
    st.write("전체에서 각 부분이 차지하는 비율을 보여줍니다.")
    
    labels, sizes, colors = generate_pie_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # 기본 원 그래프
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    set_korean_text(ax1, title='기본 원 그래프')
    
    # 분리된 원 그래프
    explode = (0.1, 0, 0, 0, 0)  # 첫 번째 조각만 분리
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, 
            explode=explode, shadow=True, startangle=90)
    set_korean_text(ax2, title='분리된 원 그래프')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("**데이터 설명:**")
    for label, size in zip(labels, sizes):
        st.write(f"- {label}: {size}%")

elif chart_type == "박스 플롯":
    st.header("📦 박스 플롯 (Box Plot)")
    st.write("데이터의 분포와 이상치를 한눈에 파악할 수 있습니다.")
    
    data = generate_box_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # 기본 박스 플롯
    bp = ax1.boxplot(data, labels=['그룹 A', '그룹 B', '그룹 C', '그룹 D'])
    set_korean_text(ax1, title='박스 플롯', ylabel='값')
    # x축 라벨 폰트 설정
    if korean_font:
        for label in ax1.get_xticklabels():
            label.set_fontproperties(korean_font)
    ax1.grid(True, alpha=0.3)
    
    # 바이올린 플롯
    parts = ax2.violinplot(data, positions=[1, 2, 3, 4], showmeans=True, showmedians=True)
    set_korean_text(ax2, title='바이올린 플롯', ylabel='값')
    ax2.set_xticks([1, 2, 3, 4])
    ax2.set_xticklabels(['그룹 A', '그룹 B', '그룹 C', '그룹 D'])
    # x축 라벨 폰트 설정
    if korean_font:
        for label in ax2.get_xticklabels():
            label.set_fontproperties(korean_font)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.write("**박스 플롯 해석:**")
    st.write("- 박스: 1사분위수(Q1)부터 3사분위수(Q3)까지의 범위")
    st.write("- 중간선: 중앙값(median)")
    st.write("- 수염: 최솟값과 최댓값 (이상치 제외)")
    st.write("- 점: 이상치(outliers)")

elif chart_type == "히트맵":
    st.header("🌡️ 히트맵 (Heatmap)")
    st.write("2차원 데이터를 색상으로 표현하여 패턴을 쉽게 파악할 수 있습니다.")
    
    data = generate_heatmap_data()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 기본 히트맵
    im1 = ax1.imshow(data, cmap='viridis', aspect='auto')
    set_korean_text(ax1, title='히트맵 - Viridis', xlabel='열 인덱스', ylabel='행 인덱스')
    plt.colorbar(im1, ax=ax1)
    
    # 다른 컬러맵 히트맵
    im2 = ax2.imshow(data, cmap='RdYlBu_r', aspect='auto')
    set_korean_text(ax2, title='히트맵 - RdYlBu_r', xlabel='열 인덱스', ylabel='행 인덱스')
    plt.colorbar(im2, ax=ax2)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # 데이터 테이블 표시
    st.write("**데이터 테이블 (일부):**")
    df = pd.DataFrame(data)
    st.dataframe(df.head())

# 추가 정보 섹션
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 차트 선택 가이드")
st.sidebar.markdown("""
**선 그래프**: 시계열 데이터, 연속 데이터
**막대 그래프**: 범주형 데이터 비교
**산점도**: 두 변수 간 상관관계
**히스토그램**: 데이터 분포 확인
**원 그래프**: 비율, 구성 요소
**박스 플롯**: 분포와 이상치
**히트맵**: 2차원 데이터 패턴
""")

# 푸터
st.markdown("---")
st.markdown("💡 **팁:** 사이드바에서 다른 차트 타입을 선택해보세요!")
