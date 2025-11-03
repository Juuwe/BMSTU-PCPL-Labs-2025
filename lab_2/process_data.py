import json

import random

from typing import List, Dict

import lab_python_fp.field as field
import lab_python_fp.unique as unique
import lab_python_fp.gen_random as gen_random
import lab_python_fp.sort as sort
import lab_python_fp.cm_timer as cm_timer
import lab_python_fp.print_result as print_result


with open("data.json", 'r', encoding='utf-8') as file:
    json_data = json.load(file)

@print_result.print_result
def f1(data: List[Dict]) -> List:
    return sorted(unique.Unique(field.field(data, "job-name"), ignore_case=True), key = lambda s: s.lower())

@print_result.print_result
def f2(data: List) -> List:
    return list(filter(lambda s: "программист" in s.lower(), data))

@print_result.print_result
def f3(data: List) -> List:
    return list(map(lambda job: job + " с опытом Python", data))

@print_result.print_result
def f4(data: List) -> List:
    programmer_salary = list(zip(data, gen_random.gen_random(len(data), 100_000, 200_000)))
    return [f"{spec}, зарплата {salary} р." for spec, salary in programmer_salary]

if __name__ == "__main__":
    with cm_timer.cm_timer_1():
        f4(f3(f2(f1(json_data))))
