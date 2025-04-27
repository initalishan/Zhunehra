from zhunehra.plugins.start import start
from zhunehra.plugins.download import Download
from zhunehra.plugins.play import Play
from zhunehra.plugins.vplay import VPlay
from zhunehra.core.module_injector import *
from zhunehra.plugins import end, pause_and_resume, skip, replay, vc_update, help


start()
Download()
Play()
VPlay()
print("Zhunehra started.")
zhunehra.run_until_disconnected()