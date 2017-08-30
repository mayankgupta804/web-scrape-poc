from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import TableStyle, Paragraph
from reportlab.platypus.tables import Table


class ReportTable:
    def __init__(self, data):
        self.data = data

    def create_table(self):
        s = ReportTable.get_style_sheet()
        data2 = [[Paragraph(cell, s) for cell in row] for row in self.data]
        t = Table(data2, colWidths=[250, 250], splitByRow=1)
        t.setStyle(ReportTable.get_default_table_style())
        return t

    @staticmethod
    def get_default_table_style():
        return TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                           ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                           ('VALIGN', (0, 0), (0, -1), 'TOP'),
                           ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                           ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ])

    @staticmethod
    def get_style_sheet():
        s = getSampleStyleSheet()
        s = s["BodyText"]
        # s.wordWrap = 'CJK'
        return s
