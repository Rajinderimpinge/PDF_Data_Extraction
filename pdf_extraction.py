"""
Extract Data from PDF file
"""
from PyPDF2 import PdfReader
import os
import pprint


class PDFExtraction:
    def __init__(
        self,
    ):
        self.page_content = []
        # self.parts = []
        self.title = ""
        self.meta = ""
        self.section = []
        self.para = ""
        self.body = []
        self.section_count = 0
        # self.page = []

    def visitor_body(self, text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 24 and y < 700:
            if fontSize >= 29 and len(self.title) < 2:
                self.title = str(text)

            if text != "Overview" and fontSize == 16.0 and cm[5] >= 654.0:
                self.meta += text

            if (
                fontSize >= 21
                and fontSize <= 29
                and text != ""
                and text != " "
                and text != "\n"
            ):
                temp = {
                    "para_num": self.section_count,
                    "section_name": str(text),
                    "para": "",
                }
                self.section.append(temp)

            if (
                fontSize == 16.0
                and text != ""
                and text != " "
                and text != "\n"
                and cm[5] >= 315.0
                and cm[5] <= 503.0
            ):
                if self.section_count != len(self.section):
                    self.section_count = len(self.section)
                    self.para = ""
                self.para += str(text)
                self.section[self.section_count - 1]["para"] = self.para

            # self.page.append(temp_dt)

            # print({"text":repr(text), "cm":cm, "tm":tm, "fontDict":fontDict, "fontSize":fontSize})
            # self.parts.append(text)

    def extract_pdf(self):
        # pdf_obj = open("Advanced Data Analytics Landscape_ Quantum Computing.pdf", "rb")
        file_name = "abilify-epar-product-information_en.pdf"
        reader = PdfReader(file_name)
        number_of_pages = len(reader.pages)
        # print(type(number_of_pages))

        for pg_num in range(0, number_of_pages - 1):
            page_instance = {"page_number": pg_num + 1, "title": "", "section": []}
            try:
                page = reader.pages[pg_num]
                page.extract_text(visitor_text=self.visitor_body)
                page_instance["title"] = self.title
                if len(self.meta) > 2:
                    page_instance["meta"] = self.meta
                page_instance["section"] = self.section
                self.page_content.append(page_instance)
            except:
                print("pg_num", pg_num)

            self.title, self.meta = "", ""
            self.section, self.body = [], []
            self.section_count = 0

        print(self.page_content, file=open("output.json", "w"))

        # get image data
        """
        print(page.images)
        count = 0
        for image_file_object in page.images:
            with open(str(count) + image_file_object.name, "wb") as fp:
                fp.write(image_file_object.data)
                count += 1
        """

        # print(text.split("\n"))
        # print(reader.get_form_text_fields())


if __name__ == "__main__":
    pdf_obj = PDFExtraction()
    pdf_obj.extract_pdf()
