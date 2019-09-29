import os

import eeic_bot
import wiki
import assignment_notify

is_first = True
if is_first:
    WIKI_URL = "https://wiki.eeic.jp"
    API_URL = WIKI_URL + "/api.php"
    file_path=os.path.dirname(os.path.abspath(__file__)) + "/user_info.json"
    if os.path.exists(file_path):
        f = open(file_path)
        import json
        user_info = json.load(f)
        f.close()
        bot_username = user_info['BOT_USERNAME']
        bot_password = user_info['BOT_PASSWORD']
        api_token = user_info['API_TOKEN']
        page_name = user_info['PAGE_NAME']
    else:
        bot_username = os.environ['BOT_USERNAME']
        bot_password = os.environ['BOT_PASSWORD']
        api_token = os.environ['API_TOKEN']
        page_name = os.environ['PAGE_NAME']

    session = wiki.MediaWikiSession(API_URL, bot_username, bot_password)

    # slackBotとassingment_notify_mgrを用意
    # botを別スレッドでスタート
    bot = eeic_bot.SlackBot(API_TOKEN=api_token)
    assignment_notify_mgr = assignment_notify.AssignmentListMgr(session, page_name)

    is_first = False


def getTommorowAssignmentMessage():
    tommorow_assignment = assignment_notify_mgr.getTommorowAssignmentList()
    assignment_str = assignment_notify.parseAssignmentList(tommorow_assignment)
    if assignment_str == "":
        return ""
    else:
        message = assignment_str
        return message

assignment_channel_name = "#0-assignment"

#   明日の課題を投稿する
#   @param flag 課題が無かった場合，何もしないか
def postTommorowAssignment():
    message = "明日の課題をお知らせするよ！\n"
    assignment_msg = getTommorowAssignmentMessage()
    if assignment_msg == "":
        return
    bot.postMessage(assignment_channel_name, message + assignment_msg)


def getNextWeekAssignmentMessage():
    assignment = assignment_notify_mgr.getNextWeekAssignmentList()
    assignment_str = assignment_notify.parseAssignmentList(assignment)
    if assignment_str == "":
        return ""
    else:
        return assignment_str

def getNotDeadlineAssignmentMessage():
    assignment = assignment_notify_mgr.getNotDeadlineAssignmentList()
    assignment_str = assignment_notify.parseAssignmentList(assignment)
    if assignment_str == "":
        return ""
    else:
        return assignment_str


#   来週の課題を投稿する
#   @param flag 課題が無かった場合，Trueなら無いことを通知する Falseなら何もしない
def postNextWeekAssignment():
    message = "来週の課題をお知らせするよ！\n"
    assignment_msg = getNextWeekAssignmentMessage()
    if assignment_msg == "":
        return
    bot.postMessage(assignment_channel_name, message + assignment_msg)

