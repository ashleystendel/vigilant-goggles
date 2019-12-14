class Article:
    def __init__(self, args):
        self.abstract = args['abstract']
        self.web_url = args['web_url']
        self.snippet = args['snippet']
        self.lead_paragraph = args['lead_paragraph']
        self.print_section = args['print_section']
        self.print_page = args['print_page']
        self.source = args['source']
        self.headline.main = args['headline']['main']
        self.pub_date = args['pub_date']
        self.document_type = args['document_type']
        self.section_name = args['section_name']
        self.external_id = args['_id']

    def get_attributes(self):
        return self.__dict__
