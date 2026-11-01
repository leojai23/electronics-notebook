# The 25 robot exercises: steps, sketches and a drawn image for each one.
from figures import t, label, lead, rect, circ, line

ALL = {"chassis", "wheels", "motors", "caster", "uno", "driver", "battery", "bank"}


def _hi(x, y, w, h, on):
    return f'<rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="{h + 8}" rx="6" fill="none" stroke="var(--pt)" stroke-width="3"/>' if on else ""


def robot(cx, cy, s=1.0, rot=0, on=None, hi=(), ghost=False):
    """Top view of the robot. The front points up when rot is 0."""
    on = ALL if on is None else on
    o = f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})"' + (' opacity=".38"' if ghost else "") + ">"
    if "chassis" in on:
        o += '<rect x="-60" y="-85" width="120" height="170" rx="18" fill="var(--acrylic)" stroke="var(--acrylic-d)" stroke-width="2"/>'
    if "wheels" in on:
        o += rect(-82, 8, 20, 64, "--black", 5, "--black-l", 2) + rect(62, 8, 20, 64, "--black", 5, "--black-l", 2)
        for y in (20, 34, 48, 60):
            o += line(-78, y, -66, y, "--black-l", 2, "butt") + line(66, y, 78, y, "--black-l", 2, "butt")
    if "motors" in on:
        o += rect(-60, 26, 34, 28, "--yellow-w", 3, "--brass-d", 1) + rect(26, 26, 34, 28, "--yellow-w", 3, "--brass-d", 1)
    if "caster" in on:
        o += circ(0, -68, 10, "--silver", "--silver-d", 2)
    if "uno" in on:
        o += rect(-30, -44, 60, 60, "--teal", 4, "--teal-d", 1.5) + rect(-13, -22, 26, 10, "--black", 1) + rect(-22, -44, 16, 12, "--silver", 1)
    if "driver" in on:
        o += rect(-22, 22, 44, 20, "--red-d", 3, "--red", 1)
    if "battery" in on:
        o += rect(-36, 50, 72, 26, "--black", 3, "--black-l", 1.5)
        for x in (-32, -15, 2, 19):
            o += rect(x, 53, 14, 20, "--gold", 2)
    if "bank" in on:
        o += rect(-42, -82, 0.1, 0.1, "--mat")
    if "servo" in on:
        o += rect(-14, -92, 28, 18, "--blue", 2, "--blue-d", 1.5)
    if "sonar" in on:
        o += rect(-34, -120, 68, 24, "--blue", 3, "--blue-d", 1.5) + circ(-18, -108, 10, "--silver", "--silver-d", 1.5) + circ(18, -108, 10, "--silver", "--silver-d", 1.5)
    if "line" in on:
        o += rect(-46, -84, 18, 12, "--blue-d", 2, "--white", 1) + rect(28, -84, 18, 12, "--blue-d", 2, "--white", 1)
    if "leds" in on:
        o += circ(-44, -48, 6, "--red", "--red-d", 1.5) + circ(44, -48, 6, "--led-green", "--brass-d", 1.5)
    if "buzzer" in on:
        o += circ(-44, -18, 8, "--black", "--black-l", 1.5)
    if "button" in on:
        o += rect(36, -28, 18, 18, "--black", 2, "--black-l", 1) + circ(45, -19, 5, "--silver-d")
    o += _hi(-60, -85, 120, 170, "chassis" in hi) + _hi(-82, 8, 20, 64, "wheels" in hi) + _hi(62, 8, 20, 64, "wheels" in hi)
    o += _hi(-60, 26, 34, 28, "motors" in hi) + _hi(26, 26, 34, 28, "motors" in hi) + _hi(-10, -78, 20, 20, "caster" in hi)
    o += _hi(-30, -44, 60, 60, "uno" in hi) + _hi(-22, 22, 44, 20, "driver" in hi) + _hi(-36, 50, 72, 26, "battery" in hi)
    o += _hi(-34, -120, 68, 24, "sonar" in hi) + _hi(-14, -92, 28, 18, "servo" in hi)
    o += _hi(-46, -84, 18, 12, "line" in hi) + _hi(28, -84, 18, 12, "line" in hi)
    o += _hi(-50, -54, 12, 12, "leds" in hi) + _hi(38, -54, 12, 12, "leds" in hi) + _hi(-52, -26, 16, 16, "buzzer" in hi) + _hi(36, -28, 18, 18, "button" in hi)
    return o + "</g>"


def arrow(d, c="--pt", w=4, dash=False):
    dd = ' stroke-dasharray="9 7"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="var({c})" stroke-width="{w}" stroke-linecap="round"{dd} marker-end="url(#r-arrow)"/>'


def badge(x, y, n):
    return f'<circle cx="{x}" cy="{y}" r="13" fill="var(--pt)"/><text x="{x}" y="{y + 5}" font-size="14" font-weight="800" text-anchor="middle" fill="var(--black)">{n}</text>'


def wall(x, y, w, h, s=None):
    o = rect(x, y, w, h, "--board-d", 2, "--white", 1)
    return o + (t(x + w / 2, y - 8, s, 13, 700, "middle") if s else "")


def conn_fig(conns, note=None):
    """Connection diagram. Each row: (from text, to text, colour token)."""
    y0, step = 56, 34
    h = max(320, y0 + len(conns) * step + 44)
    o = t(30, 34, "Arduino Uno", 16, 700) + t(420, 34, "Connects to", 16, 700)
    o += rect(30, 44, 200, len(conns) * step + 8, "--teal", 8, "--teal-d", 2)
    o += rect(420, 44, 280, len(conns) * step + 8, "--card", 8)
    for i, (a, b, c) in enumerate(conns):
        y = y0 + i * step + 12
        o += t(216, y + 5, a, 14, 700, "end", "--white") + circ(230, y, 5, "--silver")
        o += circ(420, y, 5, "--silver-d") + t(434, y + 5, b, 13.5, 700, "start", "--card-ink")
        o += f'<path d="M230 {y} H420" fill="none" stroke="var(--wire-halo)" stroke-width="6"/><path d="M230 {y} H420" fill="none" stroke="var({c})" stroke-width="4"/>'
    if note:
        o += t(30, h - 16, note, 13, 400, "start", "--lab-soft")
    return o, h


def plate(body, alt, h=400):
    return (f'<svg class="plate" viewBox="0 0 720 {h}" role="img" aria-label="{alt}"><rect width="720" height="{h}" rx="8" fill="var(--mat)"/>'
            f'<rect width="720" height="{h}" rx="8" fill="url(#matgrid)"/>{body}</svg>')


FULL = ALL
WITH_S = ALL | {"sonar"}
WITH_L = ALL | {"line"}

# ---------- shared sketch parts ----------
PINS = "const int L1 = 5, L2 = 6;   // left motor\nconst int R1 = 3, R2 = 11;  // right motor\n"
DRIVE = """
void setMotor(int a, int b, int speed) {
  if (speed >= 0) {
    analogWrite(a, speed);
    analogWrite(b, 0);
  } else {
    analogWrite(a, 0);
    analogWrite(b, -speed);
  }
}

// Speeds run from -255 (full reverse) to 255 (full forward).
void drive(int left, int right) {
  setMotor(L1, L2, left);
  setMotor(R1, R2, right);
}
"""
SETUP_M = "  pinMode(L1, OUTPUT);\n  pinMode(L2, OUTPUT);\n  pinMode(R1, OUTPUT);\n  pinMode(R2, OUTPUT);\n"
SONAR_P = "const int TRIG = 7, ECHO = 8;\n"
SETUP_S = "  pinMode(TRIG, OUTPUT);\n  pinMode(ECHO, INPUT);\n"
READ = """
float readCm() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long echoTime = pulseIn(ECHO, HIGH, 30000);
  if (echoTime == 0) return 400;   // no echo: treat the way as clear
  return echoTime * 0.0343 / 2;
}
"""
NO_CODE = None


def m(setup, body, extra="", head=""):
    return f"{head}{PINS}{DRIVE}{extra}\nvoid setup() {{\n{SETUP_M}{setup}}}\n\nvoid loop() {{\n{body}}}\n"


def s(setup, body, extra="", head=""):
    return f"{head}{PINS}{SONAR_P}{DRIVE}{READ}{extra}\nvoid setup() {{\n{SETUP_M}{SETUP_S}{setup}}}\n\nvoid loop() {{\n{body}}}\n"


# ---------- figures ----------
def f_kit():
    o = t(30, 34, "Everything laid out before you start", 16, 700)
    items = [
        (110, 130, robot(0, 0, 0.55, 0, {"chassis"}), "Chassis plate"),
        (270, 110, rect(-30, -22, 60, 44, "--yellow-w", 4, "--brass-d") + rect(-46, -6, 16, 12, "--silver"), "2 geared motors"),
        (420, 110, circ(0, 0, 34, "--black", "--black-l", 3) + circ(0, 0, 14, "--yellow-w"), "2 wheels"),
        (590, 110, circ(0, 0, 18, "--silver", "--silver-d", 2) + rect(-18, -30, 36, 12, "--silver-d", 2), "Caster wheel"),
        (110, 300, rect(-46, -36, 92, 72, "--teal", 5, "--teal-d", 2) + rect(-18, -8, 36, 14, "--black", 1) + rect(-40, -36, 20, 16, "--silver", 1), "Arduino Uno"),
        (270, 300, rect(-34, -20, 68, 40, "--red-d", 4, "--red", 1.5) + rect(-28, -14, 12, 10, "--blue", 1) + rect(16, -14, 12, 10, "--blue", 1), "L9110S driver"),
        (420, 300, rect(-46, -26, 92, 52, "--black", 4, "--black-l", 2) + "".join(rect(-42 + i * 21, -20, 18, 40, "--gold", 2) for i in range(4)), "4 &#215; AA pack"),
        (590, 300, rect(-42, -24, 84, 48, "--silver-d", 8, "--silver", 2) + t(0, 5, "5V USB", 14, 700, "middle", "--black"), "USB power bank"),
    ]
    for x, y, art, name in items:
        o += f'<g transform="translate({x} {y})">{art}</g>' + t(x, y + 62, name, 14, 700, "middle")
    return plate(o, "The robot kit laid out: chassis, two motors, two wheels, caster, Arduino Uno, motor driver, battery pack and power bank")


def f_chassis():
    o = robot(250, 200, 1.5, 0, {"chassis", "motors", "wheels", "caster"}, {"motors", "wheels", "caster"})
    o += badge(120, 245, 1) + badge(380, 245, 1) + badge(112, 310, 2) + badge(388, 310, 2) + badge(250, 66, 3)
    o += label(480, 90, "Assembly order", None)
    for i, (a, b) in enumerate([("1", "Bolt on a motor each side."), ("2", "Press on a wheel each side."), ("3", "Fix the caster in front.")]):
        o += badge(494, 124 + i * 44, a) + t(516, 129 + i * 44, b, 13.5, 600)
    o += t(250, 30, "Front", 14, 700, "middle")
    return plate(o, "The chassis from above, with the motors, wheels and caster highlighted and numbered in assembly order")


def f_mount():
    o = robot(250, 205, 1.5, 0, FULL, {"uno", "driver", "battery"})
    o += lead([(250, 165), (470, 110)]) + label(478, 106, "Arduino Uno", ["Near the middle, with its USB", "socket where you can reach it."])
    o += lead([(250, 253), (470, 210)]) + label(478, 206, "Motor driver", ["Close to the motors, fixed on", "standoffs or tape."])
    o += lead([(250, 300), (470, 300)]) + label(478, 296, "Battery pack", ["At the back, over the wheels.", "The power bank goes beside it."])
    o += t(250, 30, "Front", 14, 700, "middle")
    return plate(o, "The robot from above with the Arduino, motor driver and battery pack highlighted in their mounting positions")


def f_wire_motor():
    o, h = conn_fig([("Pin 5", "Driver A-IA (left motor)", "--w1"), ("Pin 6", "Driver A-IB (left motor)", "--w2"), ("Pin 3", "Driver B-IA (right motor)", "--w3"), ("Pin 11", "Driver B-IB (right motor)", "--w4"), ("GND", "Driver GND and battery &#8722;", "--black")],
                    "Battery + to driver VCC. Left motor to Motor A, right to Motor B. Some boards print 1A in place of IA.")
    return plate(o, "Connection diagram from Arduino pins 5, 6, 3, 11 and GND to the motor driver", h)


def f_wire(conns, alt, note=None):
    o, h = conn_fig(conns, note)
    return plate(o, alt, h)


def f_test_motor():
    o = rect(150, 300, 200, 40, "--board-d", 4) + t(250, 326, "Box under the robot", 13, 700, "middle", "--black")
    o += robot(250, 180, 1.2, 0, FULL, {"wheels"})
    o += arrow("M368 240 V175") + arrow("M132 240 V175")
    o += label(430, 110, "Wheels off the ground", ["Rest the robot on a box, so it", "can't drive away during tests."])
    o += label(430, 210, "Both wheels: same way", ["Forward code should spin both", "the way the arrows show.", "If one is backwards, swap", "that motor's two wires."])
    return plate(o, "The robot resting on a box with its wheels off the ground and arrows showing both wheels turning forward")


def scene_line(x1, x2, y, on, text, ghost=True):
    o = (robot(x1, y, 0.7, 90, on, ghost=False)) + arrow(f"M{x1 + 80} {y} H{x2 - 70}") + (robot(x2, y, 0.7, 90, on, ghost=True) if ghost else "")
    return o + t((x1 + x2) / 2, y - 18, text, 14, 700, "middle")


def f_forward():
    o = scene_line(130, 540, 170, FULL, "Forward for 2 seconds") + t(600, 300, "Stop for", 14, 700, "middle") + t(600, 320, "2 seconds", 14, 700, "middle")
    o += t(130, 290, "Start here", 14, 700, "middle") + t(30, 370, "Use the floor, not a table. Give it 2 metres of clear space.", 13.5, 400, "start", "--lab-soft")
    return plate(o, "The robot starting on the left, driving forward to a position on the right, then stopping")


def f_reverse():
    o = robot(560, 170, 0.7, 90, FULL) + arrow("M480 170 H200", dash=True) + robot(130, 170, 0.7, 90, FULL, ghost=True)
    o += t(340, 150, "Backward: the front still faces right", 14, 700, "middle")
    o += t(560, 290, "Start here", 14, 700, "middle") + t(30, 370, "Reverse means both motors run the other way. The robot doesn't turn around.", 13.5, 400, "start", "--lab-soft")
    return plate(o, "The robot facing right while moving backwards to the left")


def f_spin():
    o = robot(230, 195, 1.35, 0, FULL, {"wheels"})
    o += arrow("M108 280 V190") + arrow("M352 195 V285")
    o += '<path d="M135 60 A130 130 0 0 1 325 60" fill="none" stroke="var(--pt)" stroke-width="4" marker-end="url(#r-arrow)"/>'
    o += label(450, 90, "Spin right", ["Left wheel forward.", "Right wheel backward.", "It turns on the spot."])
    o += label(450, 220, "Spin left", ["Swap both directions."])
    o += label(450, 300, "Tune the time", ["Change the delay until it", "turns exactly 90 degrees."])
    return plate(o, "The robot from above with the left wheel going forward and the right wheel going backward, causing a clockwise spin")


def f_speeds():
    o = ""
    for i, (name, val, ln) in enumerate([("Slow: 120", 120, 110), ("Medium: 180", 180, 220), ("Fast: 255", 255, 360)]):
        y = 80 + i * 118
        o += robot(90, y, 0.5, 90, FULL) + arrow(f"M150 {y} H{150 + ln}", w=5) + t(170 + ln + 8, y + 5, name, 15, 700)
    o += t(30, 385, "Below about 100, many real motors just hum and don't turn. Test yours.", 13, 400, "start", "--lab-soft")
    return plate(o, "Three robots with short, medium and long arrows showing slow, medium and fast speeds")


def f_funcs():
    o = robot(360, 205, 0.95, 0, FULL)
    o += arrow("M360 80 V30") + t(380, 40, "forward()", 15, 700)
    o += arrow("M360 325 V378") + t(380, 372, "backward()", 15, 700)
    o += arrow("M270 205 H170") + t(160, 210, "spinLeft()", 15, 700, "end")
    o += arrow("M450 205 H550") + t(560, 210, "spinRight()", 15, 700)
    return plate(o, "The robot in the centre with four arrows named forward, backward, spin left and spin right")


def f_square():
    o = '<rect x="170" y="70" width="260" height="260" rx="4" fill="none" stroke="var(--pt)" stroke-width="4" stroke-dasharray="10 7"/>'
    o += arrow("M170 330 V80") + arrow("M170 70 H420") + arrow("M430 70 V320") + arrow("M430 330 H180")
    o += robot(170, 330, 0.42, 0, FULL)
    o += badge(148, 200, 1) + badge(300, 48, 2) + badge(452, 200, 3) + badge(300, 352, 4)
    o += label(490, 110, "Four sides", ["Each side: forward, stop, spin", "right by 90 degrees, stop."])
    o += label(490, 210, "Measure the error", ["Mark the start with tape.", "How far from it do you finish?"])
    return plate(o, "A square path with four numbered sides and the robot at the bottom left corner")


def f_dance():
    o = '<path d="M90 300 C170 80 240 80 300 200 S 440 340 510 180 S 620 90 650 250" fill="none" stroke="var(--pt)" stroke-width="4" stroke-dasharray="10 7" marker-end="url(#r-arrow)"/>'
    o += robot(90, 318, 0.42, 20, FULL)
    for i, (x, y, n) in enumerate([(170, 112, 1), (300, 200, 2), (420, 300, 3), (560, 118, 4)]):
        o += badge(x, y, n)
    o += t(30, 36, "Your routine: a list of moves, played in order", 16, 700)
    o += t(30, 380, "Small stops between moves make the routine repeat more reliably.", 13.5, 400, "start", "--lab-soft")
    return plate(o, "A curving path with four numbered moves showing a dance routine")


def f_sonar_top():
    o = '<path d="M250 96 L150 16 H350 Z" fill="var(--pt)" fill-opacity=".18" stroke="var(--pt)"/>'
    o += robot(250, 245, 1.25, 0, WITH_S, {"sonar"})
    o += t(250, 36, "It sees a narrow cone", 13, 700, "middle")
    o += label(470, 90, "Mount it at the front", ["Cylinders face forward.", "Keep it level, and clear of", "wires and the wheels."])
    o += label(470, 210, "Connect it", ["VCC to 5V", "TRIG to pin 7", "ECHO to pin 8", "GND to GND"])
    return plate(o, "The robot with the distance sensor highlighted at the front and a narrow cone showing what it can detect")


def f_wallstop():
    o = robot(120, 200, 0.75, 90, WITH_S) + arrow("M210 200 H440") + robot(480, 200, 0.75, 90, WITH_S, ghost=True)
    o += wall(640, 60, 26, 280, "Wall")
    o += '<path d="M580 330 H640" stroke="var(--pt)" stroke-width="3"/>' + t(610, 322, "20 cm", 14, 700, "middle")
    o += t(330, 110, "Drive while the way is clear", 14, 700, "middle") + t(480, 290, "Stop here", 14, 700, "middle")
    return plate(o, "The robot driving towards a wall and stopping 20 centimetres away")


def f_follow():
    o = robot(120, 200, 0.75, 90, WITH_S) + rect(560, 150, 60, 100, "--tan", 16, "--tan-d", 2) + t(590, 134, "Your hand", 14, 700, "middle")
    zones = [(220, 300, "--bad-zone", "Too close: back up"), (300, 400, "--good-zone", "Just right: stop"), (400, 550, "--far-zone", "Too far: move closer")]
    for a, b, c, text in zones:
        o += rect(a, 300, b - a, 26, c, 2)
    o += t(260, 348, "Under 15", 12.5, 700, "middle") + t(350, 348, "15 to 25", 12.5, 700, "middle") + t(475, 348, "Over 25 cm", 12.5, 700, "middle")
    o += t(260, 290, "Back", 13, 700, "middle") + t(350, 290, "Stop", 13, 700, "middle") + t(475, 290, "Forward", 13, 700, "middle")
    return plate(o, "The robot facing a hand, with three distance zones for backing up, stopping and moving forward")


def f_avoid():
    o = robot(90, 300, 0.55, 90, WITH_S)
    o += arrow("M150 300 H300") + arrow("M320 300 C300 200 340 170 400 180") + arrow("M420 180 H640")
    o += rect(350, 250, 70, 110, "--board-d", 4, "--white", 1) + t(385, 240, "Obstacle", 14, 700, "middle")
    o += badge(240, 278, 1) + badge(308, 240, 2) + badge(520, 158, 3)
    o += label(30, 60, "1. Drive until something is close.") + label(30, 90, "2. Stop, reverse a little, then spin.") + label(30, 120, "3. Carry on along the clear path.")
    return plate(o, "The robot driving, turning away from an obstacle, then carrying on along a clear path")


def f_head():
    o = '<g fill="none" stroke="var(--pt)" stroke-width="3"><path d="M250 150 L90 60"/><path d="M250 150 L250 20"/><path d="M250 150 L410 60"/></g>'
    o += t(68, 56, "Left", 14, 700, "end") + t(270, 34, "Ahead", 14, 700) + t(420, 56, "Right", 14, 700)
    o += robot(250, 270, 1.15, 0, WITH_S | {"servo"}, {"servo", "sonar"})
    o += label(470, 130, "Sensor on a servo", ["Tape or bolt the sensor to the", "servo horn, so that it can look", "left, ahead and right."])
    o += label(470, 260, "Connect the servo", ["Brown to battery &#8722;", "Red to battery +", "Orange to pin 9"])
    return plate(o, "The robot with a servo-mounted distance sensor looking left, ahead and right")


def f_choose():
    o = wall(150, 40, 300, 24, None) + t(300, 32, "Wall ahead", 14, 700, "middle")
    o += robot(300, 290, 0.75, 0, WITH_S | {"servo"})
    o += '<path d="M300 190 L100 110" stroke="var(--pt)" stroke-width="3" stroke-dasharray="7 6"/><path d="M300 190 L620 110" stroke="var(--pt)" stroke-width="3" stroke-dasharray="7 6"/>'
    o += t(60, 100, "Left: 30 cm", 14, 700) + t(690, 100, "Right: 90 cm", 14, 700, "end")
    o += arrow("M400 290 C500 290 560 240 640 180") + t(690, 350, "Right has more room, so turn right", 14, 700, "end")
    return plate(o, "The robot at a wall measuring 30 centimetres to the left and 90 to the right, then turning right")


def f_line_mount():
    o = rect(0, 40, 720, 0.1, "--mat") + rect(205, 0, 90, 400, "--black", 0)
    o += robot(250, 230, 1.25, 0, WITH_L, {"line"})
    o += label(420, 80, "Two sensors, under the front", ["They look down at the floor,", "about 1 cm above it."])
    o += label(420, 180, "Black line between them", ["Both should see the white floor", "while the robot is centred."])
    o += label(420, 280, "Connect them", ["VCC to 5V, GND to GND", "Left DO to A0, right DO to A1"])
    return plate(o, "The robot driving along a black line with two downward-facing sensors on either side of it")


def f_linefollow():
    o = '<path d="M130 200 C130 90 240 60 340 100 C430 140 480 80 560 80 C670 80 670 340 540 340 H220 C150 340 130 280 130 200 Z" fill="none" stroke="var(--black)" stroke-width="20"/>'
    o += robot(130, 210, 0.45, 0, WITH_L)
    o += label(250, 190, "Follow the line", ["Left sensor sees black: steer left.", "Right sensor sees black: steer right.", "Neither sees it: go straight."])
    return plate(o, "A curved black track with the robot following it")


def f_ring():
    o = '<circle cx="250" cy="200" r="170" fill="var(--board)" stroke="var(--black)" stroke-width="18"/>'
    o += arrow("M180 260 L330 90", "--brown") + arrow("M340 110 L150 150", "--brown") + robot(170, 280, 0.45, 40, WITH_L)
    o += label(460, 120, "Stay inside the ring", ["Drive forward on the white area.", "When a sensor sees black, back", "up, spin away and carry on."])
    return plate(o, "A white circle with a black border and the robot bouncing off the edge while staying inside")


def f_mission():
    o = '<path d="M70 320 H330 C430 320 470 260 470 190 C470 100 560 70 650 70" fill="none" stroke="var(--black)" stroke-width="18"/>'
    o += robot(70, 310, 0.42, 90, WITH_L | {"sonar", "leds", "button"})
    o += rect(575, 30, 26, 80, "--board-d", 2, "--white", 1)
    o += badge(70, 245, 1) + badge(280, 290, 2) + badge(520, 45, 3) + badge(650, 130, 4)
    for i, s_ in enumerate(["1. Press the button to start. Green light on.", "2. Follow the line.", "3. Something on the line? Stop, red light, wait.", "4. When the way is clear, carry on."]):
        o += t(30, 40 + i * 24, s_, 13.5, 700)
    return plate(o, "A mission course with a start point, a curved line and an obstacle placed on the line")


# ---------- exercises ----------
R = [
    dict(title="Meet your robot kit", stage="Build", fig=f_kit, time="15 minutes",
         goal="Check that you have every part before you start building.",
         need=["2-wheel robot chassis kit, with 2 geared motors, 2 wheels and a caster", "Arduino Uno and USB cable", "L9110S motor driver board", "4 &#215; AA battery holder and batteries", "USB power bank, for the Arduino", "HC-SR04 sensor, SG90 servo, 2 line sensors, LEDs, active buzzer module and push button, for later exercises", "Jumper wires, small screwdriver and tape"],
         steps=["Lay out all the parts on a clear table, like the picture.", "Tick each one off against the list above.", "Find the two motors. Each has two wires or two metal tabs.", "Find the motor driver's labels: A-IA, A-IB, B-IA, B-IB, VCC and GND. Some boards print 1A in place of IA.", "Keep small parts, such as screws, in a tray."],
         code=NO_CODE, check="You can name every part and say what job it does.",
         think="Why does the robot use two power sources: AA batteries for the motors and USB for the Arduino?"),
    dict(title="Build the chassis", stage="Build", fig=f_chassis, time="30 minutes",
         goal="Put together the moving base of your robot.",
         need=["Chassis plate", "2 geared motors", "2 wheels", "Caster wheel", "Screws and a screwdriver"],
         steps=["Ask your guide to help check the motor wires are firmly attached.", "Bolt one motor to each side at the back, with the shafts pointing outwards (step 1 in the picture).", "Press a wheel straight onto each motor shaft (step 2).", "Screw the caster wheel under the front of the plate (step 3).", "Stand the chassis on a table. It should rest on the wheels and caster without rocking.", "Push it gently. Both wheels should turn freely."],
         code=NO_CODE, check="The chassis rolls in a straight line when you push it gently.",
         think="Why does a robot with two driving wheels need a third point of contact?"),
    dict(title="Mount the electronics", stage="Build", fig=f_mount, time="20 minutes",
         goal="Fix the main parts in place so that wires can reach and weight is balanced.",
         need=["Built chassis", "Arduino Uno", "Motor driver", "Battery holder", "Power bank", "Double-sided tape or standoffs"],
         steps=["Take the batteries out of the holder for now.", "Place the battery pack at the back, over the wheels.", "Place the motor driver between the two motors.", "Place the Arduino near the middle, where you can reach its USB socket.", "Check that nothing touches the wheels. Metal parts must not touch the Arduino's underside.", "Fix each part with tape or standoffs, and push the robot to check it still rolls well."],
         code=NO_CODE, check="You can lift the robot and shake it gently, and nothing falls off.",
         think="What happens to a robot's grip and balance if all the weight is at the front?"),
    dict(title="Wire the motor driver", stage="Build", fig=f_wire_motor, time="25 minutes",
         goal="Connect the Arduino, driver, motors and batteries correctly.",
         need=["Mounted robot", "Jumper wires", "Screwdriver for the driver's terminals, if it has them"],
         steps=["Keep the batteries out and the USB unplugged.", "Connect the left motor's two wires to Motor A on the driver, and the right motor's to Motor B.", "Connect the four control wires exactly as the picture shows: pin 5, 6, 3 and 11.", "Connect the Arduino's GND to the driver's GND. This is the shared ground.", "Connect the battery holder's red wire to driver VCC, and its black wire to driver GND.", "Have your guide check every connection against the picture. Reversed battery wires can damage the driver.", "Don't add batteries until the next exercise."],
         code=NO_CODE, check="Your guide has checked all nine connections against the picture.",
         think="Why must the Arduino and the motor driver share a ground wire?"),
    dict(title="Test each motor", stage="Move", fig=f_test_motor, time="20 minutes",
         goal="Prove that each motor works and turns the right way, with the robot safely off the ground.",
         need=["Wired robot", "A small box to rest the robot on", "4 AA batteries", "USB cable"],
         steps=["Rest the robot on a box, so that its wheels spin in the air.", "Connect USB and upload the sketch below, with the batteries still out.", "Put the batteries in. The left wheel should turn, then the right wheel.", "Check that both spin in the forward direction.", "If a wheel spins backwards, take the batteries out and swap that motor's two wires.", "Take the batteries out when you've finished."],
         code=f"{PINS}\nvoid setup() {{\n{SETUP_M}}}\n\nvoid loop() {{\n  // Left wheel forward\n  digitalWrite(L1, HIGH);\n  digitalWrite(L2, LOW);\n  delay(1500);\n  digitalWrite(L1, LOW);\n  delay(500);\n\n  // Right wheel forward\n  digitalWrite(R1, HIGH);\n  digitalWrite(R2, LOW);\n  delay(1500);\n  digitalWrite(R1, LOW);\n  delay(1500);\n}}\n",
         check="The left wheel spins forward, then the right wheel spins forward.",
         think="If a motor runs backwards, you could swap its wires or change your code. Which would you choose, and why?"),
    dict(title="Drive forward and stop", stage="Move", fig=f_forward, time="20 minutes",
         goal="Make your robot's first real journey.",
         need=["Tested robot", "Power bank", "A clear floor, at least 2 metres long"],
         steps=["Upload the sketch while the robot is on its box.", "Unplug USB. Plug the power bank into the Arduino and fix it to the robot.", "Put the robot on the floor and add the batteries.", "Watch it drive forward for 2 seconds, then stop for 2 seconds.", "Note whether it curves. Almost all small robots do, because motors are never identical."],
         code=m("", "  drive(200, 200);\n  delay(2000);\n  drive(0, 0);\n  delay(2000);\n"),
         check="The robot drives forward, stops, and repeats.",
         think="Your robot curves to the left. Which motor is faster? How could you fix it in code?"),
    dict(title="Drive backward", stage="Move", fig=f_reverse, time="10 minutes",
         goal="Use negative speeds to drive in reverse.",
         need=["Your robot", "A clear floor"],
         steps=["Change the sketch to drive forward, then backward, with stops between.", "Upload it with the robot on the box and check the wheels change direction.", "Move it to the floor and run it.", "Put tape where it starts. See how close it gets back to the tape."],
         code=m("", "  drive(200, 200);\n  delay(1500);\n  drive(0, 0);\n  delay(500);\n  drive(-200, -200);\n  delay(1500);\n  drive(0, 0);\n  delay(2000);\n"),
         check="The robot goes forward, stops, reverses, and finishes near where it started.",
         think="Why does it usually not finish exactly at the tape?"),
    dict(title="Spin on the spot", stage="Move", fig=f_spin, time="20 minutes",
         goal="Turn the robot by running its wheels in opposite directions.",
         need=["Your robot", "A clear floor", "Tape to mark angles"],
         steps=["Upload the sketch below.", "Put a strip of tape on the floor, and line the robot up with it.", "Watch the spin. Mark where it stops.", "Change the delay until it turns as close to 90 degrees as you can get.", "Write down that delay. You'll use it in later exercises."],
         code=m("", "  drive(170, -170);  // spin right\n  delay(400);\n  drive(0, 0);\n  delay(2000);\n"),
         check="The robot turns about 90 degrees on the spot.",
         think="Does your 90-degree time still work on carpet? What about with weak batteries?"),
    dict(title="Control speed", stage="Move", fig=f_speeds, time="15 minutes",
         goal="Use PWM to drive at different speeds, and find the slowest working speed.",
         need=["Your robot", "A measuring tape", "A timer"],
         steps=["Upload the sketch below and watch the three speeds.", "Measure how far the robot travels in 2 seconds at each speed.", "Work out each speed in cm per second.", "Lower the first number until the robot stops moving. That's its stall point.", "Write down your results in a table."],
         code=m("", "  drive(120, 120);\n  delay(2000);\n  drive(180, 180);\n  delay(2000);\n  drive(255, 255);\n  delay(2000);\n  drive(0, 0);\n  delay(3000);\n"),
         check="The robot visibly speeds up in three steps, and you have a table of results.",
         think="Is a speed of 240 exactly twice as fast as 120? Check your measurements."),
    dict(title="Write your own drive functions", stage="Move", fig=f_funcs, time="20 minutes",
         goal="Name your moves, so that later programs read almost like English.",
         need=["Your robot"],
         steps=["Read the sketch and find the four new functions.", "Upload it and check that each move does what its name says.", "Add a new function called stopRobot().", "Replace each drive(0, 0); with your new function.", "Keep this sketch. Later exercises build on these ideas."],
         code=m("", "  forward(1000);\n  spinLeft(400);\n  forward(1000);\n  spinRight(400);\n  backward(1000);\n  delay(2000);\n",
                """
const int SPEED = 180;

void forward(int ms) {
  drive(SPEED, SPEED);
  delay(ms);
  drive(0, 0);
}

void backward(int ms) {
  drive(-SPEED, -SPEED);
  delay(ms);
  drive(0, 0);
}

void spinLeft(int ms) {
  drive(-SPEED, SPEED);
  delay(ms);
  drive(0, 0);
}

void spinRight(int ms) {
  drive(SPEED, -SPEED);
  delay(ms);
  drive(0, 0);
}
"""),
         check="Each named move does what its name says.",
         think="Why does using a named constant such as SPEED make your program easier to change?"),
    dict(title="Drive a square", stage="Move", fig=f_square, time="30 minutes",
         goal="Combine driving and turning into a planned path.",
         need=["Your robot", "Tape", "Your 90-degree time from Exercise 8"],
         steps=["Mark the starting corner with tape.", "Put your 90-degree time into the TURN constant.", "Upload the sketch and run it on the floor.", "See how far from the tape it finishes.", "Adjust TURN and run it again. Try to finish within 10 cm of the start.", "Record how each change affected the result."],
         code=m("", "  for (int side = 0; side < 4; side++) {\n    drive(180, 180);\n    delay(1200);\n    drive(0, 0);\n    delay(300);\n    drive(170, -170);\n    delay(TURN);\n    drive(0, 0);\n    delay(300);\n  }\n  delay(5000);\n", head="const int TURN = 400;\n"),
         check="The robot traces a recognisable square and ends near the start.",
         think="A small error on each corner gets bigger by the end. How could a sensor help the robot correct itself?"),
    dict(title="Program a dance routine", stage="Move", fig=f_dance, time="30 minutes",
         goal="Plan and code a sequence of your own design.",
         need=["Your robot", "Paper and pencil", "Some music, if you like"],
         steps=["Draw your dance on paper as a list of at least 6 moves.", "Use the sketch below as a starting point.", "Turn each move into a line that calls step().", "Add a short pause between moves.", "Test it, and adjust the timings.", "Perform it for your guide."],
         code=m("", "  step(200, 200, 600);    // forward\n  step(-170, 170, 300);   // spin left\n  step(170, -170, 600);   // spin right\n  step(-170, 170, 300);   // spin left\n  step(-200, -200, 600);  // backward\n  step(120, 255, 900);    // curve left\n  delay(3000);\n",
                "\nvoid step(int left, int right, int ms) {\n  drive(left, right);\n  delay(ms);\n  drive(0, 0);\n  delay(150);\n}\n"),
         check="The robot performs your routine, the same way two times in a row.",
         think="The left and right wheels are at different speeds in the curve. How does that make the robot turn?"),
    dict(title="Add a start button", stage="Add-ons", fig=lambda: f_wire([("Pin 2", "Button, one corner leg", "--w1"), ("GND", "Button, opposite corner leg", "--black")], "Connection diagram from Arduino pin 2 and GND to diagonally opposite legs of a push button", "The button sits across the breadboard's centre gap. Use diagonally opposite legs."), time="15 minutes",
         goal="Stop the robot driving off as soon as it powers up.",
         need=["Your robot", "Push button", "Small breadboard, stuck on the robot", "2 jumper wires"],
         steps=["Stick the small breadboard on the robot.", "Put the button across the centre gap.", "Wire it as the picture shows.", "Upload the sketch below.", "Power on. The robot should wait until you press the button.", "Press it, and the robot should drive for 2 seconds, then wait again."],
         code=m("  pinMode(BUTTON, INPUT_PULLUP);\n", "  if (digitalRead(BUTTON) == LOW) {\n    delay(500);  // time to move your hand away\n    drive(200, 200);\n    delay(2000);\n    drive(0, 0);\n  }\n", head="const int BUTTON = 2;\n"),
         check="Nothing moves until you press the button.",
         think="Why is a start button a safety feature on real machines?"),
    dict(title="Add status lights", stage="Add-ons", fig=lambda: f_wire([("Pin 12", "Red LED + (through 220 &#937;)", "--red"), ("Pin 13", "Green LED + (through 220 &#937;)", "--w3"), ("GND", "Both LED &#8722; legs", "--black")], "Connection diagram from Arduino pins 12, 13 and GND to a red LED and a green LED", "On an Uno R4, use 1 k&#937; resistors in place of 220 &#937;."), time="20 minutes",
         goal="Let the robot show what it's doing.",
         need=["Your robot", "Red LED and green LED", "2 resistors: 220 &#937; on an Uno R3, or 1 k&#937; on an R4", "Jumper wires"],
         steps=["Put each LED and its resistor on the breadboard.", "Wire them as the picture shows.", "Upload the sketch below.", "Green should light while the robot drives.", "Red should light while it's stopped."],
         code=m("  pinMode(RED_LED, OUTPUT);\n  pinMode(GREEN_LED, OUTPUT);\n", "  digitalWrite(GREEN_LED, HIGH);\n  digitalWrite(RED_LED, LOW);\n  drive(180, 180);\n  delay(1500);\n\n  digitalWrite(GREEN_LED, LOW);\n  digitalWrite(RED_LED, HIGH);\n  drive(0, 0);\n  delay(1500);\n", head="const int RED_LED = 12, GREEN_LED = 13;\n"),
         check="Green shows when driving, and red shows when stopped.",
         think="What other things could a robot usefully show with just two lights?"),
    dict(title="Add a horn", stage="Add-ons", fig=lambda: f_wire([("Pin 4", "Buzzer module signal", "--w2"), ("5V", "Buzzer module VCC", "--red"), ("GND", "Buzzer module GND", "--black")], "Connection diagram from Arduino pin 4, 5V and GND to an active buzzer module", "Avoid tone() here: it interferes with speed control on pins 3 and 11."), time="15 minutes",
         goal="Make the robot beep before it moves.",
         need=["Your robot", "Active buzzer module with a built-in transistor (it beeps by itself)", "3 jumper wires"],
         steps=["Use a buzzer module, not a bare buzzer. A bare active buzzer often draws 25&#8211;30 mA, which is too much for a pin. With a bare buzzer, use a transistor as in Lab Example 15.", "Check whether your module turns on with HIGH or LOW. Some work the opposite way to this code.", "Wire it as the picture shows.", "Upload the sketch below.", "It should beep twice, then drive.", "Change the beep pattern to something of your own."],
         code=m("  pinMode(BUZZER, OUTPUT);\n", "  beep(150);\n  delay(150);\n  beep(150);\n  delay(300);\n  drive(180, 180);\n  delay(1500);\n  drive(0, 0);\n  delay(3000);\n", "\nvoid beep(int ms) {\n  digitalWrite(BUZZER, HIGH);\n  delay(ms);\n  digitalWrite(BUZZER, LOW);\n}\n", head="const int BUZZER = 4;\n"),
         check="Two beeps come before each drive.",
         think="Why do reversing trucks beep? When should your robot use a warning sound?"),
    dict(title="Mount the distance sensor", stage="Sense", fig=f_sonar_top, time="20 minutes",
         goal="Give the robot eyes, and check its readings before trusting them.",
         need=["Your robot", "HC-SR04 sensor", "4 jumper wires", "Ruler"],
         steps=["Fix the sensor to the front, with its cylinders facing forward.", "Wire it: VCC to 5V, TRIG to pin 7, ECHO to pin 8, GND to GND.", "Upload the sketch below, and leave USB connected.", "Open the Serial Monitor at 9600.", "Hold a book 10, 20 and 50 cm away, and compare the readings with a ruler."],
         code=f"{SONAR_P}{READ}\nvoid setup() {{\n{SETUP_S}  Serial.begin(9600);\n}}\n\nvoid loop() {{\n  Serial.println(readCm());\n  delay(200);\n}}\n",
         check="Each reading is within a couple of centimetres of the ruler.",
         think="Try a cushion, and a book held at an angle. What do you see, and what does it mean for your robot?"),
    dict(title="Stop before a wall", stage="Sense", fig=f_wallstop, time="20 minutes",
         goal="Make the robot react to the world by itself.",
         need=["Your robot with its sensor", "A wall or a large box"],
         steps=["Upload the sketch below.", "Start the robot about 1 metre from a wall, and stay close.", "It should stop about 20 cm from the wall.", "Measure the real stopping distance.", "Try again at a faster speed. Does it stop further along?", "Set a stopping distance that always works."],
         code=s("", "  if (readCm() < 20) {\n    drive(0, 0);\n  } else {\n    drive(170, 170);\n  }\n  delay(60);\n"),
         check="The robot stops before touching the wall, every time.",
         think="Faster robots need a bigger stopping distance. Why?"),
    dict(title="Follow your hand", stage="Sense", fig=f_follow, time="20 minutes",
         goal="Hold a set distance, using three zones.",
         need=["Your robot with its sensor", "Your hand or a book"],
         steps=["Upload the sketch below.", "Hold a book about 20 cm in front of the robot.", "Slowly move it away. The robot should follow.", "Move it close. The robot should back up.", "Change the zone limits and see how the behaviour changes."],
         code=s("", "  float cm = readCm();\n  if (cm < 15) {\n    drive(-150, -150);\n  } else if (cm > 25 && cm < 80) {\n    drive(150, 150);\n  } else {\n    drive(0, 0);\n  }\n  delay(60);\n"),
         check="The robot keeps about 20 cm from the book as you move it.",
         think="Why does this sketch include the limit of 80 cm? What would happen without it?"),
    dict(title="Avoid obstacles", stage="Sense", fig=f_avoid, time="30 minutes",
         goal="Build a robot that can wander by itself.",
         need=["Your robot with its sensor", "Boxes to use as obstacles"],
         steps=["Set up a small course with boxes.", "Upload the sketch below.", "Let it run, and stay near it.", "Note any place where it gets stuck.", "Adjust the reversing and turning times.", "Try narrower gaps once it works."],
         code=s("", "  if (readCm() < 25) {\n    drive(0, 0);\n    delay(200);\n    drive(-170, -170);\n    delay(400);\n    drive(170, -170);\n    delay(350);\n    drive(0, 0);\n    delay(100);\n  } else {\n    drive(170, 170);\n  }\n  delay(60);\n"),
         check="The robot drives around your course for a minute without crashing.",
         think="Where can it still get stuck? The sensor's narrow cone may be part of the reason."),
    dict(title="Give the robot a turning head", stage="Sense", fig=f_head, time="30 minutes",
         goal="Mount the sensor on a servo, so that it can look around.",
         need=["Your robot", "SG90 servo", "470 &#181;F capacitor rated 16 V or higher", "Tape or a small bracket"],
         steps=["Remove the sensor from the chassis.", "Fix the servo at the front of the robot.", "Without power, centre the horn by hand very gently, or use the sketch to set 90&#176;, then fit the horn pointing forward.", "Fix the sensor to the horn. Leave enough slack in the wires for it to turn.", "Wire the servo: brown to battery &#8722;, red to battery +, orange to pin 9.", "Add the capacitor across the battery + and &#8722;, with its stripe on &#8722;.", "Upload the sketch below. The head should look left, ahead and right."],
         code="#include <Servo.h>\nServo head;\n\nvoid setup() {\n  head.attach(9);\n}\n\nvoid loop() {\n  head.write(150);  // left\n  delay(800);\n  head.write(90);   // ahead\n  delay(800);\n  head.write(30);   // right\n  delay(800);\n  head.write(90);\n  delay(800);\n}\n",
         check="The head turns smoothly to all three positions, and its wires don't pull.",
         think="Servo power comes from the batteries, not the Arduino. Why is that safer?"),
    dict(title="Look and choose a direction", stage="Sense", fig=f_choose, time="40 minutes",
         goal="Make a decision based on measurements.",
         need=["Your robot with its turning head", "Boxes to use as walls"],
         steps=["Upload the sketch below.", "Place the robot facing a wall, with more room on one side.", "It should stop, look left, look right, and turn to the clearer side.", "Swap the side with more room, and test again.", "Build a small maze and see how far it gets."],
         code=s("  head.attach(9);\n  head.write(90);\n  delay(500);\n", "  if (readCm() < 25) {\n    drive(0, 0);\n    float leftCm = lookAt(150);\n    float rightCm = lookAt(30);\n    head.write(90);\n    delay(300);\n    if (leftCm > rightCm) {\n      drive(-170, 170);\n    } else {\n      drive(170, -170);\n    }\n    delay(350);\n    drive(0, 0);\n  } else {\n    drive(170, 170);\n  }\n  delay(60);\n",
                "\nfloat lookAt(int angle) {\n  head.write(angle);\n  delay(400);\n  return readCm();\n}\n", head="#include <Servo.h>\nServo head;\n"),
         check="At a wall, the robot chooses the side with more room.",
         think="What should the robot do if both sides are blocked? Add this to your code."),
    dict(title="Fit line sensors", stage="Line", fig=f_line_mount, time="25 minutes",
         goal="Teach the robot to see the floor.",
         need=["Your robot", "2 line sensor modules with digital output (DO)", "Black electrical tape", "White or light floor", "Jumper wires"],
         steps=["Fix a sensor under each front corner, about 1 cm above the floor.", "Wire both: VCC to 5V and GND to GND. Left DO goes to A0, and right DO goes to A1.", "Upload the sketch below, and open the Serial Monitor.", "Hold each sensor over white, then over black tape.", "Write down which reading means black. Many modules read 1 on black, but some are the other way round.", "Turn the module's small screw, if it has one, until the reading changes cleanly."],
         code="const int LEFT_EYE = A0, RIGHT_EYE = A1;\n\nvoid setup() {\n  pinMode(LEFT_EYE, INPUT);\n  pinMode(RIGHT_EYE, INPUT);\n  Serial.begin(9600);\n}\n\nvoid loop() {\n  Serial.print(\"Left: \");\n  Serial.print(digitalRead(LEFT_EYE));\n  Serial.print(\"  Right: \");\n  Serial.println(digitalRead(RIGHT_EYE));\n  delay(200);\n}\n",
         check="Each sensor reads differently on white and on black.",
         think="Why might bright sunlight or a shiny floor confuse these sensors?"),
    dict(title="Follow a line", stage="Line", fig=f_linefollow, time="45 minutes",
         goal="Build the classic line-following robot.",
         need=["Your robot with line sensors", "Black tape, on a white or light floor"],
         steps=["Make a wide oval track with the tape. Avoid sharp corners to begin with.", "If your sensors read 0 on black, change BLACK in the sketch to 0.", "Start with a low speed, so that it has time to react.", "Place the robot over the line, with a sensor on each side.", "Upload the sketch and let it run.", "If it wobbles, reduce the speeds. If it runs off on bends, make the turns sharper."],
         code=m("  pinMode(LEFT_EYE, INPUT);\n  pinMode(RIGHT_EYE, INPUT);\n", "  bool leftBlack = digitalRead(LEFT_EYE) == BLACK;\n  bool rightBlack = digitalRead(RIGHT_EYE) == BLACK;\n\n  if (leftBlack && !rightBlack) {\n    drive(0, 170);    // line is to the left\n  } else if (rightBlack && !leftBlack) {\n    drive(170, 0);    // line is to the right\n  } else {\n    drive(140, 140);  // go straight\n  }\n", head="const int LEFT_EYE = A0, RIGHT_EYE = A1;\nconst int BLACK = 1;\n"),
         check="The robot completes a full lap of your track.",
         think="Why does this sketch have no delay() in its loop? Try adding delay(300) and see what happens."),
    dict(title="Stay inside a ring", stage="Line", fig=f_ring, time="30 minutes",
         goal="Use line sensors to keep the robot inside a boundary.",
         need=["Your robot with line sensors", "Black tape, making a ring about 1 metre across"],
         steps=["Make a ring from tape on the floor.", "Put the robot inside it.", "Upload the sketch below.", "When it reaches the line, it should back up and turn away.", "Tune the reversing time, so that it never crosses the line.", "Add an obstacle in the middle, using what you learned in Exercise 19, as a challenge."],
         code=m("  pinMode(LEFT_EYE, INPUT);\n  pinMode(RIGHT_EYE, INPUT);\n", "  bool leftBlack = digitalRead(LEFT_EYE) == BLACK;\n  bool rightBlack = digitalRead(RIGHT_EYE) == BLACK;\n\n  if (leftBlack || rightBlack) {\n    drive(-170, -170);\n    delay(400);\n    if (leftBlack) {\n      drive(170, -170);  // line on the left, so spin right\n    } else {\n      drive(-170, 170);  // line on the right, so spin left\n    }\n    delay(350);\n  } else {\n    drive(160, 160);\n  }\n", head="const int LEFT_EYE = A0, RIGHT_EYE = A1;\nconst int BLACK = 1;\n"),
         check="The robot stays inside the ring for a full minute.",
         think="How does the robot's speed affect how far it crosses the line before it reacts?"),
    dict(title="Final mission", stage="Line", fig=f_mission, time="1 to 2 hours",
         goal="Combine everything into one complete robot.",
         need=["Your robot with sensor, line sensors, LEDs and start button", "Black tape track", "A box to use as an obstacle"],
         steps=["Fit every add-on and test each one with its earlier exercise.", "Keep the sensor fixed facing forward for this mission.", "Build a track, and put a box on the line partway round.", "Upload the sketch below. If your sensors read 0 on black, change BLACK.", "Press the button. Green lights, and the robot follows the line.", "When it reaches the box, it should stop and show red.", "Lift the box away. The robot should carry on.", "Demonstrate the whole mission to your guide, and celebrate."],
         code=s("  pinMode(LEFT_EYE, INPUT);\n  pinMode(RIGHT_EYE, INPUT);\n  pinMode(BUTTON, INPUT_PULLUP);\n  pinMode(RED_LED, OUTPUT);\n  pinMode(GREEN_LED, OUTPUT);\n  digitalWrite(RED_LED, HIGH);\n  while (digitalRead(BUTTON) == HIGH) {\n    delay(10);\n  }\n  delay(500);\n",
                "  if (readCm() < 15) {\n    drive(0, 0);\n    digitalWrite(GREEN_LED, LOW);\n    digitalWrite(RED_LED, HIGH);\n    delay(100);\n    return;\n  }\n  digitalWrite(RED_LED, LOW);\n  digitalWrite(GREEN_LED, HIGH);\n\n  bool leftBlack = digitalRead(LEFT_EYE) == BLACK;\n  bool rightBlack = digitalRead(RIGHT_EYE) == BLACK;\n  if (leftBlack && !rightBlack) {\n    drive(0, 170);\n  } else if (rightBlack && !leftBlack) {\n    drive(170, 0);\n  } else {\n    drive(140, 140);\n  }\n",
                head="const int LEFT_EYE = A0, RIGHT_EYE = A1, BLACK = 1;\nconst int BUTTON = 2, RED_LED = 12, GREEN_LED = 13;\n"),
         check="The robot starts on your press, follows the line, stops for the box, then carries on.",
         think="You've built sense, think and act into one machine. What would you add next, and which new sensor would it need?"),
]
for i, r in enumerate(R):
    r["n"] = i + 1
