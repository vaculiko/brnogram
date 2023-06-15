from bs4 import BeautifulSoup
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import io


def extract_text_by_page(pdf_path):
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            
            text = fake_file_handle.getvalue()
            yield text
    
            # close open handles
            converter.close()
            fake_file_handle.close()
    
def extract_text(pdf_path):
    tot = {}
    for i, page in enumerate(extract_text_by_page(pdf_path)):
        tot.update({i+1 : page})
    return tot

if __name__ == "__main__":
    path = "scraper\pdf\Music-Lab_Program_4_2022.pdf"
    pdf_miner = extract_text(path)
    print('The pdf has {} pages and the data structure is a {} where the index refers to the page number.'.format( ((list(pdf_miner.keys())[0])) , type(pdf_miner)))
    text = pdf_miner[1]
    # soup = BeautifulSoup(text)
    # print(soup.find(":"))
    print(text.split("  ")[1])