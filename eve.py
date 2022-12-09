import functions as fn


def parse_eve():
    '''
    The function get evening indicators
    '''
    result_e = fn.result_e
    result_m = fn.gc.open('Sheets-1').worksheet(fn.today[3:]).row_values(fn.gc.open('Sheets-1')
                                                                      .worksheet(fn.today[3:]).find(fn.today).row)
    fn.parse_marks(fn.products, result_e)
    fn.add_to_gsheet(result_e)

    # Calculate the difference between evening and morning data
    result_diff = ['Разница', fn.today]
    for i in range(2, len(result_m)):
        if '.' not in result_m[i] and result_e[i].isdigit():
            result_diff.append(int(result_e[i]) - int(result_m[i]))
        else:
            mark = 5
            summ = 0
            for p in result_diff[-5:]:
                summ += int(p) * mark
                mark -= 1
            try:
                avg = '%.2f' % (summ / sum([int(m) for m in result_diff[-5:]]))
            except ZeroDivisionError:
                avg = result_e[i]
            result_diff.append(avg)
    fn.add_to_gsheet(result_diff)


if __name__ == '__main__':
    parse_eve()
