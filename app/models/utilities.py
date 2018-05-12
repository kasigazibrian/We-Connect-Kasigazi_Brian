"""Utilities python file"""
import re


class Utilities(object):

    @staticmethod
    def is_valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    @staticmethod
    def is_valid_phone_number(phone_number):
        if re.match(r"^\d{12}$", phone_number):
            return True
        return False

    @staticmethod
    def is_valid_gender(gender):
        if re.match(r"(^(?:m|M|male|Male|f|F|female|Female)$)", gender):
            return True
        return False
