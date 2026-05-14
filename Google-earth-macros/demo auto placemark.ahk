#Requires AutoHotkey v2.0
#SingleInstance Force

CoordMode "Mouse", "Window"

#HotIf WinActive("ahk_exe googleearth.exe")

!p:: {
    Send "^+p"

    Sleep 75

    MouseGetPos &initX, &initY

    MouseClickDrag "Left", 790, 340, initX, initY
}

#HotIf
