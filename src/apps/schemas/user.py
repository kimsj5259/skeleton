from enum import Enum


class GenderEnum(str, Enum):
    female = "female"
    male = "male"
    other = "other"