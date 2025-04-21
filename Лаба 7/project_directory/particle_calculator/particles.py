from abc import ABC, abstractmethod
import math


class Particle(ABC):
    """Абстрактный базовый класс для частиц."""

    def __init__(self, name, mass, charge):
        self._name = name
        self._mass = mass
        self._charge = charge

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Имя частицы должно быть строкой")
        self._name = value

    @abstractmethod
    def calculate_specific_charge(self):
        pass

    @abstractmethod
    def calculate_compton_wavelength(self):
        pass

    def __str__(self):
        return f"{self._name} (масса: {self._mass} кг, заряд: {self._charge} Кл)"

    def __eq__(self, other):
        if not isinstance(other, Particle):
            return False
        return math.isclose(self._mass, other.mass) and math.isclose(self._charge, other.charge)


class Electron(Particle):
    def __init__(self):
        super().__init__("Электрон", 9.10938356e-31, -1.602176634e-19)

    def calculate_specific_charge(self):
        return self._charge / self._mass

    def calculate_compton_wavelength(self):
        return 6.62607015e-34 / (self._mass * 299792458)

    def __repr__(self):
        return f"Electron(mass={self._mass}, charge={self._charge})"


class Proton(Particle):
    def __init__(self):
        super().__init__("Протон", 1.67262192369e-27, 1.602176634e-19)

    def calculate_specific_charge(self):
        return self._charge / self._mass

    def calculate_compton_wavelength(self):
        return 6.62607015e-34 / (self._mass * 299792458)


class Neutron(Particle):
    def __init__(self):
        super().__init__("Нейтрон", 1.674927471e-27, 0)

    def calculate_specific_charge(self):
        return 0

    def calculate_compton_wavelength(self):
        return 6.62607015e-34 / (self._mass * 299792458)