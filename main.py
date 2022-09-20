import time
import morn
import eve


def main():
    counter = 0
    while True:
        if counter == 0:
            morn.parse_morn()
            counter = 1
            # Следующий запуск цикла через 14 часов
            time.sleep(50400)
        elif counter == 1:
            eve.parse_eve()
            counter = 0
            # Следующий запуск цикла через 10 часов
            time.sleep(36000)


if __name__ == '__main__':
    main()
