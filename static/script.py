class Make:
    def __init__(self, make: str):
        self.make: str = make

    def display_make(self) -> None:
        print(self.make)
class Year:
    def __init__(self, year: int):
        self.year = year

    def display_year(self) -> None:
        print(self.year)
class Model(Make, Year):
    def __init__(self, make: str, year: int, model: str):
        Make.__init__(self, make)
        Year.__init__(self, year)
        self.model = model

    def display_model(self) -> None:
        print(self.model)

    def display_all(self) -> None:
        print(self.year, self.make, self.model)

car_1 = Model('Porsche', 1973, '911 Carrera RS')

car_1.display_all()


