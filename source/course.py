# The Arduino coding course: 12 lessons, each with runnable code and a task that checks itself.
L = []


def lesson(title, goal, sections, code, tasks, run=None, lab=None, note=None, io=None):
    L.append(dict(n=len(L) + 1, title=title, goal=goal, sections=sections, code=code, tasks=tasks, run=run, lab=lab, note=note, io=io or []))


lesson("Your first sketch", "Understand the two parts every Arduino program has.",
       [("Setup and loop", "<p>An Arduino program is called a <strong>sketch</strong>. Every sketch has two parts: <code>setup()</code> runs once at the start, and <code>loop()</code> then repeats forever.</p>"),
        ("Rules that catch everyone", "<ul class=\"tight\"><li>Most lines end with a semicolon <code>;</code></li><li>Curly brackets <code>{ }</code> hold a block of code together.</li><li>Capital letters matter: <code>Serial</code> works, but <code>serial</code> doesn't.</li><li>Text after <code>//</code> is a comment. The Arduino ignores it.</li></ul>")],
       """void setup() {
  Serial.begin(9600);          // get ready to print
  Serial.println("I run once!");
}

void loop() {
  Serial.println("I keep repeating.");
  delay(1000);                 // wait 1 second
}
""",
       [dict(ask="Make it print <code>Hello, robot!</code> once at the start.", start="void setup() {\n  Serial.begin(9600);\n  // Print your message here\n}\n\nvoid loop() {\n}\n", model="void setup() {\n  Serial.begin(9600);\n  Serial.println(\"Hello, robot!\");\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="Hello, robot!", say="It prints Hello, robot!")], hint="Use Serial.println, with your text inside double quotes.")], lab="ex-2")

lesson("Controlling pins", "Turn something on and off using a pin.",
       [("Two steps", "<p>First, tell the Arduino a pin is an output, using <code>pinMode</code>. Then set it HIGH (5 V, on) or LOW (0 V, off), using <code>digitalWrite</code>.</p><p>Pin 13 has a small LED on the Uno board itself, so it's perfect for testing. The runner below shows it as a light.</p>")],
       """void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
}
""",
       [dict(ask="Make pin 13 blink faster, with each change taking 200 milliseconds.", start="void setup() {\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  digitalWrite(13, HIGH);\n  delay(1000);\n  digitalWrite(13, LOW);\n  delay(1000);\n}\n", model="void setup() {\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  digitalWrite(13, HIGH);\n  delay(200);\n  digitalWrite(13, LOW);\n  delay(200);\n}\n", run=2100, expect=[dict(toggles=13, atLeast=8, say="Pin 13 changes at least 8 times in about 2 seconds")], hint="Change the numbers inside delay().")], lab="ex-2", io=[13])

lesson("Variables", "Store a value, and give it a name.",
       [("A labelled box", "<p>A <strong>variable</strong> is a labelled box that holds a value. You choose its type, its name and its starting value.</p>"),
        ("Common types", "<div class=\"tw\"><table><tr><th>Type</th><th>Holds</th><th>Example</th></tr><tr><td><code>int</code></td><td>Whole numbers, &#8722;32768 to 32767 on an Uno</td><td><code>int score = 10;</code></td></tr><tr><td><code>long</code></td><td>Bigger whole numbers</td><td><code>long big = 100000;</code></td></tr><tr><td><code>float</code></td><td>Numbers with decimals</td><td><code>float volts = 2.5;</code></td></tr><tr><td><code>bool</code></td><td>true or false</td><td><code>bool on = true;</code></td></tr></table></div>"),
        ("Where it's declared matters", "<p>A variable made outside all functions is <strong>global</strong>, and it keeps its value between loops. One made inside a function is <strong>local</strong>, and it starts afresh each time.</p>")],
       """int count = 0;      // global: it remembers its value

void setup() {
  Serial.begin(9600);
}

void loop() {
  count = count + 1;
  Serial.print("Count: ");
  Serial.println(count);
  delay(500);
}
""",
       [dict(ask="Make a variable called <code>score</code> starting at 10, add 5 to it, then print it after <code>Score: </code>.", start="void setup() {\n  Serial.begin(9600);\n  // Your code here\n}\n\nvoid loop() {\n}\n", model="void setup() {\n  Serial.begin(9600);\n  int score = 10;\n  score = score + 5;\n  Serial.print(\"Score: \");\n  Serial.println(score);\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="Score: 15", say="It prints Score: 15")], hint="Declare it with int score = 10; then use score = score + 5;")])

lesson("Doing maths", "Calculate with numbers, and avoid the common traps.",
       [("The operators", "<p>Use <code>+</code>, <code>-</code>, <code>*</code> and <code>/</code>. The remainder operator, <code>%</code>, is useful too: <code>7 % 2</code> is 1.</p>"),
        ("The whole number trap", "<p>Dividing two whole numbers gives a whole number. <code>7 / 2</code> is 3, not 3.5. To keep the decimals, include a decimal in the sum: <code>7 / 2.0</code>.</p>"),
        ("The size trap", "<p>On an Uno, an <code>int</code> can't go above 32767. <code>300 * 200</code> needs a <code>long</code>, written as <code>300L * 200</code> on a real board.</p>")],
       """void setup() {
  Serial.begin(9600);
  Serial.println(7 / 2);       // whole numbers: 3
  Serial.println(7 / 2.0);     // decimals: 3.50
  Serial.println(7 % 2);       // remainder: 1

  // Ohm's Law: current = voltage / resistance
  float volts = 3.0;
  float ohms = 220.0;
  float milliamps = volts / ohms * 1000;
  Serial.println(milliamps);   // about 13.64
}

void loop() {
}
""",
       [dict(ask="Work out the current for 3 V across a 1000 &#937; resistor, in milliamps, and print it. You should get 3.00.", start="void setup() {\n  Serial.begin(9600);\n  float volts = 3.0;\n  float ohms = 1000.0;\n  // Calculate milliamps and print it\n}\n\nvoid loop() {\n}\n", model="void setup() {\n  Serial.begin(9600);\n  float volts = 3.0;\n  float ohms = 1000.0;\n  float milliamps = volts / ohms * 1000;\n  Serial.println(milliamps);\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="3\\.00", say="It prints 3.00")], hint="Use the same formula as the example, with float variables.")])

lesson("Making decisions", "Use if and else to choose what happens.",
       [("If, else if, else", "<p>An <code>if</code> runs its block only when its test is true. <code>else</code> covers everything else.</p>"),
        ("Comparisons", "<div class=\"tw\"><table><tr><th>Symbol</th><th>Meaning</th></tr><tr><td><code>==</code></td><td>is equal to</td></tr><tr><td><code>!=</code></td><td>is not equal to</td></tr><tr><td><code>&lt;</code> and <code>&gt;</code></td><td>less than, greater than</td></tr><tr><td><code>&amp;&amp;</code> and <code>||</code></td><td>and, or</td></tr></table></div><p><strong>Watch out:</strong> a single <code>=</code> sets a value, and a double <code>==</code> compares. Mixing them up is a very common bug.</p>")],
       """int distance = 15;

void setup() {
  Serial.begin(9600);
  if (distance < 10) {
    Serial.println("Stop!");
  } else if (distance < 30) {
    Serial.println("Slow down");
  } else {
    Serial.println("All clear");
  }
}

void loop() {
}
""",
       [dict(ask="With <code>temp</code> set to 35, print <code>Hot</code> if it's over 30, and <code>OK</code> otherwise.", start="int temp = 35;\n\nvoid setup() {\n  Serial.begin(9600);\n  // Your if and else here\n}\n\nvoid loop() {\n}\n", model="int temp = 35;\n\nvoid setup() {\n  Serial.begin(9600);\n  if (temp > 30) {\n    Serial.println(\"Hot\");\n  } else {\n    Serial.println(\"OK\");\n  }\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="Hot", say="It prints Hot"), dict(notSerial="OK", say="It doesn't also print OK")], hint="if (temp > 30) { ... } else { ... }")], lab="ex-12")

lesson("Repeating with loops", "Repeat code without writing it again.",
       [("for: a set number of times", "<p>A <code>for</code> loop has three parts: a start, a test, and a step. <code>i++</code> means add 1 to i.</p>"),
        ("while: as long as something is true", "<p>A <code>while</code> loop keeps going until its test is false. Check that something changes inside it, or it may never finish.</p>")],
       """void setup() {
  Serial.begin(9600);

  for (int i = 1; i <= 5; i++) {
    Serial.println(i);
  }

  int fuel = 3;
  while (fuel > 0) {
    Serial.print("Fuel left: ");
    Serial.println(fuel);
    fuel = fuel - 1;
  }
}

void loop() {
}
""",
       [dict(ask="Use a <code>for</code> loop to count down, printing 5, 4, 3, 2, 1 on separate lines.", start="void setup() {\n  Serial.begin(9600);\n  // Your for loop here\n}\n\nvoid loop() {\n}\n", model="void setup() {\n  Serial.begin(9600);\n  for (int i = 5; i >= 1; i--) {\n    Serial.println(i);\n  }\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="5\\s+4\\s+3\\s+2\\s+1", say="It counts down from 5 to 1")], hint="Start at 5, continue while i >= 1, and use i-- to subtract 1.")], lab="ex-5")

lesson("Writing functions", "Give a block of code a name, and reuse it.",
       [("Why bother?", "<p>A <strong>function</strong> is a named block of code. It makes programs shorter and easier to read, and you only fix a bug in one place.</p>"),
        ("Inputs and outputs", "<p>Functions can take values, called <strong>parameters</strong>, and can give back one value using <code>return</code>. <code>void</code> means it gives nothing back.</p>")],
       """void blinkTimes(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(13, HIGH);
    delay(150);
    digitalWrite(13, LOW);
    delay(150);
  }
}

int doubled(int x) {
  return x * 2;
}

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
  Serial.println(doubled(21));
  blinkTimes(3);
}

void loop() {
}
""",
       [dict(ask="Write a function <code>square</code> that takes a number and returns it multiplied by itself. Print <code>square(7)</code>.", start="// Write your function here\n\nvoid setup() {\n  Serial.begin(9600);\n  // Print square(7) here\n}\n\nvoid loop() {\n}\n", model="int square(int x) {\n  return x * x;\n}\n\nvoid setup() {\n  Serial.begin(9600);\n  Serial.println(square(7));\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="49", say="It prints 49")], hint="Copy the shape of doubled(), and change what it returns.")], lab="ex-4", io=[13])

lesson("Lists with arrays", "Keep many related values together.",
       [("Numbered boxes", "<p>An <strong>array</strong> holds a list of values. Positions start at 0, so the first item is <code>pins[0]</code>. Going past the end is a common bug, because a real Arduino won't warn you.</p>")],
       """int notes[] = {262, 330, 392};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    Serial.print("Note ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(notes[i]);
  }
}

void loop() {
}
""",
       [dict(ask="Add up the array's 4 values using a loop, and print the total. You should get 100.", start="int values[] = {10, 20, 30, 40};\n\nvoid setup() {\n  Serial.begin(9600);\n  int total = 0;\n  // Your loop here\n  Serial.println(total);\n}\n\nvoid loop() {\n}\n", model="int values[] = {10, 20, 30, 40};\n\nvoid setup() {\n  Serial.begin(9600);\n  int total = 0;\n  for (int i = 0; i < 4; i++) {\n    total = total + values[i];\n  }\n  Serial.println(total);\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="\\b100\\b", say="It prints 100")], hint="Inside the loop, use total = total + values[i];")], lab="ex-5")

lesson("Reading inputs", "Read buttons and dials.",
       [("Digital and analog", "<p><code>digitalRead</code> gives HIGH or LOW. <code>analogRead</code> gives a number from 0 to 1023. <code>map</code> rescales a number to the range you want.</p><p>The runner below has a button on pin 2 and a dial on A0, so try them while the code runs.</p>")],
       """void setup() {
  pinMode(2, INPUT_PULLUP);    // pressed reads LOW
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(13, digitalRead(2) == LOW);

  int dial = analogRead(A0);
  int percent = map(dial, 0, 1023, 0, 100);
  Serial.println(percent);
  delay(300);
}
""",
       [dict(ask="Turn pin 13 on only while the button on pin 2 is held down.", start="void setup() {\n  pinMode(2, INPUT_PULLUP);\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  // Your if and else here\n}\n", model="void setup() {\n  pinMode(2, INPUT_PULLUP);\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  if (digitalRead(2) == LOW) {\n    digitalWrite(13, HIGH);\n  } else {\n    digitalWrite(13, LOW);\n  }\n}\n", run=900, press=[[300, 1], [600, 0]], expect=[dict(highAt=13, t=500, say="Pin 13 is on while the button is held"), dict(lowAt=13, t=850, say="Pin 13 goes off when it's released"), dict(lowAt=13, t=200, say="Pin 13 is off before you press")], hint="With INPUT_PULLUP, a pressed button reads LOW.")], lab="ex-8", io=[13, "button", "dial"])

lesson("Timing without delay", "Do two things at once, using millis().",
       [("The problem with delay()", "<p><code>delay()</code> stops everything. While it's waiting, your robot can't read a sensor or a button.</p>"),
        ("The fix", "<p><code>millis()</code> tells you how many milliseconds have passed since the start. Check it each time around the loop, and act only when enough time has passed. Nothing has to wait.</p>")],
       """unsigned long lastChange = 0;
bool ledOn = false;

void setup() {
  pinMode(13, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  if (millis() - lastChange >= 500) {
    lastChange = millis();
    ledOn = !ledOn;
    digitalWrite(13, ledOn);
  }

  // This still responds straight away:
  if (digitalRead(2) == LOW) {
    Serial.println("Button pressed!");
  }
}
""",
       [dict(ask="Blink pin 13 every 250 milliseconds, without using <code>delay()</code>.", start="unsigned long lastChange = 0;\nbool ledOn = false;\n\nvoid setup() {\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  // Use millis() here\n}\n", model="unsigned long lastChange = 0;\nbool ledOn = false;\n\nvoid setup() {\n  pinMode(13, OUTPUT);\n}\n\nvoid loop() {\n  if (millis() - lastChange >= 250) {\n    lastChange = millis();\n    ledOn = !ledOn;\n    digitalWrite(13, ledOn);\n  }\n}\n", run=2100, expect=[dict(toggles=13, atLeast=6, say="Pin 13 changes at least 6 times in about 2 seconds"), dict(noCode="delay\\s*\\(", say="The code doesn't use delay()")], hint="Copy the if block from the example, and change 500 to 250.")], lab="ex-9", io=[13, "button"])

lesson("Finding bugs with Serial", "Use print statements to see what your code is really doing.",
       [("Print what you think is true", "<p>When code misbehaves, print your variables. Often one is not what you assumed, and the Serial Monitor shows you straight away.</p>"),
        ("The method", "<ol class=\"steps\"><li>Say what you expected, and what happened.</li><li>Print the values just before the part in doubt.</li><li>Change one thing, then test again.</li><li>Remove the extra prints when you've finished.</li></ol>")],
       """int speed = 100;

void setup() {
  Serial.begin(9600);
  speed = speed + 50;
  Serial.print("speed is now ");   // a debug print
  Serial.println(speed);
  if (speed > 120) {
    Serial.println("Fast enough");
  }
}

void loop() {
}
""",
       [dict(ask="This code should print <code>Five</code> only when <code>x</code> is 5, but it prints it for 3. Find the bug and fix it.", start="int x = 3;\n\nvoid setup() {\n  Serial.begin(9600);\n  if (x = 5) {\n    Serial.println(\"Five\");\n  } else {\n    Serial.println(\"Not five\");\n  }\n}\n\nvoid loop() {\n}\n", model="int x = 3;\n\nvoid setup() {\n  Serial.begin(9600);\n  if (x == 5) {\n    Serial.println(\"Five\");\n  } else {\n    Serial.println(\"Not five\");\n  }\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="Not five", say="It prints Not five for x = 3"), dict(notSerial="^Five", say="It doesn't print Five")], hint="Look closely at the if. One = sets a value, and two compare.")])

lesson("Reading error messages", "Understand what the Arduino software is telling you.",
       [("Read the first error first", "<p>One mistake can cause many messages. Fix the first one, then try again. Look at the line it names, and also the line above, because that's often where the mistake really is.</p>"),
        ("Common messages", "<div class=\"tw\"><table><tr><th>The Arduino software says</th><th>It usually means</th></tr><tr><td><code>expected ';' before ...</code></td><td>A semicolon is missing, usually on the line above.</td></tr><tr><td><code>'x' was not declared in this scope</code></td><td>A misspelled name, wrong capitals, or a variable made somewhere else.</td></tr><tr><td><code>expected '}' at end of input</code></td><td>A closing bracket is missing.</td></tr><tr><td><code>Servo.h: No such file or directory</code></td><td>A library isn't installed, or the name is misspelled.</td></tr><tr><td><code>Problem uploading to board</code></td><td>Check the port, the board setting, the USB cable, and pins 0 and 1.</td></tr></table></div><p>This notebook's simulators use their own, friendlier wording, so their messages look a little different.</p>")],
       """void setup() {
  Serial.begin(9600);
  Serial.println("No errors here.");
}

void loop() {
}
""",
       [dict(ask="This code has three mistakes. Fix them so that it runs, and prints <code>Fixed!</code>.", start="void setup() {\n  serial.begin(9600)\n  Serial.println(\"Fixed!\");\n\n\nvoid loop() {\n}\n", model="void setup() {\n  Serial.begin(9600);\n  Serial.println(\"Fixed!\");\n}\n\nvoid loop() {\n}\n", run=500, expect=[dict(serial="Fixed!", say="It runs and prints Fixed!")], hint="Check the capital letter, the semicolon, and the closing bracket of setup().")])
