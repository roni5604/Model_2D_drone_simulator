import time
import threading
from typing import List, Callable


class CPU:
    all_cpus: List['CPU'] = []

    def __init__(self, hz: int, name: str):
        self.hz = hz
        self.functions_list: List[Callable[[int], None]] = []
        self.is_play = False
        self.is_played_before_stop = False
        self.elapsed_milli = 0

        self.thread = threading.Thread(target=self.thread_run, name=f"Eventor_{name}")
        self.thread.daemon = True
        self.thread.start()

        CPU.all_cpus.append(self)

    @staticmethod
    def stop_all_cpus():
        for cpu in CPU.all_cpus:
            cpu.is_play = False

    @staticmethod
    def resume_all_cpus():
        for cpu in CPU.all_cpus:
            cpu.resume()

    def resume(self):
        if self.is_played_before_stop:
            self.is_play = True

    def add_function(self, func: Callable[[int], None]):
        self.functions_list.append(func)

    def play(self):
        self.is_play = True
        self.is_played_before_stop = True
        self.resume()

    def stop(self):
        self.is_play = False
        self.is_played_before_stop = False

    def get_elapsed_milli(self) -> int:
        return self.elapsed_milli

    def reset_clock(self):
        self.elapsed_milli = 0

    def thread_run(self):
        functions_size = 0
        last_sample_times = []
        i = 0

        time_to_sleep = max(2, 1000 // self.hz)

        while True:
            if functions_size != len(self.functions_list):
                functions_size = len(self.functions_list)
                last_sample_times = [0] * functions_size
                i = 0

            if functions_size == 0:
                continue

            last_sample = time.time() * 1000

            try:
                time.sleep(time_to_sleep / 1000.0)
                while not self.is_play:
                    last_sample = time.time() * 1000
            except InterruptedError:
                pass

            diff = int(time.time() * 1000 - last_sample)
            before_index = self.get_cyclic(i - 1, functions_size)
            actual_diff = last_sample_times[before_index] + diff - last_sample_times[i]
            last_sample_times[i] = last_sample_times[before_index] + diff

            curr_func = self.functions_list[i]
            curr_func(actual_diff)
            self.elapsed_milli += actual_diff

            i = (i + 1) % functions_size

    @staticmethod
    def get_cyclic(i: int, size: int) -> int:
        i %= size
        if i < 0:
            return size + i
        return i
