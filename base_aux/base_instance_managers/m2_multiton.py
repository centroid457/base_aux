class Template_Multiton:
    """
    NOTE
    ----
    never use nesting!
    its only for sample template!
    """
    _MULTITON = {}
    param1: int
    param2: str

    def __new__(cls, param1: int, param2: str, *args, **kwargs):
        key = (param1, param2)
        if key not in cls._MULTITON:
            instance = super().__new__(cls)      # kwArgs NOT NEED!!!
            cls._MULTITON[key] = instance
        return cls._MULTITON[key]

    def __init__(self, param1: int, param2: str, p3=None):
        self.param1 = param1
        self.param2 = param2


obj1 = Template_Multiton(1, "X")
obj2 = Template_Multiton(2, "Y")
obj3 = Template_Multiton(1, "X")  # Возвращает существующий экземпляр
obj4 = Template_Multiton(1, "zzz", 2)

print(f"{obj1.param1=}")
print(f"{obj2.param1=}")

print(obj1 is obj3)  # True
