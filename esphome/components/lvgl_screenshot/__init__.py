"""LVGL Screenshot Component - serves a JPEG snapshot of the active LVGL screen via HTTP.

Optionally accepts a `pages:` map so the endpoint can switch the panel to a named
page before capturing: GET /screenshot?page=<name>. Without ?page it captures
whatever is currently shown.
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_NAME, CONF_PAGES, CONF_PORT

CODEOWNERS = ["@dcgrove"]
DEPENDENCIES = ["lvgl"]

from esphome.components.lvgl.types import lv_page_t

lvgl_screenshot_ns = cg.esphome_ns.namespace("lvgl_screenshot")
LvglScreenshot = lvgl_screenshot_ns.class_("LvglScreenshot", cg.Component)

CONF_SETTLE_TIME = "settle_time"
CONF_RESTORE_PAGE = "restore_page"
CONF_PAGE_ID = "page"

PAGE_SCHEMA = cv.Schema(
    {
        # Query name used in ?page=<name>; the LVGL page id it maps to.
        cv.Required(CONF_NAME): cv.string_strict,
        cv.Required(CONF_PAGE_ID): cv.use_id(lv_page_t),
    }
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(LvglScreenshot),
        cv.Optional(CONF_PORT, default=8080): cv.port,
        # How long to let LVGL run after switching pages before capturing, so
        # layout settles and on_load handlers get a chance to populate widgets.
        cv.Optional(
            CONF_SETTLE_TIME, default="300ms"
        ): cv.positive_time_period_milliseconds,
        # Return to the previously-shown page after capturing a ?page= request,
        # so a remote screenshot does not hijack the physical panel.
        cv.Optional(CONF_RESTORE_PAGE, default=True): cv.boolean,
        cv.Optional(CONF_PAGES): cv.ensure_list(PAGE_SCHEMA),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    cg.add(var.set_port(config[CONF_PORT]))
    cg.add(var.set_settle_ms(config[CONF_SETTLE_TIME].total_milliseconds))
    cg.add(var.set_restore_page(config[CONF_RESTORE_PAGE]))
    for page in config.get(CONF_PAGES, []):
        page_var = await cg.get_variable(page[CONF_PAGE_ID])
        cg.add(var.register_page(page[CONF_NAME], page_var))
