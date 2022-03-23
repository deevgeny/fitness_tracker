class InfoMessage:
    """Training info message."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        # Declare instance attributes
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Return training info message using instance attributes."""
        message = f'Тип тренировки: {self.training_type}; '
        message += f'Длительность: {self.duration:.3f} ч.; '
        message += f'Дистанция: {self.distance:.3f} км; '
        message += f'Ср. скорость: {self.speed:.3f} км/ч; '
        message += f'Потрачено ккал: {self.calories:.3f}.'
        return message


class Training:
    """Training (parent class)."""
    # Declare class attributes
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        # Declare instance attributes
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in kilometers using below formula:
        mean_speed = action * LEN_STEP / M_IN_KM.
        """
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get mean speed using below formula:
        mean_speed = distance / duration.
        """
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Get spent calories.
        This method will be overriden by child class.
        """
        pass

    def show_training_info(self) -> InfoMessage:
        """Return InfoMessage class instance."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: Running (child class)."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        # Inherit from parent class
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Override parent class method.
        Get spent calories using below formulas:
        expr_1 = (18 * mean_speed - 20)
        calories = expr_1 * weight / M_IN_KM * duration_in_minutes.
        """
        # Prepare formula terms
        coeff_1: int = 18
        coeff_2: int = 20
        mean_speed = self.get_mean_speed()
        duration_in_minutes = self.duration * 60

        # Calculate calories
        expr_1 = (coeff_1 * mean_speed - coeff_2)
        calories = expr_1 * self.weight / self.M_IN_KM * duration_in_minutes
        return calories


class SportsWalking(Training):
    """Training: Sports walking (child class)."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        # Inherit from parent class
        super().__init__(action, duration, weight)
        # Declare extra attribute for child class
        self.height = height

    def get_spent_calories(self) -> float:
        """Override parent class method.
        Get spent calories using below formulas:
        expr_1 = (mean_speed ** 2 // height) * 0.029 * weight
        calories = (0.035 * weight + expr_1) * duration_in_minutes.
        """
        # Prepare formula terms
        coeff_1: float = 0.029
        coeff_2: float = 0.035
        mean_speed = self.get_mean_speed()
        power: int = 2
        duration_in_minutes = self.duration * 60

        # Calculate calories
        expr_1 = (mean_speed ** power // self.height) * coeff_1 * self.weight
        calories = (coeff_2 * self.weight + expr_1) * duration_in_minutes
        return calories


class Swimming(Training):
    """Training: Swimming (child class)."""
    # Override parent class attribute
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        # Inherit from parent class
        super().__init__(action, duration, weight)
        # Declare extra attributes for child class
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Override parent class method.
        Get mean speed using below formulas:
        expr_1 = lenght_pool * count_pool
        mean_speed = expr_1 / M_IN_KM / duration.
        """
        expr_1 = self.length_pool * self.count_pool
        mean_speed = expr_1 / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Override parent class method.
        Get spent calories using below formula:
        calories = (mean_speed + 1.1) * 2 * weight.
        """
        # Prepare formula terms
        coeff_1: float = 1.1
        coeff_2: int = 2
        mean_speed = self.get_mean_speed()

        # Calculate calories
        calories = (mean_speed + coeff_1) * coeff_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Read sensors data and return training class instance."""
    class_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return class_dict[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
