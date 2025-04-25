from telethon import Button

queue_buttons = [
    [
        Button.inline("Skip", data=b"skip"),
        Button.inline("Stop", data=b"stop")
    ],
    [
        Button.url("Subscibe To Zhunehra", "https://t.me/zhunehra")
        ]
]