from zhunehra.plugins.start import start
from zhunehra.plugins.download import Download
from zhunehra.core.module_injector import *

start()
Download()

zhunehra.run_until_disconnected()