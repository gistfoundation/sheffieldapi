from datetime import datetime


def parse_date(date, alt_datetime=None):
    if not date: return None
    try:
        date = datetime.strptime(date, '%a %d %b %Y')
    except:
        if alt_datetime:
            date = "%s %s" % (date, alt_datetime.strftime('%b %Y'))
        date = datetime.strptime(date, '%a %d %b %Y')
    return date

def start_end_date(date):
    if ',' in date:
        first_date, _, second_date = date.partition(', ')
        end = parse_date(second_date)
        start = parse_date(first_date, alt_datetime=end)
        # TODO: Handle the case where we get comma separated
        return start, end
    start, _, end = date.partition(' to ')
    if not end:
        start, _, end = date.partition(' - ')
    if end:
        end = parse_date(end)
        start = parse_date(start, alt_datetime=end)
        return start, end
    else:
        return parse_date(start), parse_date(end)

def start_end_time(time):
    start, _, end = time.partition(' to ')
    if not end:
        start, _, end = time.partition(' - ')
    return start, end
