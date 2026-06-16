# Waveshare ESP32-P4 86-Panel — Home Assistant LVGL Wall Panel

An ESPHome firmware + Home Assistant config for the **Waveshare ESP32-P4-86-Panel**:
a 720×720 round-cornered touchscreen wall panel that runs a full LVGL UI and a
local voice assistant, talking to Home Assistant over the native API.

It's built as a stack of small, composable ESPHome **packages** — a hardware
contract, a device-core foundation, the voice/audio stack, and one package per
screen — so you can enable or drop features without forking the whole config.
All of your installation-specific entities live in a single
[`esphome/modules/user-config.yaml`](esphome/modules/user-config.yaml) file.

> This is a genericized, public version of a working personal panel. The page
> code is shipped as-is; the entity IDs it reads are surfaced as configurable
> substitutions so you can point it at your own Home Assistant.

---

## Features

| Screen | What it shows / does |
|--------|----------------------|
| **Home** | Clock, battery state-of-charge ring, now-playing media with album art, quick room/playlist pickers |
| **Energy** | Live solar / battery / grid power and a daily energy-flow (Sankey-style) breakdown |
| **Climate** | Heat-pump / thermostat control: setpoint, current temp, humidity, flow & hot-water temps |
| **Lights** | Four configurable light toggles (incl. the panel's own backlight) |
| **Security** | Alarm panel — arm home/away/night and a PIN keypad to disarm |
| **Screensaver** | Terminal-style clock + weather forecast, shown on idle |

Plus:
- **Voice assistant** — on-device micro-wake-word (`okay_nabu`, `hey_jarvis`, …) or
  HA-side wake word, with on-device and external (Sonos) audio output.
- **Bluetooth proxy / BLE tracker** — the panel doubles as a BLE proxy for HA
  (the ESP32-P4's radio is the on-board hosted ESP32-C6).
- **HTTP screenshot endpoint** — `GET http://<panel-ip>:8080/screenshot` returns a
  JPEG of the live screen, handy for remote UI work (optional; see
  [`display-capture.yaml`](esphome/modules/display-capture.yaml)).

---

## Hardware

- **Waveshare ESP32-P4-86-Panel** (86×86 mm wall-box form factor)
- ESP32-P4 + on-board **ESP32-C6** (hosted, provides WiFi + BLE)
- 720×720 MIPI-DSI display, GT911 capacitive touch
- ES8311 DAC + ES7210 ADC, speaker amp, microphone
- Two on-board relays, PWM backlight

See [`docs/HARDWARE.md`](docs/HARDWARE.md) for the full pin map and the
engineering-sample silicon notes.

---

## Quick start

1. **Install ESPHome** (2026.4.0 or newer — this project uses LVGL 9.5).
2. **Clone this repo** and enter the `esphome/` folder.
3. **Create your secrets:**
   ```bash
   cp esphome/secrets.yaml.example esphome/secrets.yaml
   # edit secrets.yaml — WiFi + a generated API key
   ```
4. **Point it at your entities:** edit
   [`esphome/modules/user-config.yaml`](esphome/modules/user-config.yaml).
   Either change the entity names to match yours, or create matching template
   sensors in HA (the [`homeassistant/`](homeassistant/) folder has ready-made
   examples). See [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md).
5. **Flash:**
   ```bash
   cd esphome
   esphome run waveshare-p4-86-panel.yaml
   ```

Full walkthrough: [`docs/INSTALLATION.md`](docs/INSTALLATION.md).

---

## Repository layout

```
esphome/
  waveshare-p4-86-panel.yaml      # composition root — you don't normally edit this
  secrets.yaml.example            # copy to secrets.yaml
  modules/
    user-config.yaml              # ★ your entities/host live here
    hardware/p4-86-panel.yaml     # board, display, touch, audio, BLE
    ui-foundation.yaml            # API, WiFi, logger, theme, library packages
    assist.yaml                   # voice assistant + audio stack
    ui-shared.yaml                # shared LVGL singletons + sensors
    display-capture.yaml          # optional screenshot endpoint
    page-*.yaml                   # one package per screen
    widgets/                      # reusable LVGL tile templates
  components/
    lvgl_screenshot/              # vendored screenshot component (LVGL v9 port)
  esphome-modular-lvgl-buttons/   # vendored MIT LVGL library (Andrew Gillis)
  assets/                         # fonts, wake-word models, on-device sounds
homeassistant/                    # example template sensors the panel reads
docs/                             # installation, configuration, hardware
```

---

## Home Assistant side

The panel reads a set of **normalised** entities (e.g. `sensor.pv_power`,
`sensor.battery_soc`, `sensor.weather_forecast`). The [`homeassistant/`](homeassistant/)
folder contains example template sensors that produce those names from a
specific integration stack (Sigenergy inverter, Sonos, Spotify, a generic
alarm). Each file flags its **input** entities with `# CHANGE` — point those at
your own integrations, or skip the templates entirely and set the entity names
in `user-config.yaml` directly. Details in [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md).

---

## Credits & licence

- UI library: **[esphome-modular-lvgl-buttons](https://github.com/agillis/esphome-modular-lvgl-buttons)**
  by Andrew Gillis (MIT) — vendored under `esphome/esphome-modular-lvgl-buttons/`.
- Screenshot component: derived from **dcgrove/esphome-lvgl-screenshot**, ported
  to LVGL v9 here.
- See [`NOTICE`](NOTICE) for all third-party attributions (fonts, wake-word
  models, stb_image_write).

This project's own configuration and code is released under the
[MIT licence](LICENSE).
