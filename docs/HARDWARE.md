# Hardware — Waveshare ESP32-P4-86-Panel

The full hardware contract lives in
[`esphome/modules/hardware/p4-86-panel.yaml`](../esphome/modules/hardware/p4-86-panel.yaml).
This page summarises it and calls out the non-obvious bits.

## Board

- **SoC:** ESP32-P4 (`board: esp32-p4-evboard`), 32 MB flash, PSRAM.
- **Radio:** the P4 has no native WiFi/BT. An on-board **ESP32-C6** provides
  both, driven over SDIO via the `esp32_hosted` component. Its firmware is
  kept current by an `update:` platform pointing at Espressif's hosted-firmware
  manifest.
- **Framework:** ESP-IDF, with `execute_from_psram` and experimental IDF
  features enabled.

### Engineering-sample silicon

These panels ship **engineering-sample** P4 silicon (eco2 ROM, chip rev v1.3).
The config sets:

```yaml
esp32:
  engineering_sample: true
```

Without it, ESP-IDF assumes production silicon and the FreeRTOS timer-task
static stack allocation asserts at boot
(`vApplicationGetTimerTaskMemory: pxStackBufferTemp != NULL`). PSRAM is left at
its default mode (not `hex`) for the same stability reason.

## Peripherals & pin map

| Function | Component | Key pins |
|---|---|---|
| Display | `mipi_dsi`, model `WAVESHARE-P4-86-PANEL`, 720×720 | DSI |
| Backlight | `ledc` PWM (`gpio_backlight_pwm`) | GPIO26 (inverted, capped 80 %) |
| Touch | `gt911` on I²C bus A | SDA GPIO7, SCL GPIO8 @ 400 kHz |
| Hosted radio | `esp32_hosted` (ESP32-C6) | reset 54, cmd 19, clk 18, d0–d3 14/15/16/17 |
| Audio bus | `i2s_audio` | MCLK 13, LRCLK 10, BCLK 12 |
| DAC (out) | `es8311` @ 0x18 | — |
| ADC (mic in) | `es7210` @ 0x40 | — |
| Speaker | `i2s_audio` speaker | DOUT GPIO9 |
| Microphone | `i2s_audio` mic | DIN GPIO11 |
| Amp enable | `gpio` switch | GPIO53 |
| Relays | two `gpio` outputs | GPIO32, GPIO46 |
| LDO | `esp_ldo` channel 3 | 2.5 V |

## Bluetooth

Because the radio is the hosted ESP32-C6, BLE rides the same co-processor as
WiFi. The hardware package enables both a scanner and a proxy:

```yaml
esp32_ble_tracker:
  scan_parameters:
    active: true
bluetooth_proxy:
  active: true
```

So the panel works as a Home Assistant **Bluetooth proxy** and BLE presence
scanner with no extra hardware.

## Display / LVGL

```yaml
lvgl:
  rotation: ${rotation}      # "0" | "90" | "180" | "270"
  byte_order: little_endian
```

`buffer_size: 100%` is set in `ui-shared.yaml` — a full-screen LVGL draw buffer.
This is also what makes the screenshot endpoint able to capture the whole frame.

## Screenshot endpoint

`components/lvgl_screenshot/` exposes `GET :8080/screenshot` (JPEG). It reads
LVGL's active full-screen RGB565 buffer and encodes it on-device. It's a local
port of `dcgrove/esphome-lvgl-screenshot` updated for the LVGL v9 API
(`lv_display_get_buf_active`, raw RGB565 reads). Remove the `display_capture`
package include from `waveshare-p4-86-panel.yaml` if you don't want it.
