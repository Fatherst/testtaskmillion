class PhoneMask:
    def __init__(self, phone, mask_number=3, mask_symbol='x'):
        if not isinstance(phone, str):
            raise TypeError("Номер телефона должен быть строкой")
        if not isinstance(mask_symbol, str):
            raise TypeError("Заменяющий символ должен быть строкой")
        if not isinstance(mask_number, int):
            raise TypeError("Число экранирования должен быть целым числом")
        if len(mask_symbol) != 1:
            raise ValueError("Заменяющий символ должен быть только один")
        self.phone = phone
        self.mask_number = mask_number
        self.mask_symbol = mask_symbol

    def mask(self):
        phone_wo_spaces = self.phone.replace(' ', '')
        masked_part = phone_wo_spaces[len(phone_wo_spaces):-(self.mask_number + 1):-1]
        masked_phone = phone_wo_spaces[::-1].replace(masked_part, self.mask_symbol * len(masked_part), 1)[::-1]
        formatted = masked_phone[:2] + " " + masked_phone[2:]
        i = 6
        while i < len(formatted):
            formatted = formatted[:i] + " " + formatted[i:]
            i += 4
        return formatted

print(PhoneMask('+7 111 222 333',4,'z').mask())
