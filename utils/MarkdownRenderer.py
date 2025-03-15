import mistune

class MarkdownRenderer(mistune.HTMLRenderer):
    def __init__(self, domain:str, base:str, escape=True, allow_harmful_protocols=None):
        super().__init__(escape, allow_harmful_protocols)
        self.__domain = domain
        self.__base = base

    def image(self, text, url, title=None):
        if url.startswith("../.."):
            wrapUrl = f"{self.__domain}{self.__base}/{url[len('../..'):]}"
            return super().image(text, wrapUrl, title)

        return super().image(text, url, title)