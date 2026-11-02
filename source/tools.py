# Live Tools: pages for the calculators in tools.js.
OHM = [("1", "&#937;"), ("1000", "k&#937;"), ("1000000", "M&#937;")]
FARAD = [("0.000000000001", "pF"), ("0.000000001", "nF"), ("0.000001", "&#956;F")]


def num(k, label, val, unit="", units=None, slider=None, hide_if=None, unit_val=None):
    if units:
        opts = "".join(f'<option value="{v}"{" selected" if v == unit_val else ""}>{t}</option>' for v, t in units)
        tail = f'<select data-u="{k}" aria-label="Unit for {label}">{opts}</select>'
    else:
        tail = f'<span class="tf-u">{unit}</span>' if unit else ""
    bar = ""
    if slider:
        a, b, s = slider
        bar = f'<input type="range" data-s="{k}" min="{a}" max="{b}" step="{s}" value="{val}" aria-label="{label} slider">'
    hide = f' data-hide-if="{hide_if}"' if hide_if else ""
    return f'<div class="tf"{hide}><label>{label}<span class="tf-in"><input type="number" inputmode="decimal" data-f="{k}" value="{val}" min="0" step="any">{tail}</span></label>{bar}</div>'


def text(k, label, val, hint=""):
    return f'<div class="tf"><label>{label}<span class="tf-in"><input type="text" data-t="{k}" value="{val}" autocomplete="off" autocapitalize="off" spellcheck="false"></span></label><span class="tf-hint">{hint}</span></div>'


def pick(k, label, options, val=None, fills=None):
    opts = "".join(f'<option value="{v}"{" selected" if v == val else ""}>{t}</option>' for v, t in options)
    if fills:
        return f'<div class="tf"><label>{label}<span class="tf-in"><select data-fills="{fills}">{opts}</select></span></label></div>'
    return f'<div class="tf"><label>{label}<span class="tf-in"><select data-c="{k}">{opts}</select></span></label></div>'


COLOUR_ROWS = [("black", "Black", "0", "&#215;1", ""), ("brown", "Brown", "1", "&#215;10", "&#177;1%"), ("red", "Red", "2", "&#215;100", "&#177;2%"), ("orange", "Orange", "3", "&#215;1 k", ""), ("yellow", "Yellow", "4", "&#215;10 k", ""), ("green", "Green", "5", "&#215;100 k", "&#177;0.5%"), ("blue", "Blue", "6", "&#215;1 M", "&#177;0.25%"), ("violet", "Violet", "7", "&#215;10 M", "&#177;0.1%"), ("grey", "Grey", "8", "&#215;100 M", "&#177;0.05%"), ("white", "White", "9", "&#215;1 G", ""), ("gold", "Gold", "", "&#215;0.1", "&#177;5%"), ("silver", "Silver", "", "&#215;0.01", "&#177;10%")]
COLOUR_TABLE = '<div class="tw"><table><tr><th>Colour</th><th>Digit</th><th>Multiply by</th><th>Tolerance</th></tr>' + "".join(f'<tr><td><i class="sw" style="background:var(--c-{k})"></i> {n}</td><td class="val">{d}</td><td class="val">{m}</td><td class="val">{t}</td></tr>' for k, n, d, m, t in COLOUR_ROWS) + "</table></div>"

RES_FORM = """<div data-chips="resistor" class="tool-form"><div class="tf-row"><div class="tf"><label>How many bands?<span class="tf-in"><select data-count><option value="4">4 bands</option><option value="5">5 bands</option></select></span></label></div>
<div class="tf"><label>Or type a value<span class="tf-in"><input type="text" data-typed autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="res-typed-note"></span></label></div></div><p class="tf-hint" data-typed-note id="res-typed-note" aria-live="polite"></p><div class="bands"></div></div>"""
DIODE_FORM = """<div data-chips="diode" class="tool-form"><div class="tf"><label>Or type a part number<span class="tf-in"><input type="text" data-typed autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="dio-typed-note"></span></label></div><p class="tf-hint" data-typed-note id="dio-typed-note" aria-live="polite"></p><div class="bands"></div></div>"""

TOOLS = [
    dict(slug="resistor", title="Resistor Colour Code", short="Resistor Colours", blurb="Colours to value, and value to colours.", art="resistor", form=RES_FORM, chips=True,
         intro="Resistors are too small to print numbers on, so they wear coloured stripes. Tap the colours you can see, or type a value to see which colours to look for.",
         how=["The digit bands make a number. Red, red makes 22.", "The multiply band says what to multiply it by. Brown means &#215;10, so 22 becomes 220 &#937;.", "The last band is the tolerance: how far the real value might be from the label. Gold means within 5%.", "Start reading from the end furthest from the gold or silver band. If you aren't sure, check with a multimeter."],
         extra="<h2>Colour chart</h2>" + COLOUR_TABLE,
         q="What value is green, blue, red, gold?", a="5, 6 makes 56. Red means &#215;100, so that's 5,600 &#937;, or 5.6 k&#937;, within 5%.", topic="resistor"),
    dict(slug="diode", title="Diode Colour Code", short="Diode Colours", blurb="Read the coloured rings on a glass diode.", art="diode", form=DIODE_FORM, chips=True,
         intro="Some small glass diodes have coloured rings instead of printed numbers. The rings spell out the digits after &#8220;1N&#8221; in the part number, using the same colours as resistors. Tap the rings you can see, or type a part number.",
         how=["Start at the wide ring. It's the first digit, and it also marks the <strong>cathode</strong>, the end current flows out of.", "Each ring is one digit: yellow is 4, brown is 1, and so on. Yellow, brown, yellow, grey is 4, 1, 4, 8, so that's a 1N4148.", "Many diodes have only one band and a printed number, such as a black 1N4007 with a silver band. That band still marks the cathode.", "This code is for leaded glass diodes. Tiny surface-mount glass diodes use other colours, so check the maker's sheet for those."],
         extra='<h2>LEDs are different</h2><p>An LED has no colour code. Its colour tells you roughly how much voltage it uses, which the <a href="#tool-led">LED Resistor tool</a> uses for you.</p><div class="tw"><table><tr><th>LED colour</th><th>Voltage it uses (typical)</th></tr><tr><td>Red</td><td class="val">about 2.0 V</td></tr><tr><td>Yellow</td><td class="val">about 2.1 V</td></tr><tr><td>Green</td><td class="val">about 2.2 V</td></tr><tr><td>Blue</td><td class="val">about 3.0 V</td></tr><tr><td>White</td><td class="val">about 3.0 V</td></tr></table></div><p class="src-note">Band meaning checked against the <a href="https://dl7avf.info/charts/farbcode/index.html">KyteLabs diode colour chart</a> and the <a href="https://en.wikipedia.org/wiki/1N4148_signal_diode">1N4148 article</a>. Ratings are typical. Check the sheet for your exact part.</p>',
         q="If a 1N4007 used colour rings, what would they be?", a="The digits are 4, 0, 0, 7, so yellow (wide), black, black, violet.", topic="diode"),
    dict(slug="led", title="LED Resistor Calculator", short="LED Resistor", blurb="The right resistor for any LED.", art="led",
         fields=[num("v", "Supply voltage", 5, "V", slider=(1, 12, 0.5)), pick("c", "LED colour", [("2", "Red"), ("2.1", "Yellow"), ("2.2", "Green"), ("3", "Blue"), ("3", "White"), ("", "Other (type its voltage)")], fills="vf"), num("vf", "Voltage the LED uses", 2, "V"), num("ma", "Current you want", 10, "mA", slider=(1, 30, 1)), num("n", "LEDs in a row", 1, "", slider=(1, 6, 1))],
         intro="Without a resistor, an LED can burn out in a flash. Tell this tool about your LED, and it picks a safe resistor you can really buy.",
         how=["The LED uses some of the voltage. The rest has to go across the resistor.", "Resistance = leftover voltage &#247; current. For 5 V and a red LED at 10 mA: (5 &#8722; 2) &#247; 0.01 = 300 &#937;.", "Shops sell standard values, so the tool picks the next one up. More resistance means a little less current, which is the safe direction."],
         q="You have a 9 V battery and a blue LED, and you want 20 mA. Which resistor do you need?", a="(9 &#8722; 3) &#247; 0.02 = 300 &#937;. The next standard value up is 330 &#937;, which gives about 18 mA.", topic="led"),
    dict(slug="ohm", title="Ohm's Law Calculator", short="Ohm's Law", blurb="Voltage, current, resistance and power.", art="resistor",
         fields=[pick("find", "What do you want to find?", [("i", "Current"), ("v", "Voltage"), ("r", "Resistance")], "i"), num("v", "Voltage", 5, "V", hide_if="find=v"), num("i", "Current", 20, "mA", hide_if="find=i"), num("r", "Resistance", 220, units=OHM, unit_val="1", hide_if="find=r")],
         intro="Voltage, current and resistance are tied together. If you know any two, you can work out the third. This one rule explains most of electronics.",
         how=["Think of water in a pipe. Voltage is the push, current is the flow, and resistance is how narrow the pipe is.", "Voltage = current &#215; resistance.", "Current = voltage &#247; resistance.", "Resistance = voltage &#247; current.", "Power = voltage &#215; current. Power in a resistor all turns into heat."],
         q="How much current flows if you put 5 V across 1 k&#937;?", a="5 &#247; 1000 = 0.005 A, which is 5 mA.", topic="resistor"),
    dict(slug="divider", title="Voltage Divider Calculator", short="Voltage Divider", blurb="Turn a big voltage into a smaller one.", art="pot",
         fields=[num("vin", "Voltage in", 9, "V", slider=(1, 24, 0.5)), num("r1", "R1 (top resistor)", 10, units=OHM, unit_val="1000"), num("r2", "R2 (bottom resistor, to GND)", 10, units=OHM, unit_val="1000")],
         intro="Two resistors in a row can make a smaller voltage. It's how a dial works, and how an Arduino can safely measure a 9 V battery.",
         how=["Current flows through R1, then R2, then to GND. Voltage out is measured where they meet.", "Voltage out = voltage in &#215; R2 &#247; (R1 + R2).", "A bigger R2 gives more voltage out. A bigger R1 gives less.", "Dividers are for signals. Don't power a motor or a relay with one, because the voltage collapses as soon as it has to supply real current."],
         q="R1 and R2 are both 10 k&#937;, and 9 V goes in. What comes out?", a="9 &#215; 10 &#247; 20 = 4.5 V. Equal resistors always give half.", topic="pot"),
    dict(slug="combine", title="Series and Parallel Resistors", short="Series and Parallel", blurb="Combine resistors to make a new value.", art="breadboard",
         fields=[text("list", "Resistor values, with commas", "220, 330, 1k", "You can type forms such as 220, 4.7k or 1M.")],
         intro="Don't have the resistor you need? You can often make it from others.",
         how=["<strong>In a row (series):</strong> just add them up. The total is always bigger than the biggest one.", "<strong>Side by side (parallel):</strong> current gets more paths, so the total is always smaller than the smallest one.", "Two equal resistors side by side give exactly half of one.", "Capacitors do the opposite: they add up when side by side."],
         q="What do two 220 &#937; resistors make, in a row and side by side?", a="In a row: 440 &#937;. Side by side: 110 &#937;.", topic="resistor"),
    dict(slug="capcode", title="Capacitor Code Reader", short="Capacitor Code", blurb="What does 104 mean? Find out.", art="capacitor",
         fields=[text("code", "Code printed on the capacitor", "104", "You can type forms such as 104, 473J, 22, 4n7 or 100n.")],
         intro="Small ceramic capacitors use a three-digit code. Large electrolytic ones usually just print the real value, such as 470&#956;F.",
         how=["The first two digits are a number. The third says how many zeros follow.", "The answer is in picofarads, which are tiny. 104 means 10 and 4 zeros: 100,000 pF, which is 100 nF.", "A letter after the digits is the tolerance. J is &#177;5%, K is &#177;10%, M is &#177;20%.", "Two digits or fewer means the value in pF, so 22 means 22 pF."],
         extra='<h2>Common codes</h2><div class="tw"><table><tr><th>Code</th><th>Value</th></tr><tr><td class="val">101</td><td>100 pF</td></tr><tr><td class="val">102</td><td>1 nF</td></tr><tr><td class="val">103</td><td>10 nF</td></tr><tr><td class="val">104</td><td>100 nF, the most common</td></tr><tr><td class="val">105</td><td>1 &#956;F</td></tr></table></div>',
         q="What is a capacitor marked 473?", a="47 and 3 zeros: 47,000 pF, which is 47 nF.", topic="capacitor"),
    dict(slug="rc", title="RC Timing Calculator", short="RC Timing", blurb="How fast does a capacitor charge?", art="capacitor",
         fields=[num("r", "Resistor", 10, units=OHM, unit_val="1000"), num("c", "Capacitor", 100, units=FARAD, unit_val="0.000001")],
         intro="A capacitor filling through a resistor is like a bucket filling through a thin hose. Bigger values take longer. Here you can see the curve change.",
         how=["The time constant = R &#215; C. After one time constant, the capacitor is about 63% full.", "After five time constants, it's about 99% full, so we call it full.", "It starts quickly, then slows down as it fills up.", "A resistor and capacitor also make a filter, which calms fast changes in a signal. The cut-off frequency is where it starts to work."],
         q="10 k&#937; and 100 &#956;F: how long until it's about full?", a="One time constant is 10,000 &#215; 0.0001 = 1 second. Five of those is 5 seconds.", topic="capacitor"),
    dict(slug="base", title="Transistor Base Resistor", short="Base Resistor", blurb="Switch a big load safely from a pin.", art="transistor",
         fields=[pick("part", "Transistor", [("tip120", "TIP120 (used in this notebook)"), ("bc547", "BC547 (small, 100 mA)"), ("p2222", "PN2222 (small, 600 mA)")], "tip120"), num("vc", "Control voltage", 5, "V"), num("ma", "Load current", 500, "mA", slider=(10, 3000, 10))],
         intro="A transistor lets a tiny current from a pin switch a big one. The base resistor sets that tiny current. Too little and the transistor gets hot. Too much and the pin is hurt.",
         how=["The base current needed = load current &#247; a safe gain. This tool uses 250 for the TIP120, and 10 for small transistors. These are lower than the best the parts can do, so the transistor turns fully on.", "Resistor = (control voltage &#8722; voltage the base uses) &#247; base current.", "The base uses about 2.5 V on a TIP120 and about 0.7 V on a small transistor.", "The tool rounds down to a standard value, so a little more base current flows, not less.", "The 1 k&#937; used in this notebook's TIP120 builds gives 2.5 mA, which is enough for about 600 mA of load."],
         q="A 1 A motor, a TIP120 and a 5 V pin: which base resistor?", a="1 A &#247; 250 = 4 mA. (5 &#8722; 2.5) &#247; 0.004 = 625 &#937;. Round down to 560 &#937;.", topic="transistor"),
    dict(slug="adc", title="Analog and PWM Calculator", short="Analog and PWM", blurb="Turn Arduino numbers into volts.", art="microcontroller",
         fields=[pick("ref", "Board voltage", [("5", "5 V (Uno)"), ("3.3", "3.3 V")], "5"), num("read", "analogRead value", 512, "", slider=(0, 1023, 1)), num("pwm", "analogWrite value", 128, "", slider=(0, 255, 1))],
         intro="An Arduino thinks in numbers, but circuits work in volts. This tool converts between them. Drag the sliders and watch.",
         how=["analogRead turns 0 to 5 V into a number from 0 to 1023. So volts = reading &#215; 5 &#247; 1023.", "analogWrite doesn't make a lower voltage. It flicks the pin on and off very fast. 0 is always off, and 255 is always on.", "The average is what an LED or motor feels, so 128 feels like about half power.", "On an Uno, analogWrite only works on the pins marked ~: 3, 5, 6, 9, 10 and 11."],
         q="analogRead gives 512 on a 5 V Uno. What is the voltage?", a="512 &#215; 5 &#247; 1023 = about 2.5 V, which is half way.", topic="microcontroller"),
    dict(slug="sonar", title="Ultrasonic Distance Calculator", short="Ultrasonic", blurb="Echo time to distance.", art="ultrasonic",
         fields=[num("us", "Echo time", 1000, "&#956;s", slider=(100, 25000, 50)), num("temp", "Air temperature", 20, "&#176;C", slider=(0, 45, 1))],
         intro="An ultrasonic sensor shouts and listens for the echo. It measures the time, so your code has to work out the distance.",
         how=["The sound goes there and back, so divide by 2.", "Distance = time &#215; speed of sound &#247; 2.", "Sound travels at about 343 metres per second at 20 &#176;C. It's a little faster in warm air.", "That's about 0.0343 cm in each microsecond, which is the number you'll see in code."],
         q="The echo takes 1000 &#956;s at 20 &#176;C. How far away is the object?", a="1000 &#215; 0.0343 &#247; 2 = about 17 cm.", topic="ultrasonic"),
    dict(slug="battery", title="Battery Life Calculator", short="Battery Life", blurb="How long will your project run?", art="power",
         fields=[pick("t", "Battery", [("2000", "AA alkaline (about 2000 mAh)"), ("1900", "AA rechargeable (about 1900 mAh)"), ("400", "9 V block (about 400 mAh)"), ("", "Other (type it)")], fills="mah"), num("mah", "Capacity", 2000, "mAh"), num("ma", "Your circuit draws", 200, "mA", slider=(5, 2000, 5))],
         intro="Battery labels say how much charge is inside, in milliamp-hours (mAh). Divide by how much your circuit uses, and you know roughly how long it'll run.",
         how=["Time = capacity &#215; 0.7 &#247; current. The 0.7 allows for batteries giving less than the label in real use.", "A pack of 4 AAs in a row gives more volts, but not more mAh. It still counts as one AA's capacity.", "Big currents drain batteries faster than this sum says, so treat the answer as a rough guide.", "Motors use the most, especially when they start or get stuck."],
         q="A 2000 mAh pack runs a robot drawing 200 mA. About how long will it last?", a="2000 &#215; 0.7 &#247; 200 = 7 hours.", topic="power"),
    dict(slug="robot", title="Robot Speed and Turn Calculator", short="Robot Speed", blurb="Plan your delay() times.", art="dc-motor",
         fields=[num("mm", "Wheel diameter", 65, "mm"), num("rpm", "Motor speed", 200, "rpm", slider=(20, 400, 5)), num("track", "Gap between the wheels", 13, "cm"), num("dist", "Distance to drive", 50, "cm", slider=(5, 300, 5))],
         intro="Robots that drive by timing need to know how long to run the motors. This gives you a first guess for your delay() numbers.",
         how=["One wheel turn travels the wheel's circumference: &#960; &#215; diameter.", "Speed = turns per second &#215; circumference.", "To spin on the spot, each wheel drives along part of a circle. A 90&#176; turn is &#960; &#215; wheel gap &#247; 4.", "These are top speeds with no load. A real robot is slower, and its batteries change it too. Start with these numbers, test, and adjust.", "Check your motor's label for its real speed. 200 rpm is only a starting guess."],
         q="65 mm wheels at 200 rpm: how far does the robot go in one wheel turn, and how fast is that?", a="&#960; &#215; 6.5 = about 20.4 cm per turn. 200 rpm is 3.33 turns per second, so about 68 cm per second.", topic="dc-motor"),
    dict(slug="regulator", title="Regulator Heat Calculator", short="Regulator Heat", blurb="Will your regulator overheat?", art="regulator",
         fields=[num("vin", "Voltage in", 9, "V", slider=(5, 30, 0.5)), num("vout", "Voltage out", 5, "V"), num("ma", "Current used", 200, "mA", slider=(10, 2000, 10))],
         intro="A linear regulator like the LM7805 gets rid of extra voltage by turning it into heat. This tool shows how much.",
         how=["Heat = (voltage in &#8722; voltage out) &#215; current.", "Without a heat sink, about 1 W is a sensible limit. That's a rule of thumb, not an exact limit.", "A 7805-type regulator needs about 2 V more at its input than its output.", "If it's too hot, lower the input voltage, use a heat sink, or use a switching regulator, which wastes much less."],
         q="9 V in, 5 V out, 500 mA. Is a bare regulator OK?", a="(9 &#8722; 5) &#215; 0.5 = 2 W. That's too much without a heat sink.", topic="regulator"),
]
TOOL_LINKS = {}
for _t in TOOLS:
    TOOL_LINKS.setdefault(_t["topic"], []).append((_t["slug"], _t["short"]))


def tool_links(slug):
    links = TOOL_LINKS.get(slug)
    if not links:
        return ""
    return '<p class="tool-link"><strong>Live tools:</strong> ' + ", ".join(f'<a href="#tool-{s}">{n}</a>' for s, n in links) + "</p>"


def tools_pages(thumb, ans, ul):
    cards = "".join(f'<a class="tc" href="#tool-{t["slug"]}">{thumb(t["art"])}<div><b>{t["short"]}</b><span>{t["blurb"]}</span></div></a>' for t in TOOLS)
    out = f"""
<section id="page-tools" data-page data-name="Live Tools" hidden>
<h1>Live Tools</h1><p class="sub">{len(TOOLS)} calculators that update as you type</p>
<p>Use these while you build. Change a number or tap a colour, and the answer changes straight away. Each tool also shows how the sum works, so you can do it yourself.</p>
<p class="src-note">The answers come from standard formulas and typical part values, so they're a good starting point. Before power goes on, your guide should still check the circuit, and your part's own sheet.</p>
<div class="cards c4">{cards}</div></section>"""
    for i, t in enumerate(TOOLS):
        prev_ = TOOLS[i - 1] if i else None
        next_ = TOOLS[i + 1] if i < len(TOOLS) - 1 else None
        nav = (f'<a href="#tool-{prev_["slug"]}">&larr; {prev_["short"]}</a>' if prev_ else '<a href="#tools">&larr; All tools</a>') + (f'<a href="#tool-{next_["slug"]}">{next_["short"]} &rarr;</a>' if next_ else '<a href="#tools">All tools &rarr;</a>')
        if t.get("chips"):
            form = t["form"]
        else:
            form = f'<form class="tool-form" data-tool="{t["slug"]}" autocomplete="off">{"".join(t["fields"])}</form>'
        out += f"""
<section id="page-tool-{t['slug']}" data-page data-name="{t['short']}" hidden>
<h1>{t['title']}</h1><p class="sub">Live Tools &middot; Tool {i + 1} of {len(TOOLS)}</p>
<p>{t['intro']}</p>
<div class="tool-grid">{form}<div class="tool-out" aria-live="polite"></div></div>
<h2>How it works</h2>{ul(t['how'])}{t.get('extra', '')}
<h2>Try this</h2><ol class="q"><li>{t['q']}{ans(t['a'])}</li></ol>
<div class="links"><a href="#{t['topic']}">Read the topic</a><a href="#tools">All tools</a></div>
<div class="pn">{nav}</div>
</section>"""
    return out
