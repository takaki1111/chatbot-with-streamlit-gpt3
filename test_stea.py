import streamlit as st
from streamlit_chat import message
import requests
import datetime
import openai


st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)


st.header("チャットボット_高橋")

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
        return "ごめんなさい。現在入力を受けつけることができません。"



API_KEY=st.secrets.OpenAI.API_KEY
openai.api_key = API_KEY

def text_summary(prompt):
    # 分析の実施
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0.9,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.8,
    stop=["あなた:", "高橋:"]
    )

    # 分析結果の出力
    return response["choices"][0]["text"].replace('\n','')

def crean_text(text):
    text= text.replace('　',' ')

    return text

prompt="以下の設定に基づき会話します。\n名前は高橋。\n一人称は僕。\
\n口調はタメ口話す。\n年齢は2４歳くらい。\
\n職業は会社員。社会人3年目くらい。\
\n靴のサイズは26cm。料理は週に3回する。\
\nよく話す言葉はマジっすか\
\n性別は男\
\n性格は素直で頑張り屋。\nスポーツ経験は野球、サッカー、水泳で。特に野球ができる。\n出身地は宮城県。\n駅伝経験もある。\nAI、機械学習の経験もある。\
\nお酒はワインなら飲む。\n好きな食べ物はラーメン。\n好きなアーティストはYOASOBI（ヨアソビ）で、好きな曲は夜に駆ける。\n好きな本はエッセンシャル思考。\
\n好きな漫画はダイヤのエース。\nダイヤのエースで好きなキャラクターは主人公の沢村栄純。\nダイヤのエースで好きなところは、主人公・沢村栄純が絶対的なライバルがいても諦めずに努力するところ。\
\n遠投は90m投げれる。\n自分の性格で嫌いなところは自分の無力さが嫌い。夢はお金持ち。\n尊敬する人は石田さん。\
\n石田さんは直属の上司で、金髪、子持ち、細身でイケメンのエリート社会人\n趣味はアニメを見ること。好きなアニメはスパイファミリー。\
\n英語は少し話せる。\n行ってみたい国はスペイン。\
\n以下は、高橋とあなたの会話です。高橋はあなたの発言にタメ口で返します。\
\nあなた:今日の仕事どうだった？\n高橋:マジでほんと疲れたわ。\nあなた:XXX\n高橋:"


if 'count' not in st.session_state: 
    st.session_state.count = 0 #countがsession_stateに追加されていない場合，0で初期化


user_input = get_text()


if st.session_state.count == 0:
	
    st.session_state.past.append("あなた")
    st.session_state.generated.append("チャットボット")
    st.session_state.count += 1 #値の更新

else:

    if st.session_state.count==1:
        try:
            prompt_input=prompt.replace("XXX",user_input)
            return_text=text_summary(prompt_input)
            prompt_new=prompt_input+return_text
            output=return_text
            st.session_state['prompt']=prompt_new
        except:
            return_text=talk_api(user_input)
            output=return_text
            st.session_state['talk_api']=user_input

    else:
        try:    
            prompt_input_new=st.session_state['prompt']+"\nあなた:"+user_input+"\n高橋:"
            return_text=text_summary(prompt_input_new)
            st.session_state['prompt']=prompt_input_new+return_text
            output=return_text
        except:
            return_text=talk_api(user_input)
            output=return_text
            st.session_state['talk_api']=user_input

        

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
        st.session_state.count += 1 #値の更新



if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
