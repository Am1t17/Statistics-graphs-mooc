import json
import xlsxwriter
import video_to_data


class VideosStatisticts:

    def __init__(self,ExcelNAme: str):
        self.workbook = xlsxwriter.Workbook("video_graph_to_"+ExcelNAme)
        self.title_format = self.workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})
        self.url_format = self.workbook.add_format({
            'bold': 1,
            'border': 1,
            'underline': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'blue'})
        self.video_subtitles = ['Users', 'Watch Time', 'Percent']
        self.title_start_col = 1
        self.subtitle_start_col = 1
        self.sum_col_idx = 1
        self.time_col_idx = 2
        self.percent_col_idx = 3

    # def __del__(self):
    #     self.workbook.close()

    @staticmethod
    def calculate_percent(watchers: list):
        total_watchers = watchers[0]
        percent_list = list()
        for watchers_count in watchers:
            per = float("%.f" % (watchers_count / total_watchers * 100))
            percent_list.append(per)
        return percent_list

    @staticmethod
    def get_xlsx_column_string(n):
        """The character 'A' is represented by the number 65,
        26 is the number of characters in English alphabet."""
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string

    def create_xlsx_cell_index(self, col, row):
        col_str = self.get_xlsx_column_string(col)
        return "{col}{row}".format(col=col_str, row=row)

    def create_xlsx_cell_range(self, c_start, c_end, r_start, r_end):
        start_str = self.create_xlsx_cell_index(c_start, r_start)
        end_str = self.create_xlsx_cell_index(c_end, r_end)
        return "{start}:{end}".format(start=start_str, end=end_str)

    def merge_cells_and_write_url(self, worksheet, url, title, videos_num):
        title_end_col = self.title_start_col + \
                        (videos_num * len(self.video_subtitles)) - 1
        title_range = self.create_xlsx_cell_range(
            self.title_start_col, title_end_col, 1, 1)
        worksheet.merge_range(title_range, title, self.url_format)
        title_cell = self.create_xlsx_cell_index(self.title_start_col, 1)
        worksheet.write_url(title_cell, url, self.url_format, string=title)
        self.title_start_col = title_end_col + 1

    def write_subtitle(self, worksheet, sub_title):
        subtitle_end_col = self.subtitle_start_col + \
                           len(self.video_subtitles) - 1
        subtitle_range = self.create_xlsx_cell_range(
            self.subtitle_start_col, subtitle_end_col, 2, 2)
        worksheet.merge_range(subtitle_range, sub_title, self.title_format)
        self.subtitle_start_col = subtitle_end_col + 1

    def create_video_table(self, worksheet, videos_dict: dict):
        # The first returned value of videos_dict.items() is unused,
        # therfore we assign it to nothing '_'
        for _, video_data in videos_dict.items():
            self.write_subtitle(worksheet, video_data["video_name"])

            # Merge column's title with its data
            table = video_data["video_graph"]
            sum_col = [self.video_subtitles[0]] + table["sum"]
            time_col = [self.video_subtitles[1]] + table["time"]
            percent_list = self.calculate_percent(table["sum"])
            percent_col = [self.video_subtitles[2]] + percent_list

            sum_col_xlsx_idx = self.create_xlsx_cell_index(self.sum_col_idx, 3)
            time_col_xlsx_idx = self.create_xlsx_cell_index(
                self.time_col_idx, 3)
            percent_col_xlsx_idx = self.create_xlsx_cell_index(
                self.percent_col_idx, 3)

            worksheet.write_column(sum_col_xlsx_idx, sum_col)
            worksheet.write_column(time_col_xlsx_idx, time_col)
            worksheet.write_column(percent_col_xlsx_idx, percent_col)

            self.sum_col_idx += 3
            self.time_col_idx += 3
            self.percent_col_idx += 3

    def xlsx_workbook(self, data_dict: dict):

        # The first returned value of data_dict.items() is unused,
        # therfore we assign it to nothing '_'
        for _, sheet_data in data_dict.items():
            # worksheet name cannot  be longer than 31 chars
            worksheet_name = sheet_data['display_name'][:30]
            worksheet = self.workbook.add_worksheet(name=worksheet_name)
            worksheet.right_to_left()

            self.title_start_col = 1
            self.subtitle_start_col = 1
            self.sum_col_idx = 1
            self.time_col_idx = 2
            self.percent_col_idx = 3

            # The first returned value of sheet_data["children"].items()
            # is unused, therfore we assign it to nothing '_'
            for _, child_data in sheet_data["children"].items():
                videos_num = len(child_data["videos"])
                if videos_num != 0 and child_data["videos"]:
                    self.merge_cells_and_write_url(worksheet,
                                                   child_data["url_link"],
                                                   child_data["display_name"],
                                                   videos_num)
                    self.create_video_table(worksheet, child_data["videos"])


while True:
    JSON_name = input('enter json name:')
    try:
        json_file = open(JSON_name, "r")
        JF = json.load(json_file)
        json_file.close()
    except FileNotFoundError:
        print("Json file not found.")
    else:
        break

while True:
    CSV_name = input('enter csv name:')
    try:
        datastore = video_to_data.filter_table_videos(CSV_name,JF)
    except FileNotFoundError:
        print("Json file not found.")
    else:
        break
Excel = VideosStatisticts(CSV_name)
print(datastore)
file2 = open("json1","w",encoding="utf-8")
json.dump(datastore,file2,ensure_ascii=False)
file2.close()
#Excel.xlsx_workbook(datastore)
#Excel.workbook.close()



