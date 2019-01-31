import datetime

for num in range(1, 1295):
    old_time = datetime.datetime.now()
    input_f = open('testfilesnow/input_{:04d}.txt'.format(num), "r")
    output = 0
    current_sum = 0
    dic = []
    stck = []

    def is_non_attacking(row, col):
        for j in range(len(stck)):
            if stck[j][0] == row or stck[j][1] == col or row - col == stck[j][0] - stck[j][1] or -col - row == -stck[j][1] - stck[j][0]:
                return False
        return True


    def rec(yy, count):
        global current_sum
        global output

        if count == 0:
            output = max(current_sum, output)
            return

        for y in range(yy, len(dic)):
            value = dic[y][2]
            if output >= current_sum + value * count:
                return
            if is_non_attacking(dic[y][0], dic[y][1]):
                stck.append((dic[y][0], dic[y][1]))
                current_sum += value
                rec(y + 1, count - 1)
                popped = stck.pop()
                current_sum -= Matrix[popped[0]] [popped[1]]


    for i, line in enumerate(input_f):
        if i == 0:
            n = int(line.strip('\n'))
            Matrix = [[0 for x in range(n)] for y in range(n)]
        elif i == 1:
            p = int(line.strip('\n'))
        elif i == 2:
            s = int(line.strip('\n'))
        else:
            inp = line.strip('\n').split(',')
            Matrix[int(inp[0])][int(inp[1])] += 1

    for i in range(n):
        for j in range(n):
            dic.append([i, j, Matrix[i][j]])

    dic = sorted(dic, key=lambda t: t[2], reverse=True)


    for v in range(n*n):
        stck = []
        current_sum = 0
        val = dic[v][2]
        stck.append([dic[v][0], dic[v][1]])
        current_sum += val
        rec(v + 1, p - 1)

    outputstr = "n = "+str(n)+" ,p = "+str(p)+",s = "+str(s)+",G = "+str(output)+" ,execution time = "
    new_time = datetime.datetime.now()

    exec_time = new_time - old_time
    open("output.txt", "a").write(outputstr+"%.2f\n" % exec_time.total_seconds())