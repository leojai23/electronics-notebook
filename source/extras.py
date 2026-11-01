# Extra study content: sensor and robot quizzes, robot flashcards, and the fault-finding guide.
from figures import t, rect, circ
from sensor_art import plate

SENSOR_QUIZ = [
    ("An LM35 reads 0.25 V. What temperature is that?", ["2.5&#176;C", "25&#176;C", "250&#176;C", "0.25&#176;C"], 1, "The LM35 gives 10 mV per degree, so 250 mV is 25&#176;C."),
    ("What two things does a DHT11 report?", ["Temperature and humidity", "Light and sound", "Distance and speed", "Pressure and weight"], 0, "It sends both readings as digital data on one wire."),
    ("A capacitive soil sensor reads a higher voltage. What does that usually mean?", ["The soil is wetter", "The soil is drier", "The soil is hotter", "The sensor is broken"], 1, "On these probes, higher voltage means drier soil."),
    ("Why do a water sensor's bare tracks need care?", ["They get very hot", "They corrode when powered all the time", "They use too much data", "They only work in the dark"], 1, "Power the tracks only when you take a reading."),
    ("How does a phone know which way up it is?", ["An accelerometer feels gravity", "An LDR sees the sky", "A pH sensor", "A load cell"], 0, "An accelerometer can tell which way is down."),
    ("What does a gyroscope measure?", ["How heavy something is", "How fast something rotates", "How wet the air is", "How loud a sound is"], 1, "It measures rotation, in degrees per second."),
    ("Which sensor uses laser light to measure distance?", ["RADAR", "LIDAR", "Ultrasonic", "Geiger counter"], 1, "LIDAR times how long laser pulses take to return."),
    ("Which usually works better in thick fog?", ["RADAR", "LIDAR", "A camera", "An LDR"], 0, "Radio waves are affected far less by fog than light is."),
    ("Why does an LDR need a second resistor to work with an Arduino?", ["To make it brighter", "To turn its resistance into a voltage", "To make it digital", "To cool it down"], 1, "A voltage divider turns changing resistance into a voltage that A0 can read."),
    ("Why can't an Arduino Uno handle a camera sensor?", ["It has too little memory and speed for image data", "It has no pins", "Cameras need 12 V", "It can't use light"], 0, "One picture needs far more memory than the Uno's 2 kB."),
    ("What does each click of a Geiger counter mean?", ["One detected particle", "One second has passed", "One litre of air", "One metre of distance"], 0, "Each detection makes one pulse. Counts per minute shows the level."),
    ("Why is a hobby MQ-2 module not a home safety alarm?", ["It's too small", "It isn't a certified safety device", "It can't sense smoke", "It needs the internet"], 1, "Homes need certified alarms. These modules are for learning."),
    ("What does pH 3 tell you about a liquid?", ["It's acidic", "It's neutral", "It's alkaline", "It's very hot"], 0, "Under 7 is acidic, and over 7 is alkaline."),
    ("What does the HX711 board do for a load cell?", ["It cools it", "It amplifies a tiny signal and sends numbers", "It adds weight", "It measures light"], 1, "A load cell's voltage is tiny, so the HX711 amplifies and reads it."),
    ("A YF-S201 gives 75 pulses per second. About what is the flow?", ["1 L/min", "10 L/min", "75 L/min", "450 L/min"], 1, "Pulses per second is about 7.5 &#215; L/min, so 75 &#247; 7.5 = 10."),
    ("Why must an AD8232 ECG project stay on battery power?", ["Batteries are stronger", "So no mains-powered equipment connects to your body", "It reads faster", "Mains has no voltage"], 1, "Unplug the laptop from the wall when electrodes are on your skin."),
]

ROBOT_QUIZ = [
    ("Why should you test new code with the robot on a box?", ["The box adds power", "The wheels spin safely in the air", "The sensor sees better", "It makes the code faster"], 1, "It can't drive off while you check that the wheels turn the right way."),
    ("Why does the robot use a motor driver board?", ["Arduino pins can't supply motor current", "It makes the wheels bigger", "It stores the code", "It reads the sensors"], 0, "Pins only send signals. The driver switches the battery power."),
    ("Why must the Arduino and motor driver share a ground?", ["So that signals have a common reference", "To add more voltage", "To make the wires shorter", "To charge the battery"], 0, "Without a shared ground, the driver can't read the signals reliably."),
    ("How do you spin the robot on the spot?", ["Run both wheels forward", "Run the wheels in opposite directions", "Stop one wheel only", "Turn the caster"], 1, "One wheel forward and the other backward turns the robot without moving it along."),
    ("Your robot curves left when driving straight. What's the likely cause?", ["The left motor is a bit slower", "The right motor is a bit slower", "The code has no loop", "The caster is too big"], 0, "A slower left wheel makes the robot turn towards the left."),
    ("What usually happens if you set a very low motor speed, such as 40?", ["The motor runs fastest", "The motor may just hum and not turn", "The Arduino resets", "The motor reverses"], 1, "Motors need a minimum level to overcome friction."),
    ("Why does the horn exercise use an active buzzer, not tone()?", ["tone() interferes with PWM on pins 3 and 11", "tone() needs a library", "Active buzzers are louder", "tone() only works on A0"], 0, "The right motor uses pins 3 and 11 for speed control."),
    ("Why does a square path rarely end exactly at the start?", ["Small errors add up on every corner", "Squares have five sides", "The Arduino forgets", "The floor is too flat"], 0, "A small turning error on each corner grows by the end."),
    ("A robot with one fixed sensor gets stuck against the side of a box. Why?", ["The narrow beam can't see beside it", "The sensor is too loud", "The box is too soft", "The Arduino is too fast"], 0, "The sensor looks straight ahead, so a corner beside it can be missed."),
    ("Why mount the sensor on a servo?", ["To look left and right before choosing", "To make it louder", "To power the wheels", "To save battery"], 0, "A turning head can compare the room on each side."),
    ("Why does the line-following code have no delay() in its loop?", ["So that it can react quickly to the line", "Because delay() is broken", "To save memory", "So that the wheels stop"], 0, "A long delay lets the robot run off the line between readings."),
    ("Why should you take the batteries out when you've finished?", ["To stop accidental starts and flat batteries", "To make it heavier", "To delete the code", "To cool the sensor"], 0, "It prevents surprises, and keeps your batteries charged."),
]

ROBOT_CARDS = [
    ("Chassis", "The robot's frame, which everything is mounted on."), ("Caster wheel", "A free-turning wheel that supports the robot without driving it."),
    ("Motor driver", "A board that lets small signals control the larger current that motors need."), ("Shared ground", "A wire joining the &#8722; sides of separate supplies, so that signals have a common reference."),
    ("Differential drive", "Steering by running the two wheels at different speeds."), ("Spin on the spot", "Turning by running the wheels in opposite directions."),
    ("PWM", "Fast on-off pulsing, used to control motor speed."), ("Stall point", "The lowest level where a motor still turns."),
    ("Function", "A named block of code that you can call, such as forward()."), ("Calibration", "Measuring and adjusting, so that a robot's numbers match the real world."),
    ("Line sensor", "A downward-facing sensor that tells black from white."), ("Blind spot", "An area a sensor can't see, such as beside a narrow beam."),
    ("Sense, think, act", "The loop that robots repeat: read sensors, decide, then move."), ("Power bank", "A USB battery, used here to run the Arduino away from a computer."),
]

FAULT_STEPS = [
    "<strong>Stop and unplug.</strong> If anything is hot or smells, let it cool first.",
    "<strong>Say what you expected, and what happened.</strong> \"The LED should blink, but it stays dark\" is already half the answer.",
    "<strong>Check power first.</strong> Is the Arduino's power light on? Is the battery fresh? Are the power rails connected?",
    "<strong>Follow the wires.</strong> Trace each connection from start to end, using your finger and the steps for that build.",
    "<strong>Check direction.</strong> LEDs, electrolytic capacitors, diodes, transistors and modules must go the right way round.",
    "<strong>Test one thing at a time.</strong> Run a tiny sketch that tests only the part in doubt. Change one thing, then test again.",
    "<strong>Compare with the simulator.</strong> Open the same example and check that your wiring and code match.",
    "<strong>Write it down.</strong> Record the problem and the fix in the <a href=\"#buildlog\">Build Log</a>.",
]

FAULTS = [
    ("Uploading code", [
        ("The upload fails or the port isn't listed", ["The wrong board or port is selected in the Arduino software.", "Some USB cables only charge, and can't carry data.", "A wire on pin 0 or 1 is interfering with USB. Unplug it and try again.", "Some clone boards need a USB driver, such as CH340."], None),
        ("The code won't compile", ["Read the first error, and look at that line and the one above it.", "Look for a missing semicolon or bracket.", "Capital letters matter: <code>digitalWrite</code>, not <code>digitalwrite</code>."], "ex-2"),
        ("The code uploads, but nothing happens", ["Check that the pin number in the code matches your wire.", "Check for <code>pinMode(pin, OUTPUT)</code> in <code>setup()</code>.", "Try the Blink example to prove the board works."], "ex-2"),
    ]),
    ("LEDs and resistors", [
        ("The LED stays dark", ["It may be backwards. The long leg goes towards the positive side.", "Both legs may be in the same joined group of holes.", "The resistor may be in the wrong row, or be the wrong value.", "The LED may already be burned out. Try another."], "ex-1"),
        ("The LED is very dim", ["The resistor value may be too high. Read its bands again.", "The pin may be set as an INPUT. Check <code>pinMode</code>."], "ex-6"),
        ("The LED flashed once and died", ["It had too little resistance in series, or none. Replace it and add a resistor."], "ex-1"),
    ]),
    ("Buttons and dials", [
        ("The button acts randomly", ["The pin may be floating. Use <code>INPUT_PULLUP</code>, or a resistor to GND or 5V.", "A pressed button reads LOW when using <code>INPUT_PULLUP</code>.", "Real buttons bounce. A short delay helps."], "ex-8"),
        ("The button seems always pressed", ["It may be turned 90 degrees, so its legs are always joined. Rotate it, and place it across the centre gap."], "ex-8"),
        ("The dial's readings don't change", ["Check that the middle leg goes to the analog pin, and the outer legs to 5V and GND."], "ex-10"),
    ]),
    ("Motors and servos", [
        ("The motor doesn't turn", ["Is the battery connected and fresh?", "Does the battery &#8722; join Arduino GND?", "Check the transistor's leg order against its data sheet.", "The speed may be too low. Try full speed first."], "ex-16"),
        ("The Arduino resets when the motor or servo starts", ["It's probably sharing power with the Arduino. Use a separate battery with a shared ground.", "Add a 470 &#181;F capacitor across the motor or servo supply."], "ex-19"),
        ("The servo jitters or ignores commands", ["The battery &#8722; may not be joined to Arduino GND.", "The batteries may be weak.", "Check that the orange wire goes to the pin named in <code>attach()</code>."], "ex-19"),
        ("The transistor or motor gets very hot", ["Unplug it. The motor may be stalled, or the diode may be backwards.", "Check the diode: its stripe faces the battery +."], "ex-16"),
    ]),
    ("Sensors", [
        ("The distance sensor reads 0 or never changes", ["Check that VCC and GND are correct.", "Check that TRIG and ECHO aren't swapped.", "Soft or angled surfaces can give no echo. Test with a book."], "ex-22"),
        ("An analog reading jumps around", ["Check for loose wires, and for a shared GND.", "Take several readings and average them.", "An unconnected analog pin wanders. Check the signal wire."], "ex-26"),
        ("An I2C sensor isn't found", ["SDA goes to A4, and SCL to A5, on an Uno. Check that they aren't swapped.", "Check whether the board accepts 5 V. Some are 3.3 V only."], None),
        ("A library sensor gives no reading or an error", ["Install the library named on the sensor's page.", "Check that the pin number in the code matches your wiring.", "Some sensors, such as the DHT11, can't be read too often."], None),
    ]),
    ("Robots", [
        ("The robot spins when it should go straight", ["One motor's wires are probably reversed. Take out the batteries, and swap that motor's wires."], "rsim-5"),
        ("The robot curves", ["This is normal, because motors are never identical. Lower the faster motor's speed in your code."], "rsim-6"),
        ("The robot is slow or stops working", ["Replace or recharge the batteries first.", "Check that nothing is rubbing against the wheels."], None),
        ("The robot crashes into some things", ["The sensor may miss soft objects, or things beside its beam.", "Make the stopping distance bigger, or slow down.", "Try a turning sensor head."], "rsim-19"),
        ("The robot loses the line", ["Slow down, and make the turns sharper.", "Check your sensor height, and which reading means black."], "rsim-23"),
    ]),
]


def _shuffle(questions):
    """Moves each right answer to a varied position, the same way on every build."""
    out = []
    for i, (q, opts, c, fb) in enumerate(questions):
        shift = (i * 3 + len(q)) % len(opts)
        new = opts[shift:] + opts[:shift]
        out.append((q, new, (c - shift) % len(opts), fb))
    return out


SENSOR_QUIZ, ROBOT_QUIZ = _shuffle(SENSOR_QUIZ), _shuffle(ROBOT_QUIZ)


def fig_fault():
    o = t(24, 30, "Work through these in order, starting with the simplest", 15, 700)
    steps = [("1", "Power", ["Is it on?", "Fresh battery?"]), ("2", "Wires", ["Right holes?", "Shared GND?"]), ("3", "Direction", ["Any part in", "backwards?"]), ("4", "Code", ["Right pins?", "Any errors?"]), ("5", "One part", ["Test it", "on its own"])]
    for i, (n, name, lines) in enumerate(steps):
        x = 18 + i * 138
        o += rect(x, 56, 126, 124, "--card", 8) + circ(x + 22, 80, 14, "--pt") + t(x + 22, 85, n, 14, 800, "middle", "--black")
        o += t(x + 12, 118, name, 13.5, 700, "start", "--card-ink")
        for j, s_ in enumerate(lines):
            o += t(x + 12, 138 + j * 16, s_, 11.5, 400, "start", "--card-soft")
        if i < 4:
            o += f'<line x1="{x + 126}" y1="118" x2="{x + 138}" y2="118" stroke="var(--pt)" stroke-width="3"/>'
    o += t(24, 208, "Most faults are found in steps 1 to 3.", 13, 400, "start", "--lab-soft")
    return plate(o, "Five fault-finding steps in order: power, wires, direction, code, then test one part", 226)


def faults_page(ul):
    groups = ""
    for name, items in FAULTS:
        rows = ""
        for sym, causes, link in items:
            label = "Try it in the Robot Simulator" if link and link.startswith("rsim") else "See it in the Practical Lab"
            tail = f'<p style="margin:6px 0 0"><a href="#{link}">{label}</a></p>' if link else ""
            rows += f'<details class="fault"><summary>{sym}</summary><div class="ans-box">{ul(causes)}{tail}</div></details>'
        groups += f"<h2>{name}</h2>{rows}"
    return f"""<section id="page-faults" data-page data-name="Fix It Guide" hidden>
<h1>Fix It Guide</h1><p class="sub">What to do when something doesn't work</p>
<p><strong>Every builder runs into faults, and finding them is a big part of engineering.</strong> Start with the steps below, then find your problem in the list. Have your guide check anything that gets hot or smells.</p>
<figure><div class="fig-scroll">{fig_fault()}</div></figure>
<h2>The method</h2><ol class="steps">{"".join(f"<li>{x}</li>" for x in FAULT_STEPS)}</ol>
<h2>Using a multimeter</h2>
<p>A multimeter is a low-cost tool that shows what's really happening. Ask your guide to help the first few times, and use it on low-voltage projects only.</p>
<ul class="tight"><li><strong>Voltage (V):</strong> with power on, touch the probes across two points. Is there 5 V between the 5V rail and GND?</li><li><strong>Continuity (the beep setting):</strong> with power off, check whether two points are joined. Use it to find broken wires.</li><li><strong>Resistance (&#937;):</strong> with power off, and the part out of the circuit, check a resistor's value.</li></ul>
{groups}
<div class="safe" style="margin-top:22px"><h3>When to stop</h3>{ul(["Something is hot, smoking or smells: unplug it, and tell your guide.", "A capacitor has bulged, or a battery is swollen or leaking: don't use it. Ask your guide to dispose of it safely.", "Never test a fault by connecting anything to a wall socket."])}</div>
</section>"""
