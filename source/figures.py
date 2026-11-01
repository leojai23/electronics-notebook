# Hand-drawn SVG illustrations: each part sits on a green cutting mat with labels.
H = 400


def t(x, y, s, size=14, w=600, a="start", c="--lab"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" text-anchor="{a}" fill="var({c})">{s}</text>'


def label(x, y, name, sub=None, a="start"):
    out = t(x, y, name, 15, 700, a)
    if sub:
        for i, line in enumerate(sub if isinstance(sub, list) else [sub]):
            out += t(x, y + 18 + i * 16, line, 12.5, 400, a, "--lab-soft")
    return out


def lead(points):
    """Amber leader line. Starts with a dot on the part."""
    p = " ".join(f"{x},{y}" for x, y in points)
    x0, y0 = points[0]
    return (f'<polyline points="{p}" fill="none" stroke="var(--pt)" stroke-width="1.5"/>'
            f'<circle cx="{x0}" cy="{y0}" r="3.5" fill="var(--pt)"/>')


def card(x, y, w, h, title, inner):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="var(--card)"/>'
            f'<text x="{x + w / 2}" y="{y + 20}" font-size="12" font-weight="600" text-anchor="middle" fill="var(--card-soft)">{title}</text>'
            f'<g transform="translate({x + w / 2} {y + h / 2 + 10})" fill="none" stroke="var(--card-ink)" stroke-width="2">{inner}</g></g>')


def sym_text(x, y, s, size=12):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="600" text-anchor="middle" fill="var(--card-ink)" stroke="none">{s}</text>'


def rect(x, y, w, h, fill, rx=0, stroke=None, sw=1):
    st = f' stroke="var({stroke})" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="var({fill})"{st}/>'


def line(x1, y1, x2, y2, c, sw=4, cap="round"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var({c})" stroke-width="{sw}" stroke-linecap="{cap}"/>'


def circ(x, y, r, fill, stroke=None, sw=1):
    st = f' stroke="var({stroke})" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="var({fill})"{st}/>'


# ---------- parts (drawn at figure coordinates; `box` is the thumbnail crop) ----------

def breadboard():
    o = rect(30, 28, 410, 350, "--board", 8, "--board-d", 1.5)
    o += line(46, 44, 430, 44, "--red", 2) + line(46, 92, 430, 92, "--blue", 2)
    o += line(46, 330, 430, 330, "--red", 2) + line(46, 378 - 14, 430, 364, "--blue", 2)
    o += rect(34, 202, 402, 20, "--board-d", 3)
    cols = [58 + i * 19 for i in range(20)]
    for y in [60, 78, 340, 356]:
        for x in cols:
            o += rect(x - 3, y - 3, 6, 6, "--hole", 1)
    for y in [110, 130, 150, 170, 190, 234, 254, 274, 294, 314]:
        for x in cols:
            o += rect(x - 3, y - 3, 6, 6, "--hole", 1)
    o += f'<rect x="48" y="50" width="382" height="20" rx="10" fill="var(--pt)" fill-opacity=".28" stroke="var(--pt)" stroke-width="2"/>'
    o += f'<rect x="400" y="100" width="20" height="100" rx="10" fill="var(--pt)" fill-opacity=".28" stroke="var(--pt)" stroke-width="2"/>'
    return o


def resistor():
    o = line(40, 120, 140, 120, "--silver", 5) + line(350, 120, 450, 120, "--silver", 5)
    o += '<path d="M140 92 q18 -8 34 0 h142 q18 -8 34 0 v56 q-16 8 -34 0 h-142 q-16 8 -34 0 z" fill="var(--tan)" stroke="var(--tan-d)" stroke-width="1.5"/>'
    for x, c in [(178, "--red"), (208, "--red"), (238, "--brown"), (312, "--gold")]:
        o += rect(x - 7, 89, 14, 62, c)
    return o


def led():
    o = line(205, 262, 205, 372, "--silver", 5) + line(255, 262, 255, 330, "--silver", 5)
    o += '<path d="M170 240 v-110 a60 60 0 0 1 120 0 v110 z" fill="var(--red)" fill-opacity=".85" stroke="var(--red-d)" stroke-width="2"/>'
    o += rect(160, 240, 140, 22, "--red-d", 3)
    o += line(205, 240, 205, 170, "--silver", 4) + line(255, 240, 255, 196, "--silver", 4)
    o += '<path d="M255 196 h-28 v-16 h28 z" fill="var(--silver)"/>'
    o += '<path d="M190 96 q-10 18 -8 50" fill="none" stroke="var(--white)" stroke-opacity=".65" stroke-width="5" stroke-linecap="round"/>'
    o += line(290, 240, 290, 262, "--board", 3, "butt")
    return o


def capacitor():
    o = line(120, 270, 120, 372, "--silver", 5) + line(180, 270, 180, 335, "--silver", 5)
    o += rect(80, 90, 140, 180, "--cap", 10, "--cap-d", 2)
    o += '<ellipse cx="150" cy="90" rx="70" ry="14" fill="var(--silver)" stroke="var(--silver-d)" stroke-width="1.5"/>'
    o += '<path d="M90 90 L210 90 M150 76 L150 104" stroke="var(--silver-d)" stroke-width="2"/>'
    o += rect(180, 100, 36, 168, "--stripe", 0)
    for y in [125, 165, 205, 245]:
        o += t(198, y + 4, "&#8722;", 18, 800, "middle", "--cap")
    o += t(134, 170, "470", 18, 700, "middle", "--white") + t(134, 192, "&#181;F", 14, 600, "middle", "--white") + t(134, 222, "16V", 14, 600, "middle", "--white")
    o += line(335, 262, 335, 350, "--silver", 4) + line(375, 262, 375, 350, "--silver", 4)
    o += circ(355, 222, 44, "--ceramic", "--ceramic-d", 2) + t(355, 228, "104", 18, 700, "middle", "--white")
    return o


def transistor():
    o = line(85, 276, 85, 372, "--silver", 8, "butt") + line(135, 276, 135, 372, "--silver", 8, "butt") + line(185, 276, 185, 372, "--silver", 8, "butt")
    o += rect(58, 50, 154, 96, "--silver", 4, "--silver-d", 1.5)
    o += circ(135, 92, 20, "--mat", "--silver-d", 2)
    o += rect(50, 146, 170, 130, "--black", 4, "--black-l", 1.5)
    o += t(135, 202, "TIP120", 20, 700, "middle", "--lab") + t(135, 228, "printed side", 12.5, 400, "middle", "--lab-soft")
    o += t(85, 392, "B", 14, 700, "middle") + t(135, 392, "C", 14, 700, "middle") + t(185, 392, "E", 14, 700, "middle")
    o += line(305, 228, 305, 305, "--silver", 4) + line(335, 228, 335, 305, "--silver", 4) + line(365, 228, 365, 305, "--silver", 4)
    o += '<path d="M285 228 v-50 a50 50 0 0 1 100 0 v50 z" fill="var(--black)" stroke="var(--black-l)" stroke-width="1.5"/>'
    o += t(335, 200, "2N2222", 12, 600, "middle", "--lab")
    return o


def dc_motor():
    o = '<path d="M60 185 C 30 185 34 300 52 342" fill="none" stroke="var(--red)" stroke-width="5"/>'
    o += '<path d="M60 245 C 46 245 56 300 82 342" fill="none" stroke="var(--black-l)" stroke-width="5"/>'
    o += rect(60, 160, 40, 110, "--brass", 5, "--brass-d", 1.5)
    o += rect(100, 140, 210, 150, "--silver", 8, "--silver-d", 2)
    for y in [165, 195, 235, 265]:
        o += line(120, y, 290, y, "--silver-d", 1.5, "butt")
    o += rect(310, 180, 26, 70, "--silver-d", 3)
    o += rect(336, 207, 90, 16, "--silver", 2, "--silver-d", 1)
    o += '<path d="M440 170 a50 50 0 0 1 0 90" fill="none" stroke="var(--pt)" stroke-width="3"/>'
    o += '<path d="M440 260 l-14 -2 l8 -12 z" fill="var(--pt)"/>'
    return o


def servo():
    o = '<path d="M60 310 C 30 330 30 362 70 372" fill="none" stroke="var(--brown)" stroke-width="5"/>'
    o += '<path d="M66 310 C 46 330 46 356 78 364" fill="none" stroke="var(--red)" stroke-width="5"/>'
    o += '<path d="M72 310 C 62 330 62 350 86 356" fill="none" stroke="var(--orange)" stroke-width="5"/>'
    o += rect(84, 346, 44, 28, "--black", 3, "--black-l", 1)
    o += rect(40, 212, 280, 18, "--blue-d", 3)
    o += rect(70, 170, 220, 142, "--blue", 6, "--blue-d", 2)
    o += t(180, 256, "SG90", 22, 700, "middle", "--white")
    for a in (-90, 90):
        o += f'<rect x="-8" y="-104" width="16" height="104" rx="8" transform="translate(150 150) rotate({a})" fill="none" stroke="var(--white)" stroke-width="2" stroke-dasharray="5 5"/>'
    o += rect(128, 148, 44, 26, "--blue-d", 3)
    o += '<rect x="-9" y="-112" width="18" height="112" rx="9" transform="translate(150 150)" fill="var(--white)" stroke="var(--board-d)" stroke-width="1.5"/>'
    o += circ(150, 150, 8, "--silver", "--silver-d", 1.5)
    return o


def ultrasonic():
    o = rect(36, 96, 300, 152, "--blue", 8, "--blue-d", 2)
    for cx in (106, 266):
        o += circ(cx, 176, 54, "--silver", "--silver-d", 2) + circ(cx, 176, 42, "--silver-d")
        for r in (32, 21, 10):
            o += f'<circle cx="{cx}" cy="176" r="{r}" fill="none" stroke="var(--mesh)" stroke-width="3"/>'
    o += rect(170, 166, 32, 20, "--silver", 8, "--silver-d", 1)
    o += t(186, 114, "HC-SR04", 13, 700, "middle", "--white")
    for x in (156, 176, 196, 216):
        o += line(x, 248, x, 290, "--brass", 5, "butt")
    o += '<g fill="none" stroke="var(--pt)" stroke-width="3" stroke-linecap="round">'
    for x in (350, 372, 394):
        o += f'<path d="M{x} 130 q16 42 0 84"/>'
    o += '</g>'
    return o


def arduino():
    o = '<path d="M40 40 H456 L474 58 V120 L456 138 V328 L440 346 H40 Z" fill="var(--teal)" stroke="var(--teal-d)" stroke-width="2"/>'
    o += rect(14, 70, 84, 66, "--silver", 3, "--silver-d", 1.5) + rect(22, 80, 50, 46, "--silver-d", 2)
    o += rect(14, 258, 76, 62, "--black", 3, "--black-l", 1.5) + circ(34, 289, 12, "--silver-d")
    o += rect(180, 52, 254, 16, "--black", 2)
    for i in range(18):
        o += rect(186 + i * 13.6, 56, 7, 7, "--hole", 1)
    o += rect(168, 318, 266, 16, "--black", 2)
    for i in range(14):
        o += rect(174 + i * 18.4, 322, 7, 7, "--hole", 1)
    o += rect(210, 214, 220, 54, "--black", 4, "--black-l", 1.5) + t(320, 247, "ATmega328P", 14, 700, "middle", "--lab")
    for i in range(14):
        o += rect(217 + i * 15, 206, 7, 8, "--silver") + rect(217 + i * 15, 268, 7, 8, "--silver")
    o += rect(52, 58, 28, 12, "--silver", 2) + circ(66, 64, 4, "--red")
    o += t(290, 150, "UNO", 24, 800, "middle", "--white")
    return o


# ---------- figures: part + callouts + symbol card ----------

def fig_breadboard():
    o = breadboard()
    o += lead([(430, 60), (468, 60)]) + label(476, 58, "Power rails", ["The whole line is joined.", "Red is +, blue is &#8722;."])
    o += lead([(420, 150), (468, 150)]) + label(476, 146, "A joined group", ["These 5 holes share a metal strip.", "Every other group works the same."])
    o += lead([(436, 212), (468, 212)]) + label(476, 214, "Centre gap", ["The two halves don't connect", "across it."])
    o += card(486, 286, 214, 96, "Circuit symbol", sym_text(0, -6, "None", 16) + sym_text(0, 16, "It only holds the parts", 12))
    return o


def fig_resistor():
    o = resistor()
    o += lead([(208, 89), (208, 52)]) + label(208, 42, "Colour bands give the value", None, "middle")
    o += lead([(312, 151), (312, 182), (346, 182)]) + label(352, 187, "Gold band: within 5%")
    o += lead([(420, 120), (476, 120)]) + label(484, 116, "Wire legs", ["Either way round is fine."])
    chips = [(40, "--red", "2", "--white"), (106, "--red", "2", "--white"), (172, "--brown", "&#215;10", "--white"), (360, "--gold", "&#177;5%", "--black")]
    o += t(40, 232, "Reading this resistor", 14, 700)
    for x, c, s, ink in chips:
        o += rect(x, 248, 58, 44, c, 5) + t(x + 29, 276, s, 16, 700, "middle", ink)
    o += t(244, 277, "= 220 &#937;", 19, 700)
    o += t(40, 322, "First two bands are digits. The third multiplies them.", 12.5, 400, "start", "--lab-soft")
    o += t(40, 342, "The last band shows how close it is to the label.", 12.5, 400, "start", "--lab-soft")
    sym = '<path d="M-78 4 H-36 l5 -14 l10 28 l10 -28 l10 28 l10 -28 l10 28 l5 -14 H78"/>'
    o += card(486, 218, 214, 110, "Circuit symbol", sym)
    return o


def fig_led():
    o = led()
    o += lead([(205, 340), (112, 340)]) + label(26, 336, "Long leg", ["+ (anode)"])
    o += lead([(255, 310), (330, 310)]) + label(338, 306, "Short leg", ["&#8722; (cathode)"])
    o += lead([(290, 251), (330, 225), (344, 225)]) + label(350, 222, "Flat edge", ["Also marks the &#8722; side."])
    o += lead([(280, 120), (344, 120)]) + label(350, 116, "Plastic dome", ["Its colour usually matches the light."])
    sym = ('<path d="M-78 4 H-18 M18 4 H78 M18 -16 V24"/><path d="M-18 -16 V24 L18 4 Z"/>'
           '<path d="M6 -18 L16 -30 M10 -30 H16 V-24 M18 -12 L28 -24 M22 -24 H28 V-18"/>')
    o += card(486, 286, 214, 100, "Circuit symbol", sym)
    return o


def fig_capacitor():
    o = capacitor()
    o += t(150, 52, "Electrolytic", 15, 700, "middle") + t(355, 150, "Ceramic disc", 15, 700, "middle")
    o += lead([(216, 130), (262, 96), (428, 96)]) + label(436, 92, "Stripe marks the &#8722; side", ["Get this right every time."])
    o += lead([(120, 352), (108, 352)]) + label(10, 357, "Long leg: +")
    o += lead([(180, 320), (214, 320)]) + label(222, 325, "Short leg: &#8722;")
    o += lead([(399, 222), (428, 222)]) + label(436, 218, "No + or &#8722; side", ["104 means 100 nF."])
    sym = '<path d="M-78 4 H-8 M-8 -20 V28 M8 -20 V28 M8 4 H78"/>' + sym_text(-22, -8, "+", 16)
    o += card(486, 286, 214, 100, "Circuit symbol", sym)
    return o


def fig_transistor():
    o = transistor()
    o += lead([(212, 92), (262, 92)]) + label(268, 72, "Metal tab", ["Joined to the collector leg."], "start")
    o += lead([(385, 190), (428, 190)]) + label(436, 170, "Small type", ["Same job, lower current.", "Leg order varies by part."])
    o += t(135, 30, "Power type", 15, 700, "middle")
    o += lead([(185, 340), (246, 340)]) + label(252, 336, "Three legs", ["Base, collector, emitter"])
    sym = ('<circle cx="0" cy="4" r="30"/><path d="M-78 4 H-12 M-12 -14 V22 M-12 -3 L16 -18 V-34 M16 26 V42"/>'
           '<path d="M-12 11 L16 26"/><path d="M6 25 L16 26 L11 17" fill="var(--card-ink)"/>')
    sym += sym_text(-62, -4, "B") + sym_text(30, -24, "C") + sym_text(30, 42, "E")
    o += card(486, 240, 214, 148, "Circuit symbol", sym)
    return o


def fig_dc_motor():
    o = dc_motor()
    o += lead([(390, 215), (390, 100), (428, 100)]) + label(436, 96, "Shaft", ["This is the part that spins."])
    o += lead([(205, 140), (205, 70)]) + label(205, 60, "Metal can", None, "middle")
    o += t(205, 36, "Magnets and coils inside", 12.5, 400, "middle", "--lab-soft")
    o += lead([(120, 322), (72, 322)]) + label(128, 327, "Two wires")
    o += t(128, 345, "Swap them and it spins", 12.5, 400, "start", "--lab-soft") + t(128, 361, "the other way.", 12.5, 400, "start", "--lab-soft")
    sym = '<path d="M-78 4 H-26 M26 4 H78"/><circle cx="0" cy="4" r="26"/>' + sym_text(0, 11, "M", 20)
    o += card(486, 280, 214, 106, "Circuit symbol", sym)
    return o


def fig_servo():
    o = servo()
    o += t(150, 30, "90&#176;", 13, 700, "middle") + t(46, 132, "0&#176;", 13, 700, "middle") + t(254, 132, "180&#176;", 13, 700, "middle")
    o += lead([(160, 80), (330, 80)]) + label(338, 76, "Horn", ["Turns to an exact angle.", "Never force it by hand."])
    o += lead([(290, 240), (338, 240)]) + label(346, 236, "Plastic gears inside", ["They strip if you force them."])
    o += lead([(128, 360), (196, 360)]) + label(204, 340, "Wires (SG90)")
    o += t(204, 358, "Brown: ground", 12.5, 600, "start", "--lab-soft") + t(204, 374, "Red: power", 12.5, 600, "start", "--lab-soft") + t(204, 390, "Orange: signal", 12.5, 600, "start", "--lab-soft")
    sym = '<rect x="-46" y="-22" width="92" height="52" rx="4"/><path d="M-78 -10 H-46 M-78 4 H-46 M-78 18 H-46"/>' + sym_text(0, 9, "SERVO", 14)
    o += card(486, 280, 214, 106, "Usually drawn as a box", sym)
    return o


def fig_ultrasonic():
    o = ultrasonic()
    o += rect(412, 96, 16, 152, "--board-d", 2) + t(420, 80, "Wall", 13, 700, "middle")
    o += lead([(106, 122), (106, 58)]) + label(106, 48, "Sends the sound", None, "middle")
    o += lead([(266, 122), (266, 58)]) + label(266, 48, "Hears the echo", None, "middle")
    for i, (x, s) in enumerate([(156, "VCC"), (176, "TRIG"), (196, "ECHO"), (216, "GND")]):
        o += f'<text transform="translate({x + 4} 300) rotate(90)" font-size="12" font-weight="700" fill="var(--lab)">{s}</text>'
    o += t(36, 372, "Distance = echo time &#215; speed of sound &#247; 2", 14, 700)
    o += t(36, 390, "Divide by 2 because the sound goes there and back.", 12.5, 400, "start", "--lab-soft")
    o += t(460, 150, "40 kHz sound", 15, 700) + t(460, 168, "Too high for you to hear.", 12.5, 400, "start", "--lab-soft")
    sym = '<rect x="-60" y="-24" width="120" height="56" rx="4"/><circle cx="-28" cy="4" r="14"/><circle cx="28" cy="4" r="14"/>'
    o += card(486, 270, 214, 116, "Usually drawn as a box", sym)
    return o


def fig_microcontroller():
    o = arduino()
    o += lead([(306, 52), (306, 22)]) + t(300, 18, "Digital pins 0&#8211;13", 15, 700, "middle")
    o += lead([(30, 70), (30, 30)]) + t(20, 20, "USB socket", 15, 700)
    o += lead([(52, 320), (52, 372)]) + label(22, 390, "Power jack")
    o += lead([(430, 240), (476, 240)]) + label(484, 214, "The chip", ["ATmega328P: runs your code"])
    o += lead([(240, 334), (240, 372)]) + label(172, 390, "5V, GND, then A0&#8211;A5")
    sym = '<rect x="-46" y="-30" width="92" height="66" rx="4"/><path d="M-70 -14 H-46 M-70 4 H-46 M-70 22 H-46 M46 -14 H70 M46 4 H70 M46 22 H70"/>' + sym_text(0, 10, "MCU", 15)
    o += card(486, 262, 214, 124, "Usually drawn as a box", sym)
    return o


FIGS = {
    "breadboard": (fig_breadboard, breadboard, "20 20 430 366", "A breadboard with its power rails and joined groups of holes highlighted"),
    "resistor": (fig_resistor, resistor, "30 60 430 120", "A resistor with coloured bands, showing how red-red-brown-gold reads as 220 ohms"),
    "led": (fig_led, led, "60 50 340 330", "An LED showing the long positive leg, short negative leg, flat edge and dome"),
    "capacitor": (fig_capacitor, capacitor, "60 60 360 320", "An electrolytic capacitor with a stripe marking its negative side, beside a ceramic disc capacitor"),
    "transistor": (fig_transistor, transistor, "30 40 380 340", "A TIP120 power transistor with a metal tab and three legs, beside a small half-round transistor"),
    "dc-motor": (fig_dc_motor, dc_motor, "10 120 450 230", "A small DC motor with its shaft, metal can and two wires"),
    "servo": (fig_servo, servo, "20 30 320 350", "An SG90 servo motor with its horn at 90 degrees, and dashed outlines at 0 and 180 degrees"),
    "ultrasonic": (fig_ultrasonic, ultrasonic, "20 80 420 220", "An HC-SR04 distance sensor sending sound towards a wall"),
    "microcontroller": (fig_microcontroller, arduino, "6 30 480 325", "An Arduino Uno board with its USB socket, power jack, pin rows and main chip labelled"),
}


def figure(slug):
    fn, _, _, alt = FIGS[slug]
    return (f'<svg class="plate" viewBox="0 0 720 {H}" role="img" aria-label="{alt}">'
            f'<rect width="720" height="{H}" rx="8" fill="var(--mat)"/><rect width="720" height="{H}" rx="8" fill="url(#matgrid)"/>{fn()}</svg>')


def thumb(slug):
    _, part, box, _ = FIGS[slug]
    x, y, w, h = [float(v) for v in box.split()]
    # Centre the part inside a 3:2 mat so that every card lines up.
    tw = max(w, h * 1.5) * 1.12
    th = tw / 1.5
    vx = x + w / 2 - tw / 2
    vy = y + h / 2 - th / 2
    return (f'<svg class="thumb" viewBox="{vx:.1f} {vy:.1f} {tw:.1f} {th:.1f}" aria-hidden="true">'
            f'<rect x="{vx:.1f}" y="{vy:.1f}" width="{tw:.1f}" height="{th:.1f}" fill="var(--mat)"/>'
            f'<rect x="{vx:.1f}" y="{vy:.1f}" width="{tw:.1f}" height="{th:.1f}" fill="url(#matgrid)"/>{part()}</svg>')


DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<pattern id="matgrid" width="100" height="100" patternUnits="userSpaceOnUse">'
        '<path d="M20 0V100M40 0V100M60 0V100M80 0V100M0 20H100M0 40H100M0 60H100M0 80H100" stroke="var(--mat-line)" stroke-width="1" fill="none"/>'
        '<path d="M0 0H100M0 0V100" stroke="var(--mat-major)" stroke-width="1.5" fill="none"/>'
        '</pattern></defs></svg>')
