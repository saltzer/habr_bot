from lib.utils import log
from datetime import datetime
import os, subprocess


def register_vm_queries(dispatcher, bot, invite_code, uptime):
    @dispatcher.callback_query_handler(lambda c: c.data == "reboot")
    async def process_callback_button(callback_query):
        log("Command executed -- reboot " + " | Time: " + str(datetime.now()) + "\n")
        os.system("reboot")
        await bot.answer_callback_query(callback_query.id)

    @dispatcher.callback_query_handler(lambda c: c.data == "shutdown")
    async def process_callback_button(callback_query):
        log("Command executed -- shutdown " + " | Time: " + str(datetime.now()) + "\n")
        os.system("shutdown")
        await bot.answer_callback_query(callback_query.id)

    @dispatcher.callback_query_handler(lambda c: c.data == "get_log")
    async def process_callback_button(callback_query):
        try:
            with open("log.txt", "rb") as file:
                await bot.send_document(invite_code, file)
            await bot.answer_callback_query(callback_query.id)
        except:
            await bot.send_message(invite_code, "Error send log")

    @dispatcher.callback_query_handler(lambda c: c.data == "restart_bot")
    async def process_callback_button(callback_query):
        os.system("pkill -f main.py | python PycharmProjects/habr_bot/main.py")     # не пашет, киляет процесс, но не запускает заново
        await bot.answer_callback_query(callback_query.id)

    @dispatcher.callback_query_handler(lambda c: c.data == "get_info")
    async def process_callback_button(callback_query):
        try:
            ip_command = ["wget -O - -q icanhazip.com"]
            ip_process = subprocess.Popen(
                ip_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            res = ip_process.stdout.read().decode("gbk")

            mem_used_command = ["free -m | awk {'print $3'} | tail -n2 | head -n1"]
            mem_used_process = subprocess.Popen(
                mem_used_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            shell = True,
            )
            mem_used = str.rstrip(mem_used_process.stdout.read().decode("gbk"))

            mem_total_command = ["free -m | awk {'print $2'} | tail -n2 | head -n1"]
            mem_total_process = subprocess.Popen(
                mem_total_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            mem_total = str.rstrip(mem_total_process.stdout.read().decode("gbk"))

            os_command = ["uname -r"]
            os_process = subprocess.Popen(
                os_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            os = os_process.stdout.read().decode("gbk")

            disk_command = ["df -h /dev/sda2 | awk {'print $3'} | tail -c4"]
            disk_process = subprocess.Popen(
                disk_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            disk = disk_process.stdout.read().decode("gbk")

            disk_all_command = ["df -h /dev/sda2 | awk {'print $2'} | tail -c5"]
            disk_all_process = subprocess.Popen(
                disk_all_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            disk_all = disk_all_process.stdout.read().decode("gbk")

            cpu_command = ["top -n 1 -b | awk '/^%Cpu/{print $2}'"]
            cpu_process = subprocess.Popen(
                cpu_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            cpu = str.rstrip(cpu_process.stdout.read().decode("gbk"))

            await bot.send_message(invite_code, "IP:                       " + res +
                                                "Uptime:             " + uptime + "\n" +
                                                "Kernel:               " + os +
                                                "CPU Usage:       " + cpu + " %" + "\n" +
                                                "RAM Used:        " + mem_used + "M" + "\n" +
                                                "RAM Total:         " + mem_total + "M" + "\n" +
                                                "DiskUsed:          " + disk +
                                                "DiskTotal:          " + disk_all)
            await bot.answer_callback_query(callback_query.id)
        except:
            await bot.send_message(invite_code, "Error get info")