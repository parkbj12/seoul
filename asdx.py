import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import DistilBertTokenizer, DistilBertModel
import torch
import openai
import chardet
import folium
from streamlit_folium import st_folium

@st.cache_data
def load_data(file_path):
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            encoding = result['encoding']
        return pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Data file path
FILE_PATH = '서울시 생활체육포털(3만).csv'

# Load data
data = load_data(FILE_PATH)

# Main application
st.title("서울시 체육 네트워크")
st.subheader('원하시는 구를 클릭하세요')
st.sidebar.header("메뉴")

menu = st.sidebar.selectbox(
    "페이지 선택",
    options=["홈", "구 별 데이터", "추천 시스템", "챗봇"]
)

if menu == "홈":

    
    # Create Folium map
    seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # District coordinates
    district_coords = {
        "강서구": [37.5509, 126.8495],
        "양천구": [37.5172, 126.8660],
        "은평구": [37.6176, 126.9227],
        "도봉구": [37.6688, 127.0467],
        "노원구": [37.6542, 127.0563],
        "강북구": [37.6396, 127.0254],
        "중랑구": [37.5951, 127.0928],
        "강동구": [37.5503, 127.1463],
        "송파구": [37.5047, 127.1142],
        "성북구": [37.6060, 127.0204],
        "동대문구": [37.5743, 127.0390],
        "광진구": [37.5384, 127.0823],
        "종로구": [37.5730, 126.9794],
        "서대문구": [37.5791, 126.9368],
        "중구": [37.5635, 126.9976],
        "성동구": [37.5636, 127.0363],
        "마포구": [37.5638, 126.9085],
        "용산구": [37.5326, 126.9903],
        "강남구": [37.5172, 127.0473],
        "서초구": [37.4837, 127.0323],
        "동작구": [37.5126, 126.9394],
        "영등포구": [37.5265, 126.8963],
        "관악구": [37.4785, 126.9519],
        "금천구": [37.4563, 126.8950],
        "구로구": [37.4954, 126.8874],
    }

    # Add markers
    for district, coords in district_coords.items():
        folium.Marker(
            location=coords,
            popup=f"<b>{district}</b>",
            tooltip=f"{district} !",
            icon=folium.Icon(icon="info-sign")
        ).add_to(seoul_map)

    # Render the map
    clicked_data = st_folium(seoul_map, width=725, height=500)
   

    # Handle marker click event
    if clicked_data and "last_object_clicked" in clicked_data:
        last_clicked = clicked_data["last_object_clicked"]
        if last_clicked and "last_object_clicked_popup" in clicked_data:
            # Extract district name
            district = clicked_data["last_object_clicked_popup"].strip()
            st.info(f"클릭한 구: {district}(자세한 내용은 구 별 데이터에서 확인하세요.)")
           

            
            # Filter and display data for the clicked district
            district_data = data[data["지역구"].str.strip().str.lower() == district.lower()]
            if not district_data.empty:
                st.dataframe(district_data.reset_index(drop=True))
            else:
                st.warning(f"{district}에 대한 데이터가 없습니다.")
        else:
            st.warning("클릭한 마커에 'popup' 정보가 없습니다.")
    else:
        st.warning("클릭한 데이터가 없습니다.")
        
           
elif menu == "구 별 데이터":
    st.subheader("서울시 구 별 프로그램 데이터")
    district = st.selectbox("지역을 선택하세요", options=data["지역구"].unique())
    search_query = st.text_input("검색어를 입력하세요")
    
    district_data = data[data["지역구"] == district]
    if search_query:
        district_data = district_data[
            district_data.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)
        ]
    
    if not district_data.empty:
        st.dataframe(district_data.iloc[:, 1:].reset_index(drop=True))
    else:
        st.warning("검색 결과가 없습니다.")

         


elif menu == "추천 시스템":
    st.subheader("추천 시스템")
    
    @st.cache_resource
    def load_model():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-multilingual-cased')
        model = DistilBertModel.from_pretrained('distilbert-base-multilingual-cased').to(device)
        return tokenizer, model, device

    tokenizer, model, device = load_model()
    
    @st.cache_data
    def load_embedding_data():
        rec_data = pd.read_csv('recommendation_data_with_embeddings.csv', encoding='cp949')
        rec_data['embedding'] = rec_data['embedding'].apply(lambda x: np.array(list(map(float, x.split(',')))))
        return rec_data
    
    rec_data = load_embedding_data()

    def get_distilbert_embedding(text):
        inputs = tokenizer([text], return_tensors="pt", truncation=True, padding=True, max_length=128)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state[:, 0, :].cpu().numpy()

    def recommend_program(user_input, rec_data, top_n=5):
        user_embedding = get_distilbert_embedding(user_input)
        rec_data['similarity'] = rec_data['embedding'].apply(lambda x: cosine_similarity([x], user_embedding)[0][0])
        recommended = rec_data.sort_values(by='similarity', ascending=False).head(top_n)
        return recommended[['대상', '내용', '지역구', '장소', '전화번호', '기관홈페이지']]

    target = st.text_input("찾고 싶은 대상을 입력하세요 (ex. 어르신)")
    region = st.text_input("찾고 싶은 지역구를 입력하세요 (ex. 강서구)")

    if st.button("추천"):
        user_input = f"{region} {target}"
        recommendations = recommend_program(user_input, rec_data)
        st.dataframe(recommendations)

 # OpenAI API 키를 받아서 응답을 생성하는 함수
def generate_response(user_message, api_key):
    # OpenAI API 키 설정
    openai.api_key = api_key

    # OpenAI GPT-3.5 Turbo 모델에 요청 보내기 (v1/chat/completions 엔드포인트 사용)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPT-3.5 Turbo 모델 사용
        messages=[{"role": "user", "content": user_message}]  # 메시지 형식에 맞게 작성
    )

    return response['choices'][0]['message']['content']  # 응답 텍스트 반환    

# 챗봇 페이지일 때 API 키 입력 받기
if menu == "챗봇":
    st.subheader("🏋️GYM 챗봇🏋️")
    
    # API 키 입력 필드
    openai_api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

    # API 키가 입력되었는지 확인
    if openai_api_key:
        st.session_state['openai_api_key'] = openai_api_key
        st.write("API 키가 저장되었습니다.")
    else:
        st.write("API 키를 입력하세요.")

    # 챗봇 기능을 여기에 추가
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_message = st.text_input("챗봇에게 질문하세요!", key="user_input")

    if st.button("전송"):
        if user_message:
            st.session_state["chat_history"].append({"role": "user", "content": user_message})
            # 챗봇 응답 생성 (API 키 사용)
            response = generate_response(user_message, openai_api_key)  # 두 번째 인자로 API 키 전달
            st.session_state["chat_history"].append({"role": "assistant", "content": response})

    # 채팅 기록 출력
    for message in st.session_state["chat_history"]:
        if message["role"] == "user":
            st.markdown(f"**사용자:** {message['content']}")
        else:
            st.markdown(f"**챗봇:** {message['content']}")
