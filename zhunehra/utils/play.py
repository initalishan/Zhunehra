from telethon import Button

play_buttons = [
    [
        Button.inline("Pause", data=b"pause"),
        Button.inline("Replay", data=b"replay"),
        Button.inline("Resume", data=b"resume")
    ],
    [
        Button.inline("Skip", data=b"skip"),
        Button.inline("Stop", data=b"stop")
    ],
    [
        Button.url("Subscibe To Zhunehra", "https://t.me/zhunehra")
        ]
]