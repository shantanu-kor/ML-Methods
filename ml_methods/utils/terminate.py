from time import sleep

def __stop() -> None:
    exit(1)

def __ask(q: str) -> None:
    if q == 'n':
        pass
    elif q == 'y':
        __stop()
    else:
        print("Invalid Input!\n")
        a = input("exit? y/n\n")
        __ask(a)

def __wait(t=5) -> None:
    try:
        if type(t) != int or t < 0:
            __stop()
        print("Press Ctrl+C to continue...")
        for i in range(t):
            if i == t - 1:
                print("1")
                sleep(0.5)
                print("exiting...")
                sleep(0.5)
            else:
                print(t - i)
                sleep(1)
        __stop()
    except KeyboardInterrupt:
        print("\n")

def retrn(r: str, e: str | TypeError | Exception):
    try:
        print(e,"\n")
        match r:
            case 'c':
                pass
            case 'w':
                __wait()
            case 'a':
                a = input("exit? y/n\n")
                __ask(a)
            case _:
                raise Exception("Invalid argument: r => 'c'/'w'/'a'")
    except:
        __stop()