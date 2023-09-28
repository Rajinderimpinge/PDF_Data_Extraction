"""
Extract Data from PDF file
"""
from PyPDF2 import PdfReader
import os, json
import pprint


class PDFExtraction:
    def __init__(
        self,
    ):
        self.page_content = []
        self.font_cls = {
            "/TimesNewRomanPSMT": 0,
            "/TimesNewRomanPS-BoldMT": 0,
            "/TimesNewRomanPS-ItalicMT": 0,
        }
        self.pg_num = 0
        self.header_level = 0
        self.section = []
        self.section_count = 0
        self.para = ""
        self.error = False

    def visitor_body(self, text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 39:
            if len(text) > 0:
                pre_para = False
                if (
                    fontDict["/BaseFont"] == "/TimesNewRomanPS-BoldMT"
                    and len(text) > 0
                    and "\n" not in text
                ):
                    temp = {
                        "para_num": self.section_count,
                        "section_name": str(text),
                        "para": "",
                    }
                    self.section.append(temp)
                    # self.page_content[self.pg_num-1][self.header_level]['header']+=text
                if fontDict["/BaseFont"] in [
                    "/TimesNewRomanPSMT",
                    "/TimesNewRomanPS-ItalicMT",
                ]:
                    if len(self.section) == 0:
                        pre_para = True
                    elif self.section_count != len(self.section):
                        self.section_count = len(self.section)
                        self.para = ""

                    self.para += str(text)
                    if pre_para:
                        connt = 0
                        while True:
                            try:
                                self.page_content[-connt]["pageObj"][-1][
                                    "para"
                                ] += self.para
                                break
                            except:
                                connt += 1
                    else:
                        self.section[self.section_count - 1]["para"] = self.para

                    # print("Body", text)
                    # self.page_content[self.pg_num-1][self.header_level+1]['body']+=text
                print(
                    {
                        "text": repr(text),
                        "cm": cm,
                        "tm": tm,
                        "fontDict": fontDict,
                        "fontSize": fontSize,
                    },
                    file=open("expla3.json", "a"),
                )

    def extract_pdf(self):
        file_name = "abilify-epar-product-information_en.pdf"
        reader = PdfReader(file_name, strict=True)
        for page in reader.pages:
            try:
                self.pg_num += 1
                if self.pg_num == 1:
                    continue
                page_instance = {"page_number": self.pg_num, "pageObj": []}
                page.extract_text(visitor_text=self.visitor_body)
                # print(self.page_content)
                page_instance["pageObj"] = self.section
                self.page_content.append(page_instance)
            except Exception as e:
                print(str(e))
                print(self.pg_num)
                self.error = True
            self.section = []
            self.section_count = 0

        for i in self.page_content:
            for j in i["pageObj"]:
                j["para"] = self.para_cleaning(j["para"])
        with open("output.json", "w") as f:
            f.write(json.dumps(self.page_content, indent=4))

    def para_cleaning(self, data):
        data = data.rsplit("\n \n")
        temp = dict()
        for i, dt in enumerate(data):
            dt = dt.strip()
            dt = dt.strip(" ")
            if len(dt) > 0:
                if len(dt) < 85 and dt != " ":
                    if len(temp) == 0:
                        temp = {dt: {}}
                    else:
                        ky = list(temp.keys())[-1]
                        temp[ky] = {dt: {}}
                else:
                    keys = list(temp.keys())
                    if len(keys) > 0:
                        temp[keys[-1]] = dt
        return temp if len(temp) > 0 else "".join(data)


if __name__ == "__main__":
    pdf_obj = PDFExtraction()
    pdf_obj.extract_pdf()
