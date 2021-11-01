from flask import Flask, request
import requests
import controller
app = Flask(__name__)
app.secret_key = '1234'


class Save_data:
    def __init__(self, category):
       self.category_data=category


@app.route("/sanity", methods=['GET'])
def index():
    """
    server home page 
    :return: str to show that the server is running
    """
    return 'Server is running'

TOKEN = '1758654061:AAEssDofSVaUS7TsQ0_ely37IkmnIbZW0QU'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://37fbfd3bd764.ngrok.io/message'.format(TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/message', methods=["POST"])
def handle_message():
    """
    get message from the telegram bot and send the wright answer
    """
    print("got message")
    answer='I dont understand :('
    save = Save_data("")
    lst_of_text = list(request.get_json()['message']['text'].split(" "))
    command = " ".join(str(x) for x in lst_of_text)
    if command == '/exercise':
        answer="In which category?"
    if command == '/back' or command == '/arms' or command == '/chest' or command == '/legs' or command == '/abs' or command == '/shoulders' or command == '/calves':
        is_in_history=controller.check_history(command[1:])
        if(is_in_history=='Come on dude,you need to train all the muscles!'):
            answer='Come on dude,you need to train all the muscles!'+"\n"+"please choose another category"
        else:
            save.category_data=is_in_history
            answer = "Great! What equipment do you have?"
    if command == '/dumbbell' or command == '/bench' or command == '/barbell' or command == '/gym mat' or command == '/incline bench' or command == '/kettlebell' or command == '/none (bodyweight exercise)' or command == '/pull-up bar' or command == '/swiss Ball' or command == '/sz-Bar':
        answer=controller.exercise(save.category_data, command[1:])
    chat_id = request.get_json()['message']['chat']['id']
    res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, answer))
    """res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                       .format(TOKEN, chat_id, answer[1]))"""
    return "success"


if __name__ == '__main__':
    app.run(port=5002)
