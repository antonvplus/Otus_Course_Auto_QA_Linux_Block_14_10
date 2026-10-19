import subprocess
from datetime import datetime


def dual_print(text):
    print(text)
    print(text, file=file)

result = subprocess.run(['ps', 'aux'],check=False, capture_output=True, text=True)

lines = result.stdout.strip().split("\n")
headers = lines[0].split()
users = {}

processes = []
for line in lines[1:]:
    line = line.split()
    temp = {}
    for i in range(len(headers)):
        if i == 0 and line[i] not in users:
            users[line[i]] = 1
        elif i == 0 and line[i] in users:
            users[line[i]] += 1
        if len(headers) != len(line):
            if i + 1 == len(headers):
                temp[headers[i]] = line[i:]
            else:
                temp[headers[i]] = line[i]
        else:
            temp[headers[i]] = line[i]
    processes.append(temp)

with open(f"{datetime.now().strftime("%d-%m-%Y-%H:%M")}-scan.txt", "w", encoding="utf-8") as file:
    dual_print("Отчёт о состоянии системы:")
    dual_print(f"Пользователи системы: {(', ').join(f"'{u}'" for u in users)}")
    dual_print(f"Процессов запущено: {len(processes)}\n")
    dual_print("Пользовательских процессов:")
    for k,v in users.items():
        dual_print(f"{k}: {v}")
    dual_print("\n")
    dual_print(f"Всего памяти используется: {sum([float(line["%MEM"]) for line in processes]):.1f}%")
    dual_print(f"Всего CPU используется: {sum([float(line["%CPU"]) for line in processes]):.1f}%")
    dual_print(f"Больше всего памяти использует: {(" ").join(max(processes, key=lambda x: float(x["%MEM"]))["COMMAND"]):.20}..."
        if len((" ").join(max(processes, key=lambda x: float(x["%MEM"]))["COMMAND"])) > 20
        else f"Больше всего памяти использует: {(" ").join(max(processes, key=lambda x: float(x["%MEM"]))["COMMAND"])}")
    dual_print(f"Больше всего CPU использует: {(" ").join(max(processes, key=lambda x: float(x["%CPU"]))["COMMAND"]):.20}..."
        if len((" ").join(max(processes, key=lambda x: float(x["%CPU"]))["COMMAND"])) > 20
        else f"Больше всего CPU использует: {(" ").join(max(processes, key=lambda x: float(x["%CPU"]))["COMMAND"])}")
