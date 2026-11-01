# Drawings for the sensor pages: a labelled picture and a circuit diagram per sensor.
from figures import t, label, lead, rect, circ, line, ultrasonic, card, sym_text


def plate(body, alt, h=400):
    return (f'<svg class="plate" viewBox="0 0 720 {h}" role="img" aria-label="{alt}"><rect width="720" height="{h}" rx="8" fill="var(--mat)"/>'
            f'<rect width="720" height="{h}" rx="8" fill="url(#matgrid)"/>{body}</svg>')


def path(d, c, w=3, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="var({c})" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def arcs(x, y, n=3, up=False, c="--pt", gap=14, h=16):
    o = ""
    for i in range(n):
        r = i * gap
        o += path(f"M{x + r} {y - h - i * 5} q{10 + i * 3} {h + i * 5} 0 {2 * h + i * 10}", c, 2.5)
    return o


def drop(x, y, s=1.0):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -10 C6 -2 8 2 8 5 A8 8 0 0 1 -8 5 C-8 2 -6 -2 0 -10Z" fill="var(--w3)"/>'


def pins(x, y, labels, step=22, length=30, c="--brass"):
    o = ""
    for i, s in enumerate(labels):
        px = x + i * step
        o += line(px, y, px, y + length, c, 5, "butt")
        o += f'<text transform="translate({px + 4} {y + length + 6}) rotate(90)" font-size="11.5" font-weight="700" fill="var(--lab)">{s}</text>'
    return o


# Output signal shapes shown in the card on each picture.
def wave(kind):
    k = {
        "analog": '<path d="M-84 24 C-50 24 -30 -14 0 -8 S50 22 84 -18"/>' + sym_text(-66, -14, "0&#8211;5 V", 11),
        "digital": '<path d="M-84 22 H-30 V-16 H34 V22 H84"/>' + sym_text(-58, 8, "LOW", 10.5) + sym_text(2, -22, "HIGH", 10.5),
        "pulses": '<path d="M-84 22 H-66 V-14 H-54 V22 H-30 V-14 H-18 V22 H6 V-14 H18 V22 H42 V-14 H54 V22 H84"/>',
        "i2c": '<path d="M-84 -14 H-60 V-24 H-46 V-14 H-30 V-24 H-16 V-14 H6 V-24 H20 V-14 H84" stroke-width="1.75"/><path d="M-84 20 H-70 V8 H-56 V20 H-42 V8 H-28 V20 H-14 V8 H0 V20 H14 V8 H28 V20 H84" stroke-width="1.75"/>' + sym_text(-74, -28, "SDA", 10) + sym_text(-74, 36, "SCL", 10),
        "image": "".join(f'<rect x="{-48 + c * 16}" y="{-26 + r * 16}" width="14" height="14" fill="var(--{["w3", "pt", "led-green", "red", "w2", "silver"][(r * 3 + c * 2) % 6]})" stroke="none"/>' for r in range(4) for c in range(6)),
        "ecg": '<path d="M-84 12 H-60 q6 -10 12 0 H-34 l5 7 l8 -40 l8 46 l5 -13 H6 q10 -14 20 0 H84"/>',
    }[kind]
    return k


def sig(kind, title="Output signal", x=486, y=282, w=214, h=104):
    return card(x, y, w, h, title, wave(kind))


# ---------- pictures: (drawing fn, labels fn, thumbnail crop) ----------
def p_temp():
    o = path("M90 208 v-70 a48 44 0 0 1 96 0 v70 z", "--black-l", 2, "var(--black)")
    o += line(110, 208, 110, 320, "--silver", 6, "butt") + line(138, 208, 138, 320, "--silver", 6, "butt") + line(166, 208, 166, 320, "--silver", 6, "butt")
    o += t(138, 165, "LM35", 18, 800, "middle") + t(138, 186, "flat side", 11.5, 400, "middle", "--lab-soft")
    o += rect(262, 92, 110, 136, "--w3-d", 6, "--blue-d", 2)
    for r in range(6):
        for c in range(5):
            o += rect(274 + c * 18, 104 + r * 19, 12, 13, "--blue-d", 2)
    o += line(292, 228, 292, 310, "--silver", 5, "butt") + line(317, 228, 317, 310, "--silver", 5, "butt") + line(342, 228, 342, 310, "--silver", 5, "butt")
    return o


def l_temp():
    o = t(138, 352, "+Vs", 13, 700, "end") + t(138, 370, "", 11)
    o = t(110, 342, "+Vs", 12.5, 700, "middle") + t(138, 360, "Out", 12.5, 700, "middle") + t(166, 342, "GND", 12.5, 700, "middle")
    o += t(292, 330, "VCC", 11.5, 700, "middle") + t(317, 348, "DATA", 11.5, 700, "middle") + t(342, 330, "GND", 11.5, 700, "middle")
    o += t(138, 74, "LM35: analog", 15, 700, "middle") + t(317, 74, "DHT11: digital", 15, 700, "middle")
    o += label(420, 70, "LM35", ["Voltage rises 10 mV for each 1&#176;C.", "Flat side towards you, legs down:", "+Vs, Out, GND from the left."])
    o += label(420, 170, "DHT11", ["Sends temperature and humidity", "as digital data on one wire."])
    return o + sig("analog", "LM35 output")


def p_hum():
    o = rect(120, 90, 180, 170, "--w3-d", 8, "--blue-d", 2)
    for r in range(8):
        for c in range(7):
            o += rect(136 + c * 22, 106 + r * 18, 16, 12, "--blue-d", 2)
    o += rect(96, 260, 228, 40, "--blue", 4, "--blue-d", 2)
    o += pins(180, 300, ["DATA", "VCC", "GND"], 30)
    for x, y, s in [(70, 110, 1), (345, 90, 1.2), (60, 200, 0.9), (360, 190, 1), (210, 58, 1.1), (290, 62, 0.8)]:
        o += drop(x, y, s)
    return o


def l_hum():
    o = lead([(300, 140), (420, 140)]) + label(428, 112, "Humidity plate", ["Its electrical property changes", "as it soaks up moisture."])
    o += label(428, 206, "Water in the air", ["Reads about 20&#8211;90% relative", "humidity (RH)."])
    return o + sig("digital", "Digital data, one wire")


def p_rain():
    o = rect(40, 80, 190, 150, "--w3-d", 4, "--blue-d", 2)
    for i in range(8):
        y = 92 + i * 17
        o += path(f"M{50 if i % 2 else 66} {y} H{216 if i % 2 else 220}", "--silver", 4)
    o += path("M50 92 V{0}".format(92 + 7 * 17), "--silver", 4) if False else ""
    for x, y, s in [(70, 54, 1), (130, 40, 1.2), (185, 60, 0.9)]:
        o += drop(x, y, s)
    o += rect(70, 280, 130, 60, "--blue", 4, "--blue-d", 2) + rect(92, 292, 36, 26, "--black", 2) + circ(166, 305, 10, "--blue-d", "--silver", 2)
    o += path("M110 230 C100 250 110 262 110 280", "--w1", 3) + path("M160 230 C170 250 160 262 160 280", "--w2", 3)
    # tipping bucket
    o += path("M300 60 H420 L372 120 H348 Z", "--silver", 3, "var(--silver-d)")
    o += path("M322 180 L398 150", "--white", 7) + path("M322 180 V150 M398 150 V120", "--white", 3) + circ(360, 165, 6, "--pt")
    o += rect(322, 210, 76, 60, "--board-d", 4)
    o += t(360, 48, "Tipping bucket", 13.5, 700, "middle")
    return o


def l_rain():
    o = t(135, 262, "", 11) + t(226, 300, "Comparator board", 13, 700)
    o += t(226, 318, "AO, DO, VCC, GND", 11.5, 400, "start", "--lab-soft")
    o += lead([(230, 155), (262, 155)]) + t(268, 150, "Wet", 12.5, 700) + t(268, 166, "tracks", 12.5, 700)
    o += label(452, 70, "Water sensor", ["Water bridges the tracks, so", "more water means less resistance."])
    o += label(452, 160, "Rain gauge", ["Each tip of the bucket is a click,", "commonly 0.2 mm of rain."])
    return o + sig("pulses", "Gauge: one pulse per tip")


def p_soil():
    o = rect(0, 240, 440, 160, "--soil", 0)
    for x, y in [(40, 300), (90, 350), (160, 280), (230, 340), (320, 300), (380, 360)]:
        o += circ(x, y, 6, "--soil-d")
    o += path("M170 60 h90 v210 l-45 70 l-45 -70 z", "--black-l", 2, "var(--black)")
    o += rect(180, 70, 70, 70, "--blue-d", 4) + rect(198, 88, 34, 24, "--black-l", 2)
    o += path("M300 240 C340 120 330 220 300 240 C320 200 355 180 370 160", "--led-green", 5)
    o += pins(190, 40, ["", "", ""], 25, 28) if False else ""
    o += line(180, 30, 180, 60, "--brass", 5, "butt") + line(215, 30, 215, 60, "--brass", 5, "butt") + line(250, 30, 250, 60, "--brass", 5, "butt")
    o += line(150, 150, 280, 150, "--white", 2, "butt")
    return o


def l_soil():
    o = t(180, 22, "GND", 11, 700, "middle") + t(215, 22, "VCC", 11, 700, "middle") + t(250, 22, "AO", 11, 700, "middle")
    o += lead([(280, 150), (450, 150)]) + label(458, 110, "Keep electronics dry", ["Only push it in up to the line.", "The top part isn't waterproof."])
    o += label(458, 200, "Capacitive probe", ["Wetter soil changes the", "capacitance, with no bare metal."])
    return o + sig("analog", "Higher voltage = drier")


def gy521():
    o = rect(90, 110, 220, 150, "--blue", 6, "--blue-d", 2) + rect(166, 150, 68, 68, "--black", 3, "--black-l", 2) + t(200, 188, "MPU", 13, 700, "middle") + t(200, 204, "6050", 13, 700, "middle")
    o += pins(116, 260, ["VCC", "GND", "SCL", "SDA"], 28, 28)
    return o


def p_acc():
    o = path("M200 184 H372", "--red", 4) + path("M200 184 V40", "--led-green", 4) + path("M200 184 L70 80", "--w3", 4)
    o += path("M372 184 l-12 -7 v14 z", "--red", 2, "var(--red)") + path("M200 40 l-7 12 h14 z", "--led-green", 2, "var(--led-green)") + path("M70 80 l14 3 l-8 10 z", "--w3", 2, "var(--w3)")
    return o + gy521()


def l_acc():
    o = t(384, 190, "X", 15, 800) + t(218, 44, "Z", 15, 800) + t(50, 72, "Y", 15, 800)
    o += label(452, 70, "Senses three directions", ["Measures acceleration along X, Y", "and Z, including gravity."])
    o += label(452, 170, "It knows which way is down", ["That's how a phone screen", "turns the right way up."])
    return o + sig("i2c", "I2C data")


def p_gyro():
    o = gy521()
    o += path("M90 70 A130 40 0 0 1 320 72", "--red", 4, extra=' marker-end="url(#r-arrow)"')
    o += path("M350 110 A40 110 0 0 1 350 270", "--led-green", 4, extra=' marker-end="url(#r-arrow)"')
    o += path("M46 260 A36 100 0 0 1 46 110", "--w3", 4, extra=' marker-end="url(#r-arrow)"')
    return o


def l_gyro():
    o = t(205, 92, "Yaw", 14, 700, "middle") + t(398, 195, "Pitch", 14, 700) + t(12, 195, "Roll", 14, 700)
    o += label(452, 60, "Senses rotation", ["Measures how fast it turns,", "in degrees per second."])
    o += label(452, 150, "Often shares a chip", ["The MPU-6050 has both a gyroscope", "and an accelerometer inside."])
    return o + sig("i2c", "I2C data")


def p_ultra():
    return ultrasonic() + rect(412, 96, 16, 152, "--board-d", 2)


def l_ultra():
    o = t(420, 80, "Wall", 13, 700, "middle")
    for i, s in enumerate(["VCC", "TRIG", "ECHO", "GND"]):
        o += f'<text transform="translate({160 + i * 20} 298) rotate(90)" font-size="11.5" font-weight="700" fill="var(--lab)">{s}</text>'
    o += t(36, 372, "Distance = echo time &#215; speed of sound &#247; 2", 13.5, 700)
    o += label(460, 120, "Sound there and back", ["Sends a 40 kHz pulse and times", "the echo. It needs a surface", "that reflects sound."])
    return o + sig("pulses", "ECHO pulse length = distance", 470, 282, 230)


def p_lidar():
    o = rect(40, 250, 210, 80, "--blue-d", 22, "--black-l", 2) + rect(90, 225, 110, 40, "--w3-d", 12) + circ(88, 334, 18, "--black", "--black-l", 3) + circ(205, 334, 18, "--black", "--black-l", 3)
    o += rect(128, 190, 34, 36, "--black", 6, "--silver", 2)
    for i, (x, y) in enumerate([(20, 90), (70, 50), (145, 30), (220, 50), (270, 90), (300, 150), (10, 170)]):
        o += f'<line x1="145" y1="205" x2="{x}" y2="{y}" stroke="var(--pt)" stroke-width="1.5" stroke-dasharray="4 4"/>' + circ(x, y, 3.5, "--pt")
    o += rect(328, 252, 98, 80, "--w2-d", 5, "--black-l", 1.5) + rect(365, 278, 24, 18, "--black", 2)
    o += pins(344, 332, ["", "", "", ""], 20, 16)
    return o


def l_lidar():
    o = t(145, 368, "Spinning lidar on a car", 13.5, 700, "middle") + t(377, 240, "VL53L0X", 13, 700, "middle") + t(377, 370, "Small module", 12.5, 400, "middle", "--lab-soft")
    o += label(452, 60, "Laser time-of-flight", ["Times how long laser pulses", "take to bounce back."])
    o += label(452, 150, "Builds a 3D point map", ["Each dot is one measured", "point in the world."])
    return o + sig("i2c", "Module: I2C data")


def p_radar():
    o = rect(50, 140, 170, 90, "--blue", 5, "--blue-d", 2) + path("M70 165 h40 v40 h40 v-40 h40", "--silver", 3)
    o += pins(70, 230, ["3V3", "GND", "OUT", "VIN", "CDS"], 22, 24)
    for i in range(4):
        o += path(f"M{240 + i * 18} {150 - i * 7} q{14 + i * 3} {35 + i * 7} 0 {70 + i * 14}", "--pt", 3)
    o += circ(385, 112, 16, "--tan") + path("M385 128 V200 M385 150 L350 180 M385 150 L420 175 M385 200 L360 258 M385 200 L412 258", "--tan", 8)
    return o


def l_radar():
    o = t(135, 124, "RCWL-0516", 13.5, 700, "middle")
    o += label(452, 60, "Radio waves, not light", ["Motion changes the frequency", "of the reflected waves."])
    o += label(452, 150, "Senses movement", ["Larger car radars also", "measure speed and distance."])
    return o + sig("digital", "OUT goes HIGH on motion")


def p_ldr():
    o = circ(170, 180, 80, "--ceramic", "--ceramic-d", 3) + path("M118 150 H210 L128 170 H214 L126 190 H214 L130 210 H222", "--black", 5)
    o += line(140, 258, 140, 350, "--silver", 5, "butt") + line(200, 258, 200, 350, "--silver", 5, "butt")
    o += circ(345, 80, 30, "--gold")
    for dx, dy in [(-44, 36), (-58, 12), (-24, 54)]:
        o += path(f"M{345 + dx} {80 + dy} L{345 + dx * 1.7} {80 + dy * 1.7}", "--gold", 3) if False else ""
    for x, y in [(290, 110), (275, 135), (300, 145)]:
        o += path(f"M{x} {y} L{x - 25} {y + 15}", "--gold", 3, extra=' marker-end="url(#r-arrow)"')
    return o


def l_ldr():
    o = label(452, 70, "Light Dependent Resistor", ["More light: lower resistance.", "Less light: higher resistance."])
    o += label(452, 160, "Needs a partner resistor", ["A voltage divider turns", "resistance into a voltage."])
    return o + sig("analog", "Analog voltage")


def p_ir():
    o = rect(50, 150, 210, 90, "--blue-d", 5, "--black-l", 2)
    o += circ(90, 130, 22, "--board", "--silver", 2) + circ(90, 130, 12, "--w3-d") + rect(79, 150, 22, 14, "--silver")
    o += circ(150, 130, 22, "--black", "--black-l", 2) + rect(139, 150, 22, 14, "--silver")
    o += circ(215, 200, 12, "--w3-d", "--silver", 2)
    o += pins(100, 240, ["VCC", "GND", "OUT"], 30, 26)
    o += path("M90 104 C110 40 200 40 320 70", "--red", 3, extra=' stroke-dasharray="8 6" marker-end="url(#r-arrow)"')
    o += path("M340 104 C260 80 200 90 158 104", "--red", 3, extra=' stroke-dasharray="8 6" marker-end="url(#r-arrow)"')
    o += rect(330, 50, 40, 150, "--board-d", 3, "--white", 1)
    return o


def l_ir():
    o = t(350, 40, "Object", 13, 700, "middle") + t(90, 92, "", 10) + t(44, 138, "Sends", 12, 700, "end") + t(180, 134, "Receives", 12, 700)
    o += label(452, 60, "Invisible infrared light", ["The LED sends IR, and the sensor", "looks for the reflection."])
    o += label(452, 150, "Same idea as a TV remote", ["Remotes send coded IR flashes", "to a receiver in the TV."])
    return o + sig("digital", "Usually LOW when blocked")


def p_image():
    o = rect(60, 110, 150, 150, "--blue-d", 6, "--black-l", 2) + circ(135, 185, 52, "--black", "--silver", 4) + circ(135, 185, 28, "--w3-d", "--black-l", 3) + circ(122, 172, 8, "--white")
    for i in range(3):
        o += path(f"M240 {130 + i * 50} L{222} {150 + i * 30}", "--gold", 3, extra=' marker-end="url(#r-arrow)"') if False else ""
    o += path("M212 185 H270", "--pt", 4, extra=' marker-end="url(#r-arrow)"')
    cs = ["--w3", "--pt", "--led-green", "--red", "--w2", "--silver"]
    for r in range(7):
        for c in range(8):
            o += rect(284 + c * 19, 118 + r * 19, 17, 17, cs[(r * 3 + c * 2 + r * c) % 6], 1)
    return o


def l_image():
    o = t(135, 94, "Lens and sensor", 13.5, 700, "middle") + t(360, 100, "Grid of pixels", 13.5, 700, "middle")
    o += t(360, 278, "Each pixel measures light", 12.5, 400, "middle", "--lab-soft")
    o += label(470, 90, "Light becomes numbers", ["Millions of tiny light sensors", "make one digital picture."])
    o += label(470, 180, "CCD and CMOS", ["Two designs. Most phone cameras", "and small modules use CMOS."])
    return o + sig("image", "A picture made of pixels")


def p_geiger():
    o = rect(60, 130, 260, 56, "--silver", 28, "--silver-d", 2) + line(36, 158, 60, 158, "--silver", 5, "butt") + line(320, 158, 348, 158, "--silver", 5, "butt")
    o += line(80, 158, 300, 158, "--pt", 2, "butt")
    o += path("M40 40 L190 160", "--red", 3, extra=' stroke-dasharray="6 5"') + circ(190, 158, 7, "--red")
    o += rect(70, 240, 250, 90, "--blue-d", 5, "--black-l", 2) + rect(95, 262, 60, 34, "--black", 3) + circ(275, 285, 18, "--black", "--silver", 2)
    o += path("M48 158 C20 200 60 240 90 240", "--w1", 3) + path("M340 158 C360 200 320 240 300 240", "--w2", 3)
    return o


def l_geiger():
    o = t(190, 212, "Sealed gas-filled tube", 13.5, 700, "middle") + t(195, 354, "Ready-made counter board", 13, 700, "middle") + t(60, 34, "Particle", 12.5, 700)
    o += label(452, 60, "One particle, one click", ["Radiation ionises the gas, causing", "a tiny pulse of electric current."])
    o += label(452, 150, "High voltage inside", ["An SBM-20 tube runs at about 400 V.", "Use a finished board, with an adult."])
    return o + sig("pulses", "One pulse per detection")


def module_mq(name):
    o = rect(90, 180, 230, 110, "--blue", 5, "--blue-d", 2) + circ(165, 150, 58, "--silver", "--silver-d", 3)
    for r in range(-3, 4):
        for c in range(-3, 4):
            if r * r + c * c <= 11:
                o += circ(165 + c * 13, 150 + r * 13, 3.5, "--silver-d")
    o += circ(280, 205, 13, "--blue-d", "--white", 2) + rect(235, 235, 24, 16, "--red", 2) + rect(270, 235, 24, 16, "--led-green", 2)
    o += pins(130, 290, ["VCC", "GND", "DO", "AO"], 28, 26)
    return o


def p_mq():
    o = module_mq("MQ-2")
    for x, y, r in [(50, 70, 18), (80, 45, 24), (110, 78, 16), (60, 110, 14), (285, 70, 20), (320, 95, 14), (340, 55, 12)]:
        o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--board-d)" fill-opacity=".55"/>'
    return o


def l_mq():
    o = t(165, 76, "", 12) + lead([(223, 150), (430, 150)])
    o += label(452, 60, "Heated sensing layer", ["Gas changes its resistance.", "The metal can gets hot, so don't touch it."])
    o += label(452, 145, "Two outputs", ["AO: how much gas.", "DO: over a level set by the dial."])
    return o + sig("analog", "AO rises with more gas")


def p_ph():
    o = path("M70 180 V330 a12 12 0 0 0 12 12 H240 a12 12 0 0 0 12 -12 V180", "--white", 3, "transparent")
    o += path("M72 240 V330 a10 10 0 0 0 10 10 H240 a10 10 0 0 0 10 -10 V240 Z", "--w3", 0, "var(--w3)", ' fill-opacity=".55"')
    o += rect(145, 60, 34, 220, "--black", 4, "--black-l", 2) + rect(149, 280, 26, 22, "--white", 0) + circ(162, 306, 16, "--white", "--silver", 2)
    o += path("M162 60 C162 20 280 20 310 74", "--black-l", 5)
    o += rect(290, 74, 130, 72, "--blue-d", 5, "--black-l", 2) + rect(300, 88, 26, 26, "--silver", 3) + circ(380, 104, 11, "--blue", "--white", 2)
    cols = ["--red", "--red", "--orange", "--orange", "--gold", "--gold", "--led-yellow", "--led-green", "--led-green", "--w3", "--w3", "--blue", "--blue", "--w2", "--w2"]
    for i, c in enumerate(cols):
        o += rect(278 + i * 11, 252, 11, 26, c)
    return o


def l_ph():
    o = t(278, 296, "0", 11.5, 700, "middle") + t(355, 296, "7", 11.5, 700, "middle") + t(437, 296, "14", 11.5, 700, "middle")
    o += t(290, 242, "Acid", 12, 700, "middle") + t(355, 242, "Neutral", 12, 700, "middle") + t(430, 242, "Alkali", 12, 700, "middle")
    o += t(162, 372, "Glass bulb in the liquid", 12.5, 700, "middle") + t(355, 62, "Amplifier board", 12.5, 700, "middle")
    o += label(470, 90, "A tiny voltage", ["The glass electrode gives a tiny", "voltage, close to 59 mV per pH", "unit at 25&#176;C."])
    return o + sig("analog", "Board: analog voltage", 486, 282)


def p_breath():
    o = module_mq("MQ-3")
    for x, y, r in [(310, 60, 24), (340, 100, 18), (278, 44, 15), (366, 62, 12)]:
        o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="var(--w3)" fill-opacity=".4"/>'
    return o


def l_breath():
    o = t(330, 26, "Breath", 13, 700, "middle")
    o += label(452, 60, "Alcohol changes resistance", ["Hobby testers use a heated layer.", "This one is the MQ-3."])
    o += label(452, 150, "A learning tool only", ["Its reading isn't accurate enough", "to decide whether anyone can drive."])
    return o + sig("analog", "AO rises with more alcohol")


def p_press():
    o = circ(130, 170, 92, "--board", "--silver", 5)
    for a in range(-120, 121, 30):
        import math
        r = math.radians(a - 90)
        o += line(130 + 74 * math.cos(r), 170 + 74 * math.sin(r), 130 + 84 * math.cos(r), 170 + 84 * math.sin(r), "--black", 3, "butt")
    o += line(130, 170, 185, 125, "--red", 4) + circ(130, 170, 7, "--black")
    o += t(130, 228, "kPa", 13, 700, "middle", "--black")
    o += rect(280, 110, 120, 90, "--w2-d", 5, "--black-l", 1.5) + rect(326, 142, 24, 24, "--silver", 2, "--silver-d", 1)
    o += pins(290, 200, ["VCC", "GND", "SCL", "SDA"], 22, 22)
    for x in (300, 338, 376):
        o += path(f"M{x} 54 V90", "--pt", 3, extra=' marker-end="url(#r-arrow)"')
    return o


def l_press():
    o = t(130, 298, "Gauge: the idea", 13.5, 700, "middle") + t(340, 44, "Air pressing down", 12.5, 700, "middle") + t(340, 280, "BMP280", 13.5, 700, "middle")
    o += label(452, 60, "Measures push per area", ["Air pressure falls as you go", "higher, so it can estimate height."])
    o += label(452, 150, "Check the voltage", ["The BMP280 chip is a 3.3 V part.", "Choose a 5 V-ready board for an Uno."])
    return o + sig("i2c", "I2C data")


def p_load():
    o = rect(60, 130, 300, 70, "--silver", 3, "--silver-d", 2) + circ(170, 165, 20, "--mat", "--silver-d", 2) + circ(210, 165, 20, "--mat", "--silver-d", 2) + rect(170, 145, 40, 40, "--mat")
    o += rect(280, 200, 80, 22, "--black", 2) + rect(60, 108, 80, 22, "--black", 2)
    o += rect(280, 60, 80, 44, "--gold", 3, "--brass-d", 2) + t(320, 88, "1 kg", 16, 800, "middle", "--black")
    o += path("M320 104 V128", "--pt", 4, extra=' marker-end="url(#r-arrow)"')
    o += rect(120, 280, 180, 76, "--led-green", 5, "--black-l", 2) + rect(180, 300, 46, 30, "--black", 2) + t(210, 374, "HX711 board", 13, 700, "middle")
    cs = ["--red", "--black", "--white", "--led-green"]
    for i, c in enumerate(cs):
        o += path(f"M{76 + i * 12} 200 C{76 + i * 12} 250 {140 + i * 14} 240 {140 + i * 14} 280", c, 3)
    return o


def l_load():
    o = label(452, 60, "Metal bends a tiny bit", ["Strain gauges glued inside turn", "that bend into a tiny voltage."])
    o += label(452, 150, "HX711 amplifies it", ["Reads the tiny signal and", "sends numbers to the Arduino."])
    return o + sig("pulses", "Clocked digital data")


def p_level():
    o = path("M60 70 V340 a8 8 0 0 0 8 8 H320 a8 8 0 0 0 8 -8 V70", "--white", 4)
    o += rect(63, 170, 262, 175, "--w3-d", 0)
    o += rect(180, 60, 72, 26, "--blue", 3, "--blue-d", 2) + circ(198, 90, 11, "--silver", "--silver-d", 1) + circ(234, 90, 11, "--silver", "--silver-d", 1)
    o += path("M216 104 V160", "--pt", 3, extra=' stroke-dasharray="5 5" marker-end="url(#r-arrow)"')
    o += rect(100, 100, 8, 100, "--silver") + rect(84, 150, 40, 30, "--gold", 12, "--brass-d", 2)
    return o


def l_level():
    o = t(100, 62, "Float", 13, 700, "middle") + t(216, 50, "Ultrasonic", 13, 700, "middle")
    o += label(370, 80, "Float switch", ["Rises with the water and closes a", "switch. Output: on or off."])
    o += label(370, 170, "Non-contact", ["An ultrasonic sensor on the lid", "measures down to the surface."])
    return o + sig("digital", "Float switch output")


def p_flow():
    o = rect(30, 150, 370, 80, "--silver-d", 6, "--black-l", 2) + rect(140, 130, 150, 120, "--black", 10, "--black-l", 2)
    for a in range(6):
        import math
        r = math.radians(a * 60)
        o += line(215, 190, 215 + 44 * math.cos(r), 190 + 44 * math.sin(r), "--w3", 7)
    o += circ(215, 190, 9, "--silver")
    o += path("M46 190 H120", "--w3", 5, extra=' marker-end="url(#r-arrow)"') + path("M310 190 H386", "--w3", 5, extra=' marker-end="url(#r-arrow)"')
    o += path("M190 130 C190 90 140 90 120 60", "--red", 3) + path("M215 130 C215 80 215 70 215 56", "--black", 3) + path("M240 130 C240 90 290 90 310 60", "--led-yellow", 3)
    return o


def l_flow():
    o = t(120, 50, "VCC", 12.5, 700, "middle") + t(215, 46, "GND", 12.5, 700, "middle") + t(310, 50, "Signal", 12.5, 700, "middle") + t(215, 280, "Spinning wheel with a magnet", 13, 700, "middle")
    o += t(215, 298, "A Hall sensor counts each turn.", 12, 400, "middle", "--lab-soft")
    o += label(452, 60, "Faster flow, more pulses", ["Common YF-S201: about 450", "pulses per litre."])
    o += label(452, 150, "Frequency &#8776; 7.5 &#215; L/min", ["Calibrate with a measuring jug.", "Accuracy is only about &#177;10%."])
    return o + sig("pulses", "Pulses from the Hall sensor")


def p_pulse():
    o = path("M60 300 V130 a50 50 0 0 1 100 0 V300 z", "--tan-d", 2, "var(--tan)")
    o += path("M78 120 a32 32 0 0 1 64 0 v16 H78 z", "--board", 2, "transparent")
    o += circ(110, 190, 34, "--black", "--black-l", 3) + circ(110, 190, 10, "--led-green")
    for i in range(3):
        o += path(f"M{200 + i * 14} {130 + i * 8} q10 60 0 {120 - i * 16}", "--led-green", 2.5) if False else ""
    o += path("M145 190 C200 160 200 260 250 250", "--w1", 3)
    o += path("M240 200 H280 q8 -12 16 0 H310 l8 -42 l10 74 l8 -32 H380", "--red", 4)
    return o


def l_pulse():
    o = t(310, 150, "Each beat", 13, 700, "middle") + t(110, 330, "Fingertip on sensor", 12.5, 700, "middle")
    o += label(452, 60, "Green light through skin", ["Blood absorbs light. Each heartbeat", "changes how much comes back."])
    o += label(452, 150, "Stay still", ["Movement and pressure", "spoil the reading."])
    return o + sig("analog", "Analog wave")


def p_ecg():
    o = path("M70 340 C70 180 100 100 170 100 S270 180 270 340 Z", "--tan-d", 2, "var(--tan)") + circ(170, 66, 34, "--tan", "--tan-d", 2)
    for x, y, c in [(118, 170, "--red"), (222, 170, "--w3"), (222, 290, "--led-green")]:
        o += circ(x, y, 12, "--white", c, 4)
    o += path("M118 170 C300 120 310 160 340 190", "--red", 2.5) + path("M222 170 C300 170 320 190 340 200", "--w3", 2.5) + path("M222 290 C300 290 330 240 340 210", "--led-green", 2.5)
    o += rect(340, 170, 90, 90, "--red-d", 5, "--red", 2) + rect(365, 200, 40, 30, "--black", 2)
    return o


def l_ecg():
    o = t(385, 158, "AD8232", 13, 700, "middle") + t(170, 372, "Sticky electrodes", 12.5, 700, "middle")
    o += label(452, 60, "The heart's electricity", ["Measures tiny voltages from", "the heart, through the skin."])
    o += label(452, 150, "Battery power only", ["Keep the laptop off mains charging.", "This is not a medical device."])
    return o + sig("ecg", "ECG wave")


PICS = {
    "temperature": (p_temp, l_temp, "70 60 320 280"), "humidity": (p_hum, l_hum, "40 40 340 300"), "rain": (p_rain, l_rain, "30 30 400 320"), "soil": (p_soil, l_soil, "60 20 330 340"),
    "accelerometer": (p_acc, l_acc, "40 30 350 280"), "gyroscope": (p_gyro, l_gyro, "30 50 350 270"), "ultrasonic": (p_ultra, l_ultra, "20 80 420 220"), "lidar": (p_lidar, l_lidar, "0 20 440 340"), "radar": (p_radar, l_radar, "40 90 390 190"),
    "ldr": (p_ldr, l_ldr, "80 40 300 310"), "ir": (p_ir, l_ir, "40 40 340 240"), "image": (p_image, l_image, "50 100 400 170"), "geiger": (p_geiger, l_geiger, "20 30 350 300"),
    "gas": (p_mq, l_mq, "30 30 320 290"), "ph": (p_ph, l_ph, "60 20 390 330"), "breath": (p_breath, l_breath, "90 30 290 290"),
    "pressure": (p_press, l_press, "30 40 380 200"), "load": (p_load, l_load, "50 50 320 310"), "level": (p_level, l_level, "50 50 290 300"), "flow": (p_flow, l_flow, "20 40 390 220"),
    "pulse": (p_pulse, l_pulse, "50 70 340 240"), "ecg": (p_ecg, l_ecg, "60 30 380 320"),
}


def picture(slug, alt):
    p, l, _ = PICS[slug]
    return plate(p() + l(), alt)


def thumb(slug):
    p, _, box = PICS[slug]
    x, y, w, h = [float(v) for v in box.split()]
    tw = max(w, h * 1.5) * 1.1
    th = tw / 1.5
    vx, vy = x + w / 2 - tw / 2, y + h / 2 - th / 2
    return (f'<svg class="thumb" viewBox="{vx:.1f} {vy:.1f} {tw:.1f} {th:.1f}" aria-hidden="true"><rect x="{vx:.1f}" y="{vy:.1f}" width="{tw:.1f}" height="{th:.1f}" fill="var(--mat)"/>'
            f'<rect x="{vx:.1f}" y="{vy:.1f}" width="{tw:.1f}" height="{th:.1f}" fill="url(#matgrid)"/>{p()}</svg>')


# ---------- circuit diagrams ----------
WIRE = {"5V": "--red", "3.3V": "--w1", "GND": "--black"}


def zig(x, y, name):
    return (f'<path d="M{x - 22} {y} l4 -9 l8 18 l8 -18 l8 18 l8 -18 l8 18 l4 -9" fill="var(--mat)" stroke="var(--pt)" stroke-width="2.5"/>'
            + t(x, y - 14, name, 12, 700, "middle", "--pt"))


def vzig(x, y1, y2, name):
    m = (y1 + y2) / 2
    return (line(x, y1, x, m - 22, "--pt", 2.5, "butt") + line(x, m + 22, x, y2, "--pt", 2.5, "butt")
            + f'<path d="M{x} {m - 22} l-9 4 l18 8 l-18 8 l18 8 l-18 8 l9 4" fill="none" stroke="var(--pt)" stroke-width="2.5"/>' + t(x + 14, m + 4, name, 12, 700, "start", "--pt"))


def wire_col(a, i):
    if a in WIRE:
        return WIRE[a]
    return f"--w{(i % 5) + 1}"


def circuit(sensor, rows, note=None, pull=None, alt=None, sensor_sub=None):
    """Uno on the left, sensor on the right. rows: (Uno pin, sensor pin[, inline resistor]). pull: (from row, to row, value)."""
    y0, step = 84, 44
    n = len(rows)
    h = max(280, y0 + n * step + (54 if note else 24))
    o = t(24, 24, "Circuit diagram", 15, 700)
    o += rect(30, 56, 150, n * step + 14, "--teal", 8, "--teal-d", 2) + t(105, 48, "Arduino Uno", 14, 700, "middle")
    o += rect(500, 56, 190, n * step + 14, "--card", 8) + t(595, 48, sensor, 14, 700, "middle")
    for i, r in enumerate(rows):
        a, b = r[0], r[1]
        y = y0 + i * step
        c = wire_col(a, i)
        o += f'<path d="M180 {y} H500" fill="none" stroke="var(--wire-halo)" stroke-width="6"/><path d="M180 {y} H500" fill="none" stroke="var({c})" stroke-width="4"/>'
        o += circ(180, y, 5, "--silver") + circ(500, y, 5, "--silver-d")
        o += t(168, y + 5, a, 14, 700, "end", "--white") + t(514, y + 5, b, 14, 700, "start", "--card-ink")
        if len(r) > 2 and r[2]:
            o += zig(340, y, r[2])
    if pull:
        a, b, val = pull
        ya, yb = y0 + a * step, y0 + b * step
        o += vzig(420, ya, yb, val) + circ(420, ya, 4, "--pt") + circ(420, yb, 4, "--pt")
    if note:
        o += t(30, h - 16, note, 13, 400, "start", "--lab-soft")
    return plate(o, alt or f"Circuit diagram connecting {sensor} to an Arduino Uno", h)


def divider(top, bot, node="A0", note=None, alt=None):
    """A voltage divider: 5V, sensor, measuring point, resistor, GND."""
    h = 340
    o = t(24, 24, "Circuit diagram: voltage divider", 15, 700)
    o += rect(30, 56, 150, 250, "--teal", 8, "--teal-d", 2) + t(105, 48, "Arduino Uno", 14, 700, "middle")
    ys = {"5V": 84, node: 180, "GND": 276}
    for k, y in ys.items():
        o += circ(180, y, 5, "--silver") + t(168, y + 5, k, 14, 700, "end", "--white")
    o += path(f"M180 84 H420", "--red", 4) + path(f"M180 276 H420", "--black", 4) + path(f"M180 180 H420", "--w1", 4) + circ(420, 180, 6, "--pt")
    o += line(420, 84, 420, 108, "--red", 4, "butt") + line(420, 156, 420, 204, "--w1", 4, "butt") + line(420, 252, 420, 276, "--black", 4, "butt")
    o += rect(392, 108, 56, 48, "--ceramic", 6, "--ceramic-d", 2) + t(456, 137, top, 14, 700)
    o += f'<path d="M420 204 l-12 4 l24 8 l-24 8 l24 8 l-24 8 l12 4" fill="var(--mat)" stroke="var(--pt)" stroke-width="2.5"/>' + t(442, 232, bot, 14, 700, "start", "--pt")
    o += t(300, 170, "Voltage measured here", 12.5, 700, "middle", "--lab-soft")
    if note:
        o += t(30, h - 12, note, 13, 400, "start", "--lab-soft")
    return plate(o, alt or f"Voltage divider circuit with {top} and {bot} connected to Arduino {node}", h)


def chain(first, middle, last, left, right, note=None, alt=None):
    """Arduino, module, then the sensing part."""
    y0, step = 84, 42
    n = max(len(left), len(right))
    h = max(270, y0 + n * step + (52 if note else 22))
    bh = n * step + 14
    o = t(24, 24, "Circuit diagram", 15, 700)
    o += rect(24, 56, 120, bh, "--teal", 8, "--teal-d", 2) + t(84, 48, first, 13.5, 700, "middle")
    o += rect(300, 56, 130, bh, "--card", 8) + t(365, 48, middle, 13.5, 700, "middle")
    o += rect(575, 56, 120, bh, "--card", 8) + t(635, 48, last, 13.5, 700, "middle")
    for i, (a, b) in enumerate(left):
        y = y0 + i * step
        c = wire_col(a, i)
        o += f'<path d="M144 {y} H300" stroke="var({c})" stroke-width="4" fill="none"/>' + circ(144, y, 4.5, "--silver") + circ(300, y, 4.5, "--silver-d") + t(134, y + 5, a, 13, 700, "end", "--white") + t(310, y + 5, b, 12.5, 700, "start", "--card-ink")
    for i, (a, b, c) in enumerate(right):
        y = y0 + i * step
        o += f'<path d="M430 {y} H575" stroke="var({c})" stroke-width="4" fill="none"/>' + circ(430, y, 4.5, "--silver-d") + circ(575, y, 4.5, "--silver-d") + t(420, y + 5, a, 12.5, 700, "end", "--card-ink") + t(585, y + 5, b, 12.5, 700, "start", "--card-ink")
    if note:
        o += t(24, h - 14, note, 12.5, 400, "start", "--lab-soft")
    return plate(o, alt or f"Circuit diagram connecting {last}, {middle} and {first}", h)
