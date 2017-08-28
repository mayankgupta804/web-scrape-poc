from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate

from config.properties import Properties
from report.reportTable import ReportTable


class Report:
    def __init__(self, mongod):
        self.mongod = mongod
        self.canvas = canvas.Canvas("report.pdf")
        self.doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30,
                                     bottomMargin=18)
        self.elements = []

    def create_header_table(self):
        data = self.get_header_data()
        header_table = ReportTable(data).create_table()
        self.elements.append(header_table)
        data = self.mongod.get_all_spellings()
        spellings_table = ReportTable(data).create_table()
        self.elements.append(spellings_table)
        data = self.mongod.get_all_broken_links()
        broken_links_table = ReportTable(data).create_table()
        self.elements.append(broken_links_table)
        data = self.mongod.get_all_missing_images()
        missing_images_table = ReportTable(data).create_table()
        self.elements.append(missing_images_table)
        self.doc.build(self.elements)

    def get_header_data(self):
        crawled_urls_count = self.mongod.get_crawled_urls_count()
        spellings_count = self.mongod.get_spellings_count()
        data = [["Base Url", Properties.home_page],
                ["No of crawled Urls", str(crawled_urls_count)],
                ["No of Spelling Mistakes", str(spellings_count)]]
        return data
