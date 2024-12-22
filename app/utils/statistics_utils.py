

def get_color_to_casualties_grade(grade):
    if grade > 20:
        return 'red'
    elif grade > 10:
        return 'orange'
    elif grade > 5:
        return 'pink'
    else:
        return 'green'


def sort_top_percentage_change(data):
    sorted_data = sorted(data, key=lambda x: x['percentage_change'], reverse=True)
    return sorted_data[:5]


def calculate_percent_change(area):
    percent_change = ((area['first_year_sum_events']['sum_events'] - area['last_year_sum_events']['sum_events']) /
                             area['first_year_sum_events']['sum_events']) * 100
    return round(percent_change, 2)