from datetime import datetime

d = "27 SEP 19"

dt = datetime.strptime(d, '%d %b %y')
print(dt)
