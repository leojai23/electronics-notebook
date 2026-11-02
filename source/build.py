# Builds the single-file Electronics Study Notebook.
import html as html_mod, json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from figures import figure, thumb, DEFS
from content_a import TOPICS_A
from content_b import TOPICS_B, QUIZ, ASSIGNMENTS, CASE, SOURCES
from robots import R as ROBOTS
from intro import intro_page
from extras import SENSOR_QUIZ, ROBOT_QUIZ, ROBOT_CARDS, faults_page
from unit2 import UNIT2, UNIT2_QUIZ
from course import L as LESSONS
from handbook import SESSIONS, MISTAKES, RUBRIC, ROBOT_ANSWERS, SENSOR_ANSWERS, PARTS
from sensors import S as SENSORS, CATS as SENSOR_CATS
from sensor_art import picture as sensor_picture, thumb as sensor_thumb
from tools import TOOLS, tools_pages, tool_links

TOPICS = TOPICS_A + TOPICS_B
UNIT = "Unit I"
# Rough page counts for the print menu, measured from a real PDF of each set.
PAGES = {"unit1": 40, "unit2": 35, "sensors": 85, "coding": 25, "robots": 65, "tools": 20, "guide": 20, "all": 330}

CSS = """
/* Layout: the MBA notebook's header + sidebar + topic column, with each part photographed on a green cutting mat. */
:root {
  --bg:#f3f6f3; --panel:#ffffff; --text:#17231f; --soft:#51625b; --border:#d5dfd9;
  --accent:#0d6049; --accent-soft:#dcebe4; --on-accent:#ffffff; --warn:#8f4a06; --warn-soft:#fbeedd; --good:#17724f; --bad:#b3261e;
  --display:'Bricolage Grotesque','Trebuchet MS',sans-serif; --body:'Atkinson Hyperlegible',Verdana,sans-serif; --mono:'JetBrains Mono',Consolas,monospace;
  --mat:#15463a; --mat-line:#215a4b; --mat-major:#2d6b59; --lab:#f4f7ef; --lab-soft:#c9dbd0; --pt:#ffc65c;
  --card:#fbfbf6; --card-ink:#1c2a25; --card-soft:#56655e;
  --silver:#c9ced1; --silver-d:#8f979c; --black:#23262b; --black-l:#4b5158; --tan:#d9b98a; --tan-d:#b8965f;
  --red:#d23b35; --red-d:#9e2521; --brown:#7a4a26; --gold:#c9a227; --board:#f3f2ec; --board-d:#c8c7bd; --hole:#3a3f3f;
  --blue:#2f5fa8; --blue-d:#234a85; --teal:#0b7c86; --teal-d:#075c64; --orange:#e67e22; --brass:#b98d3f; --brass-d:#8d6a2c;
  --led-green:#2fae4f; --led-yellow:#e9c22d; --led-blue:#2f7fe0; --yellow-w:#e8b923; --w1:#f08a24; --w2:#b388ff; --w3:#4fc3f7; --w4:#ffd54f; --w5:#ff80ab; --wire-halo:#ffffff55;
  --acrylic:#cfe3e6; --acrylic-d:#8fb3b8; --bad-zone:#d9534f; --good-zone:#5cb85c; --far-zone:#5b9bd5;
  --w3-d:#2f7fa8; --w2-d:#6a3fb0; --soil:#5a3d27; --soil-d:#46301e;
  --pt-tint:#fff0cf;
  --c-black:#17181a; --c-brown:#7a4a26; --c-red:#d23b35; --c-orange:#e67e22; --c-yellow:#f2cf2f; --c-green:#2fa04f; --c-blue:#2f6fd0; --c-violet:#8a4fc7; --c-grey:#8f979c; --c-white:#f7f7f2; --c-gold:#c9a227; --c-silver:#d5d9dc; --c-glass:#e9dcc2;
  --cap:#20335c; --cap-d:#142242; --stripe:#d9dce3; --ceramic:#c8782f; --ceramic-d:#96591f; --white:#ffffff; --mesh:#6f777c;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg:#101613; --panel:#18211d; --text:#e4ece7; --soft:#a1b1a9; --border:#2c3a34;
  --accent:#62d0a8; --accent-soft:#1d3a30; --on-accent:#08231a; --warn:#f0b36a; --warn-soft:#33260f; --good:#62d0a8; --bad:#ff8a80; color-scheme:dark } }
:root[data-theme="dark"] {
  --bg:#101613; --panel:#18211d; --text:#e4ece7; --soft:#a1b1a9; --border:#2c3a34;
  --accent:#62d0a8; --accent-soft:#1d3a30; --on-accent:#08231a; --warn:#f0b36a; --warn-soft:#33260f; --good:#62d0a8; --bad:#ff8a80; color-scheme:dark }
:root[data-reading="day"] {
  --bg:#f3f6f3; --panel:#ffffff; --text:#17231f; --soft:#51625b; --border:#d5dfd9;
  --accent:#0d6049; --accent-soft:#dcebe4; --on-accent:#ffffff; --warn:#8f4a06; --warn-soft:#fbeedd; --good:#17724f; --bad:#b3261e; color-scheme:light }
:root[data-reading="sepia"] {
  --bg:#ece3d2; --panel:#f6efe0; --text:#3a3226; --soft:#655946; --border:#d9ccb4;
  --accent:#0b5a44; --accent-soft:#dcdcc0; --on-accent:#fdf8ec; --warn:#7f4105; --warn-soft:#f0dcbb; --good:#14634a; --bad:#a3231b; color-scheme:light }
:root[data-reading="dark"] {
  --bg:#101613; --panel:#18211d; --text:#e4ece7; --soft:#a1b1a9; --border:#2c3a34;
  --accent:#62d0a8; --accent-soft:#1d3a30; --on-accent:#08231a; --warn:#f0b36a; --warn-soft:#33260f; --good:#62d0a8; --bad:#ff8a80; color-scheme:dark }
:root[data-reading="night"] {
  --bg:#0f0d0b; --panel:#17140f; --text:#c9b89c; --soft:#a09279; --border:#2a251d;
  --accent:#e0ac62; --accent-soft:#2e2414; --on-accent:#1c1204; --warn:#ef9f6b; --warn-soft:#33200f; --good:#a9c98a; --bad:#ff8a80; color-scheme:dark }
:root[data-reading="night"] .site { background:var(--accent-soft); color:var(--text) }
* { box-sizing:border-box }
[hidden] { display:none !important }
body { background:var(--bg); color:var(--text); font:16px/1.6 var(--body) }
a { color:var(--accent) } a:hover { text-decoration:underline }
a:focus-visible, button:focus-visible, summary:focus-visible, input:focus-visible { outline:3px solid var(--accent); outline-offset:2px }
.site { background:var(--accent); color:var(--on-accent); padding-block:14px }
.site-in { max-width:1040px; margin:auto; padding-inline:16px; display:flex; flex-wrap:wrap; gap:4px 16px; justify-content:space-between; align-items:baseline }
.brand { font:700 19px var(--display); color:inherit; text-decoration:none }
.crumbs { font-size:14px } .crumbs a { color:inherit }
.layout { max-width:1040px; margin:auto; padding:24px 16px 56px; display:grid; grid-template-columns:230px minmax(0,1fr); gap:32px; align-items:start }
.side { position:sticky; top:12px; background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px 14px; font-size:14.5px }
.side summary { font:700 15px var(--display); cursor:pointer }
.side h3 { font:600 12px var(--body); letter-spacing:.07em; text-transform:uppercase; color:var(--soft); margin:14px 0 6px }
.side ol, .side ul { margin:0; padding:0; list-style:none }
.side li a { display:flex; gap:7px; padding:4px 6px; border-radius:5px; text-decoration:none; color:var(--text) }
.side li a.on { background:var(--accent-soft); color:var(--accent); font-weight:700 }
.side .n { font:12px var(--mono); color:var(--soft); min-width:14px; padding-top:3px }
.side .tick { margin-left:auto; color:var(--good); font-weight:700 }
.prog { margin-top:12px; font-size:13px; color:var(--soft) }
.bar { height:6px; background:var(--accent-soft); border-radius:3px; overflow:hidden; margin-top:4px } .bar i { display:block; height:100%; background:var(--accent) }
main { min-width:0 }
h1 { font:700 clamp(28px,5vw,38px)/1.15 var(--display); margin:0 0 4px; text-wrap:balance }
h2 { font:700 22px/1.25 var(--display); color:var(--accent); margin:36px 0 12px; padding-bottom:6px; border-bottom:2px solid var(--accent-soft); text-wrap:balance }
h3 { font:700 17px/1.3 var(--display); margin:22px 0 6px }
p { margin:0 0 12px; max-width:68ch } .sub { color:var(--soft); margin:0 0 18px }
figure { margin:18px 0 8px } .fig-scroll { overflow-x:auto } .plate { display:block; width:100%; min-width:480px; font-family:var(--body); border-radius:8px }
figcaption { font-size:14px; color:var(--soft); margin-top:8px }
table { border-collapse:collapse; width:100%; font-size:15px; background:var(--panel) } .tw { overflow-x:auto }
th, td { border:1px solid var(--border); padding:8px 10px; text-align:left; vertical-align:top } th { background:var(--accent-soft); font-weight:700 }
td.val { font-family:var(--mono); font-size:13.5px }
ul.tight, ol.q { padding-left:22px; margin:6px 0 12px; max-width:68ch } ul.tight li, ol.q li { margin-bottom:6px }
.safe { background:var(--warn-soft); border-radius:8px; padding:12px 16px; margin-top:8px } .safe h3 { margin-top:0; color:var(--warn) }
.exam { background:var(--accent-soft); border-radius:8px; padding:4px 18px 8px; margin-top:32px } .exam h2 { border:0; margin-top:14px; margin-bottom:4px }
dl.terms { display:grid; grid-template-columns:minmax(120px,190px) minmax(0,1fr); gap:6px 16px; margin:0 } dt { font-weight:700 } dd { margin:0 }
.marks { color:var(--soft); font-size:13.5px }
details.ans summary { cursor:pointer; color:var(--accent); font-size:14.5px; margin-top:2px }
.ans-box { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:8px 12px; margin-top:6px }
.pn { display:flex; flex-wrap:wrap; justify-content:space-between; gap:10px; margin-top:32px; padding-top:14px; border-top:1px solid var(--border); font-weight:600 }
.cards { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; margin:12px 0 }
.tc { display:block; background:var(--panel); border:1px solid var(--border); border-radius:8px; overflow:hidden; text-decoration:none; color:var(--text) }
.tc:hover { border-color:var(--accent); text-decoration:none } .thumb { display:block; width:100%; aspect-ratio:3/2 }
.tc div { padding:9px 12px 12px } .tc b { font:700 16px var(--display); display:block } .tc span { font-size:13.5px; color:var(--soft); line-height:1.35; display:block; margin-top:2px }
.links { display:flex; flex-wrap:wrap; gap:10px; margin:12px 0 }
.links a { flex:1 1 auto; text-align:center; background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:10px 14px; font-weight:700; text-decoration:none } .links a:hover { border-color:var(--accent) }
.q-card { background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px 16px; margin-bottom:12px } .q-card p { font-weight:700; margin-bottom:6px }
.q-card label { display:flex; gap:8px; padding:3px 0; align-items:flex-start } .q-card input { margin-top:6px }
.fb { font-size:14.5px; margin-top:6px } .fb.ok { color:var(--good) } .fb.no { color:var(--bad) }
button { font:700 15px var(--body); background:var(--accent); color:var(--on-accent); border:0; border-radius:6px; padding:9px 16px; cursor:pointer }
button.alt { background:var(--accent-soft); color:var(--accent) } .score { font:700 20px var(--display); margin-left:12px }
.fc { background:var(--panel); border:1px solid var(--border); border-radius:10px; min-height:190px; padding:24px; display:grid; place-items:center; text-align:center; cursor:pointer; width:100%; color:var(--text); font:400 17px/1.5 var(--body); margin:12px 0 }
.fc b { font:700 26px var(--display) } .fc-row { display:flex; flex-wrap:wrap; gap:8px; align-items:center } select { font:15px var(--body); padding:7px; background:var(--panel); color:var(--text); border:1px solid var(--border); border-radius:6px }
.layout.wide { max-width:1360px; grid-template-columns:minmax(0,1fr) } .layout.wide .side { position:static }
.toolbar { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:12px 0 8px } .toolbar .sep { width:1px; height:26px; background:var(--border) }
.toolbar button { padding:8px 12px } button.stop { background:var(--bad); color:var(--bg) } button.alt.on { background:var(--accent); color:var(--on-accent) }
.toolbar label { font-size:14px; display:flex; gap:6px; align-items:center }
#sim-status { font-size:14.5px; color:var(--soft); margin:0 0 10px; min-height:22px; max-width:none }
.confirm { background:var(--warn-soft); border-radius:8px; padding:10px 14px; margin-bottom:10px; display:flex; flex-wrap:wrap; gap:10px; align-items:center } .confirm span { flex:1 1 240px }
.sim-grid { display:grid; grid-template-columns:minmax(0,1fr) minmax(320px,420px); gap:16px; align-items:start }
.sim-grid > div { min-width:0 }
.sim-canvas { overflow-x:auto; border-radius:8px } #sim-svg { display:block; width:100%; min-width:560px; font-family:var(--body); border-radius:8px; touch-action:manipulation; cursor:default }
#sim-svg .node { cursor:pointer } #sim-svg .part, #sim-svg .wire { cursor:pointer } #sim-svg.placing .part, #sim-svg.placing .wire { pointer-events:none }
#sim-svg .node.hi circle { fill:var(--pt); fill-opacity:.42 } #sim-svg .node:hover .hole { fill:var(--pt) }
#sim-svg .sel > * { filter:drop-shadow(0 0 3px var(--pt)) drop-shadow(0 0 2px var(--pt)) }
#sim-hole { font-size:13px; color:var(--soft); min-height:20px; margin-top:4px }
#sim-props { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:7px 12px; font-size:14.5px; margin-top:6px; display:flex; flex-wrap:wrap; gap:6px 12px; align-items:center } #sim-props select { padding:4px }
#sim-controls { display:flex; flex-direction:column; gap:6px; background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:10px 12px; margin-top:8px }
.ctl { display:flex; flex-wrap:wrap; gap:6px 10px; align-items:center } .ctl-l { font-weight:700; font-size:14.5px; min-width:120px } .ctl input[type=range] { flex:1 1 150px; accent-color:var(--accent); min-width:0 } .ctl output { font:13.5px var(--mono); min-width:58px } .ctl-chk { font-size:14.5px; display:flex; gap:7px; align-items:center }
button.hold { touch-action:none; user-select:none } button.hold.on { background:var(--accent); color:var(--on-accent) }
.msg { border-radius:6px; padding:8px 12px; margin-top:8px; font-size:14.5px; background:var(--warn-soft) } .msg.bad { background:var(--bad); color:var(--bg) } .msg.good { background:var(--accent-soft) }
.code-label { font-weight:700; font-family:var(--display); display:block; margin-bottom:4px }
.code-box { display:flex; border:1px solid var(--border); border-radius:6px; overflow:hidden; background:var(--panel); height:420px }
#sim-gutter { flex:0 0 38px; overflow:hidden; text-align:right; padding:8px 6px 8px 0; background:var(--accent-soft); color:var(--soft); font:13px/1.45 var(--mono) } #sim-gutter span { display:block } #sim-gutter span.err { background:var(--bad); color:var(--bg); font-weight:700 }
#sim-code { flex:1 1 auto; min-width:0; border:0; outline:0; resize:none; padding:8px 10px; background:transparent; color:var(--text); font:13px/1.45 var(--mono); white-space:pre; overflow:auto; tab-size:2 } .code-box:focus-within { outline:3px solid var(--accent); outline-offset:1px }
#sim-serial { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:8px 10px; height:130px; overflow:auto; font:13px/1.4 var(--mono); margin:4px 0 0; white-space:pre-wrap }
.check-head { font:700 16px var(--display); margin-top:12px } .check-head.ok { color:var(--good) } .check-head.no { color:var(--warn) }
ul.check-list { list-style:none; padding:0; margin:6px 0 } .check-list li { display:flex; gap:7px; margin-bottom:4px; font-size:14.5px } .check-list li.ok span { color:var(--good); font-weight:800 } .check-list li.no span { color:var(--bad); font-weight:800 }
ol.ex-list { padding-left:28px; margin:6px 0 } ol.ex-list li { margin-bottom:8px; max-width:68ch } ol.ex-list .marks { display:block } ol.ex-list a { font-weight:700 } .done { color:var(--good); font-size:13px; font-weight:700 }
pre.code { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:10px 12px; font:13px/1.45 var(--mono); overflow-x:auto; max-height:460px; margin:6px 0 0 } .code-head { display:flex; justify-content:space-between; align-items:flex-end; gap:8px; margin-top:22px } .code-head h3 { margin:0 } .code-head button { padding:5px 12px; font-size:14px }
.steps { padding-left:26px; max-width:68ch } .steps li { margin-bottom:8px; padding-left:3px } .steps li::marker { font-weight:800; color:var(--accent) }
.good-box { background:var(--accent-soft); border-radius:8px; padding:10px 16px; margin-top:18px } .good-box h3 { margin:0 0 4px }
@media (max-width:1040px) { .sim-grid { grid-template-columns:minmax(0,1fr) } .code-box { height:340px } }
.io-flow { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin:10px 0 }
.io-flow div { background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:9px 12px; min-width:0; position:relative }
.io-flow b { display:block; font:700 12px var(--body); letter-spacing:.06em; text-transform:uppercase; color:var(--accent); margin-bottom:3px } .io-flow span { font-size:14.5px; line-height:1.4; display:block }
.stats { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin:14px 0 } .stats div { background:var(--accent-soft); border-radius:8px; padding:10px 12px } .stats b { display:block; font:700 28px/1.1 var(--display); color:var(--accent) } .stats span { font-size:14px }
@media (max-width:560px) { .stats { grid-template-columns:repeat(2,minmax(0,1fr)) } }
#rs-canvas { display:block; width:100%; aspect-ratio:320/210; border-radius:8px; border:6px solid var(--mat); touch-action:none; cursor:grab; background:var(--card) }
#rs-read { display:flex; flex-wrap:wrap; gap:6px; margin-top:8px } #rs-read span { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:4px 9px; font:13px var(--mono) } #rs-read b { font-family:var(--body); margin-right:3px }
#rs-gutter { flex:0 0 38px; overflow:hidden; text-align:right; padding:8px 6px 8px 0; background:var(--accent-soft); color:var(--soft); font:13px/1.45 var(--mono) } #rs-gutter span { display:block } #rs-gutter span.err { background:var(--bad); color:var(--bg); font-weight:700 }
#rs-code { flex:1 1 auto; min-width:0; border:0; outline:0; resize:none; padding:8px 10px; background:transparent; color:var(--text); font:13px/1.45 var(--mono); white-space:pre; overflow:auto; tab-size:2 }
#rs-serial { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:8px 10px; height:110px; overflow:auto; font:13px/1.4 var(--mono); margin:4px 0 0; white-space:pre-wrap }
.rs-ctl { display:flex; flex-wrap:wrap; gap:10px 16px; align-items:center; background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:9px 12px; margin-top:8px }
.log-table input[type=text] { width:100%; min-width:140px; font:14px var(--body); padding:5px 7px; background:var(--bg); color:var(--text); border:1px solid var(--border); border-radius:5px } .log-table select { padding:4px; font-size:14px }
#log-out { width:100%; height:120px; margin-top:8px; font:13px var(--mono); background:var(--panel); color:var(--text); border:1px solid var(--border); border-radius:6px; padding:8px }
.search { position:relative; flex:1 1 220px; max-width:360px; min-width:0 } #nb-search { width:100%; font:15px var(--body); padding:6px 11px; border-radius:6px; border:1px solid transparent; background:var(--bg); color:var(--text) }
#nb-results { position:absolute; z-index:20; left:0; right:0; top:calc(100% + 4px); min-width:min(420px,calc(100vw - 32px)); max-height:70vh; overflow:auto; background:var(--panel); color:var(--text); border:1px solid var(--border); border-radius:8px; box-shadow:0 8px 24px #00000040 }
#nb-results a { display:block; padding:8px 12px; text-decoration:none; color:var(--text); border-bottom:1px solid var(--border) } #nb-results a:hover, #nb-results a.on { background:var(--accent-soft) } #nb-results b { display:block; font:700 15px var(--display) } #nb-results span { display:block; font-size:13.5px; line-height:1.35; color:var(--soft) } #nb-results .sr-g { font-size:11.5px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:var(--accent) } #nb-results mark { background:var(--pt); color:#000; border-radius:2px } .sr-none { padding:12px; font-size:14.5px }
details.fault { background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:9px 13px; margin-bottom:8px; max-width:none } details.fault summary { font-weight:700; cursor:pointer } details.fault .ans-box { border:0; padding:6px 0 0; margin:0; background:transparent } details.fault code { font:13px var(--mono); background:var(--accent-soft); padding:1px 4px; border-radius:3px }
.reading { display:flex } .reading button { background:transparent; color:inherit; border:1px solid currentColor; border-right-width:0; border-radius:0; padding:3px 10px; min-height:30px; font:600 13px var(--body) } .reading button:first-child { border-radius:5px 0 0 5px } .reading button:last-child { border-radius:0 5px 5px 0; border-right-width:1px } .reading button:hover { background:#ffffff26 } .reading button[aria-pressed="true"] { background:var(--bg); color:var(--text) }
:root[data-reading="night"] .reading button[aria-pressed="true"] { background:var(--accent); color:var(--on-accent) }
.site a:focus-visible, .site button:focus-visible { outline-color:currentColor }
.nb-fab { position:fixed; right:calc(16px + env(safe-area-inset-right)); z-index:999; width:44px; height:44px; padding:0; border-radius:50%; display:grid; place-items:center; background:var(--accent); color:var(--on-accent); border:0; cursor:pointer; box-shadow:0 2px 8px #00000047; text-decoration:none }
.nb-fab:hover, .nb-fab:focus-visible { text-decoration:none; filter:brightness(1.12) } .nb-fab svg { width:21px; height:21px; display:block; fill:none; stroke:currentColor; stroke-width:2; stroke-linecap:round; stroke-linejoin:round }
#nb-home-btn { bottom:calc(16px + env(safe-area-inset-bottom)) } #nb-print-btn { bottom:calc(68px + env(safe-area-inset-bottom)) } #nb-search-btn { bottom:calc(120px + env(safe-area-inset-bottom)) }
.nb-fab::after { content:attr(data-tip); position:absolute; right:calc(100% + 9px); top:50%; transform:translateY(-50%); background:var(--text); color:var(--bg); font:600 12.5px/1 var(--body); padding:7px 10px; border-radius:6px; white-space:nowrap; opacity:0; pointer-events:none; transition:opacity .12s ease }
.nb-fab:hover::after, .nb-fab:focus-visible::after { opacity:1 } @media (hover:none) { .nb-fab::after { display:none } }
#nb-print-menu { position:fixed; right:calc(70px + env(safe-area-inset-right)); bottom:calc(16px + env(safe-area-inset-bottom)); z-index:1001; display:none; width:min(300px,calc(100vw - 86px)); background:var(--panel); color:var(--text); border:1px solid var(--border); border-radius:10px; box-shadow:0 8px 28px #00000059; overflow:hidden }
#nb-print-menu.open { display:block } #nb-print-menu button, #nb-print-menu a { display:block; width:100%; text-align:left; border:0; border-radius:0; background:transparent; color:var(--text); font:400 14.5px/1.3 var(--body); padding:10px 14px; border-top:1px solid var(--border); text-decoration:none; overflow-wrap:anywhere }
#nb-print-menu button:hover, #nb-print-menu button:focus, #nb-print-menu a:hover, #nb-print-menu a:focus { background:var(--accent-soft); outline:0 } #nb-print-menu b { display:block } #nb-print-menu small { display:block; font-size:12.5px; color:var(--soft); margin-top:2px } #nb-print-menu .hd { padding:8px 14px; font:700 11.5px var(--body); letter-spacing:.06em; text-transform:uppercase; color:var(--soft) } .pm-note { padding:0 14px 10px; font-size:14px; line-height:1.35 }
#nb-scrim { position:fixed; inset:0; z-index:1000; background:#00000073 }
.search.float { position:fixed; z-index:1001; top:9vh; left:50%; transform:translateX(-50%); width:min(560px,calc(100vw - 32px)); max-width:none; flex:none } .search.float #nb-search { font-size:17px; padding:11px 14px; border:1px solid var(--border); box-shadow:0 8px 28px #00000059 } .search.float #nb-results { min-width:0; max-height:66vh }
.print-copy, .print-only { display:none }
.tool-grid { display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:18px; align-items:start; margin:14px 0 } .tool-grid > * { min-width:0 }
.tool-form { background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px 14px } .tf { margin-bottom:12px } .tf:last-child { margin-bottom:0 } .tf label { display:block; font-weight:700; font-size:14.5px } .tf-in { display:flex; gap:6px; align-items:center; margin-top:4px; font-weight:400 } .tf-in input { flex:1 1 auto; min-width:0; width:100%; font:16px var(--body); padding:7px 9px; background:var(--bg); color:var(--text); border:1px solid var(--border); border-radius:6px } .tf-in select { flex:0 0 auto; max-width:100% } .tf-in select:only-child { flex:1 1 auto; min-width:0; width:100% } .tf-u { font-size:14.5px; color:var(--soft); min-width:24px } .tf input[type=range] { display:block; width:100%; margin-top:7px; accent-color:var(--accent) } .tf-hint { display:block; font-size:13.5px; color:var(--soft); margin:4px 0 0; font-weight:400; min-height:0 } .tf-row { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px } .tf-row .tf { margin:0 }
.tool-big { background:var(--accent-soft); border-radius:8px; padding:12px 16px } .tool-big span { display:block; font-size:14px; color:var(--soft) } .tool-big b { display:block; font:700 clamp(26px,5vw,34px)/1.15 var(--display); color:var(--accent); overflow-wrap:anywhere }
.tool-art { display:block; width:100%; height:auto; margin:12px 0 4px; font-family:var(--body) } table.tool-rows { margin-top:8px } .tool-rows th { background:transparent; font-weight:400; color:var(--soft); width:54% } .tool-rows td { font-weight:700; overflow-wrap:anywhere }
.bands { display:grid; grid-template-columns:repeat(var(--n,4),minmax(0,1fr)); gap:6px; margin-top:10px } fieldset.band { border:0; padding:0; margin:0; min-width:0 } fieldset.band legend { font:700 12.5px var(--body); padding:0 0 4px; overflow-wrap:anywhere }
.chip { display:flex; gap:5px; align-items:center; padding:3px; border-radius:5px; cursor:pointer; font-size:12.5px; line-height:1.1; border:2px solid transparent; min-width:0 } .chip input { position:absolute; opacity:0; width:1px; height:1px } .chip i { flex:0 0 15px; height:22px; border-radius:3px; border:1px solid var(--soft) } .chip span { min-width:0; overflow-wrap:anywhere } .chip small { display:block; font-size:11.5px; color:var(--soft) } .chip:hover { background:var(--accent-soft) } .chip:has(input:checked) { border-color:var(--accent); background:var(--accent-soft); font-weight:700 } .chip:has(input:focus-visible) { outline:3px solid var(--accent); outline-offset:1px }
i.sw { display:inline-block; width:14px; height:14px; border-radius:3px; border:1px solid var(--soft); vertical-align:-2px; margin-right:4px } .tool-link { margin-top:10px }
@media (max-width:780px) { .tool-grid { grid-template-columns:minmax(0,1fr) } }
@media (max-width:560px) { .reading { flex:1 1 100%; order:5 } .reading button { flex:1; padding:3px 4px } }
.code-top { display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:6px; margin-bottom:6px } .code-top .code-label { margin:0 } .code-tabs { display:flex; gap:4px } .code-tabs button { padding:4px 12px; font-size:14px }
.blockbox { height:460px; border:1px solid var(--border); border-radius:6px; overflow:hidden; margin-bottom:8px } .code-box.short { height:210px } .sim-grid.blocks-on { grid-template-columns:minmax(0,1fr) minmax(0,1.15fr) } .src-note { font-size:13.5px; color:var(--soft); margin-top:14px; max-width:none }
@media (max-width:1040px) { .sim-grid.blocks-on { grid-template-columns:minmax(0,1fr) } }
.runner { background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:10px 12px; margin:8px 0 10px }
.run-code { width:100%; display:block; font:13px/1.45 var(--mono); padding:8px 10px; background:var(--bg); color:var(--text); border:1px solid var(--border); border-radius:6px; white-space:pre; overflow:auto; resize:vertical; tab-size:2 }
.run-row { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:8px 0 } .run-row button { padding:7px 12px } .run-label { font-weight:700; font-size:13.5px; margin-top:2px } .run-out { background:var(--bg); border:1px solid var(--border); border-radius:6px; padding:8px 10px; min-height:44px; max-height:150px; overflow:auto; font:13px/1.4 var(--mono); margin:4px 0 0; white-space:pre-wrap } .run-out.bad { color:var(--bad) }
.led-wrap { font-size:14px; display:inline-flex; gap:6px; align-items:center } .led-dot { width:15px; height:15px; border-radius:50%; background:var(--border); display:inline-block; border:2px solid var(--soft) } .led-dot.lit { background:var(--pt); border-color:var(--pt); box-shadow:0 0 9px var(--pt) } code { font:0.9em var(--mono); background:var(--accent-soft); padding:1px 4px; border-radius:3px }
.badge { display:inline-block; background:var(--accent-soft); color:var(--accent); border-radius:999px; padding:2px 10px; font-size:13px; font-weight:700 }
.cards.c4 { grid-template-columns:repeat(4,minmax(0,1fr)) } .cards.c3 { grid-template-columns:repeat(3,minmax(0,1fr)) } .cards.c2 { grid-template-columns:repeat(2,minmax(0,1fr)) }
.cards.c5 { grid-template-columns:repeat(6,minmax(0,1fr)) } .cards.c5 > a { grid-column:span 2 } .cards.c5 > a:nth-child(n+4) { grid-column:span 3 }
.tc b { overflow-wrap:anywhere }
@media (max-width:1100px) { .cards.c4 { grid-template-columns:repeat(2,minmax(0,1fr)) } }
.real { list-style:none; padding:0; margin:6px 0; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px } .real li { background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:9px 12px; min-width:0 } .real b { display:block; font-family:var(--display) }
@media (max-width:780px) { .io-flow { grid-template-columns:repeat(2,minmax(0,1fr)) } .cards.c4, .cards.c3 { grid-template-columns:repeat(2,minmax(0,1fr)) } .cards.c5 { grid-template-columns:repeat(2,minmax(0,1fr)) } .cards.c5 > a, .cards.c5 > a:nth-child(n+4) { grid-column:span 1 } .cards.c5 > a:last-child, .cards.c3 > a:last-child { grid-column:span 2 } }
@media (max-width:460px) { .real { grid-template-columns:minmax(0,1fr) } }
@media print {
  :root:root:root { --bg:#fff; --panel:#fff; --text:#000; --soft:#333; --border:#999; --accent:#0d6049; --accent-soft:#e7f0ec; --on-accent:#fff; --warn:#7a3f05; --warn-soft:#f7efe3; --good:#17724f; --bad:#b3261e; color-scheme:light }
  .site, .side, footer, .pn, .toolbar, .links, button, #sim-status, .nb-fab, #nb-print-menu, #nb-scrim, .tool-link, .code-tabs, .blockbox, #sim-hole, #sim-props, #sim-controls, #sim-msgs, #sim-gutter, #rs-gutter, #sim-serial, #sim-serial-h, .run-row, .run-label, .run-out, .task-res, .fc, .fc-row, #fc-pos, input[type=range], details.ans summary { display:none !important }
  .ans-box::before { content:'Answer: '; font-weight:700 }
  #page-sim a[href="#lab"] { display:none } .code-top { break-after:avoid } .print-copy, .runner { break-inside:avoid } @page { margin:14mm } .print-break { break-before:page } .print-copy, .print-only { display:block } main textarea { display:none !important } .code-box { display:block; height:auto; border:0; overflow:visible; background:transparent } .sim-grid, .sim-grid.blocks-on { display:block } #sim-svg { min-width:0 } .sim-canvas { overflow:visible } .tool-grid { grid-template-columns:minmax(0,1fr) minmax(0,1fr) } .tf-in input { border:1px solid #999 } .ans-box { border-left:3px solid #999; border-radius:0; border-top:0; border-right:0; border-bottom:0 } .cards, .cards.c4, .cards.c3, .cards.c5 { grid-template-columns:repeat(3,minmax(0,1fr)) } .cards.c5 > a, .cards.c5 > a:nth-child(n+4) { grid-column:auto } .tc { break-inside:avoid }
  body { background:#fff; font-size:11pt } .layout, .layout.wide { display:block; max-width:none; padding:0 }
  * { -webkit-print-color-adjust:exact; print-color-adjust:exact }
  figure, table, pre, .exam, .safe, .q-card, .real li { break-inside:avoid } h2, h3 { break-after:avoid }
  .plate { min-width:0 } pre.code { max-height:none; overflow:visible; white-space:pre-wrap } .fig-scroll, .tw { overflow:visible }
}
footer { text-align:center; color:var(--soft); font-size:14px; padding:0 16px 28px }
@media (max-width:780px) { .layout { grid-template-columns:minmax(0,1fr); gap:18px } .side { position:static } .cards { grid-template-columns:repeat(2,minmax(0,1fr)) } }
@media (max-width:460px) { dl.terms { grid-template-columns:minmax(0,1fr); gap:0 } dd { margin-bottom:8px } }
"""

JS = r"""
(function () {
  var TOPIC = %(topics)s, CARDS = %(cards)s, KEY = 'elec-read';
  var read = {}; try { read = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) {}
  var pages = document.querySelectorAll('[data-page]'), links = document.querySelectorAll('.side a[href^="#"]');
  var crumb = document.getElementById('crumb'), side = document.getElementById('side');
  function paint() {
    var n = 0; TOPIC.forEach(function (t) { var el = document.getElementById('tick-' + t); if (read[t]) { n++; if (el) el.textContent = '✓'; } });
    document.getElementById('prog-n').textContent = n + ' of ' + TOPIC.length + ' topics read';
    document.getElementById('prog-bar').style.width = (n / TOPIC.length * 100) + '%%';
  }
  function route() {
    var id = (location.hash || '').slice(1) || 'home', isSim = /^ex-([1-9]|1[0-9]|2[0-8])$/.test(id) || id === 'sandbox', isRobot = /^rsim-([5-9]|1[0-9]|2[0-5])$/.test(id);
    var page = document.getElementById(isSim ? 'page-sim' : isRobot ? 'page-rsim' : 'page-' + id);
    if (!page) { id = 'home'; page = document.getElementById('page-home'); }
    document.getElementById('layout').classList.toggle('wide', isSim || isRobot);
    if (window.ELabUI) { if (isSim) window.ELabUI.open(id); else window.ELabUI.close(); }
    if (window.ERobotUI) { if (!isRobot) window.ERobotUI.close(); }
    pages.forEach(function (p) { p.hidden = p !== page; });
    if (window.ECourse) window.ECourse.stopAll();
    var navId = isSim ? 'lab' : (isRobot || /^robot-/.test(id)) ? 'robots' : /^tool-/.test(id) ? 'tools' : /^code-/.test(id) ? 'coding' : /^guide/.test(id) ? 'guide' : id === 'notes-unit2' ? 'unit2' : /^sensor-/.test(id) ? 'sensors' : /^quiz/.test(id) ? 'quiz' : id;
    links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + navId); });
    crumb.textContent = id === 'home' ? 'Overview' : (page.getAttribute('data-name') || '');
    if (TOPIC.indexOf(id) > -1) { read[id] = 1; try { localStorage.setItem(KEY, JSON.stringify(read)); } catch (e) {} }
    paint();
    side.open = !(isSim || isRobot || window.matchMedia('(max-width:780px)').matches);
    if (isRobot && window.ERobotUI) window.ERobotUI.open(+id.slice(5));
    window.scrollTo(0, 0);
  }
  if (window.ELabUI) window.ELabUI.init();
  if (window.ENotebookSearch) window.ENotebookSearch.init();
  if (window.ERobotUI) window.ERobotUI.init();
  if (window.EBlocks) { window.EBlocks.attach('sim', 'lab', window.ELabUI.blockHost()); window.EBlocks.attach('rs', 'robot', window.ERobotUI.blockHost()); }
  if (window.EBuildLog) window.EBuildLog.init();
  if (window.ECourse) window.ECourse.init();
  if (window.EParts) window.EParts.init();
  if (window.ETools) window.ETools.init();
  window.NB_CARDS = CARDS;
  if (window.EReading) window.EReading.init();
  addEventListener('hashchange', route);
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy]'); if (!b) return;
    var pre = document.getElementById(b.getAttribute('data-copy')), text = pre.textContent;
    function done(msg) { b.textContent = msg; setTimeout(function () { b.textContent = 'Copy code'; }, 1800); }
    function fallback() { var r = document.createRange(); r.selectNodeContents(pre); var s = getSelection(); s.removeAllRanges(); s.addRange(r); done('Selected: press Ctrl+C'); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { done('Copied'); }, fallback); else fallback();
  });
  route();

  addEventListener('keydown', function (e) {
    if (e.target.matches('input,select,textarea')) return;
    var cur = (location.hash || '').slice(1), i = TOPIC.indexOf(cur);
    if (i < 0) return;
    if (e.key === 'ArrowRight' && i < TOPIC.length - 1) location.hash = TOPIC[i + 1];
    if (e.key === 'ArrowLeft' && i > 0) location.hash = TOPIC[i - 1];
  });

  document.querySelectorAll('.quiz-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var right = 0, qs = form.querySelectorAll('.q-card');
      qs.forEach(function (q) {
        var pick = q.querySelector('input:checked'), fb = q.querySelector('.fb'), ok = pick && pick.value === q.getAttribute('data-c');
        if (ok) right++;
        fb.hidden = false; fb.className = 'fb ' + (ok ? 'ok' : 'no');
        fb.innerHTML = (ok ? 'Correct. ' : (pick ? 'Not quite. ' : 'Not answered. ')) + q.getAttribute('data-fb');
      });
      form.querySelector('.score').textContent = right + ' / ' + qs.length;
    });
    form.addEventListener('reset', function () {
      form.querySelectorAll('.fb').forEach(function (f) { f.hidden = true; });
      form.querySelector('.score').textContent = '';
    });
  });

  var deck = [], at = 0, back = false, fc = document.getElementById('fc'), deckSel = document.getElementById('deck');
  function draw() {
    if (!deck.length) return;
    var c = deck[at];
    fc.innerHTML = back ? '<span>' + c.d + '</span>' : '<b>' + c.t + '</b>';
    document.getElementById('fc-pos').textContent = 'Card ' + (at + 1) + ' of ' + deck.length + (back ? ', answer side' : ', tap to flip');
  }
  function load() { var v = deckSel.value; deck = CARDS.filter(function (c) { return v === 'all' || c.s === v || 'g:' + c.g === v; }); at = 0; back = false; draw(); }
  deckSel.addEventListener('change', load);
  fc.addEventListener('click', function () { back = !back; draw(); });
  document.getElementById('fc-next').addEventListener('click', function () { at = (at + 1) %% deck.length; back = false; draw(); });
  document.getElementById('fc-prev').addEventListener('click', function () { at = (at - 1 + deck.length) %% deck.length; back = false; draw(); });
  document.getElementById('fc-shuffle').addEventListener('click', function () {
    for (var i = deck.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = deck[i]; deck[i] = deck[j]; deck[j] = x; }
    at = 0; back = false; draw();
  });
  load();
})();
"""


def ul(items):
    return '<ul class="tight">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ans(a):
    return f'<details class="ans"><summary>Show model answer</summary><div class="ans-box">{a}</div></details>'


def topic_page(i, t):
    prev_ = TOPICS[i - 1] if i else None
    next_ = TOPICS[i + 1] if i < len(TOPICS) - 1 else None
    rows = "".join(f'<tr><td><strong>{a}</strong></td><td class="val">{b}</td><td>{c}</td></tr>' for a, b, c in t["props"])
    terms = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in t["terms"])
    prac = "".join(f'<li>{q} <span class="marks">({k})</span>{ans(a)}</li>' for q, k, a in t["practice"])
    bloom = "".join(
        f'<h3>{lv}</h3><ol class="q">' + "".join(f'<li>{q} <span class="marks">({code})</span></li>' for q in t[code.lower()]) + "</ol>"
        for lv, code in [("K2: Understanding", "K2"), ("K3: Applying", "K3"), ("K4: Analyzing", "K4")])
    nav = (f'<a href="#{prev_["slug"]}">&larr; Previous: {prev_["short"]}</a>' if prev_ else '<a href="#intro">&larr; Introduction</a>')
    nav += (f'<a href="#{next_["slug"]}">Next: {next_["short"]} &rarr;</a>' if next_ else '<a href="#flashcards">Next: Flashcards &rarr;</a>')
    return f"""
<section id="page-{t['slug']}" data-page data-name="Unit I topic {i + 1}" hidden>
<h1>{t['title']}</h1><p class="sub">{UNIT} &middot; Topic {i + 1}</p>
<h2>1. Overview</h2><p>{t['overview']}</p>
<figure><div class="fig-scroll">{figure(t['slug'])}</div><figcaption>Figure {i + 1}. {t['title']}: what it looks like and how it's drawn on a circuit diagram. Illustration, not to scale.</figcaption></figure>
<h2>2. Detailed Notes</h2>
<h3>2.1 Name and look</h3><p>{t['look']}</p>
<h3>2.2 Purpose</h3><p>{t['purpose']}</p>
<h3>2.3 Key properties</h3><div class="tw"><table><tr><th>Property</th><th>Unit or value</th><th>What it means</th></tr>{rows}</table></div>{tool_links(t['slug'])}
<h3>2.4 Example everyday usage</h3><p>{t['everyday']}</p>
<h3>2.5 Sample robotics application</h3><p>{t['robot']}</p>
<div class="safe"><h3>2.6 Handling and safety</h3>{ul(t['safety'])}</div>
<h2>3. Key Terms</h2><dl class="terms">{terms}</dl>
<div class="exam"><h2>Exam-Prep Summary</h2>{ul(t['exam'])}</div>
<h2>4. Practice Questions</h2><ol class="q">{prac}</ol>
<h2>5. Bloom's Taxonomy Level of Distribution</h2><p class="sub">Practice questions for this topic, organised by thinking level.</p>{bloom}
<h2>6. Practical Examples</h2><p class="sub">Build and test these in the simulator.</p><ol class="q" data-ex-topic="{t['slug']}"></ol>
<div class="pn">{nav}</div>
</section>"""


def home():
    cards = "".join(
        f'<a class="tc" href="#{t["slug"]}">{thumb(t["slug"])}<div><b>{t["short"]}</b><span>{t["blurb"]}</span></div></a>' for t in TOPICS)
    src = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in SOURCES)
    return f"""
<section id="page-home" data-page data-name="Unit I overview">
<h1>Electronics Study Notebook</h1><p class="sub">17 topics, 22 sensors, 12 coding lessons, 28 simulated examples, 25 robot exercises and {len(TOOLS)} live tools</p>
<p>Learn how electronics works, then use it to build a robot. This notebook is written for a young beginner working with an adult guide, and it starts from zero.</p>
<div class="links"><a href="#intro">New here? Read the Introduction first</a></div>
<h2>Unit I: essential parts</h2><div class="cards">{cards}</div>
<h2>Unit II: more core parts</h2><div class="cards c4">{"".join(f'<a class="tc" href="#{t["slug"]}">{thumb(t["slug"])}<div><b>{t["short"]}</b><span>{t["blurb"]}</span></div></a>' for t in UNIT2)}</div>
<h2>Learn and build</h2><div class="links"><a href="#coding">Coding Course: 12 lessons</a><a href="#lab">Practical Lab: 28 examples with a simulator</a><a href="#robots">Robot Exercises: 25 builds</a><a href="#sensors">Sensors: 22 explained</a><a href="#tools">Live Tools: {len(TOOLS)} calculators</a><a href="#buildlog">Build Log</a><a href="#faults">Fix It Guide</a></div>
<h2>For the adult guide</h2><div class="links"><a href="#guide">Guide's Handbook</a><a href="#guide-answers">Answer Keys</a><a href="#parts">Shopping List</a></div>
<h2>Study tools</h2><div class="links"><a href="#flashcards">Flashcards</a><a href="#assignments">Assignments</a><a href="#quiz">Quiz</a><a href="#notes">Notes</a><a href="#case-study">Case Study</a></div>
<h2>Before you start</h2>
<div class="safe"><h3>Four safety rules for every build</h3>{ul(["<strong>Check first.</strong> Your guide looks over the wiring before power goes on.", "<strong>Unplug to change.</strong> Disconnect all power before moving any wire.", "<strong>Hot, smelly or smoking? Unplug right away.</strong> Tell your guide and let it cool.", "<strong>Low power only.</strong> Use USB and AA batteries. Never connect anything here to a wall socket."])}</div>
<h2>Sources</h2><p class="sub">Specs were checked against these pages. Other figures, such as typical LED voltages and motor ranges, are general electronics knowledge and approximate. Check the sheet for your exact part.</p><ul class="tight">{src}</ul>
</section>"""


def flash():
    opts = "".join(f'<option value="{t["slug"]}">{t["short"]}</option>' for t in TOPICS)
    return f"""
<section id="page-flashcards" data-page data-name="Flashcards" hidden>
<h1>Flashcards</h1><p class="sub">Choose a deck: Unit I topics, sensors or robot terms</p>
<div class="fc-row"><label for="deck">Deck</label><select id="deck"><option value="g:topics">Unit I: all topics</option>{opts}<option value="g:topics2">Unit II: all topics</option>{"".join(f'<option value="{t["slug"]}">{t["short"]}</option>' for t in UNIT2)}<option value="g:sensors">All 22 sensors</option><option value="g:robots">Robot terms</option><option value="all">Everything</option></select></div>
<button class="fc" id="fc" type="button"></button><div class="print-only" id="fc-print"></div>
<div class="fc-row"><button class="alt" id="fc-prev" type="button">Previous</button><button id="fc-next" type="button">Next</button><button class="alt" id="fc-shuffle" type="button">Shuffle</button><span class="marks" id="fc-pos"></span></div>
</section>"""


def assignments():
    body = ""
    for title, task, a in ASSIGNMENTS:
        body += f"<h2>{title}</h2><p>{task}</p>" + (ans(a) if a else "")
    return f'<section id="page-assignments" data-page data-name="Assignments" hidden><h1>{UNIT}: Assignments</h1><p class="sub">Work through these with your guide.</p>{body}</section>'


def quiz_links():
    return '<div class="links"><a href="#quiz">Unit I quiz</a><a href="#quiz-unit2">Unit II quiz</a><a href="#quiz-sensors">Sensors quiz</a><a href="#quiz-robots">Robots quiz</a></div>'


def quiz_page(pid, name, title, sub_, questions, prefix):
    qs = ""
    for n, (q, opts, c, fb) in enumerate(questions, 1):
        ops = "".join(f'<label><input type="radio" name="{prefix}{n}" id="{prefix}{n}o{k}" value="{k}"><span>{o}</span></label>' for k, o in enumerate(opts))
        fb_attr = fb.replace('"', "&quot;")
        qs += f'<div class="q-card" data-c="{c}" data-fb="{fb_attr}"><p>{n}. {q}</p>{ops}<div class="fb" hidden></div></div>'
    return f"""<section id="{pid}" data-page data-name="{name}" hidden><h1>{title}</h1><p class="sub">{len(questions)} questions. {sub_}</p>{quiz_links()}
<form class="quiz-form">{qs}<button type="submit">Submit</button> <button class="alt" type="reset">Clear answers</button><span class="score"></span></form></section>"""


def quiz():
    return (quiz_page("page-quiz", "Quiz", f"{UNIT}: Quiz", "Choose an answer for each, then select Submit to see your score.", QUIZ, "q")
            + quiz_page("page-quiz-unit2", "Unit II Quiz", "Unit II: Quiz", "Test what you learned in Unit II.", UNIT2_QUIZ, "uq")
            + quiz_page("page-quiz-sensors", "Sensors Quiz", "Sensors Quiz", "Test what you know about the 22 sensors.", SENSOR_QUIZ, "sq")
            + quiz_page("page-quiz-robots", "Robots Quiz", "Robots Quiz", "Test what you learned from the robot exercises.", ROBOT_QUIZ, "rq"))


def notes():
    recap = "".join(f'<tr><td><a href="#{t["slug"]}"><strong>{t["short"]}</strong></a></td><td>{t["blurb"]}</td><td class="val">{t["props"][0][1]}</td></tr>' for t in TOPICS)
    body = "".join(f'<h3>{i + 1}. {t["title"]}</h3>{ul(t["exam"])}' for i, t in enumerate(TOPICS))
    return f"""<section id="page-notes" data-page data-name="Notes" hidden><h1>{UNIT}: Notes</h1><p class="sub">Key points from every topic, for quick revision.</p>
<h2>One-page recap</h2><div class="tw"><table><tr><th>Part</th><th>Its job</th><th>Main measure</th></tr>{recap}</table></div><h2>Key points by topic</h2>{body}</section>"""


def case():
    fx = ul(CASE["facts"])
    qs = "".join(f"<li>{q}{ans(a)}</li>" for q, a in CASE["qs"])
    return f"""<section id="page-case-study" data-page data-name="Case Study" hidden><h1>{UNIT}: Case Study</h1><p class="sub">{CASE['title']}</p>
<h2>The situation</h2><p>{CASE['intro']}</p><h2>What went wrong</h2>{fx}<h2>Questions</h2><ol class="q">{qs}</ol></section>"""


def sensor_pages():
    cats = ""
    for cat in SENSOR_CATS:
        group = [x for x in SENSORS if x["cat"] == cat]
        cards_ = "".join(f'<a class="tc" href="#sensor-{x["slug"]}">{sensor_thumb(x["slug"])}<div><b>{x["short"]}</b><span>{x["blurb"]}</span></div></a>' for x in group)
        cats += f'<h2>{cat} sensors</h2><div class="cards c{len(group)}">{cards_}</div>'
    overview = "".join(f'<tr><td><a href="#sensor-{x["slug"]}"><strong>{x["short"]}</strong></a></td><td>{x["input"]}</td><td>{x["otype"]}</td><td class="val">{x["model"]}</td></tr>' for x in SENSORS)
    types = [("Analog", "A voltage that rises and falls", "A0 to A5, using analogRead(). Gives 0 to 1023.", "LM35, LDR, soil probe"), ("Digital", "Only HIGH or LOW", "Any digital pin, using digitalRead().", "IR module, float switch"), ("Pulses", "A stream of on and off signals", "Time them or count them.", "HC-SR04, flow sensor, Geiger board"), ("I2C", "Numbers sent over two wires", "A4 (SDA) and A5 (SCL), using a library.", "MPU-6050, BMP280, VL53L0X"), ("One-wire or clocked data", "Numbers sent using a set timing", "Digital pins, using a library.", "DHT11, HX711")]
    rows = "".join(f"<tr><td><strong>{a}</strong></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in types)
    out = f"""<section id="page-sensors" data-page data-name="Sensors" hidden>
<h1>Sensors</h1><p class="sub">22 sensors in 6 groups, each with a picture, properties, inputs and outputs, a circuit and real-life examples</p>
<p><strong>A sensor turns something in the real world into a signal that a circuit can read.</strong> Every sensor here follows the same path: something in the world goes in, an electrical signal comes out, and the Arduino decides what to do.</p>
<div class="io-flow"><div><b>Input</b><span>Heat, light, sound, motion or gas</span></div><div><b>Sensor</b><span>Changes it into electricity</span></div><div><b>Output</b><span>A voltage, a pulse or data</span></div><div><b>Arduino</b><span>Reads it and acts on it</span></div></div>
<div class="links"><a href="#quiz-sensors">Take the Sensors quiz</a><a href="#flashcards">Flashcards</a></div>
<h2>How sensors talk to an Arduino</h2><div class="tw"><table><tr><th>Output type</th><th>What it is</th><th>How an Uno reads it</th><th>Examples</th></tr>{rows}</table></div>
{cats}
<h2>All sensors at a glance</h2><div class="tw"><table><tr><th>Sensor</th><th>Input</th><th>Output</th><th>Example part</th></tr>{overview}</table></div>
<h2>About the numbers</h2><p>Wherever a maker's data sheet could be found and read, these pages use its figures. Some low-cost modules have no maker's data sheet, so their figures come from brand documentation or community notes, and are less certain. Each sensor page says which it used. Modules from different makers can differ, so always check the sheet for your exact part. The code has been compile-checked in this notebook's simulator engine, but hasn't been run on these real sensors.</p>
<div class="tw"><table><tr><th>Sensor</th><th>Best source available</th><th>Type</th></tr>{"".join(f'<tr><td><a href="#sensor-{x["slug"]}">{x["short"]}</a></td><td>' + (f'<a href="{x["refs"][0][1]}">{x["refs"][0][0]}</a>' if x["refs"] else "General knowledge") + f'</td><td>{x["refs"][0][2] if x["refs"] else "No specific part or source"}</td></tr>' for x in SENSORS)}</table></div>
</section>"""
    for x in SENSORS:
        n = x["n"]
        prev_ = f'<a href="#sensor-{SENSORS[n - 2]["slug"]}">&larr; {SENSORS[n - 2]["short"]}</a>' if n > 1 else '<a href="#sensors">&larr; All sensors</a>'
        next_ = f'<a href="#sensor-{SENSORS[n]["slug"]}">{SENSORS[n]["short"]} &rarr;</a>' if n < len(SENSORS) else '<a href="#sensors">All sensors &rarr;</a>'
        refs_txt = " &middot; ".join('<a href="%s">%s</a> (%s)' % (u, n_, "maker's data sheet" if k.startswith("Maker") else k.lower()) for n_, u, k in x["refs"]) or "general electronics knowledge, because this page covers many kinds of part. Check the sheet for yours."
        props = "".join(f'<tr><td><strong>{a}</strong></td><td class="val">{b}</td><td>{c}</td></tr>' for a, b, c in x["props"])
        ex = "".join(f"<li><b>{a}</b>{b}</li>" for a, b in x["examples"])
        code = ""
        if x.get("code"):
            code = f'<div class="code-head"><h3>Sample code</h3><button type="button" class="alt" data-copy="sc-{n}">Copy code</button></div><pre class="code" id="sc-{n}" tabindex="0">{html_mod.escape(x["code"], quote=False)}</pre>'
        elif x.get("library"):
            code = f'<h3>Sample code</h3><p>This sensor needs a library for its data. Install <strong>{x["library"]}</strong> from the Arduino Library Manager, then open one of its examples.</p>'
        lab_id = x.get("lab") or {"temperature": "ex-26", "soil": "ex-27", "ir": "ex-28"}.get(x["slug"])
        lab = f'<p style="margin-top:12px"><strong>Try it:</strong> <a href="#{lab_id}">run this sensor in the Practical Lab</a>.</p>' if lab_id else ""
        out += f"""<section id="page-sensor-{x['slug']}" data-page data-name="Sensor {n}" hidden>
<h1>{x['title']}</h1><p class="sub">{x['cat']} &middot; Sensor {n} of {len(SENSORS)} &middot; Example part: {x['model']}</p>
<h2>1. Overview</h2><p>{x['overview']}</p>
<figure><div class="fig-scroll">{sensor_picture(x['slug'], x['alt'])}</div><figcaption>Figure S{n}. {x['title']}. Illustration, not to scale.</figcaption></figure>
<h2>2. Properties</h2><div class="tw"><table><tr><th>Property</th><th>Typical value</th><th>What it means</th></tr>{props}</table></div>
<h2>3. Input and output</h2>
<div class="io-flow"><div><b>Input</b><span>{x['input']}</span></div><div><b>Output</b><span>{x['output']}</span></div><div><b>Connects to</b><span>{x['conn']}</span></div><div><b>Then it can</b><span>{x['does']}</span></div></div>
<h2>4. Circuit diagram</h2><figure><div class="fig-scroll">{x['circuit']()}</div></figure>
{code}{lab}
<h2>5. Real-life examples</h2><ul class="real">{ex}</ul>
<div class="safe"><h3>6. Handling and safety</h3>{ul(x['safety'])}</div>
<h3>Think Like an Engineer</h3><p>{x['think']}</p>
<p class="src-note"><strong>Where these numbers come from:</strong> {refs_txt}</p>
<div class="pn">{prev_}{next_}</div>
</section>"""
    return out


def rsim_page():
    return """<section id="page-rsim" data-page data-name="Robot Simulator" hidden>
<p class="marks" style="margin:0 0 4px"><a href="#robots" id="rs-back">&larr; Back to this exercise</a></p>
<h1 id="rs-title"></h1><p class="sub" id="rs-sub" style="margin-bottom:6px"></p>
<div class="toolbar" role="toolbar" aria-label="Robot simulator tools">
<button type="button" id="rs-start">Start</button><button type="button" class="alt" id="rs-reset">Reset</button><button type="button" class="alt" id="rs-check">Check my code</button><span class="sep"></span>
<label for="rs-map">Floor <select id="rs-map"></select></label>
<button type="button" class="alt" id="rs-left" aria-label="Turn the start position left">Turn left</button><button type="button" class="alt" id="rs-right" aria-label="Turn the start position right">Turn right</button>
<label><input type="checkbox" id="rs-mis"> Uneven motors</label><span class="sep"></span>
<button type="button" class="alt" id="rs-restore">Restore code</button>
</div>
<p id="rs-status" role="status" style="font-size:14.5px;color:var(--soft);margin:0 0 10px;min-height:22px;max-width:none"></p>
<div class="confirm" id="rs-confirm" hidden><span>Restore the original code? Your changes to this exercise will be lost.</span><button type="button" id="rs-yes">Restore</button><button type="button" class="alt" id="rs-no">Keep my changes</button></div>
<div class="sim-grid"><div>
<canvas id="rs-canvas" role="img" aria-label="Top view of the robot on the floor. Wheel speeds, sensor readings and crashes are listed below it."></canvas>
<div id="rs-read"></div>
<div class="rs-ctl" id="rs-ctl-btn" hidden><button type="button" class="alt hold" id="rs-btn">Hold to press the start button</button></div>
<div class="rs-ctl" id="rs-ctl-gap" hidden><label for="rs-gap">Distance to your hand</label><input type="range" id="rs-gap" min="5" max="120" value="40" style="flex:1 1 150px;accent-color:var(--accent)"><output id="rs-gap-out">40 cm</output></div>
<div class="rs-ctl" id="rs-ctl-box" hidden><label><input type="checkbox" id="rs-box"> Lift the box off the track</label></div>
<div id="rs-msgs" aria-live="polite"></div>
</div><div>
<div class="code-top"><label class="code-label" for="rs-code" id="rs-codelabel">Arduino code</label><div class="code-tabs" id="rs-tabs" role="tablist" aria-label="Choose how to write the program"></div></div><div id="rs-blockmsg"></div><div class="blockbox" id="rs-blockbox" hidden></div><div class="code-box"><div id="rs-gutter" aria-hidden="true"></div><textarea id="rs-code" spellcheck="false" wrap="off" autocapitalize="off" autocomplete="off"></textarea></div>
<h3 style="margin-top:12px;margin-bottom:0">Serial Monitor</h3><pre id="rs-serial" aria-live="off"></pre><div id="rs-results" aria-live="polite"></div>
</div></div>
<h2>How close is this to a real robot?</h2>
<ul class="tight"><li><strong>It runs the same code.</strong> Pins, the sensor, the servo, line sensors and button behave as the exercises wire them.</li><li><strong>The physics are simple.</strong> The floor, wheel grip, batteries and motors are idealised. A real robot won't match these timings, so you'll still need to tune it.</li><li><strong>Uneven motors</strong> makes one motor weaker, so you can see why real robots curve.</li></ul>
<div class="pn" id="rs-pn"></div>
</section>"""


def buildlog_page():
    return """<section id="page-buildlog" data-page data-name="Build Log" hidden>
<h1>Build Log</h1><p class="sub">Record what happens when you build these on real parts</p>
<p>The simulator can't prove that a real circuit works. Real parts, loose wires and weak batteries all behave differently. So when you build something for real, record it here, along with anything you had to change.</p>
<p><strong id="log-sum"></strong></p>
<div class="links"><a href="#lab">Practical Lab</a><a href="#robots">Robot Exercises</a></div>
<p class="sub">Your log is saved only in this browser, and clearing your browser data removes it. Copy your results now and then to keep them safe.</p>
<button type="button" id="log-copy">Copy my results</button><textarea id="log-out" hidden readonly aria-label="Your build results"></textarea>
<h2>Practical Lab examples</h2><div class="tw"><table class="log-table" id="log-a"></table></div>
<h2>Robot exercises</h2><div class="tw"><table class="log-table" id="log-b"></table></div>
</section>"""


UNIT2_LABEL = "Unit II"


def unit2_topic(i, t):
    prev_ = UNIT2[i - 1] if i else None
    next_ = UNIT2[i + 1] if i < len(UNIT2) - 1 else None
    rows = "".join(f'<tr><td><strong>{a}</strong></td><td class="val">{b_}</td><td>{c}</td></tr>' for a, b_, c in t["props"])
    terms = "".join(f"<dt>{a}</dt><dd>{b_}</dd>" for a, b_ in t["terms"])
    prac = "".join(f'<li>{q} <span class="marks">({k})</span>{ans(a)}</li>' for q, k, a in t["practice"])
    bloom = "".join(f'<h3>{lv}</h3><ol class="q">' + "".join(f'<li>{q} <span class="marks">({code})</span></li>' for q in t[code.lower()]) + "</ol>" for lv, code in [("K2: Understanding", "K2"), ("K3: Applying", "K3"), ("K4: Analyzing", "K4")])
    nav = (f'<a href="#{prev_["slug"]}">&larr; Previous: {prev_["short"]}</a>' if prev_ else '<a href="#unit2">&larr; Unit II overview</a>')
    nav += (f'<a href="#{next_["slug"]}">Next: {next_["short"]} &rarr;</a>' if next_ else '<a href="#quiz-unit2">Next: Unit II Quiz &rarr;</a>')
    link_txt = "".join(f'<li><a href="#{a}">{b_}</a></li>' for a, b_ in t["links"])
    links = f'<h2>6. Practical Examples</h2><ol class="q">{link_txt}</ol>' if t["links"] else ""
    src = " &middot; ".join('<a href="%s">%s</a> (%s)' % (u, n_, "maker's data sheet" if k.startswith("Maker") else k.lower()) for n_, u, k in t["refs"]) or "general electronics knowledge. Check the sheet for your part."
    return f"""<section id="page-{t['slug']}" data-page data-name="Unit II topic {i + 1}" hidden>
<h1>{t['title']}</h1><p class="sub">{UNIT2_LABEL} &middot; Topic {i + 1}</p>
<h2>1. Overview</h2><p>{t['overview']}</p>
<figure><div class="fig-scroll">{figure(t['slug'])}</div><figcaption>Figure U{i + 1}. {t['title']}. Illustration, not to scale.</figcaption></figure>
<h2>2. Detailed Notes</h2>
<h3>2.1 Name and look</h3><p>{t['look']}</p><h3>2.2 Purpose</h3><p>{t['purpose']}</p>
<h3>2.3 Key properties</h3><div class="tw"><table><tr><th>Property</th><th>Unit or value</th><th>What it means</th></tr>{rows}</table></div>{tool_links(t['slug'])}
<h3>2.4 Example everyday usage</h3><p>{t['everyday']}</p><h3>2.5 Sample robotics application</h3><p>{t['robot']}</p>
<div class="safe"><h3>2.6 Handling and safety</h3>{ul(t['safety'])}</div>
<h2>3. Key Terms</h2><dl class="terms">{terms}</dl>
<div class="exam"><h2>Exam-Prep Summary</h2>{ul(t['exam'])}</div>
<h2>4. Practice Questions</h2><ol class="q">{prac}</ol>
<h2>5. Bloom's Taxonomy Level of Distribution</h2>{bloom}
{links}
<p class="src-note"><strong>Where these numbers come from:</strong> {src}</p>
<div class="pn">{nav}</div>
</section>"""


def unit2_pages():
    cards_ = "".join(f'<a class="tc" href="#{t["slug"]}">{thumb(t["slug"])}<div><b>{t["short"]}</b><span>{t["blurb"]}</span></div></a>' for t in UNIT2)
    recap = "".join(f'<tr><td><a href="#{t["slug"]}"><strong>{t["short"]}</strong></a></td><td>{t["blurb"]}</td><td class="val">{t["props"][0][1]}</td></tr>' for t in UNIT2)
    body = "".join(f'<h3>{i + 1}. {t["title"]}</h3>{ul(t["exam"])}' for i, t in enumerate(UNIT2))
    over = f"""<section id="page-unit2" data-page data-name="Unit II overview" hidden><h1>Unit II: More Core Parts</h1><p class="sub">8 topics on the parts that support your circuits and robot</p>
<p>Unit I covered the parts in most beginner circuits. This unit explains the parts that the Lab and robot exercises also rely on: how to get input from a person, make sound, protect a circuit, run motors, switch separate circuits and power it all safely.</p>
<div class="cards c4">{cards_}</div><div class="links"><a href="#quiz-unit2">Unit II Quiz</a><a href="#notes-unit2">Unit II Notes</a><a href="#flashcards">Flashcards</a></div></section>"""
    note = f"""<section id="page-notes-unit2" data-page data-name="Unit II Notes" hidden><h1>Unit II: Notes</h1><p class="sub">Key points from every topic, for quick revision.</p><h2>One-page recap</h2><div class="tw"><table><tr><th>Part</th><th>Its job</th><th>Main value</th></tr>{recap}</table></div><h2>Key points by topic</h2>{body}</section>"""
    return over + "".join(unit2_topic(i, t) for i, t in enumerate(UNIT2)) + note


def course_pages():
    tasks = {}
    idx = "".join(f'<li><a href="#code-{l["n"]}">{l["title"]}</a><span id="d{l["n"]}" data-done-for="t{l["n"]}-0" class="done"></span><span class="marks">{l["goal"]}</span></li>' for l in LESSONS)
    out = f"""<section id="page-coding" data-page data-name="Coding Course" hidden><h1>Arduino Coding Course</h1><p class="sub">12 short lessons. Run every example, then finish its task.</p>
<p>Each lesson has code you can run and change right here, plus a task that checks your answer. No hardware is needed. When you're ready, try the same ideas in the <a href="#lab">Practical Lab</a>. If typing feels hard at first, use the Blocks tab in the Lab, then look at the code it writes.</p>
<p><strong id="course-sum"></strong></p><ol class="ex-list">{idx}</ol>
<h2>What this course leaves out</h2><p>These lessons run in this notebook's simplified simulator, which covers common Arduino code. It doesn't run <em>switch</em>, Serial input or most libraries. Everything taught here also works on a real Arduino.</p></section>"""
    for l in LESSONS:
        n = l["n"]
        secs = "".join(f"<h3>{h}</h3>{c}" for h, c in l["sections"])
        io = l["io"]
        ctl = ""
        if 13 in io:
            ctl += '<span class="led-wrap"><span class="led-dot" data-led></span> Pin 13 LED</span>'
        if "button" in io:
            ctl += '<button type="button" class="alt hold" data-hold>Hold button (pin 2)</button>'
        if "dial" in io:
            ctl += f'<label class="ctl-chk">Dial (A0) <input type="range" id="dial-{n}" data-dial min="0" max="100" value="50"></label>'
        lab = f'<p><strong>See it with a circuit:</strong> <a href="#{l["lab"]}">open the matching Lab example</a>.</p>' if l["lab"] else ""
        task_html = ""
        for i, t_ in enumerate(l["tasks"]):
            tid = f"t{n}-{i}"
            tasks[tid] = {k: t_[k] for k in ("run", "expect") if k in t_}
            if "press" in t_:
                tasks[tid]["press"] = t_["press"]
            start = html_mod.escape(t_["start"], quote=False)
            task_html += f"""<h2>Your turn</h2><p>{t_['ask']}<span class="done" data-done-for="{tid}"></span></p>
<div class="runner" data-key="course-{tid}" data-task="{tid}"><label class="code-label" for="ta-{tid}">Your code</label><textarea id="ta-{tid}" class="run-code" rows="{min(16, t_['start'].count(chr(10)) + 2)}" spellcheck="false" wrap="off" autocapitalize="off" autocomplete="off">{start}</textarea>
<div class="run-row"><button type="button" data-run>Run</button><button type="button" data-check>Check my code</button><button type="button" class="alt" data-reset>Start again</button>{ctl}</div><div class="run-label">Serial Monitor</div><pre class="run-out" aria-live="off"></pre><div class="task-res" aria-live="polite"></div></div>
<details class="ans"><summary>Show a hint</summary><div class="ans-box">{t_['hint']}</div></details>
<details class="ans"><summary>Show a model answer</summary><div class="ans-box"><pre class="code">{html_mod.escape(t_['model'], quote=False)}</pre></div></details>"""
        prev_ = f'<a href="#code-{n - 1}">&larr; Lesson {n - 1}</a>' if n > 1 else '<a href="#coding">&larr; All lessons</a>'
        next_ = f'<a href="#code-{n + 1}">Lesson {n + 1} &rarr;</a>' if n < len(LESSONS) else '<a href="#lab">Practical Lab &rarr;</a>'
        out += f"""<section id="page-code-{n}" data-page data-name="Coding Lesson {n}" hidden><h1>Lesson {n}: {l['title']}</h1><p class="sub">{l['goal']}</p>{secs}
<h2>Try it</h2><p>Select Run. Then change something, and run it again.</p>
<div class="runner" data-key="course-ex{n}"><label class="code-label" for="ex-ta-{n}">Example code</label><textarea id="ex-ta-{n}" class="run-code" rows="{min(22, l['code'].count(chr(10)) + 2)}" spellcheck="false" wrap="off" autocapitalize="off" autocomplete="off">{html_mod.escape(l['code'], quote=False)}</textarea>
<div class="run-row"><button type="button" data-run>Run</button><button type="button" class="alt" data-reset>Start again</button>{ctl}</div><div class="run-label">Serial Monitor</div><pre class="run-out" aria-live="off"></pre></div>
{lab}{task_html}<div class="pn">{prev_}{next_}</div></section>"""
    return out, tasks


def guide_pages():
    sess = ""
    for i, (name, links, goal, prep, qs, watch, done) in enumerate(SESSIONS, 1):
        ls = " &middot; ".join(f'<a href="#{a}">{b_}</a>' for a, b_ in links)
        sess += f"""<details class="fault"><summary>Session {i}: {name}</summary><div class="ans-box"><p><strong>Goal:</strong> {goal}</p><p><strong>Use:</strong> {ls}</p><p><strong>Before the session:</strong> {prep}</p><p><strong>Questions to ask:</strong></p>{ul(qs)}<p><strong>Watch for:</strong> {watch}</p><p style="margin:0"><strong>Done when:</strong> {done}</p></div></details>"""
    mist = "".join(f"<tr><td><strong>{a}</strong></td><td>{b_}</td></tr>" for a, b_ in MISTAKES)
    rub = "".join(f"<tr><td><strong>{a}</strong></td><td>{b_}</td><td>{c}</td><td>{d}</td></tr>" for a, b_, c, d in RUBRIC)
    rans = "".join(f'<details class="fault"><summary>Exercise {r["n"]}: {r["title"]}</summary><div class="ans-box"><p><strong>Question:</strong> {r["think"]}</p><p style="margin:0"><strong>A good answer:</strong> {ROBOT_ANSWERS[r["n"]]}</p></div></details>' for r in ROBOTS)
    sans = "".join(f'<details class="fault"><summary>{x["short"]}</summary><div class="ans-box"><p><strong>Question:</strong> {x["think"]}</p><p style="margin:0"><strong>A good answer:</strong> {SENSOR_ANSWERS[x["slug"]]}</p></div></details>' for x in SENSORS)
    rules = ["Read the safety notes on any project page before the session, especially those marked for adult supervision.", "Check the wiring and battery direction before power goes on, every time.", "Keep this work to USB and AA batteries. Don't let any project connect to a wall socket.", "The Geiger counter and ECG projects need a capable adult throughout. Skip them if you're not comfortable with them.", "Treat gas, alcohol, radiation, pulse and ECG projects as learning only."]
    return f"""<section id="page-guide" data-page data-name="Guide's Handbook" hidden><h1>Guide's Handbook</h1><p class="sub">For the adult working with the student. No electronics experience is needed.</p>
<p><strong>Your job is to keep it safe and ask good questions. You don't need to know the answers.</strong> Learning alongside the student works well, and it shows them how to deal with not knowing something.</p>
<div class="links"><a href="#guide-answers">Answer keys</a><a href="#parts">Shopping List</a><a href="#faults">Fix It Guide</a><a href="#buildlog">Build Log</a></div>
<h2>How to run a session</h2><ol class="steps"><li><strong>Start by recalling.</strong> Ask what they remember from last time.</li><li><strong>Set one goal.</strong> Say what you'll have working by the end.</li><li><strong>Let them do it.</strong> Keep your hands off the parts, and let them make the mistakes.</li><li><strong>Check safety.</strong> Look over the wiring before power goes on.</li><li><strong>Finish with a question.</strong> Ask what they learned, and what they'd try next.</li></ol>
<div class="safe"><h3>Your safety checklist</h3>{ul(rules)}</div>
<h2>Suggested sessions</h2><p>This is a suggested order, not a schedule. A session of 45 to 60 minutes suits many students, but follow their pace, and split or repeat sessions freely.</p>{sess}
<h2>Common situations</h2><div class="tw"><table><tr><th>What you see</th><th>What to try</th></tr>{mist}</table></div>
<h2>Seeing progress</h2><p>Use this as a conversation, not a test.</p><div class="tw"><table><tr><th>Skill</th><th>Getting started</th><th>Growing</th><th>Confident</th></tr>{rub}</table></div>
</section><section id="page-guide-answers" data-page data-name="Answer Keys" hidden><h1>Answer Keys</h1><p class="sub">Good answers to the Think Like an Engineer questions</p>
<p>Many of these have more than one good answer. Accept any reasoning that makes sense, and ask the student to test it. Answers to practice questions and quizzes are on their own pages.</p><p><a href="#guide">&larr; Guide's Handbook</a></p>
<h2>Robot exercises</h2>{rans}<h2>Sensors</h2>{sans}</section>"""


def parts_page():
    groups = ""
    for gi, (stage, use, items) in enumerate(PARTS):
        rows = "".join(f'<tr><td><label class="ctl-chk"><input type="checkbox" id="pt-{gi}-{i}" data-part="{gi}-{i}" data-name="{html_mod.escape(name, quote=True)}"> {name}</label></td><td>{qty}</td><td>{why}</td></tr>' for i, (name, qty, why) in enumerate(items))
        groups += f'<h2>{stage}</h2><p class="sub">{use}</p><div class="tw"><table><tr><th>Part</th><th>How many</th><th>What it\'s for</th></tr>{rows}</table></div>'
    return f"""<section id="page-parts" data-page data-name="Shopping List" hidden><h1>Shopping List</h1><p class="sub">Buy in stages, and tick off what you have</p>
<p><strong>You don't need to buy anything to start.</strong> The simulators and lessons work in a browser. When you're ready, start with Stage 1. Many Arduino starter kits include most of it, so compare before buying separately.</p>
<p><strong id="parts-sum"></strong></p><button type="button" id="parts-copy">Copy what I still need</button><textarea id="parts-out" hidden readonly aria-label="Parts you still need" style="width:100%;height:120px;margin-top:8px;font:13px var(--mono);background:var(--panel);color:var(--text);border:1px solid var(--border);border-radius:6px;padding:8px"></textarea>
{groups}
<h2>Before you buy</h2><ul class="tight"><li><strong>Compatible boards:</strong> many low-cost Uno-style boards work well, but some need a USB driver, such as CH340.</li><li><strong>Uno R3 or R4:</strong> this notebook assumes an R3. An R4 works too, but it needs bigger LED resistors.</li><li><strong>Extra sensors:</strong> buy the other sensors only if a project needs them. Their pages explain the parts. The Geiger counter and ECG projects need adult supervision.</li><li><strong>Batteries:</strong> avoid lithium polymer (LiPo) packs for these projects. See <a href="#power">Batteries and Power</a>.</li><li><strong>Prices and stock</strong> vary a lot by country and seller, so this list doesn't give them.</li></ul></section>"""


def lab_pages():
    idx = """<section id="page-lab" data-page data-name="Practical Lab" hidden>
<h1>Practical Lab</h1><p class="sub">28 basic examples you can build, run and check in your browser</p>
<p>Each example opens on a virtual bench, with a real breadboard layout and Arduino code you can edit. Select <strong>Start Simulation</strong> to run it, and <strong>Check my build</strong> to test it. Change anything you like: move wires, swap resistors, or break it on purpose and read the warning.</p>
<div class="links"><a href="#ex-1">Start with Example 1</a><a href="#sandbox">Free build: a blank bench</a></div>
<div id="lab-index"></div>
<h2>How close is this to the real thing?</h2>
<ul class="tight"><li><strong>It really solves the circuit.</strong> Voltages and currents are calculated from your wiring, so a wrong connection fails much as it would on a real board.</li>
<li><strong>It runs common Arduino code.</strong> That includes variables, arrays, functions, loops, the Serial Monitor, the Servo library, tone() and pulseIn(). It doesn't run <em>switch</em>, Serial input, or other libraries.</li>
<li><strong>Parts are simplified.</strong> Motors, LEDs and transistors follow simple models, and PWM is approximated. Real parts vary, so always test on the real thing.</li>
<li><strong>A pass here isn't a guarantee.</strong> Your guide should still check a real circuit before it gets power.</li></ul>
<p>For circuits beyond these parts, rebuild them in <a href="https://www.tinkercad.com/circuits">Tinkercad Circuits</a>. The code here is standard Arduino code, so you can paste it straight in.</p>
</section>"""
    sim = """<section id="page-sim" data-page data-name="Practical Lab" hidden>
<p class="marks" style="margin:0 0 4px"><a href="#lab">&larr; All examples</a></p>
<h1 id="sim-title"></h1><p class="sub" id="sim-goal" style="margin-bottom:6px"></p>
<div class="toolbar" role="toolbar" aria-label="Simulator tools">
<button type="button" id="sim-start">Start Simulation</button><button type="button" class="alt" id="sim-check">Check my build</button><span class="sep"></span>
<button type="button" class="alt" id="tool-select">Select</button><button type="button" class="alt" id="tool-wire">Wire</button>
<select id="tool-add" aria-label="Add a part"></select>
<button type="button" class="alt" id="tool-delete">Delete</button><button type="button" class="alt" id="tool-undo">Undo</button><button type="button" class="alt" id="tool-restore">Restore</button><span class="sep"></span>
<label for="sim-board">Board <select id="sim-board"><option value="R3">Uno R3</option><option value="R4">Uno R4</option></select></label>
</div>
<p id="sim-status" role="status"></p>
<div class="confirm" id="restore-confirm" hidden><span>Restore the original circuit and code? Your changes to this example will be lost.</span><button type="button" id="restore-yes">Restore</button><button type="button" class="alt" id="restore-no">Keep my changes</button></div>
<div class="sim-grid"><div>
<div class="sim-canvas"><svg id="sim-svg" role="img" aria-label="Virtual bench with an Arduino Uno and a breadboard. The written steps below give the same layout."></svg></div>
<div id="sim-hole"></div><div id="sim-props" hidden></div><div id="sim-controls" hidden></div><div id="sim-msgs" aria-live="polite"></div>
</div><div>
<div class="code-top"><label class="code-label" for="sim-code" id="sim-codelabel">Arduino code</label><div class="code-tabs" id="sim-tabs" role="tablist" aria-label="Choose how to write the program"></div></div><div id="sim-blockmsg"></div><div class="blockbox" id="sim-blockbox" hidden></div><div class="code-box"><div id="sim-gutter" aria-hidden="true"></div><textarea id="sim-code" spellcheck="false" wrap="off" autocapitalize="off" autocomplete="off"></textarea></div>
<h3 id="sim-serial-h" style="margin-top:12px;margin-bottom:0">Serial Monitor</h3><pre id="sim-serial" aria-live="off"></pre><div id="sim-results" aria-live="polite"></div>
</div></div>
<div id="sim-notes"></div><div class="pn" id="sim-pn"></div>
</section>"""
    return idx + sim


def robot_pages():
    stages = [("Build", "Build the robot"), ("Move", "Make it move"), ("Add-ons", "Add a button, lights and a horn"), ("Sense", "Give it eyes"), ("Line", "Follow lines and finish the mission")]
    idx = ""
    for key, name in stages:
        group = [r for r in ROBOTS if r["stage"] == key]
        idx += f'<h2>{name}</h2><ol class="ex-list" start="{group[0]["n"]}">' + "".join(f'<li><a href="#robot-{r["n"]}">{r["title"]}</a><span class="marks">{r["goal"]}</span></li>' for r in group) + "</ol>"
    rules = ["<strong>Test on a box first.</strong> Run new code with the wheels off the ground.", "<strong>Work on the floor.</strong> A robot on a table can drive straight off the edge.", "<strong>Take out the batteries</strong> before changing wires, and when you've finished.", "<strong>Keep fingers and hair away</strong> from spinning wheels.", "<strong>Motor hot or smelling?</strong> Take out the batteries and find out why before trying again."]
    out = f"""<section id="page-robots" data-page data-name="Robot Exercises" hidden>
<h1>Robot Exercises</h1><p class="sub">25 hands-on builds, from an empty chassis to a complete mission</p>
<p>These are for a real robot, and each exercise builds on the one before. Every one has a picture and numbered steps, and most have complete code. Exercises 5 to 25 also run in the <strong>Robot Simulator</strong>, so you can watch your code drive a virtual robot before you build it. To try the electronics first, use the <a href="#lab">Practical Lab</a>.</p>
<div class="links"><a href="#rsim-6">Open the Robot Simulator</a><a href="#buildlog">Record your real builds</a><a href="#quiz-robots">Take the Robots quiz</a></div>
<div class="safe"><h3>Robot safety</h3>{ul(rules)}</div>
{idx}
<h2>Extra parts you'll need</h2><p>Beyond the nine parts in Unit I, this project uses a 2-wheel chassis kit with geared motors, an L9110S motor driver, a USB power bank, 2 line sensor modules, an active buzzer module and a push button. The <a href="#parts">Shopping List</a> has it all.</p>
</section>"""
    for r in ROBOTS:
        n = r["n"]
        prev_ = f'<a href="#robot-{n - 1}">&larr; Exercise {n - 1}</a>' if n > 1 else '<a href="#robots">&larr; All exercises</a>'
        next_ = f'<a href="#robot-{n + 1}">Exercise {n + 1} &rarr;</a>' if n < len(ROBOTS) else '<a href="#robots">All exercises &rarr;</a>'
        code = ""
        if r["code"]:
            code = f'<div class="code-head"><h3>The code</h3><button type="button" class="alt" data-copy="rc-{n}">Copy code</button></div><pre class="code" id="rc-{n}" tabindex="0">{html_mod.escape(r["code"], quote=False)}</pre>'
        steps = "".join(f"<li>{x}</li>" for x in r["steps"])
        sim_link = f'<div class="links" style="margin-top:12px"><a href="#rsim-{n}">Try this code in the Robot Simulator</a></div>' if r["code"] else ""
        out += f"""<section id="page-robot-{n}" data-page data-name="Robot Exercise {n}" hidden>
<h1>Exercise {n}: {r['title']}</h1><p class="sub">{r['stage']} stage &middot; About {r['time']}</p><p>{r['goal']}</p>
<figure><div class="fig-scroll">{r['fig']()}</div><figcaption>Figure R{n}. {r['title']}. Illustration, not to scale.</figcaption></figure>
<h3>What you need</h3>{ul(r['need'])}
<h3>Step by step</h3><ol class="steps">{steps}</ol>
{code}
{sim_link}
<div class="good-box"><h3>Check it worked</h3><p style="margin:0">{r['check']}</p></div>
<h3>Think Like an Engineer</h3><p>{r['think']}</p>
<div class="pn">{prev_}{next_}</div>
</section>"""
    return out


COURSE_HTML, COURSE_TASKS = course_pages()
side_topics = "".join(
    f'<li><a href="#{t["slug"]}"><span class="n">{i + 1}</span><span>{t["short"]}</span><span class="tick" id="tick-{t["slug"]}"></span></a></li>' for i, t in enumerate(TOPICS))
side_u2 = "".join(f'<li><a href="#{t["slug"]}"><span class="n">{i + 1}</span><span>{t["short"]}</span><span class="tick" id="tick-{t["slug"]}"></span></a></li>' for i, t in enumerate(UNIT2))
side_more = "".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in [("flashcards", "Flashcards"), ("assignments", "Assignments"), ("quiz", "Quiz"), ("notes", "Notes"), ("case-study", "Case Study")])

cards = [{"s": t["slug"], "g": "topics", "t": a, "d": b} for t in TOPICS for a, b in t["terms"]]
cards += [{"s": x["slug"], "g": "sensors", "t": x["short"], "d": f'Senses: {x["input"]}. Output: {x["otype"]}. Example part: {x["model"]}.'} for x in SENSORS]
cards += [{"s": "robots", "g": "robots", "t": a, "d": b} for a, b in ROBOT_CARDS]
cards += [{"s": t["slug"], "g": "topics2", "t": a, "d": b} for t in UNIT2 for a, b in t["terms"]]
js = JS % {"topics": json.dumps([t["slug"] for t in TOPICS + UNIT2]), "cards": json.dumps(cards, ensure_ascii=False)}

def _set(name, desc, pages, approx):
    return {"name": name, "desc": desc, "pages": pages, "approx": approx}


_u1 = [t["slug"] for t in TOPICS] + ["notes"]
_u2 = ["unit2"] + [t["slug"] for t in UNIT2] + ["notes-unit2"]
_sn = ["sensors"] + [f"sensor-{x['slug']}" for x in SENSORS]
_cd = ["coding"] + [f"code-{n}" for n in range(1, len(LESSONS) + 1)]
_rb = ["robots"] + [f"robot-{r['n']}" for r in ROBOTS]
_tl = ["tools"] + [f"tool-{t['slug']}" for t in TOOLS]
_gd = ["guide", "guide-answers", "parts"]
_all = ["home", "intro"] + _u1 + _u2 + _sn + _cd + ["lab"] + _rb + _tl + ["faults", "assignments", "quiz", "quiz-unit2", "quiz-sensors", "quiz-robots", "case-study"] + _gd
PRINT_SETS = {
    "unit1": _set("All of Unit I", "Every topic and the notes", _u1, PAGES["unit1"]),
    "unit2": _set("All of Unit II", "Every topic and the notes", _u2, PAGES["unit2"]),
    "sensors": _set("All sensors", "All 22 sensor pages", _sn, PAGES["sensors"]),
    "coding": _set("The whole Coding Course", "All 12 lessons", _cd, PAGES["coding"]),
    "robots": _set("All robot exercises", "All 25 builds", _rb, PAGES["robots"]),
    "tools": _set("All Live Tools", f"All {len(TOOLS)} tools", _tl, PAGES["tools"]),
    "guide": _set("The Guide's Handbook", "With answer keys and shopping list", _gd, PAGES["guide"]),
    "all": _set("The whole notebook", "Everything except the simulators", _all, PAGES["all"]),
}
FABS = (
    '<button type="button" class="nb-fab" id="nb-search-btn" data-tip="Search" aria-label="Search the notebook"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M16.5 16.5L21 21"/></svg></button>'
    '<button type="button" class="nb-fab" id="nb-print-btn" data-tip="Print" aria-label="Print" aria-haspopup="menu" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 8V3h10v5M7 17H4v-7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v7h-3"/><path d="M7 14h10v7H7z"/></svg></button>'
    '<a class="nb-fab" id="nb-home-btn" href="#home" data-tip="Home" aria-label="Home"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11l9-8 9 8"/><path d="M6 9.5V21h12V9.5"/></svg></a>'
    '<div id="nb-print-menu" role="menu" aria-label="Print"></div><div id="nb-scrim" hidden></div>'
)

LAB_JS = "\n".join(open(f, encoding="utf-8").read() for f in ["lab_engine.js", "lab_examples.js", "lab_ui.js", "robot_engine.js", "search.js", "blocks.js", "course.js", "tools.js", "reading.js"]) + "\nwindow.PRINT_SETS = " + json.dumps(PRINT_SETS, ensure_ascii=False) + ";\nwindow.NB_PUBLIC = 'https://leojai23.github.io/electronics-notebook/';\nwindow.COURSE_TASKS = " + json.dumps(COURSE_TASKS, ensure_ascii=False) + ";\nwindow.ROBOT_CODE = " + json.dumps({r["n"]: {"title": r["title"], "code": r["code"]} for r in ROBOTS if r["code"]}, ensure_ascii=False).replace("</", "<\\/") + ";\nwindow.ROBOT_TITLES = " + json.dumps({r["n"]: r["title"] for r in ROBOTS}, ensure_ascii=False) + ";\n" + open("robot_ui.js", encoding="utf-8").read()
ARROW_DEFS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><marker id="r-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--pt)"/></marker></defs></svg>'

html = f"""<title>Electronics Study Notebook</title>
<script>try{{var _r=localStorage.getItem('elec-reading');if(_r)document.documentElement.setAttribute('data-reading',_r);}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS}</style>
{DEFS}{ARROW_DEFS}
<header class="site"><div class="site-in"><a class="brand" href="#home">Electronics Study Notebook</a><div class="search" role="search"><input type="search" id="nb-search" placeholder="Search (press /)" aria-label="Search the notebook" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="nb-results"><div id="nb-results" role="listbox" hidden></div></div><span class="crumbs"><a href="#home">Home</a> / <span id="crumb">Overview</span></span><div class="reading" role="group" aria-label="Reading mode"><button type="button" data-set-reading="day">Day</button><button type="button" data-set-reading="sepia">Sepia</button><button type="button" data-set-reading="dark">Dark</button><button type="button" data-set-reading="night">Night</button></div></div></header>
<div class="layout" id="layout">
<details class="side" id="side"><summary>Contents</summary>
<ul style="margin-top:8px"><li><a href="#home">Home</a></li><li><a href="#intro">Introduction</a></li></ul>
<h3>Unit I: essential parts</h3><ol>{side_topics}</ol>
<h3>Unit II: more core parts</h3><ul><li><a href="#unit2">Unit II overview</a></li></ul><ol>{side_u2}</ol>
<h3>Sensors</h3><ul><li><a href="#sensors">All 22 sensors</a></li></ul>
<h3>Learn to code</h3><ul><li><a href="#coding">Coding Course</a></li></ul>
<h3>Build things</h3><ul><li><a href="#lab">Practical Lab</a></li><li><a href="#robots">Robot Exercises</a></li><li><a href="#tools">Live Tools</a></li><li><a href="#buildlog">Build Log</a></li></ul>
<h3>Study tools</h3><ul><li><a href="#faults">Fix It Guide</a></li>{side_more}</ul>
<h3>For the guide</h3><ul><li><a href="#guide">Guide's Handbook</a></li><li><a href="#parts">Shopping List</a></li></ul>
<div class="prog"><span id="prog-n"></span><div class="bar"><i id="prog-bar"></i></div></div>
</details>
<main>{home()}{"".join(topic_page(i, t) for i, t in enumerate(TOPICS))}{intro_page(ul, len(SENSORS), len(ROBOTS), 28)}{unit2_pages()}{COURSE_HTML}{guide_pages()}{parts_page()}{sensor_pages()}{lab_pages()}{robot_pages()}{rsim_page()}{tools_pages(thumb, ans, ul)}{buildlog_page()}{faults_page(ul)}{flash()}{assignments()}{quiz()}{notes()}{case()}</main>
</div>
<footer>Electronics Study Notebook</footer>
{FABS}
<script>{LAB_JS}</script>
<script>{js}</script>
"""
with open("electronics-study-notebook.html", "w", encoding="utf-8") as f:
    f.write(html)

# The offline copy adds install support and printing, which hosted pages can't use.
head = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon.svg" type="image/svg+xml"><meta name="theme-color" content="#0d6049">
<style>html,body{margin:0}img{max-width:100%}</style><script>window.BLOCKLY_SRC = 'vendor/blockly.min.js'; window.NB_CAN_PRINT = true;</script></head><body>
"""
tail = """
<script>if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) navigator.serviceWorker.register('sw.js');</script>
</body></html>
"""
with open("offline.html", "w", encoding="utf-8") as f:
    f.write(head + html + tail)

# When this runs inside the saved folder, refresh the installable copy next to it.
if os.path.exists(os.path.join("..", "manifest.webmanifest")):
    import hashlib, shutil
    shutil.copyfile("offline.html", os.path.join("..", "index.html"))
    stamp = hashlib.sha1((head + html + tail).encode("utf-8")).hexdigest()[:10]
    sw = open("sw.template.js", encoding="utf-8").read().replace("__STAMP__", stamp)
    with open(os.path.join("..", "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)
    print("saved folder updated, cache", stamp)
print("bytes", len(html.encode("utf-8")), "topics", len(TOPICS), "cards", len(cards))
