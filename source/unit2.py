# Unit II: more core parts. Same page pattern as Unit I, with its own drawings.
import figures
from figures import t, label, lead, rect, circ, line, card, sym_text


def path(d, c, w=3, fill="none"):
    return f'<path d="{d}" fill="{fill}" stroke="var({c})" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def p_button():
    o = line(120, 270, 120, 350, "--silver", 7, "butt") + line(280, 270, 280, 350, "--silver", 7, "butt") + line(120, 100, 120, 60, "--silver", 7, "butt") + line(280, 100, 280, 60, "--silver", 7, "butt")
    o += rect(90, 90, 220, 190, "--black", 8, "--black-l", 2) + circ(200, 185, 62, "--silver-d", "--silver", 3) + circ(200, 185, 44, "--silver", "--silver-d", 2)
    return o


def f_button():
    o = p_button()
    o += lead([(120, 76), (66, 76), (66, 330), (113, 330)]) + t(12, 210, "Joined", 12.5, 700) + t(12, 226, "pair", 12.5, 700)
    o += lead([(280, 76), (340, 76), (340, 330), (287, 330)]) + t(350, 216, "Joined pair", 12.5, 700)
    o += label(452, 60, "Pressing joins the two pairs", ["Each pair of legs is always joined.", "A press connects the two pairs."])
    o += label(452, 150, "Use diagonal legs", ["Across the centre gap, opposite corners", "stay apart until you press. Always."])
    return o + card(486, 270, 214, 116, "Circuit symbol", '<path d="M-78 12 H-30 M30 12 H78 M-30 12 L24 -10"/><circle cx="-30" cy="12" r="3.5" fill="var(--card-ink)"/><circle cx="30" cy="12" r="3.5" fill="var(--card-ink)"/>')


def p_pot():
    o = line(130, 280, 130, 360, "--silver", 7, "butt") + line(200, 280, 200, 360, "--silver", 7, "butt") + line(270, 280, 270, 360, "--silver", 7, "butt")
    o += rect(90, 90, 220, 190, "--blue", 8, "--blue-d", 2) + circ(200, 180, 72, "--board", "--board-d", 3) + rect(194, 112, 12, 56, "--black", 3)
    o += path("M118 240 A100 100 0 1 1 282 240", "--pt", 3)
    return o


def f_pot():
    o = p_pot() + t(130, 384, "Left", 12.5, 700, "middle") + t(200, 384, "Wiper", 12.5, 700, "middle") + t(270, 384, "Right", 12.5, 700, "middle")
    o += label(420, 60, "A dial made from a resistor", ["The wiper slides along a resistive track.", "Turning it changes the split between", "left-to-wiper and wiper-to-right."])
    o += label(420, 160, "Wiring", ["Outer legs to 5V and GND,", "and the middle leg to an analog pin."])
    return o + card(486, 270, 214, 116, "Circuit symbol", '<path d="M-78 16 H-36 l5 -12 l10 24 l10 -24 l10 24 l10 -24 l10 24 l5 -12 H78 M0 -28 V-6"/><path d="M-6 -14 L0 -4 L6 -14 Z" fill="var(--card-ink)"/>')


def p_buzzer():
    o = line(120, 240, 120, 320, "--silver", 5, "butt") + line(170, 240, 170, 300, "--silver", 5, "butt") + circ(145, 180, 72, "--black", "--black-l", 2) + circ(145, 180, 13, "--silver-d") + t(100, 146, "+", 24, 800, "middle")
    o += path("M232 130 q22 50 0 100", "--pt") + path("M254 116 q30 64 0 128", "--pt")
    o += line(345, 200, 345, 290, "--silver", 4, "butt") + line(385, 200, 385, 290, "--silver", 4, "butt") + circ(365, 160, 46, "--brass", "--brass-d", 2) + circ(365, 160, 22, "--silver")
    return o


def f_buzzer():
    o = p_buzzer() + t(145, 356, "Active buzzer", 14, 700, "middle") + t(145, 374, "Fixed tone, on or off", 12, 400, "middle", "--lab-soft") + t(365, 330, "Passive piezo", 14, 700, "middle") + t(365, 348, "Needs tone() code", 12, 400, "middle", "--lab-soft")
    o += label(470, 60, "Active: its own tone", ["Give it power and it sounds.", "Often 25&#8211;30 mA, so it needs a", "transistor or a buzzer module."])
    o += label(470, 160, "Passive: choose the pitch", ["A signal from tone() makes the", "pitch. Check the + mark on either."])
    return o + card(486, 270, 214, 116, "Circuit symbol", '<path d="M-78 14 H-20 M20 14 H78 M-20 14 V-12 A20 20 0 0 1 20 -12 V14 Z"/>')


def p_diode():
    o = line(30, 170, 110, 170, "--silver", 7, "butt") + line(310, 170, 400, 170, "--silver", 7, "butt") + rect(110, 130, 200, 80, "--black", 8, "--black-l", 2) + rect(262, 130, 28, 80, "--silver") + t(190, 178, "1N4001", 17, 700, "middle")
    return o


def f_diode():
    o = p_diode()
    o += path("M60 250 H360", "--pt", 4) + '<path d="M360 240 L380 250 L360 260 Z" fill="var(--pt)"/>' + t(150, 276, "Current flows this way", 13.5, 700, "middle")
    o += path("M360 90 H60", "--red", 4) + '<path d="M60 80 L40 90 L60 100 Z" fill="var(--red)"/>' + t(210, 78, "Blocked this way", 13.5, 700, "middle")
    o += lead([(276, 210), (276, 330)]) + label(150, 350, "Silver band: the cathode (&#8722; side)")
    o += label(452, 150, "A one-way valve", ["It lets current through one way,", "and blocks it the other way."])
    return o + card(486, 270, 214, 116, "Circuit symbol", '<path d="M-78 12 H-18 M18 12 H78 M18 -14 V38"/><path d="M-18 -14 V38 L18 12 Z"/>')


def p_driver():
    o = rect(70, 70, 330, 230, "--red-d", 8, "--red", 2)
    for x in (90, 290):
        o += rect(x, 82, 90, 50, "--blue", 4, "--blue-d", 2) + circ(x + 24, 107, 11, "--silver", "--silver-d", 2) + circ(x + 66, 107, 11, "--silver", "--silver-d", 2)
    o += rect(130, 165, 52, 62, "--black", 3) + rect(288, 165, 52, 62, "--black", 3)
    for i in range(6):
        o += line(125 + i * 44, 300, 125 + i * 44, 335, "--brass", 6, "butt")
    return o


def f_driver():
    o = p_driver() + t(135, 62, "Motor B", 13, 700, "middle") + t(335, 62, "Motor A", 13, 700, "middle")
    for i, s in enumerate(["B-IA", "B-IB", "GND", "VCC", "A-IA", "A-IB"]):
        o += f'<text transform="translate({121 + i * 44} 344) rotate(90)" font-size="12" font-weight="700" fill="var(--lab)">{s}</text>'
    o += t(14, 395, "Some boards print 1A in place of IA.", 12, 400, "start", "--lab-soft")
    o += label(420, 330, "Two small chips", ["One for each motor."]) if False else ""
    tbl = sym_text(-60, -24, "IA", 12) + sym_text(-14, -24, "IB", 12) + sym_text(44, -24, "Motor", 12)
    for i, (a, b, c) in enumerate([("HIGH", "LOW", "Forward"), ("LOW", "HIGH", "Backward"), ("LOW", "LOW", "Stop")]):
        y = -6 + i * 18
        tbl += sym_text(-60, y, a, 11.5) + sym_text(-14, y, b, 11.5) + sym_text(44, y, c, 11.5)
    return o + card(486, 90, 214, 130, "Control table", tbl) + label(486, 260, "Low-power signals", ["Pins signal the driver, and", "the battery powers the motors."])


def p_relay():
    o = rect(60, 80, 220, 190, "--blue-d", 6, "--black-l", 2) + t(170, 170, "RELAY", 22, 800, "middle", "--white") + t(170, 196, "5 V coil", 13, 400, "middle", "--lab-soft")
    o += rect(280, 110, 70, 130, "--blue", 4, "--blue-d", 2)
    for y in (135, 175, 215):
        o += circ(315, y, 11, "--silver", "--silver-d", 2)
    for i in range(3):
        o += line(110 + i * 58, 270, 110 + i * 58, 305, "--brass", 6, "butt")
    return o


def f_relay():
    o = p_relay()
    for i, s in enumerate(["VCC", "GND", "IN"]):
        o += t(110 + i * 58, 326, s, 12.5, 700, "middle")
    for y, s in ((139, "NO"), (179, "COM"), (219, "NC")):
        o += t(360, y, s, 12.5, 700)
    o += label(452, 60, "A switch moved by a magnet", ["A small current through the coil", "pulls a metal contact across."])
    o += label(452, 150, "Low voltage only here", ["The contacts may be rated for mains.", "This notebook never uses mains."])
    return o + card(486, 270, 214, 116, "Circuit symbol", '<rect x="-74" y="-16" width="44" height="40" /><path d="M-74 -16 L-30 24 M20 28 V10 L58 -14 M62 28 V4"/>')


def p_reg():
    o = rect(100, 50, 150, 80, "--silver", 4, "--silver-d", 2) + circ(175, 88, 18, "--mat", "--silver-d", 2) + rect(90, 130, 170, 110, "--black", 4, "--black-l", 2) + t(175, 192, "LM7805", 20, 700, "middle")
    for x in (125, 175, 225):
        o += line(x, 240, x, 340, "--silver", 8, "butt")
    return o


def f_reg():
    o = p_reg() + t(125, 362, "IN", 13, 700, "middle") + t(175, 362, "GND", 13, 700, "middle") + t(225, 362, "OUT", 13, 700, "middle")
    o += lead([(250, 90), (290, 90)]) + t(296, 88, "Metal tab", 13, 700) + t(296, 104, "Gets hot. Joined to GND.", 12, 400, "start", "--lab-soft")
    o += label(452, 150, "Steady 5 V out", ["Turns a higher, changing voltage", "into a steady 5 V. Extra voltage", "becomes heat."])
    return o + card(486, 270, 214, 116, "Circuit symbol", '<rect x="-36" y="-22" width="72" height="48"/><path d="M-78 -2 H-36 M36 -2 H78 M0 26 V44"/>' + sym_text(0, 3, "7805", 14))


def p_batt():
    o = rect(40, 80, 270, 170, "--black", 6, "--black-l", 2)
    for i in range(4):
        o += rect(52 + i * 63, 92, 56, 146, "--gold", 4, "--brass-d", 2) + t(80 + i * 63, 172, "1.5 V", 13, 800, "middle", "--black")
    o += path("M90 250 C90 300 70 320 70 360", "--red", 5) + path("M260 250 C260 300 280 320 280 360", "--black-l", 5)
    o += rect(350, 110, 72, 120, "--silver-d", 6, "--black-l", 2) + t(386, 176, "9 V", 18, 800, "middle", "--black")
    return o


def f_batt():
    o = p_batt() + t(175, 62, "4 &#215; AA in series = about 6 V", 14, 700, "middle") + t(386, 92, "Weak for motors", 12, 400, "middle", "--lab-soft")
    o += t(70, 382, "+", 16, 800, "middle") + t(280, 382, "&#8722;", 16, 800, "middle")
    o += label(452, 150, "Voltage and capacity", ["Volts: how hard it pushes.", "mAh: how long it can last."])
    return o + card(486, 270, 214, 116, "Circuit symbol", '<path d="M-78 8 H-20 M-20 -16 V32 M-6 -6 V22 M8 -16 V32 M22 -6 V22 M22 8 H78"/>')


figures.FIGS.update({
    "button": (f_button, p_button, "50 50 300 310", "A square tactile push button with four legs, showing which legs are joined"),
    "pot": (f_pot, p_pot, "80 80 240 290", "A potentiometer with a dial and three legs labelled left, wiper and right"),
    "buzzer": (f_buzzer, p_buzzer, "60 100 370 230", "An active buzzer and a passive piezo buzzer side by side"),
    "diode": (f_diode, p_diode, "20 120 390 100", "A 1N4001 diode with its silver band, showing current passing one way only"),
    "driver": (f_driver, p_driver, "60 60 350 285", "An L9110S motor driver board with two motor terminals and six pins"),
    "relay": (f_relay, p_relay, "50 70 310 245", "A relay module with VCC, GND and IN pins, and COM, NO and NC terminals"),
    "regulator": (f_reg, p_reg, "80 40 190 310", "An LM7805 voltage regulator with its metal tab and IN, GND and OUT legs"),
    "power": (f_batt, p_batt, "30 70 400 300", "A four-cell AA battery holder and a nine volt battery"),
})

UNIT2 = [
    dict(slug="button", title="Push Button", short="Push Button", blurb="Lets a person give an input.", overview="A push button connects two points while you hold it down. It's the simplest way for a person to talk to a circuit, and it's how you'll start a robot or trigger a light.",
         look="A small square, usually black, with a round cap and four legs. Its symbol is a gap with a small lever across it.", purpose="It makes or breaks a connection. Released, the two sides are apart. Pressed, they're joined.",
         props=[("Rating", "Omron B3F: 1&#8211;50 mA, 3&#8211;24 V", "For small signals only, not motors."), ("Legs", "4, in 2 joined pairs", "The legs 6.5 mm apart are always joined. They span the breadboard's gap."), ("Action", "On only while held", "A press-and-hold type, not a latching one."), ("Reading", "Needs a pull-up or pull-down", "With INPUT_PULLUP, pressed reads LOW.")],
         everyday="Keyboards, TV remotes, game controllers, doorbells and lift panels.", robot="A start button stops your robot from driving off as soon as it powers up. You can also use one as a bump sensor on the front.",
         safety=["Place it across the breadboard's centre gap, and connect to diagonally opposite legs. Those stay apart until you press, whichever way it's turned.", "Don't switch motors or heavy loads through it. Use it as a signal.", "Never leave an input pin floating. Use INPUT_PULLUP, or a 10 k&#937; resistor to GND or 5V."],
         terms=[("Pull-up", "A resistor that holds an input HIGH until something pulls it LOW."), ("Floating pin", "An input connected to nothing, which reads random values."), ("Contact bounce", "A contact's tiny rapid flickers just after it's pressed or released."), ("Debounce", "Waiting briefly, so that one press counts only once.")],
         exam=["A button joins two points while it's held.", "Two pairs of legs are always joined inside.", "Inputs need a pull-up or pull-down, so that they don't float.", "With INPUT_PULLUP, a pressed button reads LOW."],
         practice=[("Why does a pressed button read LOW with INPUT_PULLUP?", "Short answer", "The pull-up holds the pin HIGH. Pressing joins the pin to GND, which pulls it LOW."), ("One press counts as three. What's happening, and how can you fix it?", "Applied", "Contact bounce. Add a short delay after detecting a press, or only accept a change that lasts."), ("Your button reads pressed all the time. What should you check?", "Applied", "You may have wired to two legs of the same joined pair. Use diagonally opposite legs instead.")],
         k2=["<strong>Explain</strong> what a floating pin is.", "<strong>Describe</strong> which legs of a button are joined, and why diagonal legs are safe to use."], k3=["<strong>Wire</strong> a button so that pin 2 reads LOW when it's pressed.", "<strong>Program</strong> a button to toggle an LED."], k4=["<strong>Compare</strong> INPUT_PULLUP with an external pull-down resistor."],
         links=[("ex-8", "Button lights an LED"), ("ex-9", "Button toggles an LED"), ("robot-13", "Add a start button to your robot")], refs=[("Omron B3F data sheet", "https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3f.pdf", "Maker's data sheet")]),
    dict(slug="pot", title="Potentiometer (Dial)", short="Potentiometer", blurb="A dial that gives an adjustable voltage.", overview="A potentiometer is a resistor with a sliding contact. Turning its knob moves that contact along a track, so the middle leg can give any voltage between its two outer legs.",
         look="A small body with a knob and three legs. Its symbol is a resistor with an arrow pointing at it.", purpose="It lets a person set a value, such as volume, brightness or speed.",
         props=[("Resistance", "Common: 10 k&#937;", "The total across the outer legs. It doesn't change."), ("Legs", "3: outer, wiper, outer", "The middle leg is the output."), ("Taper", "Linear (B) or audio (A)", "Use linear for projects like these."), ("Reading", "0&#8211;1023 on an Uno", "From 0 V to 5 V at the wiper.")],
         everyday="Volume knobs, fan speed dials, light dimmers on low-voltage lamps, and joysticks.", robot="Use one as a speed control or a steering dial. It's also handy for adjusting a sensor's limit without changing the code.",
         safety=["The outer legs go to 5V and GND, and the middle leg goes to the analog pin.", "Never connect the wiper directly to 5V or GND. At one end of its travel, that can make a short circuit through the track.", "Don't force the knob beyond its stops."],
         terms=[("Wiper", "The sliding contact, usually the middle leg."), ("Voltage divider", "Two resistances in series that give a voltage between their ends."), ("Analog input", "A pin that can read a range of voltages."), ("map()", "An Arduino function that rescales a number from one range to another.")],
         exam=["A potentiometer is an adjustable voltage divider.", "Outer legs go to 5V and GND, with the wiper as the output.", "An Uno reads it as 0 to 1023.", "Use map() to convert it to a useful range."],
         practice=[("A dial reads 512 on A0. About what voltage is that?", "Applied", "512 &#247; 1023 &#215; 5 V is about 2.5 V."), ("Turning the dial right lowers the reading. How do you reverse it?", "Applied", "Swap the two outer wires, or use map(reading, 0, 1023, 255, 0) in code."), ("Why doesn't the total resistance change as you turn it?", "Short answer", "The whole track stays between the outer legs. Only the wiper's position along it changes.")],
         k2=["<strong>Explain</strong> how the middle leg gets its voltage."], k3=["<strong>Convert</strong> a dial reading to a percentage.", "<strong>Use</strong> a dial to set a servo's angle."], k4=["<strong>Compare</strong> a dial with two buttons for setting a robot's speed."],
         links=[("ex-10", "Read a dial on the Serial Monitor"), ("ex-11", "A dial controls LED brightness"), ("ex-18", "A dial sets motor speed"), ("ex-21", "A dial steers a servo")], refs=[]),
    dict(slug="buzzer", title="Buzzer", short="Buzzer", blurb="Makes beeps and simple tunes.", overview="A buzzer turns electricity into sound. An active buzzer beeps by itself when powered. A passive one needs a signal from the Arduino, so it can play different notes.",
         look="A small black or metal disc with two legs, often with a + mark. Its symbol looks like a small dome.", purpose="It gets attention, and it gives feedback when a person isn't looking.",
         props=[("Active type", "5 V, often 25&#8211;30 mA", "Over the Uno R3's 20 mA guideline, so use a transistor or module."), ("Active pitch", "Fixed, often about 2.4 kHz", "On or off only."), ("Passive type", "Pitch set by tone()", "Piezo discs draw little current. Check your part."), ("Polarity", "Often marked +", "Follow the mark.")],
         everyday="Microwaves, smoke alarms, reversing trucks, washing machines and digital watches.", robot="A beep warns people before the robot moves. A rising tone can also show how close a wall is.",
         safety=["Don't run an active buzzer straight from a pin. Use a buzzer module, or a transistor with a 1 k&#937; base resistor.", "On an Uno, tone() interferes with PWM on pins 3 and 11. Plan for this if your motors use those pins.", "Keep loud buzzers away from ears, and stop if anyone finds the sound uncomfortable."],
         terms=[("Active buzzer", "A buzzer with its own circuit, which sounds when powered."), ("Passive buzzer", "A buzzer that needs a changing signal to make sound."), ("Frequency", "How many vibrations happen each second, measured in hertz (Hz)."), ("tone()", "An Arduino function that makes a note on a pin.")],
         exam=["An active buzzer has one fixed tone, and a passive one plays notes.", "Active buzzers can draw more current than a pin should supply.", "Higher frequency means higher pitch.", "tone() affects PWM on pins 3 and 11 on an Uno."],
         practice=[("You connect a buzzer to 5V and hear only a click. Which type is it?", "Applied", "Probably passive. It needs a changing signal, so use tone()."), ("Why not wire an active buzzer straight to pin 4?", "Short answer", "Many draw 25&#8211;30 mA, which is above the 20 mA guideline on an Uno R3, and far above an R4's 8 mA limit."), ("Why does A4 (440 Hz) sound lower than A5 (880 Hz)?", "Short answer", "Fewer vibrations each second means a lower pitch. Doubling the frequency raises the note by an octave.")],
         k2=["<strong>Explain</strong> the difference between active and passive buzzers."], k3=["<strong>Program</strong> a three-note tune.", "<strong>Wire</strong> an active buzzer through a transistor."], k4=["<strong>Analyze</strong> how tone() could affect a robot's motors."],
         links=[("ex-13", "Play notes on a buzzer"), ("ex-23", "Parking sensor"), ("robot-15", "Add a horn to your robot")], refs=[("Arduino tone() reference", "https://arduinogetstarted.com/reference/tone", "Brand documentation"), ("TMB12A05 active buzzer listing", "https://www.electrokit.com/en/active-piezo-buzzer-95db-5vdc-pcb-12x9.5mm", "Community or seller notes")]),
    dict(slug="diode", title="Diode", short="Diode", blurb="A one-way valve for current.", overview="A diode lets current flow in one direction and blocks it in the other. It protects circuits from reversed batteries and from the voltage spike a motor makes when it switches off.",
         look="A small black cylinder with a silver band at one end. Its symbol is a triangle pointing at a bar.", purpose="It controls direction. In the water model, it's a one-way valve.",
         props=[("Reverse voltage", "1N4001: up to 50 V", "The most it can block."), ("Forward current", "1N4001: 1 A average", "The most it can carry steadily."), ("Voltage drop", "Up to 1.1 V at 1 A", "It uses a little voltage while conducting."), ("Polarity", "Band marks the cathode", "Current flows towards the band.")],
         everyday="Phone chargers, power supplies and battery protection circuits. An LED is also a diode.", robot="A flyback diode across a motor absorbs its switch-off spike, which protects the transistor. It's in Lab Example 16.",
         safety=["Check the band. A flyback diode goes in reverse: its band faces the battery +.", "A backwards flyback diode makes a short circuit when the transistor turns on.", "Stay within its current rating. A hot diode means something is wrong."],
         terms=[("Anode", "The side current flows into."), ("Cathode", "The side current flows out of, marked with a band."), ("Forward voltage", "The voltage a diode uses while conducting."), ("Flyback diode", "A diode across a motor or coil that safely absorbs its switch-off spike.")],
         exam=["A diode passes current one way only.", "The band marks the cathode.", "A 1N4001 is rated for 50 V and 1 A.", "A flyback diode is placed in reverse across a motor."],
         practice=[("Why does a motor make a voltage spike when it turns off?", "Short answer", "A coil resists sudden changes in current, so its stored energy pushes back as a high voltage."), ("A 6 V supply feeds a load through a 1N4001 at 1 A. About how much voltage reaches the load?", "Applied", "About 5 V, because the diode can use up to 1.1 V."), ("Why does a flyback diode do nothing during normal running?", "Applied", "It's reversed against the battery, so it blocks. It only conducts when the switch-off spike reverses the voltage.")],
         k2=["<strong>Explain</strong> how a diode protects a transistor."], k3=["<strong>Place</strong> a flyback diode correctly across a motor."], k4=["<strong>Analyze</strong> what happens if a flyback diode is reversed."],
         links=[("ex-16", "Transistor runs a DC motor")], refs=[("onsemi 1N4001 data sheet", "https://www.onsemi.com/pdf/datasheet/1n4001-d.pdf", "Maker's data sheet")]),
    dict(slug="driver", title="Motor Driver (L9110S)", short="Motor Driver", blurb="Lets small signals run big motors.", overview="A motor driver lets the Arduino's weak signals control motors in both directions. The L9110S board has two small driver chips, so it can run the two wheels of a robot.",
         look="A small red or green board, with two screw terminals for motors and a row of six pins.", purpose="It sits between the Arduino and the motors. The pins give orders, and the battery supplies the power.",
         props=[("Supply", "2.5&#8211;12 V", "From seller listings. Use your battery pack here."), ("Current", "Up to 800 mA per motor", "From seller listings, which advise running well below this."), ("Inputs", "2 per motor: IA and IB", "Some boards print 1A and 1B."), ("Logic", "3.3 V or 5 V", "Works with an Uno."), ("Speed", "PWM on an input", "Slower levels mean slower speeds.")],
         everyday="Robot vacuums, toy cars, printers and small pumps all use motor driver circuits.", robot="It runs both wheels on your robot, including reverse and spinning on the spot. Robot Exercise 4 wires it up.",
         safety=["Check the battery's direction before connecting it. Reversed power can destroy the driver.", "Join the driver's GND to Arduino GND.", "Feel for heat, with the power off. If it's hot, the motors may be stalled or too big.", "Keep the driver's motor wires away from the sensor wires."],
         terms=[("H-bridge", "A switch arrangement that can reverse current through a motor."), ("Stall", "When a motor is stuck, and draws its largest current."), ("PWM", "Fast on-off pulsing, used to control speed."), ("Shared ground", "A wire joining the &#8722; sides of two supplies.")],
         exam=["A driver lets signals control motor power.", "Each motor uses two inputs: one direction per input.", "LOW on both inputs stops the motor.", "The driver and the Arduino must share a ground."],
         practice=[("What makes a motor spin the other way with a driver?", "Short answer", "Swap which input is HIGH and which is LOW. The driver then reverses the current through the motor."), ("Why not use a single transistor for a robot's wheels?", "Short answer", "One transistor can only run a motor in one direction. A driver can run it both ways."), ("Your motors stop when the driver gets hot. What might be wrong?", "Applied", "The motors may be stalled or drawing too much current, so check for stuck wheels and a battery that's too strong.")],
         k2=["<strong>Explain</strong> why a driver needs its own battery."], k3=["<strong>Wire</strong> two motors to an L9110S.", "<strong>Program</strong> a motor to reverse."], k4=["<strong>Compare</strong> a driver with a single transistor for a robot."],
         links=[("robot-4", "Wire the motor driver"), ("robot-5", "Test each motor"), ("rsim-8", "Spin on the spot in the Robot Simulator")], refs=[("L9110S board listing", "https://www.electrokit.com/en/motor-driver-dual-h-bridge-2.5-12v-0.8a-l9110s", "Community or seller notes")]),
    dict(slug="relay", title="Relay", short="Relay", blurb="A switch moved by a small current.", overview="A relay is a switch moved by an electromagnet. A small current in its coil pulls a contact across, so one circuit can switch another that's completely separate.",
         look="A small plastic cube, often on a blue module, with three control pins and three screw terminals.", purpose="It lets the Arduino switch a separate circuit, with no electrical connection between them.",
         props=[("Coil", "SRD-05VDC: 5 V, 70 &#937;, about 71 mA", "Far too much for a pin, so use a module or a transistor."), ("Contacts", "COM, NO, NC", "NO is normally open, and NC is normally closed."), ("Contact rating", "Often 10 A", "Sources vary by version. This notebook uses low voltage only."), ("Sound", "A click", "Moving parts mean it's slow, and wears out over time.")],
         everyday="Cars, washing machines, thermostats and home appliances use relays to switch large loads from small signals.", robot="Use one to switch a low-voltage pump or lamp from its own battery, such as in a plant watering project.",
         safety=["<strong>Use low voltage only.</strong> Never connect a wall socket or mains appliance to a relay in these projects. That's dangerous, and needs a qualified adult.", "Use a relay module, or a transistor and flyback diode. Never drive a coil straight from a pin.", "Keep the battery-powered load's wiring separate from the Arduino's wiring.", "Screw terminals must be tight. A loose wire can overheat."],
         terms=[("Coil", "The wire winding that makes a magnet when powered."), ("COM", "The common terminal that the switch moves from."), ("NO", "Normally open: connected only when the relay is on."), ("NC", "Normally closed: connected only when the relay is off."), ("Isolation", "Keeping two circuits electrically separate.")],
         exam=["A relay is a switch moved by an electromagnet.", "A 5 V coil can draw about 70 mA, so it needs a driver.", "Use COM and NO for a load that's off by default.", "Its coil needs a flyback diode, and modules often include one."],
         practice=[("Why can't an Arduino pin drive a relay coil directly?", "Short answer", "A typical coil needs about 70 mA, well above a pin's safe current."), ("You want a pump off until the relay turns on. Which terminals do you use?", "Applied", "COM and NO. They connect only when the coil is powered."), ("When would you choose a transistor instead of a relay?", "Applied", "For fast switching, such as PWM, or silent operation. Transistors have no moving parts, but they don't give the same isolation.")],
         k2=["<strong>Explain</strong> the difference between NO and NC."], k3=["<strong>Wire</strong> a relay module to control a battery-powered lamp."], k4=["<strong>Compare</strong> a relay with a transistor for switching a load."],
         links=[], refs=[("Songle SRD-05VDC-SL-C listing", "https://www.electrokit.com/en/rela-srd-1-pol-vaxlande-5v", "Community or seller notes")]),
    dict(slug="regulator", title="Voltage Regulator", short="Regulator", blurb="Gives a steady voltage from a changing one.", overview="A voltage regulator turns a higher voltage into a steady, lower one. Your Arduino Uno already has one on the board, so it can run from a higher voltage on its power jack.",
         look="A black three-legged part, often with a metal tab. Its symbol is a box with an input, an output and a ground.", purpose="It keeps the voltage steady, even as a battery fades or the load changes.",
         props=[("Output", "LM7805: 5 V", "Fixed. Other parts give other voltages."), ("Current", "Up to 1.5 A", "Needs good cooling near that limit."), ("Input", "About 7 V or more", "It needs a couple of volts more than its output."), ("Legs", "IN, GND, OUT", "Check the data sheet for your package."), ("Heat", "(Vin &#8722; 5 V) &#215; current", "All the extra voltage becomes heat.")],
         everyday="Phone chargers, game consoles and most electronic boards use regulators.", robot="If you ever power a whole robot from one larger battery, a regulator can supply 5 V for the Arduino and sensors.",
         safety=["The tab can get hot enough to burn. Unplug it and let it cool before touching it.", "Don't connect a regulator's output to the Uno's 5V pin while USB is also connected, without your guide's check.", "Add the capacitors its data sheet recommends.", "Reversed input can destroy it, so check before powering it."],
         terms=[("Linear regulator", "A regulator that turns extra voltage into heat."), ("Dropout", "The minimum extra voltage needed for a regulator to work."), ("Heat sink", "A piece of metal that helps a part cool down."), ("Dissipation", "Power turned into heat.")],
         exam=["A regulator gives a steady voltage from a higher one.", "A 7805 gives 5 V, and needs about 7 V or more at its input.", "Extra voltage turns into heat.", "An Uno has its own 5 V regulator."],
         practice=[("A 7805 is fed 9 V and supplies 0.5 A. How much power becomes heat?", "Applied", "(9 V &#8722; 5 V) &#215; 0.5 A = 2 W. That's enough to need a heat sink."), ("Why won't a 7805 work well from a 6 V battery?", "Short answer", "It needs about 2 V more than its output, so 6 V doesn't leave enough headroom."), ("Why does a higher input voltage make a regulator hotter?", "Short answer", "Current stays the same, but there's more extra voltage to get rid of as heat.")],
         k2=["<strong>Explain</strong> what dropout means."], k3=["<strong>Calculate</strong> a regulator's heat at a given current."], k4=["<strong>Compare</strong> a regulator with using a separate battery for the Arduino."],
         links=[], refs=[("TI LM340 and LM7805 data sheet", "https://www.ti.com/lit/ds/symlink/lm340.pdf", "Maker's data sheet"), ("Arduino UNO R3 user manual", "https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf", "Maker's data sheet")]),
    dict(slug="power", title="Batteries and Power", short="Batteries", blurb="Choosing and using power safely.", overview="Batteries store energy as chemicals and release it as electricity. Choosing the right one matters: too weak, and a robot acts strangely. Used carelessly, a battery can overheat. Weak batteries cause many beginner faults.",
         look="Cylinders such as AA, or a box-shaped 9 V. Its symbol is a row of long and short lines.", purpose="It supplies the push (voltage) and the amount of stored energy (capacity).",
         props=[("AA alkaline", "1.5 V. About 2850 mAh at low drain", "Energizer's figure. Heavy loads get much less."), ("AA rechargeable", "About 1.2 V", "4 cells give about 4.8 V."), ("9 V alkaline", "Roughly 500&#8211;600 mAh", "General figure. It's small, and weak for motors."), ("Series", "Voltages add up", "4 &#215; 1.5 V is about 6 V."), ("Capacity", "Milliamp-hours (mAh)", "2000 mAh at 200 mA lasts about 10 hours.")],
         everyday="Remote controls, torches, toys, phones and laptops.", robot="This notebook's robot uses 4 AA cells for its motors, and a USB power bank for the Arduino. Keeping them separate stops motors from resetting the board.",
         safety=["<strong>Never short a battery.</strong> Keep cells away from coins and keys. A short can make them dangerously hot.", "Don't mix old and new cells, or different types.", "Never charge non-rechargeable batteries, and never open a battery.", "Take batteries out when a project is stored. Swollen or leaking cells must not be used.", "This notebook avoids lithium polymer (LiPo) packs, which need special chargers and adult care."],
         terms=[("Capacity", "How much charge a battery can deliver, in mAh."), ("Series", "Connecting cells end to end, which adds their voltages."), ("Parallel", "Connecting like ends together, which adds capacity."), ("Internal resistance", "A battery's own resistance, which lowers its voltage under load.")],
         exam=["Volts are the push, and mAh are the capacity.", "Cells in series add their voltage.", "Time is about capacity &#247; current.", "Weak batteries cause many strange faults, so check them first."],
         practice=[("A robot draws 400 mA from 2000 mAh cells. About how long will it run?", "Applied", "2000 &#247; 400 = 5 hours at best. In practice it's less, because high currents reduce the usable capacity."), ("Why is a 9 V battery a poor choice for robot motors?", "Short answer", "It holds little energy, and its voltage sags under the high current that motors draw."), ("Your robot resets each time the motors start. What's the likely cause?", "Applied", "Motors pull the supply down when they share it with the Arduino. Use separate supplies with a shared ground.")],
         k2=["<strong>Explain</strong> the difference between voltage and capacity."], k3=["<strong>Calculate</strong> the run time of a robot."], k4=["<strong>Compare</strong> alkaline and rechargeable cells for a robot."],
         links=[("robot-1", "Meet your robot kit"), ("faults", "Fix It Guide")], refs=[("Energizer E91 data sheet", "https://www.farnell.com/datasheets/1571853.pdf", "Maker's data sheet")]),
]

UNIT2_QUIZ = [
    ("What does INPUT_PULLUP make a pressed button read?", ["HIGH", "LOW", "A random value", "1023"], 1, "The pull-up holds the pin HIGH, and pressing pulls it LOW."),
    ("What's the middle leg of a potentiometer called?", ["The anode", "The wiper", "The cathode", "The base"], 1, "The wiper slides along the resistive track."),
    ("Which buzzer can play different notes using tone()?", ["Active", "Passive", "Both, always", "Neither"], 1, "A passive buzzer needs a changing signal, so you choose the pitch."),
    ("Why shouldn't you run an active buzzer straight from a pin?", ["It may draw 25&#8211;30 mA, too much for a pin", "It needs 12 V", "It only works on A0", "It would be too quiet"], 0, "Use a buzzer module, or a transistor."),
    ("On a diode, what does the band mark?", ["The anode", "The cathode", "The voltage", "The maker"], 1, "Current flows towards the band."),
    ("With a motor driver, what happens with both inputs LOW?", ["Forward", "Backward", "The motor stops", "A short circuit"], 2, "Different inputs set the direction. LOW on both stops it."),
    ("About how much current does a 5 V relay coil draw?", ["About 1 mA", "About 70 mA", "About 5 A", "About 10 A"], 1, "That's why it needs a module or a transistor."),
    ("A 7805 is fed 8 V and supplies 0.25 A. How much power becomes heat?", ["0.75 W", "2 W", "8 W", "5 W"], 0, "(8 V &#8722; 5 V) &#215; 0.25 A = 0.75 W."),
    ("Four 1.5 V cells in series give about how many volts?", ["1.5 V", "4 V", "6 V", "9 V"], 2, "Voltages add up in series."),
    ("Your robot acts strangely. What should you check first?", ["The batteries", "The colour of the wheels", "The Arduino's memory", "The room temperature"], 0, "Weak batteries cause many strange faults."),
]
