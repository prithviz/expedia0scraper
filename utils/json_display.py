def printer(a):
    for i in a:
        x = 0
        for k, v in i.items():
            if k == "timings":
                for i in v:
                    x += 1
                    print "Result ", x
                    print "Arrival_date_long ", "= ", i['arrival_date_longStr']
                    print "Arrival_date ", "= ", i['arrival_date']
                    print "Departure_airport ", "= ", i['departure_airport']
                    print "Arrival_time ", "= ", i['arrival_time']
                    print "Arrival_airport", "= ", i['arrival_airport']
                    print "Departure_date_long ", "= ", i['departure_date_longStr']
                    print "Departure_date ", "= ", i['departure_date']
                    print "Departure_time ", "= ", i['departure_time']
            else:
                print k, "=", v
    return len(a)
