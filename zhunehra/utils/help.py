from telethon import Button

help_buttons = [
    [
        Button.inline("Commands", data=b"commands")
    ],
    [
        Button.inline("About Zhunehra", data=b"about_zhunehra")
    ],
    [
        Button.inline("Back", data=b"back_to_start")
    ]
]

commands_button = [
    [
        Button.inline("Play", data=b"play_command"),
        Button.inline("Vplay", data=b"vplay_command"),
        Button.inline("Stop", data=b"stop_command")
    ],
    [
        Button.inline("Skip", data=b"skip_command"),
        Button.inline("Pause", data=b"pause_command"),
        Button.inline("Resume", data=b"resume_command")
    ],
    [
        Button.inline("Replay", data=b"replay_command"),
        Button.inline("Download", data=b"download_command")
    ],
    [
        Button.inline("Back", data=b"back_to_help")
    ]
]

about_zhunehra_buttons = [
    [
        Button.url("Developer", "https://t.me/initalishan")
    ],
    [
        Button.url("Report", "https://t.me/zhunehra_chat"),
        Button.url("Channel", "https://t.me/zhunehra")
    ],
    [
        Button.inline("Back", data=b"back_to_help")
    ]
]

back_to_commands_button = [
    [
        Button.inline("Back", data=b"back_to_commands")
    ]
]