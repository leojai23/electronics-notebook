# Builds the single-file Electronics Study Notebook.
import html as html_mod, json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from figures import figure, thumb, DEFS
from content_a import TOPICS_A
from content_b import TOPICS_B, QUIZ, ASSIGNMENTS, CASE, SOURCES
from robots import R as ROBOTS
from intro import intro_page
from extras import SENSOR_QUIZ, ROBOT_QUIZ, ROBOT_CARDS, faults_page
from sensors import S as SENSORS, CATS as SENSOR_CATS
from sensor_art import picture as sensor_picture, thumb as sensor_thumb

TOPICS = TOPICS_A + TOPICS_B
UNIT = "Unit I"

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
  --cap:#20335c; --cap-d:#142242; --stripe:#d9dce3; --ceramic:#c8782f; --ceramic-d:#96591f; --white:#ffffff; --mesh:#6f777c;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg:#101613; --panel:#18211d; --text:#e4ece7; --soft:#a1b1a9; --border:#2c3a34;
  --accent:#62d0a8; --accent-soft:#1d3a30; --on-accent:#08231a; --warn:#f0b36a; --warn-soft:#33260f; --good:#62d0a8; --bad:#ff8a80; color-scheme:dark } }
:root[data-theme="dark"] {
  --bg:#101613; --panel:#18211d; --text:#e4ece7; --soft:#a1b1a9; --border:#2c3a34;
  --accent:#62d0a8; --accent-soft:#1d3a30; --on-accent:#08231a; --warn:#f0b36a; --warn-soft:#33260f; --good:#62d0a8; --bad:#ff8a80; color-scheme:dark }
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
.layout.wide ~ #print-btn { display:none }
.code-top { display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:6px; margin-bottom:6px } .code-top .code-label { margin:0 } .code-tabs { display:flex; gap:4px } .code-tabs button { padding:4px 12px; font-size:14px }
.blockbox { height:460px; border:1px solid var(--border); border-radius:6px; overflow:hidden; margin-bottom:8px } .code-box.short { height:210px } .sim-grid.blocks-on { grid-template-columns:minmax(0,1fr) minmax(0,1.15fr) } .src-note { font-size:13.5px; color:var(--soft); margin-top:14px; max-width:none }
@media (max-width:1040px) { .sim-grid.blocks-on { grid-template-columns:minmax(0,1fr) } }
.badge { display:inline-block; background:var(--accent-soft); color:var(--accent); border-radius:999px; padding:2px 10px; font-size:13px; font-weight:700 }
.cards.c4 { grid-template-columns:repeat(4,minmax(0,1fr)) } .cards.c3 { grid-template-columns:repeat(3,minmax(0,1fr)) } .cards.c2 { grid-template-columns:repeat(2,minmax(0,1fr)) }
.cards.c5 { grid-template-columns:repeat(6,minmax(0,1fr)) } .cards.c5 > a { grid-column:span 2 } .cards.c5 > a:nth-child(n+4) { grid-column:span 3 }
.tc b { overflow-wrap:anywhere }
@media (max-width:1100px) { .cards.c4 { grid-template-columns:repeat(2,minmax(0,1fr)) } }
.real { list-style:none; padding:0; margin:6px 0; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px } .real li { background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:9px 12px; min-width:0 } .real b { display:block; font-family:var(--display) }
@media (max-width:780px) { .io-flow { grid-template-columns:repeat(2,minmax(0,1fr)) } .cards.c4, .cards.c3 { grid-template-columns:repeat(2,minmax(0,1fr)) } .cards.c5 { grid-template-columns:repeat(2,minmax(0,1fr)) } .cards.c5 > a, .cards.c5 > a:nth-child(n+4) { grid-column:span 1 } .cards.c5 > a:last-child, .cards.c3 > a:last-child { grid-column:span 2 } }
@media (max-width:460px) { .real { grid-template-columns:minmax(0,1fr) } }
@media print {
  :root:root:root { --bg:#fff; --panel:#fff; --text:#000; --soft:#333; --border:#999; --accent:#0d6049; --accent-soft:#e7f0ec; --warn:#7a3f05; --warn-soft:#f7efe3; color-scheme:light }
  .site, .side, footer, .pn, .toolbar, .links, button, #sim-status, #print-btn { display:none !important }
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
    var navId = isSim ? 'lab' : (isRobot || /^robot-/.test(id)) ? 'robots' : /^sensor-/.test(id) ? 'sensors' : /^quiz/.test(id) ? 'quiz' : id;
    links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + navId); });
    crumb.textContent = id === 'home' ? 'Unit I overview' : (page.getAttribute('data-name') || '');
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
  addEventListener('beforeprint', function () { document.querySelectorAll('details.ans').forEach(function (d) { d.setAttribute('data-was', d.open ? '1' : ''); d.open = true; }); });
  addEventListener('afterprint', function () { document.querySelectorAll('details.ans').forEach(function (d) { d.open = d.getAttribute('data-was') === '1'; }); });
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
<section id="page-{t['slug']}" data-page data-name="Topic {i + 1}" hidden>
<h1>{t['title']}</h1><p class="sub">{UNIT} &middot; Topic {i + 1}</p>
<h2>1. Overview</h2><p>{t['overview']}</p>
<figure><div class="fig-scroll">{figure(t['slug'])}</div><figcaption>Figure {i + 1}. {t['title']}: what it looks like and how it's drawn on a circuit diagram. Illustration, not to scale.</figcaption></figure>
<h2>2. Detailed Notes</h2>
<h3>2.1 Name and look</h3><p>{t['look']}</p>
<h3>2.2 Purpose</h3><p>{t['purpose']}</p>
<h3>2.3 Key properties</h3><div class="tw"><table><tr><th>Property</th><th>Unit or value</th><th>What it means</th></tr>{rows}</table></div>
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
<h1>Electronics Study Notebook</h1><p class="sub">{UNIT}: Essential Components &middot; 9 topics, 22 sensors, 28 simulated examples and 25 robot exercises</p>
<p>Learn how electronics works, then use it to build a robot. This notebook is written for a young beginner working with an adult guide, and it starts from zero.</p>
<div class="links"><a href="#intro">New here? Read the Introduction first</a></div>
<h2>Unit I topics</h2><div class="cards">{cards}</div>
<h2>Build things</h2><div class="links"><a href="#lab">Practical Lab: 28 examples with a simulator</a><a href="#robots">Robot Exercises: 25 builds</a><a href="#sensors">Sensors: 22 explained</a><a href="#buildlog">Build Log</a><a href="#faults">Fix It Guide</a></div>
<h2>More for this unit</h2><div class="links"><a href="#flashcards">Flashcards</a><a href="#assignments">Assignments</a><a href="#quiz">Quiz</a><a href="#notes">Notes</a><a href="#case-study">Case Study</a></div>
<h2>Before you start</h2>
<div class="safe"><h3>Four safety rules for every build</h3>{ul(["<strong>Check first.</strong> Your guide looks over the wiring before power goes on.", "<strong>Unplug to change.</strong> Disconnect all power before moving any wire.", "<strong>Hot, smelly or smoking? Unplug right away.</strong> Tell your guide and let it cool.", "<strong>Low power only.</strong> Use USB and AA batteries. Never connect anything here to a wall socket."])}</div>
<h2>Sources</h2><p class="sub">Specs were checked against these pages. Other figures, such as typical LED voltages and motor ranges, are general electronics knowledge and approximate. Check the sheet for your exact part.</p><ul class="tight">{src}</ul>
</section>"""


def flash():
    opts = "".join(f'<option value="{t["slug"]}">{t["short"]}</option>' for t in TOPICS)
    return f"""
<section id="page-flashcards" data-page data-name="Flashcards" hidden>
<h1>Flashcards</h1><p class="sub">Choose a deck: Unit I topics, sensors or robot terms</p>
<div class="fc-row"><label for="deck">Deck</label><select id="deck"><option value="g:topics">Unit I: all topics</option>{opts}<option value="g:sensors">All 22 sensors</option><option value="g:robots">Robot terms</option><option value="all">Everything</option></select></div>
<button class="fc" id="fc" type="button"></button>
<div class="fc-row"><button class="alt" id="fc-prev" type="button">Previous</button><button id="fc-next" type="button">Next</button><button class="alt" id="fc-shuffle" type="button">Shuffle</button><span class="marks" id="fc-pos"></span></div>
</section>"""


def assignments():
    body = ""
    for title, task, a in ASSIGNMENTS:
        body += f"<h2>{title}</h2><p>{task}</p>" + (ans(a) if a else "")
    return f'<section id="page-assignments" data-page data-name="Assignments" hidden><h1>{UNIT}: Assignments</h1><p class="sub">Work through these with your guide.</p>{body}</section>'


def quiz_links():
    return '<div class="links"><a href="#quiz">Unit I quiz</a><a href="#quiz-sensors">Sensors quiz</a><a href="#quiz-robots">Robots quiz</a></div>'


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
<h3 style="margin-top:12px;margin-bottom:0">Serial Monitor</h3><pre id="sim-serial" aria-live="off"></pre><div id="sim-results" aria-live="polite"></div>
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
<h2>Extra parts you'll need</h2><p>Beyond the nine parts in Unit I, this project uses a 2-wheel chassis kit with geared motors, an L9110S motor driver, a USB power bank, 2 line sensor modules, an active buzzer and a push button.</p>
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


side_topics = "".join(
    f'<li><a href="#{t["slug"]}"><span class="n">{i + 1}</span><span>{t["short"]}</span><span class="tick" id="tick-{t["slug"]}"></span></a></li>' for i, t in enumerate(TOPICS))
side_more = "".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in [("flashcards", "Flashcards"), ("assignments", "Assignments"), ("quiz", "Quiz"), ("notes", "Notes"), ("case-study", "Case Study")])

cards = [{"s": t["slug"], "g": "topics", "t": a, "d": b} for t in TOPICS for a, b in t["terms"]]
cards += [{"s": x["slug"], "g": "sensors", "t": x["short"], "d": f'Senses: {x["input"]}. Output: {x["otype"]}. Example part: {x["model"]}.'} for x in SENSORS]
cards += [{"s": "robots", "g": "robots", "t": a, "d": b} for a, b in ROBOT_CARDS]
js = JS % {"topics": json.dumps([t["slug"] for t in TOPICS]), "cards": json.dumps(cards, ensure_ascii=False)}

LAB_JS = "\n".join(open(f, encoding="utf-8").read() for f in ["lab_engine.js", "lab_examples.js", "lab_ui.js", "robot_engine.js", "search.js", "blocks.js"]) + "\nwindow.ROBOT_CODE = " + json.dumps({r["n"]: {"title": r["title"], "code": r["code"]} for r in ROBOTS if r["code"]}, ensure_ascii=False).replace("</", "<\\/") + ";\nwindow.ROBOT_TITLES = " + json.dumps({r["n"]: r["title"] for r in ROBOTS}, ensure_ascii=False) + ";\n" + open("robot_ui.js", encoding="utf-8").read()
ARROW_DEFS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><marker id="r-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--pt)"/></marker></defs></svg>'

html = f"""<title>Electronics Study Notebook</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS}</style>
{DEFS}{ARROW_DEFS}
<header class="site"><div class="site-in"><a class="brand" href="#home">Electronics Study Notebook</a><div class="search" role="search"><input type="search" id="nb-search" placeholder="Search (press /)" aria-label="Search the notebook" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="nb-results"><div id="nb-results" role="listbox" hidden></div></div><span class="crumbs"><a href="#home">Home</a> / {UNIT} / <span id="crumb">Unit I overview</span></span></div></header>
<div class="layout" id="layout">
<details class="side" id="side"><summary>Unit I contents</summary>
<ul style="margin-top:8px"><li><a href="#home">Unit I overview</a></li><li><a href="#intro">Introduction</a></li></ul>
<h3>Unit I topics</h3><ol>{side_topics}</ol>
<h3>Sensors</h3><ul><li><a href="#sensors">All 22 sensors</a></li></ul>
<h3>Build things</h3><ul><li><a href="#lab">Practical Lab</a></li><li><a href="#robots">Robot Exercises</a></li><li><a href="#buildlog">Build Log</a></li></ul>
<h3>Study tools</h3><ul><li><a href="#faults">Fix It Guide</a></li>{side_more}</ul>
<div class="prog"><span id="prog-n"></span><div class="bar"><i id="prog-bar"></i></div></div>
</details>
<main>{home()}{"".join(topic_page(i, t) for i, t in enumerate(TOPICS))}{intro_page(ul, len(SENSORS), len(ROBOTS), 28)}{sensor_pages()}{lab_pages()}{robot_pages()}{rsim_page()}{buildlog_page()}{faults_page(ul)}{flash()}{assignments()}{quiz()}{notes()}{case()}</main>
</div>
<footer>Unit I: Essential Components</footer>
<script>{LAB_JS}</script>
<script>{js}</script>
"""
with open("electronics-study-notebook.html", "w", encoding="utf-8") as f:
    f.write(html)

# The offline copy adds install support and a print button, which hosted pages can't use.
head = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon.svg" type="image/svg+xml"><meta name="theme-color" content="#0d6049">
<style>html,body{margin:0}img{max-width:100%}</style><script>window.BLOCKLY_SRC = 'vendor/blockly.min.js';</script></head><body>
"""
tail = """
<button type="button" id="print-btn" style="position:fixed;right:16px;bottom:16px;z-index:5">Print this page</button>
<script>if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) navigator.serviceWorker.register('sw.js');
document.getElementById('print-btn').addEventListener('click', function () { window.print(); });</script>
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
