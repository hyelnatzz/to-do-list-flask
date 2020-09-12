"""import winsound
winsound.PlaySound("crash", winsound.SND_ASYNC | winsound.SND_ALIAS)

print('continued')
"""


from playsound import playsound

playsound('crash.mp3' )
print('continued')

"""import winsound         # for sound
import time             # for sleep

winsound.Beep(440, 4000)  # frequency, duration
print('while playing')
time.sleep(3)        # in seconds (0.25 is 250ms)

winsound.Beep(600, 250)
time.sleep(0.25)
"""


"""from datetime import datetime, timedelta
import time

print(datetime.strftime(datetime.now(), '%d/%m/%Y'))


def finishTime(start_time, duration):
    time_lst = start_time.split(':')
    hr, mt = [int(i) for i in time_lst]
    new_min = mt + duration
    if new_min == 60:
        hr += 1
        mt = 0
    elif new_min > 60:
        hr += 1
        mt = new_min - 60
    else:
        mt = new_min
    return ':'.join([str(i) for i in [hr,mt]])

print(finishTime('12:50', 30))"""