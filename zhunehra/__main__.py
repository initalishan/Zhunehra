from zhunehra.plugins.start import start
from zhunehra.plugins.download import Download
from zhunehra.plugins.play import Play
from zhunehra.core.module_injector import *

start()
Download()
Play()
print("Zhunehra started.")
zhunehra.run_until_disconnected()