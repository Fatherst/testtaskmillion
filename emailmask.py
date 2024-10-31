
class EmailMask:
    def __init__(self, email, mask_symbol ='x'):
        if not isinstance(mask_symbol, str):
            raise TypeError("Заменяющий символ должен быть строкой")
        if len(mask_symbol) != 1:
            raise ValueError("Заменяющий символ должен быть только один")
        self.email = email
        self.mask_symbol = mask_symbol

    def mask(self):
        try:
            local_part, domain = self.email.split('@')
            masked_local = self.mask_symbol * (len(local_part))
            return f"{masked_local}@{domain}"
        except ValueError:
            raise ValueError("Некорректный формат email")

masker = EmailMask('aaasdszxza@sdsd.ru')
print(masker.mask())