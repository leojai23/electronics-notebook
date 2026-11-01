# The Introduction page: an overview, then a detailed description of the subject and the notebook.
from figures import t, rect, circ, line
from sensor_art import plate


def box(x, y, w, h, name, lines, main=False):
    fill, stroke = ("--pt-tint", "--pt") if main else ("--card", "--card")
    o = rect(x, y, w, h, fill, 8, stroke, 2)
    o += t(x + 14, y + 24, name, 14, 700, "start", "--card-ink")
    for i, s in enumerate(lines):
        o += t(x + 14, y + 42 + i * 16, s, 12, 400, "start", "--card-soft")
    return o


def arrow(d):
    return f'<path d="{d}" fill="none" stroke="var(--pt)" stroke-width="3" marker-end="url(#r-arrow)"/>'


def fig_water():
    o = t(24, 30, "Electricity flows around a loop, like water pushed by a pump", 15, 700)
    o += arrow("M140 148 V88 H254") + arrow("M496 88 H620 V138") + arrow("M620 220 V280 H506") + arrow("M264 280 H140 V230")
    o += box(24, 148, 232, 72, "Pump = battery", ["Pushes the water along.", "This push is voltage."], True)
    o += box(264, 52, 232, 72, "Narrow pipe = resistor", ["Limits how much can flow.", "This squeeze is resistance."])
    o += box(504, 148, 192, 72, "Wheel = motor or LED", ["Uses the flow to do a job:", "spinning or making light."])
    o += box(264, 244, 232, 72, "Return pipe = wire", ["Brings the water back", "to complete the loop."])
    o += t(380, 180, "The moving water = current", 14, 700, "middle") + t(380, 198, "Break the loop and it all stops", 12.5, 400, "middle", "--lab-soft")
    return plate(o, "A water loop: pump as battery, narrow pipe as resistor, water wheel as motor or LED, and a return pipe as wire", 340)


def fig_loop():
    o = t(24, 30, "Every robot repeats three jobs: sense, think, act", 15, 700)
    o += rect(24, 56, 200, 240, "--mat", 8, "--lab-soft", 1.5) + rect(264, 56, 200, 240, "--mat", 8, "--lab-soft", 1.5) + rect(504, 56, 192, 240, "--mat", 8, "--lab-soft", 1.5)
    for x, s in [(124, "Sense"), (364, "Think"), (600, "Act")]:
        o += t(x, 84, s, 16, 700, "middle")
    o += box(40, 122, 168, 92, "Sensors", ["Measure the world:", "distance, light, heat"])
    o += box(280, 122, 168, 92, "Microcontroller", ["Runs your code and", "decides what to do"], True)
    o += box(516, 100, 168, 54, "Motors", ["Move the robot"]) + box(516, 162, 168, 54, "Servo", ["Turns to an angle"]) + box(516, 224, 168, 54, "LEDs, buzzer", ["Show or sound status"])
    o += arrow("M224 168 H260") + arrow("M464 168 H500") + arrow("M600 296 V322 H124 V300")
    o += t(362, 316, "Then check again, many times a second", 12.5, 700, "middle")
    o += rect(24, 340, 672, 36, "--card", 8) + t(360, 363, "Underneath it all: the breadboard connects the parts, and capacitors steady the power", 13, 700, "middle", "--card-ink")
    return plate(o, "The sense, think, act loop: sensors feed a microcontroller, which controls motors, a servo and lights, then repeats", 396)


def fig_path():
    o = t(24, 30, "Your path through this notebook", 15, 700)
    stages = [("1", "Introduction", ["The big", "ideas"]), ("2", "9 Topics", ["Learn each", "core part"]), ("3", "Practical Lab", ["25 examples", "in a simulator"]), ("4", "22 Sensors", ["How robots", "feel the world"]), ("5", "Robot", ["25 exercises", "on a real build"])]
    for i, (n, name, lines) in enumerate(stages):
        x = 18 + i * 138
        o += rect(x, 56, 126, 124, "--card", 8)
        o += circ(x + 22, 80, 14, "--pt") + t(x + 22, 85, n, 14, 800, "middle", "--black")
        o += t(x + 12, 118, name, 13, 700, "start", "--card-ink")
        for j, s in enumerate(lines):
            o += t(x + 12, 138 + j * 16, s, 11.5, 400, "start", "--card-soft")
        if i < 4:
            o += line(x + 126, 118, x + 138, 118, "--pt", 3, "butt")
    o += t(24, 212, "Steps 2 and 3 go together: read a topic, then try its examples. Step 5 uses everything before it.", 13, 400, "start", "--lab-soft")
    return plate(o, "Five stages in order: introduction, nine topics, practical lab, twenty-two sensors, then robot exercises", 232)


BLINK = """const int LED_PIN = 8;   // give the pin a name

void setup() {           // runs once, at power-on
  pinMode(LED_PIN, OUTPUT);
}

void loop() {            // runs over and over, forever
  digitalWrite(LED_PIN, HIGH);
  delay(1000);           // wait 1 second
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
"""


def intro_page(ul, sensor_count, robot_count, example_count):
    stat = lambda n, s: f'<div><b>{n}</b><span>{s}</span></div>'
    rows = [
        ("9 Topics", "#breadboard", "One core part per page, with an image, key terms, practice questions and Bloom's levels.", "Learning what each part does"),
        ("Practical Lab", "#lab", f"{example_count} examples on a virtual bench. You can rewire them, edit the code and run a check.", "Trying ideas safely, with no parts"),
        ("Sensors", "#sensors", f"{sensor_count} sensors, each with properties, inputs and outputs, a circuit and real-life uses.", "Choosing the right sensor"),
        ("Robot Simulator", "#rsim-6", "Run the robot exercises' code on a virtual robot before you build it.", "Testing robot code safely"),
        ("Robot Exercises", "#robots", f"{robot_count} builds with numbered steps and images, from an empty chassis to a final mission.", "Building a real robot"),
        ("Flashcards, Quizzes and Notes", "#flashcards", "Quick revision of topics, sensors and robot terms, with three quizzes.", "Checking what you remember"),
        ("Fix It Guide", "#faults", "A method for finding faults, plus common problems and their causes.", "Getting unstuck"),
        ("Assignments and Case Study", "#assignments", "Longer tasks, and a robot with four faults to solve.", "Applying what you know"),
    ]
    table = "".join(f'<tr><td><a href="{h}"><strong>{a}</strong></a></td><td>{b}</td><td>{c}</td></tr>' for a, h, b, c in rows)
    return f"""<section id="page-intro" data-page data-name="Introduction" hidden>
<h1>Introduction</h1><p class="sub">Start here: what this notebook is, what you'll learn and how to use it</p>

<h2>Overview</h2>
<p><strong>This notebook teaches you how electronics works and how to build a robot that senses and reacts to the world.</strong> It's written for a young beginner working with an adult guide. You don't need any experience, and you can start with just a web browser.</p>
<p>You'll start with the nine parts found in most beginner circuits. Next, you'll try circuits safely in a built-in simulator and explore the sensors that let machines measure the world. Finally, you'll use it all to build a real robot.</p>
<div class="stats">{stat(9, "core parts")}{stat(sensor_count, "sensors")}{stat(example_count, "simulated examples")}{stat(robot_count, "robot exercises")}</div>
<h3>By the end, you'll be able to:</h3>
{ul(["Read a simple circuit diagram, and build it on a breadboard.", "Work out which resistor to use, and explain why.", "Write Arduino code that reads sensors and controls motors, lights and sound.", "Find and fix faults in your own circuits.", "Build a robot that avoids walls and follows a line."])}
<figure><div class="fig-scroll">{fig_path()}</div></figure>

<h2>Detailed description</h2>

<h3>What are electronics and robotics?</h3>
<p><strong>Electronics</strong> is about controlling electricity to do useful jobs. A circuit might light a lamp, measure a temperature or run a whole phone. <strong>Robotics</strong> combines electronics, mechanics and code to make machines that sense what's around them, decide what to do, and then act.</p>
<p>These ideas are all around you. An automatic door, a washing machine and a car's parking sensor all use parts you'll meet in this notebook.</p>

<h3>The big idea: electricity is like water in pipes</h3>
<p>You can't see electricity, but you can picture water flowing around a closed loop of pipes. A pump pushes the water, and it comes back round to the pump.</p>
<figure><div class="fig-scroll">{fig_water()}</div></figure>
<div class="tw"><table><tr><th>Word</th><th>What it means</th><th>Water version</th><th>Measured in</th></tr><tr><td><strong>Voltage</strong></td><td>The push</td><td>Pressure from the pump</td><td class="val">Volts (V)</td></tr><tr><td><strong>Current</strong></td><td>How much is flowing</td><td>Water flowing past each second</td><td class="val">Amps (A), milliamps (mA)</td></tr><tr><td><strong>Resistance</strong></td><td>How hard it is to flow</td><td>A narrow bit of pipe</td><td class="val">Ohms (&#937;)</td></tr></table></div>
<p style="margin-top:12px">They're linked by <strong>Ohm's Law</strong>: voltage = current &#215; resistance. More push means more flow, and a narrower pipe means less flow.</p>
<ul class="tight"><li><strong>Circuit:</strong> the complete loop. Break it anywhere and everything stops.</li><li><strong>Short circuit:</strong> a path with almost no resistance, like a burst pipe. Huge current rushes through and things get hot fast. This is the main mistake to watch for.</li></ul>
<p>The analogy has limits, because real wires don't leak and water doesn't need a return pipe to flow. Treat it as a thinking tool.</p>

<h3>How a robot works: sense, think, act</h3>
<p>Almost every robot repeats the same three jobs. Once you can see this loop, big projects become much easier to plan.</p>
<figure><div class="fig-scroll">{fig_loop()}</div></figure>

<h3>Analog and digital signals</h3>
<p>Parts talk to the Arduino in two basic ways. A <strong>digital</strong> signal has only two states, HIGH or LOW, like a light switch. An <strong>analog</strong> signal can be any level in a range, like a dimmer. The <a href="#sensors">Sensors</a> section also explains pulses and data signals.</p>

<h3>How you tell it what to do: code</h3>
<p>The Arduino runs a short program called a sketch. Every sketch has two main parts: <strong>setup()</strong> runs once at the start, and <strong>loop()</strong> runs over and over. This one blinks an LED, and you can <a href="#ex-2">run it in the Practical Lab</a>.</p>
<pre class="code" tabindex="0">{BLINK}</pre>
<p style="margin-top:12px">The ideas are the same in every language, so nothing you learn early gets wasted. A good path is:</p>
<div class="tw"><table><tr><th>Stage</th><th>Language</th><th>Why it helps</th></tr><tr><td><strong>First</strong></td><td>Blocks, such as mBlock or Microsoft MakeCode</td><td>You drag and snap instructions, so you can focus on the logic with no spelling mistakes.</td></tr><tr><td><strong>Next</strong></td><td>C++, the Arduino language</td><td>It's what this notebook uses. It runs fast and talks directly to the hardware.</td></tr><tr><td><strong>Later</strong></td><td>Python and MicroPython</td><td>It's easy to read, and popular for cameras and AI. A classic Uno can't run it, so you'd need a board such as a Raspberry Pi Pico.</td></tr></table></div>

<h3>What's in this notebook</h3>
<div class="tw"><table><tr><th>Section</th><th>What you get</th><th>Best for</th></tr>{table}</table></div>

<h3>How to use it</h3>
<ol class="steps"><li><strong>Read a topic.</strong> Start with <a href="#breadboard">Breadboard</a>. Look at the picture first, then read the notes.</li><li><strong>Try it in the Lab.</strong> Each topic ends with links to its examples. Select <strong>Start Simulation</strong> to run one, and <strong>Check my build</strong> to test it.</li><li><strong>Break something on purpose.</strong> Remove a resistor or swap a wire, then read the warning. It's the safest way to learn what can go wrong.</li><li><strong>Build it for real.</strong> Copy the same holes onto a real breadboard, and have your guide check the wiring.</li><li><strong>Test yourself.</strong> Answer the practice questions before opening the model answers. Stuck on something? Use the search box, or the <a href="#faults">Fix It Guide</a>.</li><li><strong>Build the robot.</strong> Work through the Robot Exercises in order. Each one builds on the one before.</li></ol>

<h3>Who does what</h3>
<div class="tw"><table><tr><th>Student</th><th>Guide</th></tr><tr><td>Reads, thinks, builds and tests. Tries to fix problems before asking for help.</td><td>Checks the wiring before power goes on, supervises the marked projects, and asks good questions. You don't need to be an expert.</td></tr></table></div>

<h3>What you need</h3>
<ul class="tight"><li><strong>To begin:</strong> a web browser. Topics and the simulator need nothing else, and a laptop or tablet makes wiring easier than a phone.</li>
<li><strong>For real circuits:</strong> an Arduino Uno and USB cable, a breadboard, jumper wires, LEDs, 220 &#937;, 1 k&#937; and 10 k&#937; resistors, a push button, a 10 k&#937; dial (potentiometer), a light sensor (LDR), a piezo buzzer, a 470 &#181;F capacitor, a 1N4001 diode, 2N2222 and TIP120 transistors, a small DC motor, an SG90 servo, an HC-SR04 sensor and a 4 &#215; AA battery holder.</li>
<li><strong>For the robot:</strong> the extra parts are listed in <a href="#robot-1">Robot Exercise 1</a>.</li></ul>
<p><strong>Which Arduino do you have?</strong> This notebook assumes the classic <strong>Uno R3</strong>. The newer <strong>Uno R4</strong> allows only 8 mA per pin, so it needs bigger LED resistors. Each topic flags this where it matters, and the simulator can switch between the two.</p>

<div class="safe" style="margin-top:18px"><h3>Four safety rules for every build</h3>{ul(["<strong>Check first.</strong> Your guide looks over the wiring before power goes on.", "<strong>Unplug to change.</strong> Disconnect all power before moving any wire.", "<strong>Hot, smelly or smoking? Unplug right away.</strong> Tell your guide and let it cool.", "<strong>Low power only.</strong> Use USB and AA batteries. Never connect anything here to a wall socket."])}</div>
<p style="margin-top:12px">You will make mistakes. Every engineer does. A burned-out LED costs very little, and it teaches you something.</p>
<div class="pn"><a href="#home">&larr; Home</a><a href="#breadboard">Start Topic 1: Breadboard &rarr;</a></div>
</section>"""
