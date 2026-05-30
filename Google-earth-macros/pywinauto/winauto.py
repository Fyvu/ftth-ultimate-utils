from pywinauto import Application
from pywinauto.timings import Timings

Timings.fast()

app = Application(backend="uia", allow_magic_lookup=False).connect(
    path=r"googleearth.exe"
)

mainwindow = app.window(title="Google Earth Pro", control_type="Window", depth=1)

Placemark = {
    "homepass": {"icon": 144, "color": ["00ff00"]},
    "pole": {"icon": 95, "color": ["AA00FF", "00FFFF", "00FF00", "FF0000", "550000"]},
    "fdt": {"icon": 93, "color": ["AA00FF", "0000FF", "00FFFF", "FFFF00", "AA0000"]},
    "fat": {"icon": 92, "color": ["00FF00", "FFFF00", "FF0000", "FF00FF", "0000FF"]},
    "slack": {"icon": 96, "color": ["FF0000"]},
}

Path = {
    "color": [
        "00FF00",
        "FF00FF",
        "AA00FF",
        "550000",
        "FF0000",
        "FFFF00",
        "FFAA00",
        "00FFFF",
    ]
}


def placemarkEdit(Placemark, Colorindex: int):

    icon = Placemark["icon"]
    color = Placemark["color"][Colorindex]

    mainwindow.type_keys("%{ENTER}")

    editPlacemark = mainwindow.child_window(
        title="Google Earth - Edit Placemark", control_type="Window", depth=1
    )
    editPlacemark.wait("visible")
    editButton = editPlacemark.child_window(
        control_type="Button", found_index=1, depth=2
    )
    editButton.click()

    IconPane = editPlacemark.child_window(title="Icon", control_type="Window", depth=1)

    icon_item = IconPane.child_window(
        control_type="ListItem", found_index=icon
    ).wrapper_object()
    icon_item.click_input()

    colorButton = IconPane.child_window(
        control_type="Button", found_index=1, depth=2
    ).wrapper_object()
    colorButton.click_input()
    ColorPane = IconPane.child_window(
        control_type="Window", title="Select Color", depth=1
    )
    htmlColorBox = ColorPane.child_window(
        control_type="Edit", title="HTML: Alt+H", depth=2
    ).wrapper_object()

    htmlColorBox.click_input()
    htmlColorBox.type_keys(f"^a{{BACKSPACE}}#{color}{{ENTER}}", set_foreground=False)

    IconPane.child_window(control_type="Button", title="OK", depth=2).click()
    editPlacemark.child_window(control_type="Button", title="OK Enter", depth=2).click()


def editIconColor(item, colorIndex: int):
    # if item == "cable"
    placemarkEdit(Placemark[item], colorIndex)


# placemarkEdir(Placemark["FAT"], 1)
# placemarkEdir(Placemark["FDT"], 2)
# placemarkEdir(Placemark["HOMEPASS"], 0)
# placemarkEdir(Placemark["POLE"], 2)
# placemarkEdir(Placemark["SLACK CABLE"], 0)
