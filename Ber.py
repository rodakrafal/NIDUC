def compare(starting_msg, ending_msg):
    sum = 0
    for i in range(0, len(starting_msg)):
        if starting_msg[i] != ending_msg[i]:
            sum += 1
    return sum
