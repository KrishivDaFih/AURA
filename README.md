# AURA — Desktop Assistant (v1.0.0)

> **Renamed from Kairos.** Same app, same features — new name, new identity,
> and the version reset to 1.0.0 to mark the fresh start. Sections further down
> describe how each feature originally landed; where they cite old version
> numbers (1.0.1, 1.2.0, 1.4.x, 1.6.0), those are Kairos-era releases that all
> roll up into this 1.0.0.
>
> **Two things changed along with the name:**
> - Global hotkey is now **Ctrl + Shift + A** (was Ctrl + Shift + K).
> - Default wake word is now **"aura"** (was "kairos"). Editable in Settings.
>
> **Your old settings and chat history do not carry over.** Electron keys app
> data to the app identity, which changed, so AURA starts with an empty config.
> The old data is still on disk at `%APPDATA%\Kairos\` — `kairos-config.json`
> and `kairos-conversations.json`. To bring it across: install AURA, run it
> once, quit, then copy those two files into `%APPDATA%\AURA\` renamed to
> `aura-config.json` and `aura-conversations.json`. Your API keys live in the
> config file, so that also saves re-pasting them.

Multi-provider HUD assistant: Anthropic, OpenAI, or Groq. Wake word, global
hotkey, computer control, file attachments, custom connectors, and
persistent chat history.

## v1.7.0

- Frosted glass restored on the top bar, the Core / Directives / Protocol panels
  and the chat panel. It stays **off** the conversation drawer and the settings
  overlay: those two slide and fade, and blurring a layer while it animates over
  a repainting canvas is what made the colours strobe in the first place. The
  five surfaces that got the blur back never move, so they never re-composite
  mid-transition. Panel fills were thinned again (the opacity added when the
  blur was removed) so the aurora reads through the glass.
- Aurora drift slowed to 20x below its original speed.
- The background canvas is now capped at ~24fps. Each repaint forces every
  blurred layer to re-sample its backdrop, and at this drift speed the ribbons
  move only a few pixels a second, so the extra frames were pure cost.

## Fixes in this build

**Scrollbars.** The global stylesheet set `scrollbar-width` / `scrollbar-color` on
`*`. Chromium treats the standard scrollbar properties and the
`::-webkit-scrollbar-*` pseudo-elements as mutually exclusive — setting the
former on an element makes it ignore the latter. So the one rule meant to make
scrollbars thin was silently disabling every styled scrollbar in the app and
handing back the native white Windows bar. The standard properties are gone and
the webkit rules now apply everywhere. `color-scheme: dark` is also declared, so
any scrollbar or control the UA draws itself comes out dark instead of light.

**The menu strobing.** Six separate layers (top bar, rail panels, main panel,
conversation drawer, settings overlay, settings modal) each used
`backdrop-filter`, stacked over a canvas that repaints continuously. Every frame
forced all six to re-sample their backdrop, and the slide animation on top of
that is what made the colours flash instead of moving smoothly. Since the aurora
beneath is already soft, the blur was pure cost for no visual gain — all six are
now plain translucent or solid fills. The drawer also animates `transform`
rather than `left`, so it composites on the GPU instead of relaunching layout
every frame.

**Settings opening on launch.** Nothing opens it at startup now. If no provider
key is set, a dismissible hint appears above the composer instead; Settings only
opens when you click it, the hint, or when a send actually fails on a missing
key.

**Form controls.** Without `color-scheme: dark`, Chromium drew selects,
checkboxes and inputs in the OS light theme regardless of the CSS. Selects now
have a custom violet chevron, checkboxes are drawn from scratch rather than
inheriting the platform widget, and the primary button uses the blue-to-violet
gradient.

## The interface (rebuilt on the web AURA layout)

The old floating-HUD layout is gone — no more absolutely-positioned orb drifting
to a corner over a full-bleed background. The desktop app now uses the same
structure as the AURA web interface:

- **Top bar** — brand mark, wordmark with its expansion, a live state pill
  (Standby / Listening / Processing / Responding), clock, PC-control indicator,
  Settings.
- **Left rail** — three bordered panels with corner brackets. *Core* reports
  link state, active provider, session ID, exchange count and measured response
  latency. *Directives* holds four one-click prompts. *Protocol* shows persona,
  wake word and storage scope. A New session button sits at the foot.
- **Main panel** — a rounded, translucent panel holding the reactor stage, the
  transcript, and the composer. The reactor sits centred and large until your
  first message, then the whole stage collapses sideways into a compact header
  row with the session ID beside it.

**The rail readouts are real.** Link state and provider come from the actual
saved settings; exchanges are counted by observing the transcript; latency is
timed off the reactor's own thinking state. Nothing is a decorative fake
number, and none of it hooks into the chat logic — the rail *observes* the app
via MutationObserver, so the provider calls, tool execution, history and voice
code are untouched by the redesign.

The aurora field is now a fixed full-window layer behind everything, with the
panels translucent over it. Settings and the conversation sidebar moved to
window level so they overlay the whole app rather than one pane.

## AURA's own identity (not a repainted Kairos)

**Palette.** The cyan/navy HUD is gone. Surfaces are deep indigo-blue
(`#05060f` base, `#141a44` wash); the accent is violet `#9a7cff`, with a
secondary blue `#5f83ff` carrying structure and data. The reactor's plasma bed
runs violet at the core out to deep blue at the rim, so both colours are load-
bearing rather than one tinting the other. Warning states moved from orange to
rose, which sits correctly against violet.

**Aurora, not a starfield.** The old background was a flat dot field. AURA's is
its namesake: three light ribbons in blue and violet, each with its own hue,
amplitude, drift speed and phase, riding two summed sine waves so they never
loop visibly. They're drawn as bands between two curves and then blurred on the
canvas, which is what makes them read as light rather than as shapes — an
un-blurred band has a hard edge and looks like a stripe. A fine dust layer
drifts over the top with cursor parallax. Still Canvas 2D, still no WebGL.

**Boot sequence.** Launching AURA spins the core up before handing you the HUD:
the mark fades in under its own glow, four status lines report in, and a
progress bar fills — about three seconds, then it dissolves into the interface.

**Voice.** The wordmark carries its expansion (Adaptive Unified Response
Assistant) in tracked mono. Status vocabulary is AURA's own — Standby,
Listening, Processing, Responding — matching the web interface rather than the
generic "Thinking…". The system prompt gives it a defined character: calm and
quietly confident, dry rather than chirpy, acts first and reports the result
instead of narrating intentions.

## 1. Run from source

```
npm install
npm start
```

## 2. Or run the installer

`AURA-Setup-1.7.0.exe` is a real Windows installer (NSIS) — it walks you
through an install wizard, lets you pick the install folder, and adds a
**Start Menu entry, a Desktop shortcut, and an uninstaller** listed in
"Add or Remove Programs". Unsigned, so SmartScreen will still warn once:
**More info → Run anyway**.

The installer itself is styled to match the app: a generated app icon
(a small cyan reactor/orb mark), a branded header banner across the top of
each wizard page, and a full-height welcome/finish sidebar — same dark
navy + cyan palette as the HUD. All three live in `build/` as
`icon.ico`, `installerHeader.bmp` (150×57), and `installerSidebar.bmp`
(164×314) — those exact pixel dimensions are NSIS's fixed slots for these
images, so if you regenerate them, keep the same size.

`build/gen_assets.py` (Python + Pillow) is the script that drew these —
rerun it if you want to tweak the palette, wordmark, or add a proper
multi-layer vector icon later instead of the programmatically-drawn one.

### (Historical — superseded by the v1.6.0 reactor above)

### The orb was real 3D, not a flat SVG

You asked for the UI to feel more 3D, in the spirit of Zoey OS's
"living world" — a real spatial workspace rather than a flat dashboard.
I didn't copy Zoey OS's specific look (their layout, wordmark, and colors
are their own, trademarked design), but I took the part of the idea that
generalizes cleanly: your assistant should read as an actual object with
depth, not a 2D icon.

The orb is now rendered with [three.js](https://threejs.org) (WebGL) —
a rotating wireframe icosahedron shell around a real lit sphere core with
specular highlight, two independent counter-rotating shells for
parallax, and a soft additive glow layer. It genuinely responds to
depth-based lighting (two point lights, one key, one rim), not a
pre-baked gradient, so it looks different from every angle the camera
implicitly "sees" it from as it turns. Its spin speed and glow
intensity still map to the same states as before — idle, listening,
thinking, speaking — now interpolated smoothly frame-to-frame instead of
snapping between CSS animation durations.

Also given a 3D-ish treatment: the Settings modal now opens with a real
`rotateX` + perspective entrance instead of a flat fade, and chat bubbles
sit on a layered drop shadow and lift slightly on hover — small touches,
but they're in the same direction (real depth cues, not flat cards)
rather than the orb being the only 3D element in an otherwise flat app.

**three.js is vendored locally**, not loaded from a CDN — `renderer/vendor/three.module.js`
and `three.core.js` (~2MB total, MIT licensed) ship inside the app, so
the 3D orb works completely offline. Only the actual AI chat calls need
internet.

### v1.4.0 — more spatial, more human

You said the orb was looking bad and asked to make the whole UI look
fully like Zoey OS, same color. Two honest notes on how I approached
that, plus what actually changed:

**On "fully like Zoey OS":** Zoey OS's specific layout, wordmark, and
exact visual system are their own product's trademarked design — I
didn't clone it wholesale (their companions-orbiting-you world view,
their exact panel arrangement, their branding). What I did take is the
part of the ask that isn't proprietary to them: the general idea that an
AI assistant's interface can feel like an actual spatial environment with
depth, rather than a flat 2D dashboard with a decorative icon. If there's
a specific structural piece of their design you want (a particular
panel behavior, a specific interaction), tell me exactly what and I'll
build AURA's own version of it — just not a wholesale visual clone.

**What actually changed** (verified with real screenshots, since "make it
look better" only means something if I check rather than assume):

- The orb itself: smoother wireframe geometry, two tilted orbiting rings
  for a distinct silhouette, a glassy clearcoat material on the core so
  it has a real specular highlight instead of a flat gradient, and subtle
  parallax — it tilts slightly toward your cursor, like it's aware of you.
- A new drifting particle field runs behind the entire app (a second,
  separate 3D scene, kept dim and slow so it adds depth without fighting
  chat readability) — the "open space" feeling Zoey OS's world view is
  going for, done as AURA's own ambient background rather than their
  literal orbiting-companions layout.
- Chat bubbles, the settings modal, and the history panel all got a
  genuine glass treatment (backdrop blur + translucency + layered
  shadows) instead of flat solid panels, so the depth language is
  consistent across the whole app, not just the orb.
- Same cyan/navy palette throughout, as asked — nothing about the color
  identity changed, only the materials and depth.

**Voice**: the TTS voice is no longer whatever the browser defaults to.
Settings → Voice → "Auto" now scores your OS's installed voices and
picks the deepest available male one (matching common good voices like
Daniel, Ryan, Guy, David across Windows/macOS naming conventions), and
speaks slightly slower and lower-pitched than default — aiming for calm
and human rather than a chipper assistant voice. You can also pick a
specific installed voice from the dropdown if you'd rather choose
yourself. Available voices depend entirely on what's installed on your
Windows machine — if the built-in options all sound thin, installing a
better Windows voice pack (Settings → Time & Language → Speech, on
Windows) will show up here automatically.

### v1.4.1 — activity readout + voice preview

Small follow-up pass:

- A small "Idle / Listening… / Thinking… / Speaking…" label now sits under
  the docked orb once you're in chat mode — a lightweight activity readout
  in AURA's own style, not a copy of any specific product's widget chrome.
- Settings → Voice now has a **▶ Test** button next to the voice dropdown,
  so you can preview any installed voice immediately without saving
  first — useful since voice quality is entirely dependent on what's
  installed on your Windows machine and the only way to judge "does this
  sound human enough" is to actually hear it.

## The arc reactor core

The orb is gone. In its place is a **Mark 50-style arc reactor**, built from
your reference image: an armored shield housing, a hexagonal centre module
with hex shoulder plates, side mounting lugs, a glowing cyan glass bed, nested
chevron struts, and a bright triangular core.

**The shark corners are in.** Those angled armor blocks along the lower-left
and lower-right edges — chevron on top, five gill vents below — are drawn as a
single mirrored group (`#rxGill`) rotated onto the exact angle of the body's
lower edge (56.5°), so they sit flush against the frame instead of being
bolted on at an eyeballed angle.

### How it's built

The whole reactor is **one SVG, no images and no WebGL**. The silhouette is
defined once as `#rxBody` and every concentric ring — bevel, glass well,
glass rim — is that same path re-scaled about the reactor's centre, which is
why the frame stays perfectly concentric at any size. The interior (struts,
core triangle, scan sweep) is clipped to the glass outline, so nothing can
spill over the housing.

**three.js is now gone entirely**, and so is `renderer/vendor/` (~2MB). The
reason: the old orb was a live WebGL scene, which is the part that rendered
blank or blobby on some GPUs. An SVG reactor has no driver surface to fail on
— it either draws or the whole page doesn't. The ambient particle field behind
the app was also WebGL; it's been rewritten in **Canvas 2D** (110 drifting
dots with parallax on cursor movement), which looks the same and costs a
fraction of a frame.

### States

The reactor still reflects what AURA is doing, driven purely by CSS classes
on `#orbWrap` — no JS animation loop:

| State | Glass pulse | Scan sweep | Glow |
|---|---|---|---|
| Idle | 4.6s | 6s | soft |
| Listening | 2.4s | 3.2s | raised |
| Thinking | 1.0s | 1.3s | hard, wider drop-shadow |
| Speaking | 1.8s | 2.4s | hard |

It still docks: centred and large on launch, shrinking to the top-left corner
with an activity label underneath once you're in a conversation.

### Matching art

`build/gen_assets.py` now draws the reactor instead of the old orb, using the
same geometry constants as the SVG — so the app icon, the installer header
banner, and the welcome sidebar all show the same mark. The top-left brand
mark in the app is a miniature of it too.

## 3. What's new since 1.0.1

**PC control no longer confirms most actions — with two exceptions.**
You asked for it to stop asking permission, and for everything except two
tools, it now does: opening an app/URL, clipboard, screenshots, volume,
and screen lock all run **instantly**, no dialog, when "Allow AURA to
control this computer" is on.

The two exceptions are **`run_command`** (raw shell access) and calling a
**connector** — these still always show a confirmation dialog, regardless
of the "ask before each action" setting. My reasoning: those two aren't
"one specific action" the way opening Notepad is — `run_command` can do
literally anything a terminal can, and a connector call can hit an
external account using credentials you've stored. I didn't think it was
right to make those silent by default. If you disagree, it's a one-line
change: open `main.js`, find `const ALWAYS_CONFIRM = new Set(['run_command'])`
near `executeTool`, and remove `run_command` from that set (and drop the
`|| name.startsWith('connector_')` condition on the line just below it if
you want connectors silent too). I'm flagging exactly where rather than
just doing it, since silently removing the last confirmation on the two
most open-ended tools isn't something I want to do without you seeing it
first.

**File attachments.** A paperclip button next to the mic lets you attach
one file per message — text/code files get read and included inline,
images (PNG/JPG/GIF/WebP, up to 5MB) get sent as real vision input on
Anthropic and OpenAI. Groq's OpenAI-compatible endpoint accepts the same
image format, but whether it actually *works* depends on whether your
selected Groq model supports vision — check their model list.

**Connectors.** Settings → Connectors → add a name, description, HTTP
method, URL, and optional headers. AURA gets a tool it can call with a
JSON payload; whatever the endpoint returns comes back as the result. This
is a generic webhook bridge — wire it to Zapier, Make, Home Assistant, or
anything else that takes an HTTP call. There's no OAuth flow here, just
raw HTTP with headers you supply (e.g. `Authorization: Bearer ...`),
so treat the URL/headers fields like you would any place you'd paste a
secret.

**Persistent chat history.** The hamburger icon (top-left) opens a
conversation sidebar — every chat auto-saves after each exchange, titled
from your first message. Click "+ New chat" to start fresh, click any past
conversation to reload it, or delete ones you don't want kept. Everything
is stored locally in your app-data folder — nothing is synced anywhere.

## 4. Provider keys

Settings → provider dropdown → paste the matching key. Same three as
before (Anthropic / OpenAI / Groq), stored separately so switching doesn't
erase the others.

## 5. Package your own exe

```
npm run dist
```

Builds whatever `build.win.target` in `package.json` says — currently
`nsis`. Building this on the target OS (Windows itself) is still the most
reliable path; building cross-platform from Linux works here because Wine
is installed in this build environment, but that's an extra moving part
you don't need if you build on your own Windows machine.

## Project structure

```
aura-desktop/
├── package.json     — app metadata + build config (v1.0.0)
├── main.js          — window, settings, all provider calls, tool execution, connectors, history storage
├── preload.js       — secure bridge between main.js and the UI
├── renderer/
│   └── index.html   — HUD/chat UI, arc reactor SVG, settings modal, attachments, history sidebar
├── build/
│   ├── icon.ico             — app icon (used for the exe, taskbar, shortcuts)
│   ├── installerHeader.bmp  — 150×57 banner shown on each installer page
│   ├── installerSidebar.bmp — 164×314 image on the welcome/finish pages
│   └── gen_assets.py        — regenerates the three images above
└── README.md
```
