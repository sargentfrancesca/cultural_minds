def timings(participants, array):
    times = []
    staggers = len(array) - 1
    constant = array[-1]
    for i in range(0, staggers):
        try:
            previous = times[i-1]
        except IndexError:
            previous = 0
        last = array[i] + previous
        times.append(array[i] + previous)

    times_length = len(times)
    for x in range(times_length, participants):
    	pre = x - 1
        previous = times[pre]
        times.append(previous + constant)

    return times
print timings(10, [0, 2, 4])
