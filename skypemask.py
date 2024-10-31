import re

class PhoneMask:
    def __init__(self, skype):
        if not isinstance(skype, str):
            raise TypeError("Скайп должен быть строкой")
        self.skype = skype
    def mask(self):
        new_text = re.sub(r'skype:[^"?\s<>]*', 'skype:xxx', self.skype)
        return new_text

print(PhoneMask("<a href=\"skype:alex.max?call\">skype</a>").mask())
print(PhoneMask("skype:alex.max").mask())