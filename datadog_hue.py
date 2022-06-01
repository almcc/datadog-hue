import os

import click
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from phue import Bridge
from rich import print
from rich.markup import escape

OK = {"on": True, "bri": 254, "bri": 254, "hue": 44163, "sat": 254}
ALERT = {"on": True, "bri": 254, "bri": 254, "hue": 0, "sat": 254}
WARNING = {"on": True, "bri": 254, "bri": 254, "hue": 6393, "sat": 254}


@click.command()
@click.option(
    "--datadog-app-key",
    default=lambda: os.environ.get("DATADOG_APP_KEY", ""),
    help="DataDog App Key",
    show_default="$DATADOG_APP_KEY",
)
@click.option(
    "--datadog-api-key",
    default=lambda: os.environ.get("DATADOG_API_KEY", ""),
    help="DataDog Api Key",
    show_default="$DATADOG_API_KEY",
)
@click.option(
    "--datadog-site",
    default="datadoghq.eu",
    help="DataDog Site",
    show_default=True,
)
@click.option(
    "--datadog-monitor-tags",
    help="DataDog Mointor tags (comma seperated)",
    default="",
    show_default=True,
)
@click.option(
    "--datadog-ignore", help="DataDog Monitor ID's to ignore", multiple=True, type=int
)
@click.option(
    "--hue-bridge-ip",
    default=lambda: os.environ.get("HUE_BRIDGE_IP", ""),
    help="Hue Bridge IP Address",
    show_default="$HUE_BRIDGE_IP",
)
@click.option(
    "--hue-light", help="Name of Hue Light to change", multiple=True, required=True
)
def monitor(
    datadog_app_key,
    datadog_api_key,
    datadog_site,
    datadog_monitor_tags,
    datadog_ignore,
    hue_bridge_ip,
    hue_light,
):
    """Watch DataDog monitors and change the colour of lights to reflect status."""
    configuration = Configuration()
    configuration.api_key["appKeyAuth"] = datadog_app_key
    configuration.api_key["apiKeyAuth"] = datadog_api_key
    configuration.server_variables["site"] = datadog_site

    hue = Bridge(hue_bridge_ip)

    alert = False
    warning = False
    with ApiClient(configuration) as api_client:
        api_instance = MonitorsApi(api_client)
        monitors = api_instance.list_monitors(monitor_tags=datadog_monitor_tags)
        for monitor in monitors:
            print(monitor.name)
            if (
                monitor.overall_state.to_str() != "OK"
                and not monitor.options["silenced"]
                and monitor.id not in datadog_ignore
            ):
                print(
                    f"[{monitor.id}] [green]{escape(monitor.message)}[/green] - [red]{monitor.overall_state}[/red] at [blue]{monitor.overall_state_modified}[/blue]"
                )
                if monitor.overall_state.to_str() == "Alert":
                    if monitor.priority < 3:
                        alert = True
                    else:
                        warning = True
                if monitor.overall_state.to_str() == "Warn":
                    warning = True

        config = OK
        if alert:
            config = ALERT
        elif warning:
            config = WARNING

        for name in hue_light:
            hue.set_light(name, config)


if __name__ == "__main__":
    monitor()
