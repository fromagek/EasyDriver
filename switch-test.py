from switch import Switch
import time

switch=Switch(24)

for i in range(333):
	print(switch.switch_status())
	time.sleep(.1)
