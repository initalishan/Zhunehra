import subprocess

def get_ping(host="8.8.8.8"):
    try:
        output = subprocess.check_output(
            ["ping", "-c", "1", host], stderr=subprocess.STDOUT, universal_newlines=True
        )
        for line in output.split("\n"):
            if "time=" in line:
                ping_time = line.split("time=")[1].split(" ")[0]
                return f"{ping_time}ms"
        return "Ping time not found"
    except subprocess.CalledProcessError:
        return "Ping failed"