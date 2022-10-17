import re
import pytest
import types
import inspect
from conftest import Capturing

try:
    import fitness_tracker
except ModuleNotFoundError:
    assert False, 'Not possible to find `fitness_tracker.py`'
except NameError as exc:
    name = re.findall("name '(\w+)' is not defined", str(exc))[0]
    assert False, f'Class {name} not found.'
except ImportError:
    assert False, 'File `fitness_tracker.py` not found.'


def test_read_package():
    assert hasattr(fitness_tracker, 'read_package'), (
        'Create function to process incoming package - `read_package`'
    )
    assert callable(fitness_tracker.read_package), (
        'Check that `read_package` - is a function.'
    )
    assert isinstance(fitness_tracker.read_package, types.FunctionType), (
        'Check that `read_package` - is a function.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (('SWM', [720, 1, 80, 25, 40]), 'Swimming'),
    (('RUN', [15000, 1, 75]), 'Running'),
    (('WLK', [9000, 1, 75, 180]), 'SportsWalking'),
])
def test_read_package_return(input_data, expected):
    result = fitness_tracker.read_package(*input_data)
    assert result.__class__.__name__ == expected, (
        'Function `read_package` should return workout class.'
    )


def test_SummaryMessage():
    assert inspect.isclass(fitness_tracker.SummaryMessage), (
        'Check that `SummaryMessage` - is a class.'
    )
    summary_message = fitness_tracker.SummaryMessage
    summary_message_signature = inspect.signature(summary_message)
    summary_message_signature_list = list(summary_message_signature.parameters)
    for p in ['workout_type', 'duration', 'distance', 'speed', 'calories']:
        assert p in summary_message_signature_list, (
            'Method `__init__` in `SummaryMessage` class should have '
            f'attribute {p}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    (['Swimming', 1, 75, 1, 80],
        'Workout type: Swimming; '
        'Duration: 1.000 h.; '
        'Distance: 75.000 km; '
        'Average speed: 1.000 km/h; '
        'Calories spent: 80.000.'
     ),
    (['Running', 4, 20, 4, 20],
        'Workout type: Running; '
        'Duration: 4.000 h.; '
        'Distance: 20.000 km; '
        'Average speed: 4.000 km/h; '
        'Calories spent: 20.000.'
     ),
    (['SportsWalking', 12, 6, 12, 6],
        'Workout type: SportsWalking; '
        'Duration: 12.000 h.; '
        'Distance: 6.000 km; '
        'Average speed: 12.000 km/h; '
        'Calories spent: 6.000.'
     ),
])
def test_SummaryMessage_get_message(input_data, expected):
    summary_message = fitness_tracker.SummaryMessage(*input_data)
    assert hasattr(summary_message, 'get_message'), (
        'Create method `get_message` in `SummaryMessage` class.'
    )
    assert callable(summary_message.get_message), (
        'Check that `get_message` is a method in `SummaryMessage` class.'
    )
    result = summary_message.get_message()
    assert isinstance(result, str), (
        'Method `get_message` in `SummaryMessage` class '
        'should return value of type `str`'
    )
    assert result == expected, (
        'Method `get_message` in `SummaryMessage` class should return a string.\n'
        'Similar to: \n'
        'Workout type: Swimming; '
        'Duration: 1.000 h.; '
        'Distance: 75.000 km; '
        'Average speed: 1.000 km/h; '
        'Calories spent: 80.000.'
    )


def test_Workout():
    assert inspect.isclass(fitness_tracker.Workout), (
        'Check that `Workout` is a class.'
    )
    workout = fitness_tracker.Workout
    workout_signature = inspect.signature(workout)
    workout_signature_list = list(workout_signature.parameters)
    for param in ['action', 'duration', 'weight']:
        assert param in workout_signature_list, (
            'Method `__init__` in `Workout` class should have '
            f' attribute {param}.'
        )
    assert 'LEN_STEP' in list(workout.__dict__), (
        'Create `LEN_STEP` attribute in `Workout` class.'
    )
    assert workout.LEN_STEP == 0.65, (
        'Step length in `Workout` class should be equal to 0.65.'
    )
    assert 'M_IN_KM' in list(workout.__dict__), (
        'Create attribute `M_IN_KM` in `Workout` class.'
    )
    assert workout.M_IN_KM == 1000, (
        'Set up correct number of meters (1000) in one kilometer in '
        '`Workout` class.'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.273),
    ([1206, 12, 6], 0.7838999999999999),
])
def test_Workout_get_distance(input_data, expected):
    workout = fitness_tracker.Workout(*input_data)
    assert hasattr(workout, 'get_distance'), (
        'Create method `get_distance` in `Workout` class.'
    )
    result = workout.get_distance()
    assert type(result) == float, (
        'Method `get_distance` in `Trainig` class should return '
        'value of type `float`'
    )
    assert result == expected, (
        'Check distance formula in `Workout` class.'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 5.85),
    ([420, 4, 20], 0.06825),
    ([1206, 12, 6], 0.065325),
])
def test_Workout_get_mean_speed(input_data, expected):
    workout = fitness_tracker.Workout(*input_data)
    assert hasattr(workout, 'get_mean_speed'), (
        'Create method `get_mean_speed` in `Workout` class.'
    )
    result = workout.get_mean_speed()
    assert type(result) == float, (
        'Method `get_mean_speed` in `Workout` class should return '
        'value of type `float`'
    )
    assert result == expected, (
        'Check average speed formula in Traingin class.'
    )


@pytest.mark.parametrize('input_data', [
    ([9000, 1, 75]),
    ([420, 4, 20]),
    ([1206, 12, 6]),
])
def test_Workout_get_spent_calories(input_data):
    workout = fitness_tracker.Workout(*input_data)
    assert hasattr(workout, 'get_spent_calories'), (
        'Create method `get_spent_calories` in `Workout` class.'
    )
    assert callable(workout.get_spent_calories), (
        'Check that `get_spent_calories` is a function.'
    )


def test_Workout_show_workout_summary(monkeypatch):
    workout = fitness_tracker.Workout(*[720, 1, 80])
    assert hasattr(workout, 'show_workout_summary'), (
        'Create method `show_workout_summary` in `Workout` class.'
    )

    def mock_get_spent_calories():
        return 100
    monkeypatch.setattr(
        workout,
        'get_spent_calories',
        mock_get_spent_calories
    )
    result = workout.show_workout_summary()
    assert result.__class__.__name__ == 'SummaryMessage', (
        'Method `show_workout_summary` in `Workout` class should return '
        'an instance of `SummaryMessage` class.'
    )


def test_Swimming():
    assert hasattr(fitness_tracker, 'Swimming'), 'Create `Swimming` class.'
    assert inspect.isclass(fitness_tracker.Swimming), (
        'Check that `Swimming` is a class.'
    )
    assert issubclass(fitness_tracker.Swimming, fitness_tracker.Workout), (
        '`Swimming` class should a child of `Workout` class.'
    )
    swimming = fitness_tracker.Swimming
    swimming_signature = inspect.signature(swimming)
    swimming_signature_list = list(swimming_signature.parameters)
    for param in ['action', 'duration', 'weight', 'length_pool', 'count_pool']:
        assert param in swimming_signature_list, (
            'Method `__init__` in `Swimming` class should have '
            f' attribute {param}.'
        )
    assert 'LEN_STEP' in list(swimming.__dict__), (
        'Create attribute `LEN_STEP` in `Swimming` class.'
    )
    assert swimming.LEN_STEP == 1.38, (
        'Stroke length in `Swimming` class should be equal to 1.38'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 1.0),
    ([420, 4, 20, 42, 4], 0.042),
    ([1206, 12, 6, 12, 6], 0.005999999999999999),
])
def test_Swimming_get_mean(input_data, expected):
    swimming = fitness_tracker.Swimming(*input_data)
    result = swimming.get_mean_speed()
    assert result == expected, (
        'Override method `get_mean_speed` in `Swimming` class. '
        'Check average speed formula in `Swimming` class.'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([720, 1, 80, 25, 40], 336.0),
    ([420, 4, 20, 42, 4], 45.68000000000001),
    ([1206, 12, 6, 12, 6], 13.272000000000002),
])
def test_Swimming_get_spent_calories(input_data, expected):
    swimming = fitness_tracker.Swimming(*input_data)
    result = swimming.get_spent_calories()
    assert type(result) == float, (
        'Override method `get_spent_calories` in `Swimming` class.'
    )
    assert result == expected, (
        'Check spent calories formula in `Swimming` class.'
    )


def test_SportsWalking():
    assert hasattr(fitness_tracker, 'SportsWalking'), (
        'Create `SportsWalking` class.'
    )
    assert inspect.isclass(fitness_tracker.SportsWalking), (
        'Check that `SportsWalking` is a class.'
    )
    assert issubclass(fitness_tracker.SportsWalking, fitness_tracker.Workout), (
        '`SportsWalking` class should be a child of `Workout` class.'
    )
    sports_walking = fitness_tracker.SportsWalking
    sports_walking_signature = inspect.signature(sports_walking)
    sports_walking_signature_list = list(sports_walking_signature.parameters)
    for param in ['action', 'duration', 'weight', 'height']:
        assert param in sports_walking_signature_list, (
            'Method `__init__` in `SportsWalking` class should have '
            f'attribute {param}.'
        )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75, 180], 157.50000000000003),
    ([420, 4, 20, 42], 168.00000000000003),
    ([1206, 12, 6, 12], 151.20000000000002),
])
def test_SportsWalking_get_spent_calories(input_data, expected):
    sports_walking = fitness_tracker.SportsWalking(*input_data)
    result = sports_walking.get_spent_calories()
    assert type(result) == float, (
        'Override `get_spent_calories` method in `SportsWalking` class.'
    )
    assert result == expected, (
        'Check spent calories formula in `SportsWalking` class.'
    )


def test_Running():
    assert hasattr(fitness_tracker, 'Running'), 'Create `Running` class.'
    assert inspect.isclass(fitness_tracker.Running), (
        'Check that `Running` is a class.'
    )
    assert issubclass(fitness_tracker.Running, fitness_tracker.Workout), (
        '`Running` class should be a child of `Workout` class.'
    )


@pytest.mark.parametrize('input_data, expected', [
    ([9000, 1, 75], 383.85),
    ([420, 4, 20], -90.1032),
    ([1206, 12, 6], -81.32032799999999),
])
def test_Running_get_spent_calories(input_data, expected):
    running = fitness_tracker.Running(*input_data)
    assert hasattr(running, 'get_spent_calories'), (
        'Create `get_spent_calories` method in `Running` class.'
    )
    result = running.get_spent_calories()
    assert type(result) == float, (
        'Override `get_spent_calories` method in `Running` class.'
    )
    assert result == expected, (
        'Check spent calories formula in `Running` class.'
    )


def test_main():
    assert hasattr(fitness_tracker, 'main'), (
        'Create `main` program function.'
    )
    assert callable(fitness_tracker.main), 'Check that `main` is a function.'
    assert isinstance(fitness_tracker.main, types.FunctionType), (
        'Check that `main` is a function.'
    )


@pytest.mark.parametrize('input_data, expected', [
    (['SWM', [720, 1, 80, 25, 40]], [
        'Workout type: Swimming; '
        'Duration: 1.000 h.; '
        'Distance: 0.994 km; '
        'Average speed: 1.000 km/h; '
        'Calories spent: 336.000.'
    ]),
    (['RUN', [1206, 12, 6]], [
        'Workout type: Running; '
        'Duration: 12.000 h.; '
        'Distance: 0.784 km; '
        'Average speed: 0.065 km/h; '
        'Calories spent: -81.320.'
    ]),
    (['WLK', [9000, 1, 75, 180]], [
        'Workout type: SportsWalking; '
        'Duration: 1.000 h.; '
        'Distance: 5.850 km; '
        'Average speed: 5.850 km/h; '
        'Calories spent: 157.500.'
    ])
])
def test_main_output(input_data, expected):
    with Capturing() as get_message_output:
        workout = fitness_tracker.read_package(*input_data)
        fitness_tracker.main(workout)
    assert get_message_output == expected, (
        'Method `main` should print result into console.\n'
    )
