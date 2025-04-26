from telethon import Button

start_buttons = [
    [Button.url("Add me to your chat", "http://t.me/zhunehra_bot?startgroup=botstart")],
    [Button.inline("Help", data=b"help_menu")],
    [
        Button.url("Report", "https://t.me/zhunehra_chat"),
        Button.url("Channel", "https://t.me/zhunehra")
        ],
    ]
start_group_buttons = [
    [
        Button.url("Start Zhunehra", "https://t.me/zhunehra_bot?start=groupstart")
    ],
    [
        Button.url("Report", "https://t.me/zhunehra_chat"),
        Button.url("Channel", "https://t.me/zhunehra")
    ]
]