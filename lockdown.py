import datetime
from pandas import Series, concat


class LockDown(object):
    def __init__(self, country_code, lockdown_start_date, lockdown_end_date):
        self.country_code = country_code
        self.split1 = lockdown_start_date.split('.')
        self.lockdown_start_date = "{}-{}-{}".format(self.split1[2], self.split1[1], self.split1[0])
        self.lockdown_start_date_datetime_object = datetime.datetime.strptime(self.lockdown_start_date, '%Y-%m-%d')
        self.split2 = lockdown_end_date.split('.')
        self.lockdown_end_date = "{}-{}-{}".format(self.split2[2], self.split2[1], self.split2[0])
        self.lockdown_end_date_datetime_object = datetime.datetime.strptime(self.lockdown_end_date, '%Y-%m-%d')
        self.dataframe = None
        self.lockdown_success_point = 0
        self.change_on_percent = 0

    def set_data(self, dataframe, who_data, columns_will_be_added):
        data_by_country = dataframe.loc[dataframe['country_region_code'] == self.country_code]
        mask = (data_by_country['date'] >= self.lockdown_start_date) & (data_by_country['date'] <= self.lockdown_end_date)
        edited_by_date = data_by_country.loc[mask]
        who_data_by_country = who_data.loc[who_data['Country_code'] == self.country_code]
        mask2 = (who_data_by_country['date'] >= self.lockdown_start_date) & (who_data_by_country['date'] <= self.lockdown_end_date)
        who_data_edited_by_date = who_data_by_country.loc[mask2]
        columns_will_be_added_list = [Series(who_data_edited_by_date[x].to_numpy(), name=x) for x in columns_will_be_added]
        edited_by_date.reset_index(inplace=True, drop=True)
        self.dataframe = concat([edited_by_date, *columns_will_be_added_list], axis=1)

    def set_lockdown_success_point(self, point):
        self.lockdown_success_point = point

    def get_lockdown_success_point(self):
        return self.lockdown_success_point

    def set_change_percent(self, percent):
        self.change_on_percent = percent

    def get_change_percent(self):
        return self.change_on_percent

    def get_before_lockdown_average_case_count_by_week(self, who_data, week):
        datetime_week = datetime.timedelta(weeks=1)
        before_lockdown_start_date = str(self.lockdown_start_date_datetime_object - datetime_week * week)
        who_data_by_country = who_data.loc[who_data['Country_code'] == self.country_code]
        mask = (who_data_by_country['date'] >= before_lockdown_start_date) & (
                    who_data_by_country['date'] <= self.lockdown_start_date)
        edited_by_date_for_before_lockdown = who_data_by_country.loc[mask]
        print(edited_by_date_for_before_lockdown['New_cases'], before_lockdown_start_date, self.lockdown_start_date)
        return edited_by_date_for_before_lockdown['New_cases'].mean()

    def get_after_lockdown_average_case_count_by_week(self, who_data, week):
        datetime_week = datetime.timedelta(weeks=1)
        after_lockdown_start_date = str(self.lockdown_end_date_datetime_object + datetime_week * week)
        who_data_by_country = who_data.loc[who_data['Country_code'] == self.country_code]
        mask = (who_data_by_country['date'] >= self.lockdown_end_date) & (
                    who_data_by_country['date'] <= after_lockdown_start_date)
        edited_by_date_for_after_lockdown = who_data_by_country.loc[mask]
        return edited_by_date_for_after_lockdown['New_cases'].mean()

    def get_avg_values(self):
        return {
            'retail_and_recreation': self.dataframe['retail_and_recreation'].mean(),
            'grocery_and_pharmacy': self.dataframe['grocery_and_pharmacy'].mean(),
            'parks': self.dataframe['parks'].mean(),
            'transit_stations': self.dataframe['transit_stations'].mean(),
            'workplaces': self.dataframe['workplaces'].mean(),
            'residential': self.dataframe['residential'].mean(),
        }



