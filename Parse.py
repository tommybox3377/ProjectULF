from MySQL import get_ref_start_dt
import datetime
import re


def get_data_from_txt_file(index):
    #TODO ref http://mirl.sr.unh.edu/ULF/incoming/database/HAL_converted/HAL_2005_03_17.txt and log.txt end of data is empyt with repeattiung index
    #TODO also just skipped 03-17 for now
    f = open("data.txt", "r")
    data = []
    for line in f:
        match = re.search("(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)\s+(\-?\d+\.\d+)", line.strip())
        if match:
            id = int((float(match[1]))*10) + index
            data.append((id, float(match[2]), float(match[3]), float(match[4])))
        if len(data) >= 864000:
            break
    f.close()
    for datum in data:
        if abs(datum[1]) >= 100 or abs(datum[2]) >= 100 or abs(datum[3]) >= 100:
            return "data out of range" + str(datum)
    return data


def get_info_from_file_name(file):
    url = r"http://mirl.sr.unh.edu/ULF/incoming/database/HAL_converted/" + file
    y = int(re.search("(\d+)_(\d+)_(\d+)", file)[1])
    m = int(re.search("(\d+)_(\d+)_(\d+)", file)[2])
    d = int(re.search("(\d+)_(\d+)_(\d+)", file)[3])
    dt = datetime.datetime(year=y, month=m, day=d)

    start_dt = get_ref_start_dt("HAL")

    time_diff = (dt - start_dt).total_seconds()

    index = int(time_diff * 10 + 1)

    return url, index
