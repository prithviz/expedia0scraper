__AUTHOR__ = "Tony"


def format_date(date):
    import datetime
    dt = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%y')
    return dt


def choices_form(e, s=0):
    a = []
    for i in range(s, e + 1):
        x = (str(i), str(i))
        a.append(x)
    return a
