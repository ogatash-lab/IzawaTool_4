import time

# 実行時間の計測開始
def count_start(filename):
    start_time = time.perf_counter()
    with open(filename, mode = "a") as f:
        print('start_time = ' + str(start_time))
        f.write(str(start_time) + "\n")
    return 0

# 実行時間の計測終了
def count_stop(filename):
    stop_time = time.perf_counter()
    with open(filename, mode = "a") as f:
        print('stop_time = ' + str(stop_time))
        f.write(str(stop_time) + "\n")
    return 0

# result_table.pyで実行時間を表示している
def culcurate_time(filename):
    time_list = []
    with open(filename, mode = "r") as f:
        for line in f:
            time_list.append(line.replace('\n',''))
    print(time_list)

    exec_time_second = float(time_list[1]) - float(time_list[0])
    
    exec_time_minite = round(exec_time_second/60, 2)
    print(exec_time_minite)
    return str(round(exec_time_second, 3)) + " [s]"