# Screenshots

Live 720×720 captures of the panel UI, pulled via the HTTP screenshot endpoint
(`display-capture.yaml`):

```bash
curl http://<panel-ip>:8080/screenshot              # current screen
curl http://<panel-ip>:8080/screenshot?page=<name>  # a specific page
```

Captures use `lv_snapshot_take`, so they reflect the exact on-device render
regardless of LVGL's render mode.

| Page | Name | Screenshot |
|------|------|------------|
| Home / media hub | `main` | [`main.jpg`](main.jpg) |
| Energy sankey | `energy` | [`energy.jpg`](energy.jpg) |
| Climate | `climate` | [`climate.jpg`](climate.jpg) |
| Screensaver (clock + forecast) | `screensaver` | [`screensaver.jpg`](screensaver.jpg) |

> The device-info page is intentionally not published here — it shows the
> panel's MAC, IP, and Wi-Fi SSID.
