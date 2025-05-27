from pprint import pprint

from langchain_community.document_loaders import PDFPlumberLoader

inputFile = "/Users/victoraynbinder/dev/ub_kobi_mizrachi/functions/src/utils/temp_downloads/regulation_h_2016-9-13-list.pdf";
loader = PDFPlumberLoader(inputFile)
docs = loader.load()
pprint(docs)