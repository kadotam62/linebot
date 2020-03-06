from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
 
app = Flask(__name__)
 
#���ϐ��擾
# LINE Developers�Őݒ肳��Ă���A�N�Z�X�g�[�N����Channel Secret�����擾���A�ݒ肵�܂��B
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["FRCegkJfi+6B+YfYGRkwx4nK/otrtBt2ihU/vScKjzzVY7gPdDzKYZEvwTh+F/eXEUXw5P/4ZZ+twM8d6Ech2CeAqtLcloGkISjdNgMkOnilKfq2yMw/upytHfa2oWp72VP3wMcelTRxZrTfN2D6YQdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["a92c17fc24367bd759a06c6568a20d03"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
 
 
## 1 ##
#Webhook����̃��N�G�X�g���`�F�b�N���܂��B
@app.route("/callback", methods=['POST'])
def callback():
    # ���N�G�X�g�w�b�_�[���珐�����؂̂��߂̒l���擾���܂��B
    signature = request.headers['X-Line-Signature']
 
    # ���N�G�X�g�{�f�B���擾���܂��B
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
�@# ���������؂��A���Ȃ����handle�ɒ�`����Ă���֐����Ăяo���B
    try:
        handler.handle(body, signature)
�@# �������؂Ŏ��s�����ꍇ�A��O���o���B
    except InvalidSignatureError:
        abort(400)
�@# handle�̏������I�����OK
    return 'OK'
 
## 2 ##
###############################################
#LINE�̃��b�Z�[�W�̎擾�ƕԐM���e�̐ݒ�(�I�E���Ԃ�)
###############################################
 
#LINE��MessageEvent�i���ʂ̃��b�Z�[�W�𑗐M���ꂽ�ꍇ�j���N�������ꍇ�ɁA
#def�ȉ��̊֐������s���܂��B
#reply_message�̑�������event.reply_token�́A�C�x���g�̉����ɗp����g�[�N���ł��B 
#�������ɂ́Alinebot.models�ɒ�`����Ă���ԐM�p��TextSendMessage�I�u�W�F�N�g��n���Ă��܂��B
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) #�����ŃI�E���Ԃ��̃��b�Z�[�W��Ԃ��܂��B
 
# �|�[�g�ԍ��̐ݒ�
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)