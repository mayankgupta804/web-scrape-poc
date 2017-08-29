from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.flowables import PageBreak

from config.properties import Properties
from report.reportTable import ReportTable
from utility.counter import Counter


class Report:
    def __init__(self, mongod):
        self.mongod = mongod
        self.doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30,
                                     bottomMargin=18)
        self.elements = []

    def create_header_table(self):
        self.elements.append(header)
        self.elements.append(self.get_header_table())
        self.elements.append(PageBreak())
        self.elements.append(self.get_spelling_table())
        self.elements.append(PageBreak())
        self.elements.append(self.get_broken_links_table())
        self.elements.append(PageBreak())
        self.elements.append(self.get_missing_image_table())
        self.elements.append(PageBreak())
        self.doc.build(self.elements)

    def get_header_data(self):
        crawled_urls_count = self.mongod.get_crawled_urls_count()
        spellings_count = self.mongod.get_spellings_count()
        data = [["Base Url", Properties.home_page],
                ["No of crawled Urls", str(crawled_urls_count)],
                ["No of Spelling Mistakes", str(spellings_count) + "/" + str(Counter.total_spellings)]
                ]
        return data

    def get_header_table(self):
        data = self.get_header_data()
        return ReportTable(data).create_table()

    def get_spelling_table(self):
        data = [["Word", "Count", "Page"]] + \
               self.mongod.get_all_spellings()
        return ReportTable(data).create_table() if len(data) > 0 else None

    def get_broken_links_table(self):
        data = [["Url", "Status Code", "Status"]] + \
               self.mongod.get_all_broken_links()
        return ReportTable(data).create_table() if len(data) > 0 else None

    def get_missing_image_table(self):
        data = [["Url", "Status Code", "Status"]] + \
            self.mongod.get_all_missing_images()
        return ReportTable(data).create_table() if len(data) > 0 else None
