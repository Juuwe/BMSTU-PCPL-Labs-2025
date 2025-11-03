import math
import os
import sys

from colorama import Style, Fore, init

init()

def get_coeff_from_user(index, prompt) -> str:
    try:
        return float(sys.argv[index])
    except:
        while True:
            print(prompt, end = ' ')
            try:
                return float(input())
            except:
                print(Fore.YELLOW + "Incorrent coefficient. Try again")
                print(Style.RESET_ALL, end = '')

def print_answer(roots):
    print("Roots of your equation:")

    for i in range(len(roots)):
        print(Fore.GREEN + "x_" + str(i + 1), ' = ', roots[i])

def solve_incomplete_quadrate_equataion(quadr_coeff: float, free_coeff: float):
    if quadr_coeff * free_coeff > 0:
        return "No real roots"
    root = math.sqrt(-free_coeff / quadr_coeff)
    return [-root, root]

def solve_biquadrate_equation(a: float, b: float, c: float):
    if a == 0:
        if b == 0:
            return "Equation is not biquadrate"

        if c == 0:
            return [0.]

        return  solve_incomplete_quadrate_equataion(b, c)


    discrimannt = b**2 - 4 * a * c

    roots = list()

    if discrimannt < 0:
        return "No real roots"
    if discrimannt == 0:
        t = -b / (2 * a)
        if t < 0:
            return "No real roots"
        if t == 0:
            [0.]

        root = math.sqrt(t)
        return [-root, root]

    t1 = (-b + math.sqrt(discrimannt)) / (2 * a)
    t2 = (-b - math.sqrt(discrimannt)) / (2 * a)

    if t1 >= 0:
        root1 = math.sqrt(t1)
        roots.extend([-root1, root1])

    if t2 >= 0:
        root2 = math.sqrt(t2)
        roots.extend([-root2, root2])

    return sorted(roots)

def run():
    command_args = sys.argv[1:]


    coeff_a = get_coeff_from_user(1, "Enter coefficient A:")
    coeff_b = get_coeff_from_user(2, "Enter coefficient B:")
    coeff_c = get_coeff_from_user(3, "Enter coefficient C:")

    answer = solve_biquadrate_equation(coeff_a, coeff_b, coeff_c)

    if isinstance(answer, str):
        print(Fore.RED + answer)
        return

    print_answer(answer)

def main():
    try:
        run()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()
