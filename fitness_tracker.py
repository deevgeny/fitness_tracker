from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class SummaryMessage:
    """Workout summary message."""

    INFO_STRING: ClassVar[str] = (
        'Workout type: {workout_type}; '
        'Duration: {duration:.3f} h.; '
        'Distance: {distance:.3f} km; '
        'Average speed: {speed:.3f} km/h; '
        'Calories spent: {calories:.3f}.'
    )

    workout_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Return workout summary message using instance attributes."""
        return self.INFO_STRING.format(**asdict(self))


@dataclass
class Workout:
    """Workout base class."""

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

    def show_workout_summary(self) -> SummaryMessage:
        """Return InfoMessage class instance."""
        return SummaryMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Workout):
    """Workout class for running."""

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
class SportsWalking(Workout):
    """Workout class for sports walking."""

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
class Swimming(Workout):
    """Workout class for swimming."""

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


def read_package(workout_type: str, data: list) -> Workout:
    """Read sensors data and return workout class instance."""
    # Create dictionary with available workout types
    workout_types: Dict[str, Type[Workout]] = {
        c.WORKOUT_TYPE: c for c in Workout.__subclasses__()
    }

    # Evaluate if workout_type argument exists in workout_types
    if workout_type not in workout_types:
        raise ValueError(
            (f'Invalid workout_type argument value {repr(workout_type)}. '
             'Valid values: '
             f'{", ".join([repr(i) for i in workout_types])}.')
        )
    return workout_types[workout_type](*data)


def main(workout: Workout) -> None:
    """Main function.

    Prints workout summary message.
    """
    # Get InfoMessage class instance from Workout class instance
    summary = workout.show_workout_summary()
    # Print summary message
    print(summary.get_message())


if __name__ == '__main__':
    # Create sensor workout data package
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    # Run fitness tracker for different workout data packages
    for workout_type, data in packages:
        workout = read_package(workout_type, data)
        main(workout)
