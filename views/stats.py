import datetime
import os


def cpu_usage():
    percent = 0
    try:
        import psutil
        percent = psutil.cpu_percent()
    except ImportError:
        pass
    return percent, "{}%".format(percent)


def memory_usage():
    percent = 0
    value = "0B"
    try:
        import psutil
        usage = psutil.virtual_memory()
        percent = usage.percent
        value = "{}MB/{}MB".format((usage.total - usage.available) // 1048576, usage.total // 1048576)
    except ImportError:
        pass
    return percent, value


def swap_usage():
    percent = 0
    value = "0B"
    try:
        import psutil
        usage = psutil.swap_memory()
        percent = usage.percent
        value = "{}MB/{}MB".format(usage.used // 1048576, usage.total // 1048576)
    except ImportError:
        pass
    return percent, value


def disk_usage():
    percent = 0
    value = "0B"
    try:
        import psutil
        usage = psutil.disk_usage('/')
        percent = usage.percent
        value = "{:.1f}GB/{:.1f}GB".format(usage.used / 1073741824., usage.total / 1073741824.)
    except ImportError:
        pass
    return percent, value


def cpu_temperature():
    value = 0
    try:
        res = os.popen('vcgencmd measure_temp').readline()
        value = float(res.replace("temp=", "").replace("'C\n", ""))
    except ValueError:
        pass
    return value, "{}'C".format(value)

def hdd_usage():
    percent = 0
    value = "0B"
    try:
        import psutil
        usage = psutil.disk_usage('/mnt/storage')
        percent = usage.percent
        value = "{:.1f}GB/{:.1f}GB".format(usage.used / 1073741824., usage.total / 1073741824.)
    except ImportError:
        pass
    return percent, value


class StatItem:
    def __init__(self, name, percent, value):
        self.__name = name
        self.__percent = percent
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def percent(self):
        return self.__percent

    def to_dict(self):
        return {
            "id": self.name,
            "percent": self.percent,
            "value": self.value
        }


class Stats(object):
    def __init__(self):
        self.__time_of_last_update = None
        self.__stats = []

    @staticmethod
    def __now():
        return datetime.datetime.now()

    def __update(self):
        self.__time_of_last_update = self.__now()
        del self.__stats[:]
        self.__stats.extend(
                [
                    StatItem('cpu', *cpu_usage()),
                    StatItem('mem', *memory_usage()),
                    StatItem('swap', *swap_usage()),
                    StatItem('disk', *disk_usage()),
                    StatItem('hdd', *hdd_usage())
                ]
        )

    def data(self):
        self.__update()
        data = dict()
        data["time"] = self.__time_of_last_update.strftime("%Y-%m-%d %H:%M:%S")
        data["stats"] = [stat.to_dict() for stat in self.__stats]
        return data
