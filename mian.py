import os
import openai
import json

data = []

prompt = [{"role": "system","content": "日本語で返答してください。"}]

client = openai.OpenAI(api_key = os.environ["OPENAI_API_KEY"])

while(True):
    # ファイルを読み込んでJSONとしてパース
    try:
        with open('tmp.json', 'r', encoding='utf-8') as pre_ans:
            history = json.load(pre_ans)
            prompt.extend(history)
    except FileNotFoundError:
        print("tmp.jsonがありません。初回実行時はJSONファイルの読み込みをスキップします。")
    
    msg = input()

    prompt.append({"role":"user","content":str(msg)})

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt,
    )

    print(res.choices[0].message.content)

    # 辞書データの作成
    data.append({"role":"user","content":str(msg)})
    data.append({"role":"assistant","content":str(res.choices[0].message.content)})

    # JSONファイルに書き込む
    with open('tmp.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)