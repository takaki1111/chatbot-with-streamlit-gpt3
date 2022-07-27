import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)


st.header("Streamlit Chat - Demo")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def get_text():
    input_text = st.text_input("ここにチャットボットへのメッセージを入力してください","", key="input")
    return input_text 


def talk_api(message):
    apikey = "DZZxwzUDGaJiwSEiIqJW1rtEAX8aTWJH"  #@param {type:"string",title:"キー入力"}
    talk_url = "https://api.a3rt.recruit.co.jp/talk/v1/smalltalk"
    payload = {"apikey": apikey, "query": message}
    response = requests.post(talk_url, data=payload)
    try:
        return response.json()["results"][0]["reply"]
    except:
        print(response.json())
        return "ごめんなさい。もう一度教えて下さい。"


if 'count' not in st.session_state: 
    st.session_state.count = 0 #countがsession_stateに追加されていない場合，0で初期化


user_input = get_text()

if st.session_state.count == 0:
    st.session_state.past.append("あなた")
    st.session_state.generated.append("チャットボット")
    st.session_state.count += 1 #値の更新

else:



    if user_input:
        output = talk_api(user_input)

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
        st.session_state.count += 1 #値の更新


if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')