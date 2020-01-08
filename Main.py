import Download, Parse, MySQL
import datetime

start = datetime.datetime(  # inclusive
    year=2005,
    month=2,
    day=18,
    hour=0,
    minute=0,
    second=0,
    microsecond=0  # has to be in .1 sec increments
)
end = datetime.datetime(  # exclusive
    year=2005,
    month=2,
    day=19,
    hour=0,
    minute=0,
    second=0,
    microsecond=0  # has to be in .1 sec increments/ 1000000 microseconds
    # eg. microsecond=100000
    # eg. microsecond=200000
)

startdt = datetime.datetime.now()
data = MySQL.get_data("HAL", start, end)
print(data)
print(datetime.datetime.now()-startdt)
