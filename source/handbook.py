# The guide's handbook, the answer keys and the shopping list.

SESSIONS = [
    ("Meet the parts", [("intro", "Introduction"), ("breadboard", "Topic: Breadboard"), ("resistor", "Topic: Resistor")], "Understand the water model and the safety rules.", "Read the Introduction yourself first. Have a resistor, an LED and a breadboard on hand, if you have them.", ["What would happen to the water if a pipe burst?", "Why do we unplug before moving a wire?"], "Skipping the safety rules because nothing looks dangerous yet.", "The student can explain voltage, current and resistance using the water model."),
    ("First circuit", [("led", "Topic: LED"), ("ex-1", "Lab Example 1")], "Light an LED, first in the simulator and then for real.", "Open Example 1. If you have parts, lay them out ready.", ["What does the resistor do here?", "What happens if the LED is backwards?"], "Both LED legs in one joined group of holes.", "The LED lights in the simulator, and on a real board if you have one."),
    ("First code", [("code-1", "Coding Lesson 1"), ("code-2", "Coding Lesson 2"), ("ex-2", "Lab Example 2")], "Write a first program that blinks an LED.", "Try the Blocks tab and Lesson 1 yourself once.", ["What's the difference between setup() and loop()?", "What happens if you change the delay?"], "Forgetting pinMode, or a missing semicolon.", "The student changes the timing by themselves, and can explain the result."),
    ("Patterns and brightness", [("ex-4", "Lab Example 4"), ("ex-5", "Lab Example 5"), ("ex-6", "Lab Example 6"), ("ex-7", "Lab Example 7"), ("code-3", "Coding Lesson 3")], "Control several outputs, and use variables.", "Decide whether to use Blocks or Code. Either is fine at this stage.", ["Why is a bigger resistor dimmer?", "What is the variable remembering?"], "Copying code without changing it. Ask for one change each time.", "The student makes a pattern of their own."),
    ("Inputs", [("button", "Topic: Push Button"), ("pot", "Topic: Potentiometer"), ("ex-8", "Lab Example 8"), ("ex-10", "Lab Example 10"), ("code-9", "Coding Lesson 9")], "Read a button and a dial.", "Read the two Unit II topics first.", ["Why does a pressed button read LOW?", "What number does the dial give halfway?"], "A button turned 90 degrees, or a floating input.", "The student makes a dial control something."),
    ("Decisions and loops", [("code-5", "Coding Lesson 5"), ("code-6", "Coding Lesson 6"), ("code-7", "Coding Lesson 7"), ("ex-12", "Lab Example 12")], "Use if, loops and functions.", "Work through Lesson 5 once before the session.", ["When would you use a for loop instead of a while loop?", "How does a function save work?"], "Using = where == is needed.", "The student writes an if and a loop without copying."),
    ("Sound, capacitors, transistors", [("buzzer", "Topic: Buzzer"), ("capacitor", "Topic: Capacitor"), ("transistor", "Topic: Transistor"), ("ex-13", "Lab Example 13"), ("ex-14", "Lab Example 14"), ("ex-15", "Lab Example 15")], "See how small signals control bigger things.", "Check the leg order of your real transistors first.", ["Why can't the pin run this directly?", "Where is the capacitor's energy coming from?"], "Reversed electrolytic capacitors. Always check these yourself.", "The student can explain what the transistor is doing."),
    ("Motors and servos", [("dc-motor", "Topic: DC Motor"), ("diode", "Topic: Diode"), ("servo", "Topic: Servo Motor"), ("power", "Topic: Batteries and Power"), ("ex-16", "Lab Example 16"), ("ex-19", "Lab Example 19")], "Run motors safely from their own battery.", "Check all battery and diode directions yourself before power goes on.", ["Why does the motor need its own battery?", "What is the diode protecting?"], "A missing shared ground, or a reversed diode.", "The motor runs safely, and the student can explain the shared ground."),
    ("Sensors", [("sensors", "Sensors section"), ("ultrasonic", "Topic: Ultrasonic Sensor"), ("ex-22", "Lab Example 22"), ("ex-25", "Lab Example 25")], "Measure the world, and make decisions from it.", "Choose two or three sensors that interest the student. There's no need to do them all.", ["Why does the formula divide by 2?", "What could fool this sensor?"], "Trusting a reading without testing it against a ruler.", "The student tests a reading, and finds one thing that fools the sensor."),
    ("Build the robot", [("robots", "Robot Exercises"), ("robot-1", "Exercises 1 to 5"), ("driver", "Topic: Motor Driver")], "Build and wire the robot, then test each motor.", "Get the kit and tools ready. Allow extra time for this session.", ["Why test with the wheels off the ground?", "Which wire would you swap if a wheel runs backwards?"], "Reversed battery wires. Check before adding batteries.", "Both wheels spin forward, on a box."),
    ("Make it move", [("robot-6", "Exercises 6 to 12"), ("rsim-11", "Robot Simulator"), ("code-7", "Coding Lesson 7")], "Drive, turn and follow a planned path.", "Clear some floor space. Have tape ready.", ["Why doesn't it drive perfectly straight?", "What changed when the batteries got weaker?"], "Testing on a table. Move to the floor.", "The robot drives a recognisable square."),
    ("Sense and react", [("robot-13", "Exercises 13 to 21"), ("code-10", "Coding Lesson 10"), ("faults", "Fix It Guide")], "Add a start button and lights, then avoid obstacles.", "Set up boxes for a small course.", ["What can't the sensor see?", "What should it do if both sides are blocked?"], "Fixing faults for the student. Let them use the Fix It Guide.", "The robot avoids boxes for a minute."),
    ("Follow a line", [("robot-22", "Exercises 22 to 24"), ("rsim-23", "Robot Simulator")], "Use line sensors to follow a track.", "Lay a track of black tape. Avoid sharp corners at first.", ["Why does slowing down help?", "What does each sensor see when it's centred?"], "Sensor height, or reading the wrong value for black.", "The robot completes a full lap."),
    ("Final mission and showcase", [("robot-25", "Exercise 25"), ("buildlog", "Build Log"), ("quiz", "Quizzes")], "Combine everything, and show it to someone.", "Invite someone to watch. Take a photo or video, if the family agrees.", ["What was the hardest fault you fixed?", "What would you add next?"], "Rushing the last steps. Test one feature at a time.", "The student demonstrates the mission, and explains how it works."),
]

MISTAKES = [
    ("Asks you to fix it straight away", "Ask, \"What did you expect, and what happened?\" Then point to the Fix It Guide. Let them keep their hands on the parts."),
    ("Copies code without understanding it", "Ask them to explain one line, or to make one change and predict the result first."),
    ("Changes several things at once", "Undo the changes, then change one thing at a time."),
    ("Gets upset when something fails", "Say that every engineer debugs. Remind them that finding a fault counts as progress."),
    ("Rushes to power on", "Make the wiring check a habit: they trace it first, then you check it."),
    ("Trusts a reading without testing", "Ask, \"How do you know that's right?\" Compare it with a ruler, a meter or a known value."),
    ("Gets stuck on spelling and brackets", "Switch to the Blocks tab for a while, then look at the code it writes."),
]

RUBRIC = [
    ("Wiring", "Copies steps with help", "Copies steps alone and spots simple errors", "Plans and checks a circuit alone"),
    ("Coding", "Changes numbers in given code", "Writes short programs using if and loops", "Writes and organises programs using functions"),
    ("Fault finding", "Asks for help straight away", "Follows the method with some prompts", "Finds and explains faults alone"),
    ("Safety", "Needs reminders", "Follows the rules unprompted", "Spots risks and tells others"),
    ("Explaining", "Says what it does", "Says how it works", "Explains why, and suggests improvements"),
]

# Answer keys. Keys match the exercise numbers and sensor slugs.
ROBOT_ANSWERS = {
    1: "Motors draw sudden, large currents that can make the Arduino's supply dip and reset it. Separate supplies keep the Arduino steady.",
    2: "Two wheels alone would tip over. A third point, the caster, stops it tipping and still lets it turn.",
    3: "The driving wheels at the back carry less weight, so they can slip. The robot may also tip forward when it stops.",
    4: "Signals are measured against ground. Without a shared ground, the driver can't tell what the Arduino's HIGH and LOW mean.",
    5: "Either works. Swapping wires is simple and keeps the code the same for every robot. Changing code needs no tools, but you have to remember it next time.",
    6: "The left motor is slower. Lower the right motor's speed a little, such as drive(200, 190), until it goes straighter.",
    7: "Wheels slip, motors take time to speed up and slow down, and the two motors differ. Small errors build up.",
    8: "Probably not. Carpet adds friction, and weak batteries slow the motors. You'd need to tune the time again, or use a sensor.",
    9: "Usually not. A motor needs a minimum level just to start turning, so speed doesn't rise in direct proportion to the number.",
    10: "You only change it in one place, so you can't forget one, and the code says what the number means.",
    11: "A sensor can measure what really happened, then correct it. Examples are a line on the floor, a distance to a wall, wheel encoders or a gyroscope.",
    12: "The faster wheel travels further than the slower one, so the robot curves towards the slower side.",
    13: "It stops a machine moving when people don't expect it, and it gives time to move hands away first.",
    14: "Many answers work: low battery, waiting for a press, a fault, or a sensor seeing something. Blink patterns can show more.",
    15: "They warn people who can't see the driver or who aren't looking. A robot could beep before it starts moving or reverses.",
    16: "Soft and steeply angled surfaces may give no echo, or a false one. The robot may not see them, so it shouldn't trust one sensor completely.",
    17: "It travels further between readings, and it takes longer to slow down, so it needs to start stopping earlier.",
    18: "Without it, the robot would chase any far object, or drive off when it gets no echo. The limit means \"only follow something close\".",
    19: "It can get stuck beside corners, because the narrow beam only looks straight ahead. It may also miss soft objects. A turning head or bump switches would help.",
    20: "Servos draw sudden gulps of current, which can reset the Arduino if they share its 5V supply. Batteries handle them better, with a shared ground.",
    21: "It could back up and spin around, or check behind it. For example, reverse for a moment, then turn 180 degrees.",
    22: "Sunlight contains lots of infrared, which can swamp the sensor. Shiny floors can reflect it in odd directions, so black and white look wrong.",
    23: "It reacts as fast as possible. With delay(300), the robot travels several centimetres blind between readings, and can run off the line.",
    24: "A faster robot travels further before it reads the line and reacts, so it crosses further before it can reverse.",
    25: "There's no single answer. Good answers name a new ability, the sensor it needs, and how it would change the sense-think-act loop.",
}
SENSOR_ANSWERS = {
    "temperature": "0.31 V is 310 mV, so 31&#176;C. Electrical noise and small air movements cause jumps. Averaging several readings smooths them out.",
    "humidity": "Breath is warm and damp, so both readings rise. For a fair test, change one thing at a time, and keep the distance and time the same.",
    "rain": "25 &#215; 0.2 mm = 5 mm. In very light drizzle, the bucket may fill too slowly to tip, or some water may evaporate first.",
    "soil": "Soils differ in type and packing, which changes the reading. The probe should sit in the root zone, partway down and away from the edge.",
    "accelerometer": "The Z axis, which points up and down. It feels the table pushing up against gravity, even though the phone isn't moving.",
    "gyroscope": "Up to 60 degrees, because 1 &#176;/s &#215; 60 s = 60&#176;. That's why gyroscopes are combined with other sensors.",
    "ultrasonic": "The sound travels there and back, so the time covers twice the distance. A curtain soaks up the sound, so the robot may not see it.",
    "lidar": "Each covers the others' weak spots. LIDAR gives fine 3D shape, radar works in fog and measures speed, and cameras read signs, colours and lights.",
    "radar": "Ultrasonic works well for short, close distances indoors. Radar suits darkness and dust, and it can sense through thin non-metal materials.",
    "ldr": "The lamp's light makes the sensor think it's day, so the lamp turns off. Then it's dark, so the lamp turns on again. Shield the sensor, or use separate on and off levels.",
    "ir": "Many camera sensors can see infrared, so you can check whether a remote is transmitting, even though your eyes can't see it.",
    "image": "Even a small colour picture takes millions of bytes. 2 kB holds only about 2,000 bytes, a tiny fraction of one picture.",
    "geiger": "Random events vary a lot over short times. More counts over a longer time give a steadier average.",
    "gas": "The sensing layer only works properly at its running temperature. Readings straight after power-on can be falsely high or unstable.",
    "ph": "Two known points set both the middle value and the slope of the line. Without them, the numbers can be well off.",
    "breath": "Other vapours, temperature, humidity and sensor age can all change it. A wrong result could put someone in danger or treat them unfairly.",
    "pressure": "Weather changes air pressure, and the code reads that change as a change in height, even when the sensor hasn't moved.",
    "load": "Subtract the 3 g reading from every later reading. That's what the tare button does: it stores the empty reading as zero.",
    "level": "A second, independent high-level switch or overflow alarm. If one sensor fails, the other still stops the pump.",
    "flow": "45 &#247; 7.5 = 6 L/min. Check it by timing how long it takes to fill a measuring jug, then compare the two figures.",
    "pulse": "Movement changes how the skin presses on the sensor, and this looks like a beat. Count the peaks in 15 seconds, and multiply by 4.",
    "ecg": "Battery power means there's no path to mains through the equipment if something fails. Moving adds muscle signals and loose contact noise.",
}

# Stage, parts (item, quantity, what it's for)
PARTS = [
    ("Stage 1: Getting started", "Lab Examples 1 to 15, and Coding Lessons", [
        ("Arduino Uno R3 (or a compatible board)", "1", "The brain of every project"), ("USB cable that carries data", "1", "Some cables only charge"), ("Breadboard, 830 holes", "1", "Holds your circuits"), ("Jumper wires, male to male", "About 40", "Connections"),
        ("LEDs: red, yellow, green, blue", "About 10", "Outputs"), ("Resistors: 220 &#937;", "10", "For LEDs"), ("Resistors: 1 k&#937;", "10", "Transistor bases, and LEDs on an R4"), ("Resistors: 10 k&#937;", "5", "Light sensor"), ("Push buttons", "2", "Inputs"), ("Potentiometer, 10 k&#937;", "1", "Dial input"), ("Light sensor (LDR)", "1", "Night light"), ("Passive piezo buzzer", "1", "Notes and tunes"), ("Capacitors: 470 &#181;F, 16 V or higher", "2", "Steadying power"), ("Transistors: 2N2222", "2", "Small switching"),
    ]),
    ("Stage 2: Motors and servos", "Lab Examples 16 to 21", [
        ("Small DC motor, 3&#8211;6 V", "1", "Motor examples"), ("Transistor: TIP120", "1", "Switching the motor"), ("Diodes: 1N4001", "2", "Motor protection"), ("SG90 micro servo", "1", "Moving to an angle"), ("4 &#215; AA battery holder", "1", "Motor and servo power"), ("AA batteries", "4, plus spares", "Rechargeable cells give about 4.8 V"),
    ]),
    ("Stage 3: Sensors", "Lab Examples 22 to 28", [
        ("HC-SR04 ultrasonic sensor", "1", "Distance"), ("LM35 temperature sensor", "1", "Thermometer"), ("Capacitive soil moisture sensor", "1", "Plant alarm"), ("IR obstacle module (FC-51 type)", "1", "Obstacle alarm"),
    ]),
    ("Stage 4: The robot", "Robot Exercises 1 to 25", [
        ("2-wheel robot chassis kit, with geared motors, wheels and caster", "1", "The robot's body"), ("L9110S motor driver board", "1", "Runs both wheels"), ("USB power bank", "1", "Powers the Arduino on the move"), ("Line sensor modules, digital output", "2", "Following lines"), ("Active buzzer module, with a built-in transistor", "1", "The horn"), ("Small breadboard", "1", "Fits on the robot"), ("Black electrical tape", "1 roll", "Line tracks"), ("Double-sided tape", "1 roll", "Fixing parts"),
    ]),
    ("Useful tools", "Handy at every stage", [
        ("Digital multimeter", "1", "Finding faults"), ("Small screwdrivers", "1 set", "Terminals and the chassis"), ("Storage box with compartments", "1", "Small parts go missing"),
    ]),
]
