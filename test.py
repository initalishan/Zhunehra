queues = {}  

chat_id = 112233
queues.setdefault(chat_id, [])

queues[chat_id].append(("tu hai kahan", "mention", "video"))

print(queues[chat_id][0][1])