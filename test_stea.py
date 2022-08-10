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
        return "ごめんなさい。もう一度教えて下さい。"


openai.api_key = "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"

def text_summary(prompt):
    # 分析の実施
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0.8,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
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
\n以下は、高橋とあなたの会話です。高橋とあなたの発言にタメ口で返します。\
\nあなた:今日の仕事どうだった？\n高橋:マジでほんと疲れたわ。\nあなた:XXX\n高橋:"



#天気情報都道府県
area_dic = {'北海道/釧路':'014100',
            '北海道/旭川':'012000',
            '北海道/札幌':'016000',
            '青森県':'020000',
            '岩手県':'030000',
            '宮城県':'040000',
            '秋田県':'050000',
            '山形県':'060000',
            '福島県':'070000',
            '茨城県':'080000',
            '栃木県':'090000',
            '群馬県':'100000',
            '埼玉県':'110000',
            '千葉県':'120000',
            '東京都':'130000',
            '神奈川県':'140000',
            '新潟県':'150000',
            '富山県':'160000',
            '石川県':'170000',
            '福井県':'180000',
            '山梨県':'190000',
            '長野県':'200000',
            '岐阜県':'210000',
            '静岡県':'220000',
            '愛知県':'230000',
            '三重県':'240000',
            '滋賀県':'250000',
            '京都府':'260000',
            '大阪府':'270000',
            '兵庫県':'280000',
            '奈良県':'290000',
            '和歌山県':'300000',
            '鳥取県':'310000',
            '島根県':'320000',
            '岡山県':'330000',
            '広島県':'340000',
            '山口県':'350000',
            '徳島県':'360000',
            '香川県':'370000',
            '愛媛県':'380000',
            '高知県':'390000',
            '福岡県':'400000',
            '佐賀県':'410000',
            '長崎県':'420000',
            '熊本県':'430000',
            '大分県':'440000',
            '宮崎県':'450000',
            '鹿児島県':'460100',
            '沖縄県/那覇':'471000',
            '沖縄県/石垣':'474000'
            }
jma_url=jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/XXX.json"
def area_name_url(text):
  
  for k , v in area_dic.items():
    #都道府県
    if k[0:-1] in text:
      area_no=area_dic[k]
      area_descript=k +"の天気"
      #print("都道府県")
      break
    elif k[-2:] in text:
      #札幌のようなとき
      area_no=area_dic[k]
      area_descript=k[-2:] +"の天気"
      #print("札幌")
      break

    elif k[:3]=="北海道" and k[:3] in text:
      #北海道
      area_no=area_dic["北海道/札幌"]
      area_descript="北海道の天気"
      #print("北海道")
      break
    elif k[:2]=="沖縄" and k[:2] in text:
      #沖縄
      area_no=area_dic["沖縄県/那覇"]
      area_descript="沖縄の天気"
      #print("沖縄")
      break
  return area_no,area_descript




def weather_output(area_name_no): 
  jma_url_new=jma_url.replace('XXX', area_name_no)
  jma_json = requests.get(jma_url_new).json()
  jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
  #jma_weather_tomoは明日の天気
  jma_weather_tomo = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][1]
  print("jma_weather_tomo",jma_weather_tomo)
  jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
  #日付の処理
  pos = jma_date.find('T')
  today=jma_date[:pos]
  today_datetime = datetime.datetime.strptime(today, '%Y-%m-%d')
  today_str=today_datetime.strftime('%Y年%m月%d日')

  #明日の日付
  tomo_datetime=today_datetime+ datetime.timedelta(days=1)
  tomo_str=tomo_datetime.strftime('%Y年%m月%d日')
  #print(tomo_str)

  #全角スペースを削除
  #weather=jma_weather.replace('　', '')
  #jma_temp=jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][2]
  temp=jma_json[0]["timeSeries"][2]["areas"][0]["temps"]
  #print(temp)
  max_temp=temp[1]
  min_temp=temp[0]

  retuen_sent="●本日"+today_str+"の"+area_name_desc+"は" \
              + jma_weather+"の予報。"+"\n"+"・最高気温は"+max_temp+"°、"+"最低気温は"+min_temp+"°です。"\
              +"\n"+"●明日"+tomo_str + "の"+area_name_desc+"は"+jma_weather_tomo+"の予報です。"

  return retuen_sent











if 'count' not in st.session_state: 
    st.session_state.count = 0 #countがsession_stateに追加されていない場合，0で初期化


user_input = get_text()


if st.session_state.count == 0:
    st.session_state.past.append("あなた")
    st.session_state.generated.append("チャットボット")
    st.session_state.count += 1 #値の更新

else:



    if user_input:
        #if "天気" in user_input:
        #        output= "エリアがわかりません。  \n  ※エリア名は47都道府県名と札幌、旭川、釧路、那覇、石垣の入力が可能です。  \n   
        #print(message)
        #    try:
        #        area_name_no=area_name_url(user_input)[0]
        #        print(area_name_no)
        #        area_name_desc=area_name_url(user_input)[1]
        #        w=weather_output(area_name_no)
        #        output=w
        #    except:\n  ●天気情報を見るには以下のような例に従ってにエリア名を入力してください。 \n- 例)東京の天気は？ \n- 例)沖縄の天気は？  \n- 例)石垣の天気は？"
        #
        #else:
        #while st.session_state.count< 10:
        
        
        if st.session_state.count==1:
            prompt_input=prompt.replace("XXX",user_input)
            return_text=text_summary(prompt_input)
            #print("return_text",return_text)
            prompt_new=prompt_input+return_text
            #print("prompt_new",prompt_new)
            #print(n)
            #print("あなた"+text)
            print("高橋"+return_text)
            output=return_text
            st.session_state['prompt']=prompt_new

        else:
            prompt_input_new=st.session_state['prompt']+"\nあなた:"+user_input+"\n高橋:"
            return_text=text_summary(prompt_input_new)
            #print("return_text",return_text)
            st.session_state['prompt']=prompt_input_new+return_text
            #print("prompt_new",prompt_new)
            
            #print("あなた"+text)
            print("高橋"+return_text)
            output=return_text

        

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
        st.session_state.count += 1 #値の更新



if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
