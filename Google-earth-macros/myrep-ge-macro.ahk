SetTitleMatchMode, 2
CoordMode, Mouse, Window
globalDelay := 55
colorClick := 4

Slack := {X:225, Y:351, Colors:["ff0000"]}
Fdt := {X:116, Y:359, Colors:["aa00ff","0000ff","00ffff","ffff00","aa0000"]}
Fat := {X:72, Y:353, Colors:["00ff00","ffff00","ff0000","ff00ff","000ff"]}
Cable := { X: 452, Y: 31, Colors: ["00FF00", "FF00FF", "AA00FF", "550000", "FF0000", "FFFF00", "FFAA00"]}
HomePass := { X: 378,  Y:460 , Colors: ["00ff00"]}
Pole := { X: 224,  Y: 358 , Colors: ["FF0000", "00FF00", "00FFFF", "AA00FF", "550000"] }
JointClosure := { X: 417,  Y: 323 , Colors: ["00FF00", "FF00FF", "AA00FF", "550000", "FF0000", "FFFF00", "FFAA00"] }
SlingWire := { X: 452,  Y: 31, Colors: ["00FFFF"] }

RegisterIcon("s", Slack)
RegisterIcon("d", Fdt)
RegisterIcon("a", Fat)
RegisterIcon("c", Cable)
RegisterIcon("h", HomePass)
RegisterIcon("p", Pole)
RegisterIcon("j", JointClosure)
RegisterIcon("w", SlingWire)

return

RegisterIcon(Key, IconData) {
    Hotkey, IfWinActive, ahk_exe googleearth.exe
    BoundPlacement := Func("HandleAction").Bind("Placement", IconData)
    BoundFolder    := Func("HandleAction").Bind("Folder", IconData)
    Hotkey, ^!%Key%, % BoundPlacement
    Hotkey, +!%Key%, % BoundFolder
}

HandleAction(ActionType, IconData) {
    KeyWait, Ctrl
    KeyWait, Alt
    KeyWait, Shift

    TotalColors := IconData.Colors.Length()

    if (TotalColors == 1) {
        if (ActionType == "Placement")
            ChangePlacement(IconData.X, IconData.Y, IconData.Colors[1])
        else
            ChangeFolder(IconData.X, IconData.Y, IconData.Colors[1])
        return
    }

    ToolTip, % "chose color mode (1-" TotalColors ")"

    Input, UserInput, L1 T2

    ToolTip

    if (ErrorLevel == "Timeout") {
        return
    }

    if UserInput is integer
    {
        if (UserInput > 0 && UserInput <= TotalColors) {
            SelectedColor := IconData.Colors[UserInput]

            if (ActionType == "Placement")
                ChangePlacement(IconData.X, IconData.Y, SelectedColor)
            else if (ActionType == "Folder")
                ChangeFolder(IconData.X, IconData.Y, SelectedColor)
        } else {
            MsgBox, 16, Error, Color Mode %UserInput% not available! this icon only has %TotalColors% colors.
        }
    }
}

ClickWait(PosX, PosY, ClickCount := 1) {
    global globalDelay
    Click, %PosX%, %PosY%, %ClickCount%
    Sleep, %globalDelay%
}

ChangePlacement(iconx, icony, color) {
    global globalDelay
    global colorClick
    ClickWait(521, 80)
    ClickWait(iconx, icony)
    ClickWait(154, 59)
    ClickWait(435, 402, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    ClickWait(415, 435)
    ClickWait(482, 701)
    ClickWait(149, 245)
    ClickWait(112, 320)
    ClickWait(434, 423, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    Click, 398, 454
}
ChangeFolder(iconx, icony, color) {
    global globalDelay
    global colorClick

    ClickWait(151, 183)
    ClickWait(469, 428)
    ClickWait(521, 80)
    ClickWait(iconx, icony)
    ClickWait(154, 59)
    ClickWait(435, 402, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    ClickWait(415, 435)
    ClickWait(482, 701)
    ClickWait(149, 245)
    ClickWait(117, 250)
    ClickWait(434, 423, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    Click, 398, 454
}


#IfWinActive ahk_exe googleearth.exe
!e::Send, !{Enter}
+Tab::Send, {Tab 5}
#IfWinActive
