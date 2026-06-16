# Configuration

Everything installation-specific lives in
[`esphome/modules/user-config.yaml`](../esphome/modules/user-config.yaml). It's a
single block of ESPHome **substitutions** — `name: value` pairs that get
text-substituted as `${name}` throughout the rest of the config. You point the
panel at your own Home Assistant **without touching the page files**.

## Two ways to adopt

**A — keep the generic names, create matching HA sensors.**
Leave `user-config.yaml` as-is and make sure Home Assistant exposes entities
with these names. The [`homeassistant/`](../homeassistant/) folder gives you
ready-made template sensors for a Sigenergy + Sonos + Spotify setup; adapt their
**inputs** (marked `# CHANGE`) to your integrations.

**B — change the names to your real entities.**
Edit the right-hand side of each line in `user-config.yaml` to your actual
entity IDs and ignore the HA templates entirely.

A page whose entities don't exist just shows *unavailable* — it doesn't break
the rest of the panel. So you can adopt one screen at a time.

## Device & network

| Substitution | Default | Purpose |
|---|---|---|
| `name` | `waveshare-p4-86-panel` | ESPHome node name (lowercase/hyphens) |
| `friendly_name` | `Waveshare P4 86-Panel` | HA display name |
| `wifi_fallback_pwd` | `changeme123` | Hotspot password if WiFi fails — **change this** |
| `ha_base_url` | `http://homeassistant.local:8123` | Used by the voice assistant and album-art fetch |
| `location_name` | `Home` | Label shown on the screensaver |

WiFi SSID/password and the API key are **secrets**, set in `secrets.yaml`
(see `secrets.yaml.example`).

## Entity map

Each row is the substitution, its default entity name, and — where applicable —
the example HA file that produces it.

### Energy (Energy page + home-screen battery ring)
| Substitution | Default entity | Produced by |
|---|---|---|
| `solar_power_entity` | `sensor.pv_power` | your inverter (input) |
| `home_consumption_entity` | `sensor.home_power` | your inverter (input) |
| `battery_power_entity` | `sensor.battery_power` | your inverter (input) |
| `battery_soc_entity` | `sensor.battery_soc` | your inverter (input) |
| `daily_flow_pv_home_entity` | `sensor.daily_flow_pv_home` | `sigenergy_flow_meters.yaml` |
| `daily_flow_pv_battery_entity` | `sensor.daily_flow_pv_battery` | `sigenergy_flow_meters.yaml` |
| `daily_flow_pv_grid_entity` | `sensor.daily_flow_pv_grid` | `sigenergy_flow_meters.yaml` |
| `daily_flow_battery_home_entity` | `sensor.daily_flow_battery_home` | `sigenergy_flow_meters.yaml` |
| `daily_flow_battery_grid_entity` | `sensor.daily_flow_battery_grid` | `sigenergy_flow_meters.yaml` |
| `daily_flow_grid_home_entity` | `sensor.daily_flow_grid_home` | `sigenergy_flow_meters.yaml` |
| `daily_flow_grid_battery_entity` | `sensor.daily_flow_grid_battery` | `sigenergy_flow_meters.yaml` |

The Sigenergy example chain is: your inverter's instantaneous power sensors →
`sigenergy_flows.yaml` (splits into directional flows) →
`sigenergy_flow_integrations.yaml` (integrates to energy) →
`sigenergy_flow_meters.yaml` (daily utility meters). Non-Sigenergy users can
either reproduce that chain from their own power sensors, or just point the
`daily_flow_*` substitutions at whatever daily-energy sensors they already have.

### Climate (Climate page)
| Substitution | Default entity |
|---|---|
| `climate_entity` | `climate.home_heating` |
| `zone_current_temp_entity` | `sensor.zone_temperature` |
| `zone_humidity_entity` | `sensor.zone_humidity` |
| `outdoor_temp_entity` | `sensor.outdoor_temperature` |
| `heating_flow_temp_entity` | `sensor.heating_flow_temperature` |
| `hot_water_temp_entity` | `sensor.hot_water_temperature` |

### Lights (Lights page)
| Substitution | Default entity |
|---|---|
| `light_sofa_entity` | `light.living_room_lamp_1` |
| `light_hobby_entity` | `light.living_room_lamp_2` |
| `light_cabinet_entity` | `light.cabinet` |
| `light_panel_backlight_entity` | `light.waveshare_p4_86_panel_lcd_backlight` |

The panel exposes its own LCD backlight to HA as
`light.<node_name>_lcd_backlight` (hyphens in `name` become underscores). If you
change `name`, update this entity to match.

### Media (Home page media + Rooms/Playlists modals)
| Substitution | Default entity | Produced by |
|---|---|---|
| `sonos_living_room_entity` … `sonos_roam_entity` | `media_player.living_room` … `media_player.roam` | your speakers (input) |
| `external_media_player` | `living_room` | primary zone *suffix* for voice timer/wake sounds |
| `active_player_selector_entity` | `input_text.active_player` | `input_text.yaml` |
| `active_media_mirror_entity` | `sensor.active_media` | `frontroom_panel.yaml` |
| `sonos_topology_entity` | `sensor.sonos_topology` | `sonos_topology.yaml` |
| `spotify_playlists_entity` | `sensor.spotify_playlists` | `spotify_panel.yaml` |
| `spotify_media_player_entity` | `media_player.spotify` | your Spotify integration (input) |

The seven Sonos zones are listed in `user-config.yaml`, in `sonos_topology.yaml`,
and in the room-picker grid in `page-media.yaml`. To add/remove rooms you edit
those three places (the picker grid is a 3×3 of `tile_media_device` includes).

### Security (Security page)
| Substitution | Default entity |
|---|---|
| `alarm_entity` | `alarm_control_panel.alarm` |

Works with any `alarm_control_panel`. The disarm keypad sends the typed PIN as
the `code` field of `alarm_control_panel.alarm_disarm`.

### Weather (screensaver)
| Substitution | Default entity | Produced by |
|---|---|---|
| `weather_forecast_entity` | `sensor.weather_forecast` | `frontroom_weather.yaml` |

`frontroom_weather.yaml` calls `weather.get_forecasts` on your `weather.*` entity
(input, default `weather.home`) and republishes a compact today/tomorrow string
the panel parses.

## Rotation

The display rotation is set where the hardware package is included in
`waveshare-p4-86-panel.yaml`:

```yaml
hardware: !include
  file: modules/hardware/p4-86-panel.yaml
  vars:
    rotation: "0"   # "0" | "90" | "180" | "270"
```

## Gotcha: substitutions inside inline maps

If you add a substitution to an inline (`{ ... }`) YAML mapping — e.g. a
`!include {..., vars: {entity: ...}}` or a `data: {entity_id: ...}` — you must
**quote** it: `entity: "${my_entity}"`. Unquoted `${...}` contains braces that
break YAML's flow-mapping parser. Block-style values (`entity_id: ${my_entity}`
on its own line) don't need quoting.
