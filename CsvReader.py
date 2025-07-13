import pandas as pd


class CsvReader:
    def __init__(self, csv_file):
        """initializes csv_file and reads it as df"""
        self.csv_file = csv_file
        self.df = pd.read_csv(self.csv_file)

    def get_dataframe(self):
        """Returns DataFrame"""
        return self.df

    def filter_data(self, grade=None, cohort=None, region=None):
        """Returns filtered data"""
        filtered_df = self.df.copy()

        if grade and grade != "All Grades":
            filtered_df = filtered_df[filtered_df['grade'] == grade]

        if cohort and cohort != "All Cohorts":
            filtered_df = filtered_df[filtered_df['cohort'] == cohort]

        if region and region != "All Regions":
            filtered_df = filtered_df[filtered_df['region'] == region]

        return filtered_df

    def get_student_metrics(self, grade=None, cohort=None, region=None):
        """Returns student metrics based on filtered data"""
        filtered_df = self.filter_data(grade, cohort, region)

        total_students = len(filtered_df)
        active_students = len(filtered_df[filtered_df['status_flag'] == 'Active'])
        active_percentage = (active_students / total_students * 100) if total_students > 0 else 0

        return {
            'total_students': total_students,
            'active_students': active_students,
            'active_percentage': round(active_percentage, 1)
        }

    def get_kit_tracking_data(self):
        """Returns kit shipping status data for pie chart"""
        shipping_statuses = self.df['kit_shipping_status'].value_counts()

        return {
            "Category": shipping_statuses.index.tolist(),
            "Value": shipping_statuses.values.tolist()
        }

    def get_module_completion_data(self):
        """Returns module completion data for bar chart"""
        module_stats = self.df.groupby(['module_id', 'module_name']).agg({
            'student_id': 'count',
            'completion_status': lambda x: (x == 'Completed').sum()
        }).reset_index()


        module_stats['completion_rate'] = (
                module_stats['completion_status'] / module_stats['student_id'] * 100
        ).round(1)


        module_stats['module_display'] = module_stats['module_id'].str.replace('MOD00', 'Module ')
        module_stats = module_stats.sort_values('module_id')

        return {
            'Module': module_stats['module_display'].tolist(),
            'Completion_Rate': module_stats['completion_rate'].tolist()
        }

    def get_pvsa_eligible_count(self, grade=None, cohort=None, region=None):
        """Returns count of PVSA eligible students"""
        filtered_df = self.filter_data(grade, cohort, region)
        return len(filtered_df[filtered_df['notes'].str.contains('PVSA eligible', na=False)])

    def get_kits_delivered_count(self, grade=None, cohort=None, region=None):
        """Returns count of delivered kits"""
        filtered_df = self.filter_data(grade, cohort, region)
        return len(filtered_df[filtered_df['kit_shipping_status'] == 'Delivered'])

    def get_kits_pending_count(self, grade=None, cohort=None, region=None):
        """Returns count of pending kits"""
        filtered_df = self.filter_data(grade, cohort, region)
        return len(filtered_df[filtered_df['kit_shipping_status'] == 'Pending'])