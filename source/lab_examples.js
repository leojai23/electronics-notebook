/* The 25 practical examples: circuit, sketch, explanation and automatic checks. */
(function (root) {
  'use strict';
  const merge = (...xs) => ({ parts: xs.flatMap(x => x.parts || []), wires: xs.flatMap(x => x.wires || []) });
  // LED + series resistor, starting at a column and taking 6 columns.
  const led = (col, from, id, color, ohm) => ({
    parts: [{ id: 'R' + id.replace(/\D/g, ''), type: 'resistor', ohm: ohm || 220, legs: { a: `c${col}`, b: `c${col + 4}` } },
      { id, type: 'led', color: color || 'red', legs: { a: `d${col + 4}`, k: `d${col + 5}` } }],
    wires: [[from, `b${col}`], [`a${col + 5}`, `TN${col + 5}`]],
  });
  const rails = { wires: [['GND', 'TN1']] };
  const rails5 = { wires: [['5V', 'TP1'], ['GND', 'TN1']] };
  const link = { wires: [['TN30', 'BN30']] }; // joins the top and bottom ground rails
  const btn = (col, pin, id) => ({ parts: [{ id, type: 'button', legs: { a: `e${col}`, b: `f${col}` } }], wires: [[pin, `a${col}`], [`j${col}`, `BN${col}`]] });
  const pot = (col, pin, id) => ({ parts: [{ id, type: 'pot', ohm: 10000, x: 0.5, legs: { a: `c${col}`, w: `c${col + 1}`, b: `c${col + 2}` } }], wires: [[`a${col}`, `TN${col}`], [`a${col + 2}`, `TP${col + 2}`], [`b${col + 1}`, pin]] });
  const sonar = (col, x) => ({ parts: [{ id: 'S1', type: 'sonar', cm: 100, x: x || 480, legs: { vcc: `a${col}`, trig: `a${col + 1}`, echo: `a${col + 2}`, gnd: `a${col + 3}` } }], wires: [[`b${col}`, `TP${col}`], [`b${col + 1}`, 'D7'], [`b${col + 2}`, 'D6'], [`b${col + 3}`, `TN${col + 3}`]] });
  const bat = { parts: [{ id: 'B1', type: 'battery', volts: 6, x: 70, legs: { p: 'BP2', n: 'BN2' } }], wires: [['GND', 'BN1']] };
  const srv = { parts: [{ id: 'SV1', type: 'servo', x: 300, legs: { g: 'BN20', v: 'BP21', s: 'D9' } }, { id: 'C1', type: 'cap', uf: 470, rating: 16, legs: { p: 'BP6', n: 'BN6' } }] };
  const motorRig = {
    parts: [{ id: 'M1', type: 'motor', x: 200, legs: { a: 'h10', b: 'h12' } }, { id: 'D1', type: 'diode', legs: { a: 'g12', k: 'g10' } },
      { id: 'Q1', type: 'npn', model: 'TIP120', legs: { b: 'f11', c: 'f12', e: 'f13' } }, { id: 'R5', type: 'resistor', ohm: 1000, legs: { a: 'j5', b: 'j11' } }],
    wires: [['i5', 'D5'], ['j13', 'BN13'], ['j10', 'BP10']],
  };
  const DIST = `float readDistanceCm() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long echoTime = pulseIn(ECHO, HIGH);
  return echoTime * 0.0343 / 2;
}`;

  const EX = [
    { title: 'Light an LED', topics: ['breadboard', 'resistor', 'led'], c: merge(rails5, led(5, 'TP5', 'LED1')),
      goal: 'Light an LED from the 5V pin, with no code at all.',
      happen: 'The LED glows as soon as you select Start. Current flows from 5V, through the resistor and LED, to GND.',
      tryit: 'Select the resistor and change it to 1 k&#937;. Then remove the resistor\'s path and see what the simulator warns about.',
      code: `// No code needed: this circuit is powered straight from 5V.
void setup() {
}

void loop() {
}
`, test: [{ say: 'The LED stays lit.', run: 500, see: [{ p: 'LED1', is: 'on' }] }] },

    { title: 'Blink an LED', topics: ['led', 'microcontroller'], c: merge(rails, led(5, 'D8', 'LED1')),
      goal: 'Write your first program: turn an LED on and off.',
      happen: 'The LED turns on for 1 second, then off for 1 second, forever.',
      tryit: 'Change both delays to 200. Then make a pattern: short on, long off.',
      code: `const int LED_PIN = 8;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}
`, test: [{ say: 'The LED blinks on and off.', run: 4000, see: [{ p: 'LED1', is: 'blink' }] }] },

    { title: 'Two LEDs take turns', topics: ['led', 'breadboard'], c: merge(rails, led(5, 'D8', 'LED1', 'red'), led(12, 'D9', 'LED2', 'green')),
      goal: 'Control two pins so that the LEDs swap back and forth.',
      happen: 'When the red LED is on, the green one is off, and then they swap every half second.',
      tryit: 'Make them flash together. Then add a third LED.',
      code: `void setup() {
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
}

void loop() {
  digitalWrite(8, HIGH);
  digitalWrite(9, LOW);
  delay(500);
  digitalWrite(8, LOW);
  digitalWrite(9, HIGH);
  delay(500);
}
`, test: [{ say: 'Both LEDs take turns blinking.', run: 3000, see: [{ p: 'LED1', is: 'blink' }, { p: 'LED2', is: 'blink' }] }] },

    { title: 'Traffic light', topics: ['led', 'resistor'], c: merge(rails, led(3, 'D8', 'LED1', 'red'), led(10, 'D9', 'LED2', 'yellow'), led(17, 'D10', 'LED3', 'green')),
      goal: 'Run a timed sequence, just like a real traffic light.',
      happen: 'Green for 3 seconds, yellow for 1 second, then red for 3 seconds, and repeat.',
      tryit: 'Add a pedestrian button that makes the light change sooner.',
      code: `const int RED = 8;
const int YELLOW = 9;
const int GREEN = 10;

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(GREEN, OUTPUT);
}

void showLight(int pin, int ms) {
  digitalWrite(pin, HIGH);
  delay(ms);
  digitalWrite(pin, LOW);
}

void loop() {
  showLight(GREEN, 3000);
  showLight(YELLOW, 1000);
  showLight(RED, 3000);
}
`, test: [{ say: 'All three lights take their turn.', run: 8000, see: [{ p: 'LED1', is: 'blink' }, { p: 'LED2', is: 'blink' }, { p: 'LED3', is: 'blink' }] }] },

    { title: 'LED chaser', topics: ['led', 'microcontroller'], c: merge(rails, led(2, 'D8', 'LED1', 'red'), led(8, 'D9', 'LED2', 'yellow'), led(14, 'D10', 'LED3', 'green'), led(20, 'D11', 'LED4', 'blue')),
      goal: 'Use an array and a for loop to control many LEDs with little code.',
      happen: 'One light runs along the row of four LEDs, again and again.',
      tryit: 'Make the light run back the other way when it reaches the end.',
      code: `int pins[] = {8, 9, 10, 11};

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(pins[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(pins[i], HIGH);
    delay(150);
    digitalWrite(pins[i], LOW);
  }
}
`, test: [{ say: 'Each of the four LEDs lights in turn.', run: 1500, see: [{ p: 'LED1', is: 'blink' }, { p: 'LED2', is: 'blink' }, { p: 'LED3', is: 'blink' }, { p: 'LED4', is: 'blink' }] }] },

    { title: 'Compare resistor values', topics: ['resistor', 'led'], c: merge(rails, led(5, 'D8', 'LED1', 'red', 220), led(12, 'D9', 'LED2', 'red', 1000)),
      goal: 'See how resistance changes current and brightness.',
      happen: 'Both LEDs are on, and the one with the 220 &#937; resistor is clearly brighter. Select each LED to read its current.',
      tryit: 'Calculate the current for each one, then compare your answer with the simulator.',
      code: `void setup() {
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  digitalWrite(8, HIGH);
  digitalWrite(9, HIGH);
}

void loop() {
}
`, test: [{ say: 'The LED with 220 &#937; is brighter than the one with 1 k&#937;.', run: 500, see: [{ p: 'LED1', is: 'on' }, { p: 'LED2', is: 'on' }, { p: 'LED1', brighter: 'LED2' }] }] },

    { title: 'Fade an LED', topics: ['led', 'microcontroller'], c: merge(rails, led(5, 'D9', 'LED1')),
      goal: 'Use PWM (fast pulsing) to make an LED look dimmer or brighter.',
      happen: 'The LED slowly brightens, then slowly dims, like breathing.',
      tryit: 'Make it breathe twice as fast. Then try pin 8, which can\'t do PWM, and read the message.',
      code: `const int LED_PIN = 9;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  for (int level = 0; level <= 255; level += 5) {
    analogWrite(LED_PIN, level);
    delay(20);
  }
  for (int level = 255; level >= 0; level -= 5) {
    analogWrite(LED_PIN, level);
    delay(20);
  }
}
`, test: [{ say: 'The LED gets brighter and dimmer.', run: 2500, see: [{ p: 'LED1', is: 'changes', by: 5 }] }] },

    { title: 'Button lights an LED', topics: ['led', 'microcontroller'], c: merge(rails, link, led(5, 'D8', 'LED1'), btn(20, 'D2', 'BTN1')),
      goal: 'Read an input and react to it.',
      happen: 'The LED is on only while you hold the button down.',
      tryit: 'Swap it around, so that the LED is on until you press the button.',
      code: `const int BUTTON = 2;
const int LED_PIN = 8;

void setup() {
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // With INPUT_PULLUP, a pressed button reads LOW.
  if (digitalRead(BUTTON) == LOW) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
`, inputs: 'Hold the button to press it.', test: [
        { say: 'The LED is off when the button isn\'t pressed.', set: { BTN1: 0 }, run: 300, see: [{ p: 'LED1', is: 'off' }] },
        { say: 'The LED is on while the button is held.', set: { BTN1: 1 }, run: 300, see: [{ p: 'LED1', is: 'on' }] },
        { say: 'The LED goes off when the button is released.', set: { BTN1: 0 }, run: 300, see: [{ p: 'LED1', is: 'off' }] }] },

    { title: 'Button toggles an LED', topics: ['microcontroller', 'led'], c: merge(rails, link, led(5, 'D8', 'LED1'), btn(20, 'D2', 'BTN1')),
      goal: 'Use a variable to remember something between loops.',
      happen: 'Press once and the LED stays on. Press again and it stays off.',
      tryit: 'Count the presses and print the count to the Serial Monitor.',
      code: `const int BUTTON = 2;
const int LED_PIN = 8;
bool ledOn = false;
int lastReading = HIGH;

void setup() {
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int reading = digitalRead(BUTTON);
  if (lastReading == HIGH && reading == LOW) {
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn);
    delay(50); // wait for the button contacts to settle
  }
  lastReading = reading;
}
`, inputs: 'Press and release the button.', test: [
        { say: 'One press turns the LED on.', set: { BTN1: 1 }, run: 200 }, { say: 'It stays on after you let go.', set: { BTN1: 0 }, run: 300, see: [{ p: 'LED1', is: 'on' }] },
        { say: 'A second press starts turning it off.', set: { BTN1: 1 }, run: 200 }, { say: 'It stays off after you let go.', set: { BTN1: 0 }, run: 300, see: [{ p: 'LED1', is: 'off' }] }] },

    { title: 'Read a dial on the Serial Monitor', topics: ['microcontroller'], c: merge(rails5, pot(10, 'A0', 'POT1')),
      goal: 'Read an analog input and show its value on the computer.',
      happen: 'The Serial Monitor shows numbers from 0 to 1023 as you turn the dial.',
      tryit: 'Print the voltage as well: reading &#215; 5.0 &#247; 1023.',
      code: `void setup() {
  Serial.begin(9600);
}

void loop() {
  int reading = analogRead(A0);
  Serial.print("A0 reading: ");
  Serial.println(reading);
  delay(200);
}
`, inputs: 'Move the dial slider.', test: [
        { say: 'With the dial at its lowest, the reading is 0.', set: { POT1: 0 }, run: 500, see: [{ serial: 'A0 reading: 0\\n' }] },
        { say: 'With the dial at its highest, the reading is 1023.', set: { POT1: 1 }, run: 500, see: [{ serial: 'A0 reading: 1023\\n' }] }] },

    { title: 'A dial controls LED brightness', topics: ['led', 'microcontroller'], c: merge(rails5, led(3, 'D9', 'LED1'), pot(14, 'A0', 'POT1')),
      goal: 'Connect an input to an output using map().',
      happen: 'Turn the dial up and the LED gets brighter.',
      tryit: 'Reverse it, so that turning the dial up makes the LED dimmer.',
      code: `void setup() {
  pinMode(9, OUTPUT);
}

void loop() {
  int reading = analogRead(A0);
  int level = map(reading, 0, 1023, 0, 255);
  analogWrite(9, level);
  delay(10);
}
`, inputs: 'Move the dial slider.', test: [
        { say: 'With the dial low, the LED is dim.', set: { POT1: 0.1 }, run: 300, see: [{ p: 'LED1', below: 4 }] },
        { say: 'With the dial high, the LED is bright.', set: { POT1: 1 }, run: 300, see: [{ p: 'LED1', above: 10 }] }] },

    { title: 'Automatic night light', topics: ['resistor', 'led'], c: merge(rails5, led(3, 'D8', 'LED1', 'yellow'),
      { parts: [{ id: 'LDR1', type: 'ldr', light: 0.8, legs: { a: 'c13', b: 'c17' } }, { id: 'R2', type: 'resistor', ohm: 10000, legs: { a: 'd17', b: 'd22' } }], wires: [['b13', 'TP13'], ['a22', 'TN22'], ['b17', 'A0']] }),
      goal: 'Use a light sensor and a resistor to measure brightness.',
      happen: 'The LED turns on when the room gets dark, and turns off when it gets bright.',
      tryit: 'Change the number 500. Which value suits your real room?',
      code: `void setup() {
  pinMode(8, OUTPUT);
}

void loop() {
  int light = analogRead(A0);
  if (light < 500) {
    digitalWrite(8, HIGH);
  } else {
    digitalWrite(8, LOW);
  }
  delay(100);
}
`, inputs: 'Move the room light slider.', test: [
        { say: 'In a bright room, the LED is off.', set: { LDR1: 1 }, run: 400, see: [{ p: 'LED1', is: 'off' }] },
        { say: 'In a dark room, the LED is on.', set: { LDR1: 0 }, run: 400, see: [{ p: 'LED1', is: 'on' }] }] },

    { title: 'Play notes on a buzzer', topics: ['microcontroller'], c: merge(rails, { parts: [{ id: 'BZ1', type: 'buzzer', legs: { p: 'c20', n: 'c23' } }], wires: [['D4', 'a20'], ['a23', 'TN23']] }),
      goal: 'Use tone() to make sound at different pitches.',
      happen: 'The buzzer plays three rising notes, then rests. Turn on Sound to hear it.',
      tryit: 'Write your own tune by changing the numbers in the list.',
      code: `int notes[] = {262, 330, 392};

void setup() {
}

void loop() {
  for (int i = 0; i < 3; i++) {
    tone(4, notes[i]);
    delay(300);
    noTone(4);
    delay(50);
  }
  delay(600);
}
`, test: [{ say: 'The buzzer sounds and pauses.', run: 2000, see: [{ p: 'BZ1', is: 'blink' }] }] },

    { title: 'Capacitor keeps an LED lit', topics: ['capacitor', 'resistor'], c: merge(rails5, link, { parts: [{ id: 'BTN1', type: 'button', legs: { a: 'e8', b: 'f8' } }, { id: 'C1', type: 'cap', uf: 470, rating: 16, legs: { p: 'h8', n: 'h11' } }, { id: 'R1', type: 'resistor', ohm: 1000, legs: { a: 'i8', b: 'i15' } }, { id: 'LED1', type: 'led', color: 'red', legs: { a: 'h15', k: 'h16' } }], wires: [['a8', 'TP8'], ['j11', 'BN11'], ['j16', 'BN16']] }),
      goal: 'See a capacitor store charge and slowly release it.',
      happen: 'Press the button to charge the capacitor. Release it, and the LED stays on for a moment, then fades out.',
      tryit: 'Change the capacitor to 100 &#181;F or the resistor to 220 &#937;. Does the fade get shorter?',
      code: `// No code needed: this circuit runs on 5V and a capacitor.
void setup() {
}

void loop() {
}
`, inputs: 'Hold the button for a moment, then let go.', test: [
        { say: 'The LED is on while the button is held.', set: { BTN1: 1 }, run: 300, see: [{ p: 'LED1', is: 'on' }] },
        { say: 'The LED stays on just after you let go.', set: { BTN1: 0 }, run: 150, settle: 0, see: [{ p: 'LED1', is: 'on' }] },
        { say: 'A few seconds later, the LED has faded out.', run: 3000, settle: 2500, see: [{ p: 'LED1', is: 'off' }] }] },

    { title: 'Transistor switches an LED', topics: ['transistor', 'led'], c: merge(rails5, { parts: [{ id: 'R1', type: 'resistor', ohm: 220, legs: { a: 'c5', b: 'c9' } }, { id: 'LED1', type: 'led', color: 'green', legs: { a: 'd9', k: 'd10' } }, { id: 'Q1', type: 'npn', model: '2N2222', legs: { b: 'e15', c: 'e16', e: 'e17' } }, { id: 'R2', type: 'resistor', ohm: 1000, legs: { a: 'c11', b: 'c15' } }], wires: [['b5', 'TP5'], ['a10', 'a16'], ['a17', 'TN17'], ['b11', 'D5']] }),
      goal: 'Use a small signal to switch a separate current.',
      happen: 'The LED blinks, powered from 5V. Pin 5 only signals the transistor. Select each part and compare its current.',
      tryit: 'Select the base resistor and check how little current it carries, compared with the LED.',
      code: `const int BASE_PIN = 5;

void setup() {
  pinMode(BASE_PIN, OUTPUT);
}

void loop() {
  digitalWrite(BASE_PIN, HIGH);
  delay(800);
  digitalWrite(BASE_PIN, LOW);
  delay(800);
}
`, test: [{ say: 'The transistor switches the LED on and off.', run: 3000, see: [{ p: 'LED1', is: 'blink' }] }] },

    { title: 'Transistor runs a DC motor', topics: ['transistor', 'dc-motor'], c: merge(bat, motorRig),
      goal: 'Run a motor safely from its own battery, using a transistor and a diode.',
      happen: 'The motor runs for 2 seconds, then stops for 2 seconds. The Arduino pin carries only a tiny current.',
      tryit: 'Delete the diode and read the warning. Then put it back the wrong way round, and read that message too.',
      code: `const int MOTOR_PIN = 5;

void setup() {
  pinMode(MOTOR_PIN, OUTPUT);
}

void loop() {
  digitalWrite(MOTOR_PIN, HIGH);
  delay(2000);
  digitalWrite(MOTOR_PIN, LOW);
  delay(2000);
}
`, test: [{ say: 'The motor runs and stops.', run: 5000, see: [{ p: 'M1', is: 'blink' }] }] },

    { title: 'Change motor speed', topics: ['dc-motor', 'transistor'], c: merge(bat, motorRig),
      goal: 'Use PWM to control how fast a motor spins.',
      happen: 'The motor steps through slow, medium and fast.',
      tryit: 'Find the slowest speed that a real motor can reach. Real motors often stall at low levels.',
      code: `const int MOTOR_PIN = 5;

void setup() {
  pinMode(MOTOR_PIN, OUTPUT);
}

void loop() {
  analogWrite(MOTOR_PIN, 80);
  delay(1500);
  analogWrite(MOTOR_PIN, 160);
  delay(1500);
  analogWrite(MOTOR_PIN, 255);
  delay(1500);
}
`, test: [{ say: 'The motor changes speed.', run: 5000, see: [{ p: 'M1', is: 'changes', by: 0.3 }] }] },

    { title: 'A dial sets motor speed', topics: ['dc-motor', 'transistor'], c: merge(bat, motorRig, { wires: [['5V', 'TP1'], ['BN29', 'TN29']] }, pot(22, 'A0', 'POT1')),
      goal: 'Build a speed controller.',
      happen: 'Turn the dial up and the motor speeds up. Turn it all the way down and the motor stops.',
      tryit: 'Print the speed on the Serial Monitor as a percentage.',
      code: `void setup() {
  pinMode(5, OUTPUT);
}

void loop() {
  int speed = map(analogRead(A0), 0, 1023, 0, 255);
  analogWrite(5, speed);
  delay(20);
}
`, inputs: 'Move the dial slider.', test: [
        { say: 'With the dial at zero, the motor stops.', set: { POT1: 0 }, run: 300, see: [{ p: 'M1', is: 'off' }] },
        { say: 'With the dial at its highest, the motor runs fast.', set: { POT1: 1 }, run: 300, see: [{ p: 'M1', above: 0.6 }] }] },

    { title: 'Move a servo to set angles', topics: ['servo'], c: merge(bat, srv),
      goal: 'Tell a servo exactly where to go.',
      happen: 'The horn moves to 0&#176;, 90&#176; and 180&#176;, stopping for a second at each one.',
      tryit: 'Add 45&#176; and 135&#176; to the sequence.',
      code: `#include <Servo.h>
Servo arm;

void setup() {
  arm.attach(9);
}

void loop() {
  arm.write(0);
  delay(1000);
  arm.write(90);
  delay(1000);
  arm.write(180);
  delay(1000);
}
`, test: [{ say: 'The servo visits 0&#176;, 90&#176; and 180&#176;.', run: 5000, see: [{ p: 'SV1', visits: [0, 90, 180] }] }] },

    { title: 'Sweep a servo', topics: ['servo'], c: merge(bat, srv),
      goal: 'Move a servo smoothly, using a for loop.',
      happen: 'The horn sweeps slowly from one side to the other and back.',
      tryit: 'Sweep only between 45&#176; and 135&#176;. Then make it faster.',
      code: `#include <Servo.h>
Servo arm;

void setup() {
  arm.attach(9);
}

void loop() {
  for (int angle = 0; angle <= 180; angle += 2) {
    arm.write(angle);
    delay(15);
  }
  for (int angle = 180; angle >= 0; angle -= 2) {
    arm.write(angle);
    delay(15);
  }
}
`, test: [{ say: 'The servo sweeps across its full range.', run: 4000, see: [{ p: 'SV1', visits: [0, 90, 180] }] }] },

    { title: 'A dial steers a servo', topics: ['servo', 'microcontroller'], c: merge(bat, srv, { wires: [['5V', 'TP1'], ['BN29', 'TN29']] }, pot(10, 'A0', 'POT1')),
      goal: 'Make a simple steering control.',
      happen: 'The servo horn follows the dial.',
      tryit: 'Limit the steering to between 30&#176; and 150&#176;.',
      code: `#include <Servo.h>
Servo arm;

void setup() {
  arm.attach(9);
}

void loop() {
  int angle = map(analogRead(A0), 0, 1023, 0, 180);
  arm.write(angle);
  delay(15);
}
`, inputs: 'Move the dial slider.', test: [
        { say: 'With the dial at its lowest, the horn goes to 0&#176;.', set: { POT1: 0 }, run: 900, see: [{ p: 'SV1', angle: 0 }] },
        { say: 'With the dial at its highest, the horn goes to 180&#176;.', set: { POT1: 1 }, run: 900, see: [{ p: 'SV1', angle: 180 }] }] },

    { title: 'Measure distance', topics: ['ultrasonic', 'microcontroller'], c: merge(rails5, sonar(10, 300)),
      goal: 'Read the ultrasonic sensor and print the distance.',
      happen: 'The Serial Monitor shows the distance you set with the slider.',
      tryit: 'Tick Soft curtain and watch the reading go to 0. Why is that a problem for a robot?',
      code: `const int TRIG = 7;
const int ECHO = 6;

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  Serial.begin(9600);
}

${DIST}

void loop() {
  Serial.print("Distance: ");
  Serial.print(readDistanceCm());
  Serial.println(" cm");
  delay(200);
}
`, inputs: 'Move the distance slider.', test: [
        { say: 'With the wall at 50 cm, the reading is about 50 cm.', set: { S1: 50 }, run: 800, see: [{ serial: 'Distance: (49|50)\\.' }] },
        { say: 'With the wall at 120 cm, the reading is about 120 cm.', set: { S1: 120 }, run: 800, see: [{ serial: 'Distance: (119|120)\\.' }] }] },

    { title: 'Parking sensor', topics: ['ultrasonic', 'led'], c: merge(rails5, link, led(2, 'D8', 'LED1', 'green'), led(9, 'D9', 'LED2', 'yellow'), led(16, 'D10', 'LED3', 'red'), sonar(24, 470), { parts: [{ id: 'BZ1', type: 'buzzer', legs: { p: 'h5', n: 'h8' } }], wires: [['D4', 'g5'], ['j8', 'BN8']] }),
      goal: 'Show how close a wall is, using lights and sound.',
      happen: 'As the wall gets closer, green, yellow and red turn on in turn. Under 15 cm, the buzzer sounds as well.',
      tryit: 'Make the buzzer beep faster as the wall gets closer.',
      code: `const int TRIG = 7;
const int ECHO = 6;

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}

${DIST}

void loop() {
  float cm = readDistanceCm();
  digitalWrite(8, cm < 60);
  digitalWrite(9, cm < 30);
  digitalWrite(10, cm < 15);
  if (cm < 15) {
    tone(4, 880);
  } else {
    noTone(4);
  }
  delay(100);
}
`, inputs: 'Move the distance slider.', test: [
        { say: 'At 100 cm, all the lights are off.', set: { S1: 100 }, run: 500, see: [{ p: 'LED1', is: 'off' }, { p: 'LED2', is: 'off' }, { p: 'LED3', is: 'off' }] },
        { say: 'At 40 cm, only green is on.', set: { S1: 40 }, run: 500, see: [{ p: 'LED1', is: 'on' }, { p: 'LED2', is: 'off' }] },
        { say: 'At 10 cm, all the lights and the buzzer are on.', set: { S1: 10 }, run: 500, see: [{ p: 'LED1', is: 'on' }, { p: 'LED2', is: 'on' }, { p: 'LED3', is: 'on' }, { p: 'BZ1', is: 'on' }] }] },

    { title: 'Automatic gate', topics: ['ultrasonic', 'servo', 'capacitor'], c: merge(rails5, link, led(3, 'D8', 'LED1'), sonar(14, 200), { parts: [{ id: 'B1', type: 'battery', volts: 6, x: 70, legs: { p: 'BP2', n: 'BN2' } }] }, srv),
      goal: 'Combine sensing and movement, as you did in Exercise 2.',
      happen: 'When something comes within 20 cm, the LED lights and the servo swings open to 90&#176;. When it leaves, the gate closes.',
      tryit: 'Keep the gate open for 2 seconds after the object leaves.',
      code: `#include <Servo.h>
Servo gate;
const int TRIG = 7;
const int ECHO = 6;

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(8, OUTPUT);
  gate.attach(9);
}

${DIST}

void loop() {
  float cm = readDistanceCm();
  if (cm > 0 && cm < 20) {
    digitalWrite(8, HIGH);
    gate.write(90);
  } else {
    digitalWrite(8, LOW);
    gate.write(0);
  }
  delay(100);
}
`, inputs: 'Move the distance slider.', test: [
        { say: 'With nothing close, the gate stays closed.', set: { S1: 100 }, run: 1500, see: [{ p: 'LED1', is: 'off' }, { p: 'SV1', angle: 0 }] },
        { say: 'With something at 10 cm, the LED lights and the gate opens.', set: { S1: 10 }, run: 1500, see: [{ p: 'LED1', is: 'on' }, { p: 'SV1', angle: 90 }] }] },

    { title: 'Motor stops at a wall', topics: ['ultrasonic', 'dc-motor', 'transistor', 'microcontroller'], c: merge(rails5, link, led(3, 'D8', 'LED1'), sonar(14, 450), { parts: [{ id: 'B1', type: 'battery', volts: 6, x: 70, legs: { p: 'BP2', n: 'BN2' } }, { id: 'C1', type: 'cap', uf: 470, rating: 16, legs: { p: 'BP6', n: 'BN6' } }] }, motorRig),
      goal: 'Build the brain of a wall-avoiding robot: sense, think, act.',
      happen: 'The motor runs while the way is clear. When a wall comes within 20 cm, the motor stops and the LED lights.',
      tryit: 'Tick Soft curtain. The sensor reads 0, and this code treats that as clear. How could you make a robot safer?',
      code: `const int TRIG = 7;
const int ECHO = 6;
const int MOTOR_PIN = 5;
const int LED_PIN = 8;

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

${DIST}

void loop() {
  float cm = readDistanceCm();
  if (cm > 0 && cm < 20) {
    digitalWrite(MOTOR_PIN, LOW);
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(MOTOR_PIN, HIGH);
    digitalWrite(LED_PIN, LOW);
  }
  delay(100);
}
`, inputs: 'Move the distance slider.', test: [
        { say: 'With the way clear, the motor runs and the LED is off.', set: { S1: 100 }, run: 600, see: [{ p: 'M1', is: 'on' }, { p: 'LED1', is: 'off' }] },
        { say: 'With a wall at 10 cm, the motor stops and the LED lights.', set: { S1: 10 }, run: 600, see: [{ p: 'M1', is: 'off' }, { p: 'LED1', is: 'on' }] },
        { say: 'When the wall moves away, the motor starts again.', set: { S1: 100 }, run: 600, see: [{ p: 'M1', is: 'on' }] }] },

    { title: 'Digital thermometer', topics: ['microcontroller', 'led'], sensor: 'temperature', c: merge(rails5, led(3, 'D8', 'LED1'), { parts: [{ id: 'T1', type: 'lm35', tempC: 25, legs: { v: 'c13', o: 'c14', g: 'c15' } }], wires: [['b13', 'TP13'], ['b14', 'A0'], ['b15', 'TN15']] }),
      goal: 'Read an LM35 and show the temperature, with a warning light.',
      happen: 'The Serial Monitor shows the temperature from the slider. Above 30&#176;C, the LED lights.',
      tryit: 'Add a second LED that lights when it gets below 15&#176;C.',
      code: `void setup() {
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float volts = analogRead(A0) * 5.0 / 1023.0;
  float celsius = volts * 100.0;  // 10 mV per degree
  Serial.print("Temperature: ");
  Serial.println(celsius);
  digitalWrite(8, celsius > 30);
  delay(500);
}
`, inputs: 'Move the temperature slider.', test: [
        { say: 'At 20&#176;C, the reading is about 20 and the LED is off.', set: { T1: 20 }, run: 800, see: [{ serial: 'Temperature: (19|20)\\.' }, { p: 'LED1', is: 'off' }] },
        { say: 'At 40&#176;C, the reading is about 40 and the LED is on.', set: { T1: 40 }, run: 800, settle: 600, see: [{ serial: 'Temperature: (39|40)\\.' }, { p: 'LED1', is: 'on' }] }] },

    { title: 'Thirsty plant alarm', topics: ['microcontroller', 'led'], sensor: 'soil', c: merge(rails5, led(3, 'D8', 'LED1'), { parts: [{ id: 'SM1', type: 'soil', moist: 60, legs: { v: 'c13', o: 'c14', g: 'c15' } }], wires: [['b13', 'TP13'], ['b14', 'A0'], ['b15', 'TN15']] }),
      goal: 'Use a soil moisture sensor to tell when a plant needs water.',
      happen: 'When the soil gets dry, the LED lights. Water it, by moving the slider up, and the LED goes off.',
      tryit: 'Make the LED blink faster as the soil gets drier.',
      code: `const int DRY_LIMIT = 500;

void setup() {
  pinMode(8, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int reading = analogRead(A0);
  Serial.println(reading);
  digitalWrite(8, reading > DRY_LIMIT);  // a higher reading means drier soil
  delay(500);
}
`, inputs: 'Move the soil moisture slider.', test: [
        { say: 'In wet soil, the LED is off.', set: { SM1: 90 }, run: 800, settle: 600, see: [{ p: 'LED1', is: 'off' }] },
        { say: 'In dry soil, the LED is on.', set: { SM1: 10 }, run: 800, settle: 600, see: [{ p: 'LED1', is: 'on' }] }] },

    { title: 'Infrared obstacle alarm', topics: ['microcontroller', 'led'], sensor: 'ir', c: merge(rails5, led(3, 'D8', 'LED1'), { parts: [{ id: 'IR1', type: 'irmod', cm: 100, x: 300, legs: { v: 'c13', g: 'c14', o: 'c15' } }], wires: [['b13', 'TP13'], ['b14', 'TN14'], ['b15', 'D2']] }),
      goal: 'Read a digital sensor to detect something nearby.',
      happen: 'When an object comes within about 20 cm, the module\'s output goes LOW and the LED lights.',
      tryit: 'Count how many times something passes, and print the count.',
      code: `void setup() {
  pinMode(2, INPUT);
  pinMode(8, OUTPUT);
}

void loop() {
  bool blocked = digitalRead(2) == LOW;
  digitalWrite(8, blocked);
  delay(50);
}
`, inputs: 'Move the distance slider.', test: [
        { say: 'With nothing nearby, the LED is off.', set: { IR1: 100 }, run: 400, see: [{ p: 'LED1', is: 'off' }] },
        { say: 'With something 10 cm away, the LED is on.', set: { IR1: 10 }, run: 400, see: [{ p: 'LED1', is: 'on' }] }] },
  ];
  EX.forEach((e, i) => { e.n = i + 1; });
  root.ELAB_EXAMPLES = EX;
})(typeof window !== 'undefined' ? window : globalThis);
