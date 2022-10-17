# Fitness tracker module

Fitness tracker module processes sensor unit data generated during workout 
activities. The module supports three workout types: running, sports 
walking and swimming. As a result, it provides workout summary message with 
the following information: workout type, workout duration, covered distance, 
average speed and spent calories. 


## Technology stack
- Python 3.7


## Implementation
Functionality of the module is defined by below classes:
- `SummaryMessage()` - generates workout summary message objects.
- `Workout()` - base workout class.
- `Running()` - child class for running.
- `SportsWalking()` - child class for sports walking.
- `Swimming()` - child class for swimming.


## Fitness tracker sensor unit
Fitness tracker module is supposed to have a sensor unit which collects data 
during a workout and pass it to the module. Basic information such as height, 
weight and swimming pool length should be provided by user. To demonstrate the 
module's functionality, sensor unit data is artificially generated:

```python
[('SWM', [720, 1, 80, 25, 40]),
 ('RUN', [15000, 1, 75]),
 ('WLK', [9000, 1, 75, 180])]
```

SWM, RUN, WLK stands for workout types: swimming, running and sports walking.
First three values for all the tree workout types are: activity counter 
(e.g steps, strokes) , workout duration in hours and user weight in kg. 
There are two extra values for swimming: pool length and number of times the user 
overpassed the pool. And one extra value for sports walking: user height.


## How to install and run the module
```
# Clone repository
git clone https://github.com/evgeny81d/fitness_tracker

# Go to the project directory
cd fitness_tracker

# Create Python 3.7 virtual environment
python3.7 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt --upgrade pip

# Run
python3 fitness_tracker.py

# Program output
Workout type: Swimming; Duration: 1.000 h.; Distance: 0.994 km; Average speed: 1.000 km/h; Calories spent: 336.000.
Workout type: Running; Duration: 1.000 h.; Distance: 9.750 km; Average speed: 9.750 km/h; Calories spent: 699.750.
Workout type: SportsWalking; Duration: 1.000 h.; Distance: 5.850 km; Average speed: 5.850 km/h; Calories spent: 157.500.
```
