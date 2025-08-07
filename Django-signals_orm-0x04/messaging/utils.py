# messaging/utils.py

def get_thread_replies(message):
    replies = []

    def collect_replies(msg):
        for reply in msg.replies.all():
            replies.append(reply)
            collect_replies(reply)

    collect_replies(message)
    return replies
