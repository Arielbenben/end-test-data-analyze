from app.db.repository.terrorist_attacks_repository import get_all_data
import pandas as pd



def get_all_data_at_df():
    data = get_all_data()
    return pd.DataFrame(data)


def get_all_sort_by_most_deadly(num: int):
    df = get_all_data_at_df()

    df['total_casualties'] = df['casualties'].apply(lambda x: x.get('wound', 0) + x.get('killed', 0) * 2)
    if num != 0:
        return df.nlargest(num, 'total_casualties')
    else:
        return df.sort_values(by='total_casualties', ascending=False)

