# Installation

## 1. Prerequisites

- **ESPHome 2026.4.0 or newer.** This project targets LVGL 9.5, which ESPHome
  adopted in 2026.4.0. Older ESPHome will not build it.
  - CLI: `pip install -U esphome`, or use the ESPHome Dashboard / Home Assistant add-on.
- **A Waveshare ESP32-P4-86-Panel** and a USB-C cable for the first flash.
- **Home Assistant** reachable on your network, with the
  [ESPHome integration](https://www.home-assistant.io/integrations/esphome/).

## 2. Get the code

```bash
git clone https://github.com/f00lycooly/waveshare_esp32-86-esphome.git
cd waveshare_esp32-86-esphome/esphome
```

Everything ESPHome needs is self-contained in `esphome/`: the vendored LVGL
library (`esphome-modular-lvgl-buttons/`), the screenshot component
(`components/`), and the fonts/wake-word models/sounds (`assets/`).

## 3. Secrets

```bash
cp secrets.yaml.example secrets.yaml
```

Edit `secrets.yaml`:

```yaml
wifi_ssid: "YourSSID"
wifi_password: "YourPassword"
esphome_api_key: "<32-byte base64 key>"     # openssl rand -base64 32
```

`secrets.yaml` is gitignored — keep it out of version control.

## 4. Map your entities

Open [`modules/user-config.yaml`](../esphome/modules/user-config.yaml) and work
through it top to bottom. See [CONFIGURATION.md](CONFIGURATION.md) for the full
map and the two adoption strategies. At minimum set `ha_base_url`,
`friendly_name`, and `wifi_fallback_pwd`.

If you want the Energy / Media / Weather pages to show data, also set up the
matching Home Assistant template sensors (next step).

## 5. Home Assistant template sensors (optional, per page)

The [`homeassistant/`](../homeassistant/) files are examples that produce the
normalised entities the panel reads. They are **not** auto-deployed — copy what
you want into your HA config and adapt the `# CHANGE` input entities.

Typical wiring (HA `configuration.yaml`):

```yaml
template: !include_dir_merge_list templates/
input_text: !include input_text.yaml
```

…with the relevant files dropped into `config/templates/`. Reload the template
integration (or restart HA). Each file's top comment says what it produces.

On-device external sounds (voice timer/notify, when output is a Sonos) expect
MP3s under HA's `config/www/sounds/` (served at `/local/sounds/...`).

## 6. Flash

First flash over USB:

```bash
esphome run waveshare-p4-86-panel.yaml
```

Pick the serial port when prompted. Subsequent updates go over-the-air (the
device shows an OTA progress overlay).

> **First build is slow.** ESP-IDF + LVGL compiles from scratch can take several
> minutes. Later builds are incremental.

## 7. Adopt in Home Assistant

After it boots and joins WiFi, HA should auto-discover a new ESPHome device
(`waveshare-p4-86-panel`). Add it; enter the API key if asked. The panel's
sensors, the backlight light, the BLE proxy, and the wake-word/voice controls
appear under the device.

## Troubleshooting

- **Won't build / LVGL errors** — confirm ESPHome ≥ 2026.4.0 (`esphome version`).
- **Screen blank, device on WiFi** — check the display rotation var and that the
  `light.<node>_lcd_backlight` is on (it restores ON by default).
- **A page shows "unavailable"** — the entity name in `user-config.yaml` doesn't
  exist in HA yet. Fix the name or create the sensor.
- **Boot loop on first flash** — this board ships engineering-sample P4 silicon;
  the config already sets `engineering_sample: true`. See
  [HARDWARE.md](HARDWARE.md) if you hit timer-task allocation asserts.
- **Screenshot endpoint** — `curl http://<panel-ip>:8080/screenshot -o shot.jpg`.
  If colours look red/blue swapped, flip `LVGL_SS_SWAP_BYTES` in
  `components/lvgl_screenshot/lvgl_screenshot.cpp` and reflash.
