import pigpio 

def process_signal_send(pi,gpio):
    pi.write(gpio,1)
    return

def process_signal_wait(pi,gpio):
    if pi.read(gpio) == 1:
        print(True)
        return True
    else :
        print(False)
        return False

if __name__ == "__main__":
    pi = pigpio.pi()

    pi.set_mode(17, pigpio.INPUT)
    pi.set_mode(24, pigpio.OUTPUT)

    pi.set_pull_up_down(24, pigpio.PUD_DOWN)
    process_signal_send(pi,24)
    process_signal_wait(pi,17)