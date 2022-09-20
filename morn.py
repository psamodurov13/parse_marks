import functions as fn


def parse_morn():
    # Создаем новый лист, если начался новый месяц
    if fn.today[:2] == '01':
        fn.gc.open('Sheets-1').sheet1.duplicate(new_sheet_name=fn.today[3:])
        fn.gc.open('Sheets-1').worksheet(fn.today[3:]).delete_rows(start_index=3, end_index=100)

    fn.parse_marks(fn.products, fn.result_m)
    fn.add_to_gsheet(fn.result_m)
            

if __name__ == '__main__':
    parse_morn()
