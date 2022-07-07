from time import sleep


class _terminate:
    @staticmethod
    def _stop() -> None:
        exit(1)

    @classmethod
    def _ask(cls, q: str) -> None:
        if q == 'n':
            pass
        elif q == 'y':
            cls._stop()
        else:
            print("Invalid Input!\n")
            cls._stop()

    @classmethod
    def _wait(cls, t: int) -> None:
        try:
            if type(t) != int or t < 0:
                cls._stop()
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
            cls._stop()
        except KeyboardInterrupt:
            print("\n")


class Terminate(_terminate):
    @classmethod
    def stop(cls) -> None:
        cls._stop()

    @classmethod
    def ask(cls, a='n') -> None:
        cls._ask(a)

    @classmethod
    def wait(cls, t=5) -> None:
        cls._wait(t)

    @classmethod
    def retrn(cls, r: bool, e: str | TypeError | Exception):
        if r is False:
            print(e)
            print("Invalid command!\n")
            cls.wait()
        if r is True:
            print(e)
            pass
        if type(r) != bool:
            print(str(type(r)) + " is not bool")
            cls.stop()
