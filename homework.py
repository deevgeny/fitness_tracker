from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Training info message."""

    INFO_STRING: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Return training info message using instance attributes."""
        return self.INFO_STRING.format(**asdict(self))


@dataclass
class Training:
    """Training (parent class)."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    MINUTES_IN_HOUR: ClassVar[float] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Get distance in kilometers.

        Calculate distance using below formula:
        mean_speed = action * LEN_STEP / M_IN_KM.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get mean speed.

        Calcualte mean speed using below formula:
        mean_speed = distance / duration.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get spent calories.

        This method will be overriden by child class.
        """
        raise NotImplementedError(
            f'get_spent_calories() not defined in {type(self).__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Return InfoMessage class instance."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Training: Running (child class)."""

    COEFF_CALORIE_1: ClassVar[float] = 18
    COEFF_CALORIE_2: ClassVar[float] = 20
    WORKOUT_TYPE: ClassVar[str] = 'RUN'

    def get_spent_calories(self) -> float:
        """Get spent calories.

        Override parent class method.
        Get spent calories using below formulas:
        expr_1 = (18 * mean_speed - 20)
        calories = expr_1 * weight / M_IN_KM * duration_in_minutes.
        """
        # Prepare formula terms
        mean_speed = self.get_mean_speed()
        duration_in_minutes = self.duration * self.MINUTES_IN_HOUR

        # Calculate calories
        expr_1 = (self.COEFF_CALORIE_1 * mean_speed - self.COEFF_CALORIE_2)
        calories = expr_1 * self.weight / self.M_IN_KM * duration_in_minutes
        return calories


@dataclass
class SportsWalking(Training):
    """Training: Sports walking (child class)."""

    COEFF_CALORIE_1: ClassVar[float] = 0.029
    COEFF_CALORIE_2: ClassVar[float] = 0.035
    PWR: ClassVar[int] = 2
    WORKOUT_TYPE: ClassVar[str] = 'WLK'

    height: int

    def get_spent_calories(self) -> float:
        """Get spent calories.

        Override parent class method.
        Calcualte spent calories using below formulas:
        expr_1 = (mean_speed ** 2 // height) * 0.029 * weight
        expr_2 = expr_1 * 0.029 * weight
        expr_3 = (0.035 * weight + expr_2)
        calories = expr_3 * duration_in_minutes.
        """
        # Prepare formula terms
        mean_speed = self.get_mean_speed()
        duration_in_minutes = self.duration * self.MINUTES_IN_HOUR

        # Calculate calories
        expr_1 = (mean_speed ** self.PWR // self.height)
        expr_2 = expr_1 * self.COEFF_CALORIE_1 * self.weight
        expr_3 = (self.COEFF_CALORIE_2 * self.weight + expr_2)
        calories = expr_3 * duration_in_minutes
        return calories


@dataclass
class Swimming(Training):
    """Training: Swimming (child class)."""

    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_1: ClassVar[float] = 1.1
    COEFF_CALORIE_2: ClassVar[float] = 2
    WORKOUT_TYPE: ClassVar[str] = 'SWM'

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Get mean speed.

        Override parent class method.
        Get mean speed using below formulas:
        expr_1 = lenght_pool * count_pool
        mean_speed = expr_1 / M_IN_KM / duration.
        """
        expr_1 = self.length_pool * self.count_pool
        mean_speed = expr_1 / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Get spent calories.

        Override parent class method.
        Calculate spent calories using below formula:
        expr_1 = (mean_speed + 1.1) * 2
        calories = expr_1 * weight.
        """
        # Prepare formula terms
        mean_speed = self.get_mean_speed()

        # Calculate calories and return result
        expr_1 = (mean_speed + self.COEFF_CALORIE_1) * self.COEFF_CALORIE_2
        calories = expr_1 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Read sensors data and return training class instance."""
    # Create dictionary with available training types
    training_types: Dict[str, Type[Training]] = {
      c.WORKOUT_TYPE: c for c in Training.__subclasses__()
    }

    # Evaluate if workout_type argument exists in training_types
    if workout_type not in training_types:
        raise ValueError(
            (f'Invalid workout_type argument value {repr(workout_type)}. '
             'Valid values: '
             f'{", ".join([repr(i) for i in training_types])}.')
        )
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Main function.

    Prints training info message.
    """
    # Get InfoMessage class instance from Training class instance
    info = training.show_training_info()
    # Print info message
    print(info.get_message())


if __name__ == '__main__':
    # Create sensor training data package
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    # Run fitness tracker for different training data packages
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
