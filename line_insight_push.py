##import##
import urllib3
from datetime import datetime, timedelta
import json
import requests

#####################################################################
##初期設定##

#LINE API bot Key
push_line_key = "Bearer aSh7A6HQaSchUPYTEEfZFSCk/KRlAK6pFCD/ezu86qSkGcy0yTyulibAW6c06wQgMMIrnpsHLmKDrZvRyrqWrg2fOfawQPJDxGhFQeLXWp2l+V+6jEvotSQxO4KVDcbAloRcIP405UtKHQa+NJj11QdB04t89/1O/w1cDnyilFU="
#LINE API OA Key
get_line_key = "Bearer UOgOLwhPapXtmUS2u+7yC/X/T5AGfMMLATXOxvoLUZm24rzNlijMyzUc0S60chOcpXixgRY4voaEolEKgAKmocxL/BKRt30+zXPBCm5EU1Obi6hZIpP6+AleE20VaWB5aBN4ZTIVgf1u5Iwc29Y+DQdB04t89/1O/w1cDnyilFU="


###########################################################################
# ラインにメッセを送信
def push_line_msg(auth_key, msg):
    headers = {"Authorization": auth_key, "Content-Type": "application/json"}

    res = requests.post(
        "https://api.line.me/v2/bot/message/broadcast",
        headers=headers,
        json={"messages": [{"type": "text", "text": msg}]},
    ).json()


# ラインに画像を送信
def push_line_img(auth_key, image_url):
    headers = {"Authorization": auth_key, "Content-Type": "application/json"}
    res = requests.post(
        "https://api.line.me/v2/bot/message/broadcast",
        headers=headers,
        json={
            "messages": [
                {
                    "type": "image",
                    "originalContentUrl": image_url,
                    "previewImageUrl": image_url,
                }
            ]
        },
    ).json()

#指定した日付のlineインサイトを取得
def get_line_insight(auth_key,date_text):

    headers = {"Authorization": get_line_key, "Content-Type": "application/json"}

    res = requests.get(
        " https://api.line.me/v2/bot/insight/followers?date="+date_text,
        headers=headers,
    )

    return res.json()

#メイン処理
def main():
    #日付を取得
    today_text = dt_now = datetime.now().strftime('%Y%m%d')
    yesterday_text = (datetime.now() - timedelta(1)).strftime('%Y%m%d')

    today_insight_json = get_line_insight(get_line_key,today_text)
    yesterday_insight_json = get_line_insight(get_line_key,yesterday_text)

    #pushテキストを作成
    push_text = "【LINE OA】\n{0}\n・follower：{1}人({2:+}人)\n・Block：{3}人({4:+}人)".format(
        datetime.now().strftime('%Y年%m月%d日'),
        today_insight_json["followers"],
        today_insight_json["followers"] - yesterday_insight_json["followers"],
        today_insight_json["blocks"],
        today_insight_json["blocks"] - yesterday_insight_json["blocks"])

    #テキストを送信
    push_line_msg(push_line_key,push_text)

if __name__ == "__main__":
    main()
