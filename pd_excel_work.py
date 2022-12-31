import pandas as pd

ws = None


def choose_week_and_make_dataframe(week):
    """
    :param week: must be written in this format: "Week 1"
    :return:
    """
    from openpyxl import load_workbook
    global ws
    wb = load_workbook(filename="Candito 6 Week Program.xlsx", data_only=True)
    inputs = wb["Inputs"]
    Week_1 = wb["Week 1"]
    Week_2 = wb["Week 2"]
    Week_3 = wb["Week 3"]
    Week_4 = wb["Week 4"]
    Week_5 = wb["Week 5"]
    Week_6 = wb["Week 6"]
    if week == "inputs":
        ws = inputs
    if week == "Week 1":
        ws = Week_1
    if week == "Week 2":
        ws = Week_2
    if week == "Week 3":
        ws = Week_3
    if week == "Week 4":
        ws = Week_4
    if week == "Week 5":
        ws = Week_5
    if week == "Week 6":
        ws = Week_6
    try:
        data = ws.values
    except NameError:
        return "No such week"
    from itertools import islice
    cols = next(data)[1:]
    data = list(data)
    idx = [r[0] for r in data]
    data = (islice(r, 1, None) for r in data)
    df_1 = pd.DataFrame(data, index=idx, columns=cols)
    return df_1


pd.options.display.max_columns = None
pd.options.display.max_rows = None


def make_list_of_indexes_where_are_values(week):
    list_of_indexes = []
    dataframe = choose_week_and_make_dataframe(week)
    none_counter = 0
    position_counter = 0
    for index, rows in dataframe.iterrows():
        if index is None:
            none_counter += 1
            if none_counter == 2:
                position_counter += 1
                none_counter = 0
                continue
            position_counter += 1
            list_of_indexes.append(position_counter)
        else:
            position_counter += 1
            continue
    list_of_indexes.append(len(dataframe.index) + 1)
    tuple_list = [(1, list_of_indexes[1])]
    for i in range(1, len(list_of_indexes) - 1):
        tuple_list.append((list_of_indexes[i] + 0, list_of_indexes[i + 1]))
    return tuple_list


def list_of_dates_where_you_workout(week):
    dataframe = choose_week_and_make_dataframe(week)
    list_of_indexes = make_list_of_indexes_where_are_values(week)
    list_of_dates = []
    for i in range(0, len(list_of_indexes)):
        list_of_dates.append(dataframe.iloc[list_of_indexes[i][0]].name)
    return list_of_dates


def find_the_closest_date():
    from datetime import datetime, timedelta
    list_of_lists_of_dates = [list_of_dates_where_you_workout("Week 1"), list_of_dates_where_you_workout("Week 2"),
                              list_of_dates_where_you_workout("Week 3"),
                              list_of_dates_where_you_workout("Week 4"), list_of_dates_where_you_workout("Week 5")]
    list_of_times = []
    for i in range(5):
        for j in range(len(list_of_lists_of_dates[i])):
            if list_of_lists_of_dates[i][j] - datetime.today() < timedelta(days=0):
                continue
            else:
                list_of_times.append(list_of_lists_of_dates[i][j] - datetime.today())
    try:
        return min(list_of_times), datetime.today() + min(list_of_times)
    except ValueError:
        return "no Future dates"


def range_of_closest_workout():
    closet_date = find_the_closest_date()
    list_of_lists_of_dates = [list_of_dates_where_you_workout("Week 1"), list_of_dates_where_you_workout("Week 2"),
                              list_of_dates_where_you_workout("Week 3"),
                              list_of_dates_where_you_workout("Week 4"), list_of_dates_where_you_workout("Week 5")]
    date, week, index = None, None, None
    for i in range(5):
        for j in range(len(list_of_lists_of_dates[i])):
            if list_of_lists_of_dates[i][j] == closet_date[1]:
                week, date, index = "Week " + str(i + 1), list_of_lists_of_dates[i][j], j
                break

    indexes = make_list_of_indexes_where_are_values(week)
    range_of_solution = indexes[index]
    return range_of_solution, week, date


def return_workout_from_specific_range(range_of_solution, week):
    dataframe = choose_week_and_make_dataframe(week)
    return dataframe.iloc[range_of_solution[0]:range_of_solution[1]]


def return_closest_workout():
    """
    This is an important function, that combines most of the functions above and is used to return the closest workout
    :return: a slice of dataframe that contains the closest workout
    """
    range_of_solution, week, date = range_of_closest_workout()
    return return_workout_from_specific_range(range_of_solution, week)
