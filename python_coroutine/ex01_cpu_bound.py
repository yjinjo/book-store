# ex01_cpu_bound.py


def cpu_bound_func(number: int):
    total = 1
    arange = range(1, number + 1)

    for i in arange:
        for j in arange:
            for k in arange:
                total *= i * j * k

    return total


if __name__ == "__main__":
    result = cpu_bound_func(30)
    print(result)
