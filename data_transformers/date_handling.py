import re
from datetime import datetime


_date_formats = [
    "%a, %d %b %Y %H:%M:%S %z",  # "Mon, 02 Jun 2025 10:00:00 +0200"
    "%Y.%m.%d %H:%M"             # "2025.06.09 11:02"
]


def replace_dates_with_deltas(text: str, day_zero_name: str = "Start ") -> str:

    # regex to capture date substings after "Date: "
    pattern = re.compile(r"^Date:\s*(.+)$", re.MULTILINE)
    lines = pattern.findall(text)

    # parse known formats
    def parse_date(substring):
        for format in _date_formats:
            try:
                # NOTE: this doesn't take timeoózones into account.
                dt = datetime.strptime(substring, format)
                return dt.replace(tzinfo=None)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {substring}")

    # convert to datetimes
    dates = [parse_date(s.strip()) for s in lines]

    t0 = dates[0]

    # replacements
    def delta_str(dt: datetime):
        dt = dt.replace(tzinfo=None)
        delta = dt - t0
        days, secs = delta.days, delta.seconds
        hours, mins = secs // 3600, (secs % 3600) // 60
        if days > 0:
            return f"+ {days}d {hours}h"
        elif hours > 0:
            return f"+ {hours}h {mins}m"
        else:
            return f"+ {mins}m"

    deltas = [day_zero_name] + [day_zero_name + delta_str(d) for d in dates[1:]]

    # replace sequentially
    out = text
    for orig, rep in zip(lines, deltas):
        out = out.replace(f"Date: {orig}", f"Date: {rep}", 1)

    return out
