SetTitleMatchMode, 2
CoordMode, Mouse, Window
globalDelay := 55
colorClick := 4

; Penambahan properti "Type" pada objek untuk membedakan rute eksekusi
Slack := {Type: "Placemark", X:76, Y:360, Colors:["ff0000"]}
Fdt := {Type: "Placemark", X:150, Y:360, Colors:["aa00ff","0000ff","00ffff","ffff00","aa0000"]}
Fat := {Type: "Placemark", X:115, Y:360, Colors:["00ff00","ffff00","ff0000","ff00ff","000ff"]}
Cable := {Type: "Path", X: 452, Y: 31, Colors: ["00FF00", "FF00FF", "AA00FF", "550000", "FF0000", "FFFF00", "FFAA00"]}
HomePass := {Type: "Placemark", X: 378,  Y:460 , Colors: ["00ff00"]}
Pole := {Type: "Placemark", X: 224,  Y: 358 , Colors: ["550000", "AA00FF", "00FFFF", "00FF00", "FF0000"] }
JointClosure := {Type: "Placemark", X: 417,  Y: 323 , Colors: ["00FF00", "FF00FF", "AA00FF", "550000", "FF0000", "FFFF00", "FFAA00"] }
SlingWire := {Type: "Placemark", X: 452,  Y: 31, Colors: ["00FFFF"] }

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
        SelectedColor := IconData.Colors[1]
        ExecuteAction(ActionType, IconData, SelectedColor)
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
            ExecuteAction(ActionType, IconData, SelectedColor)
        } else {
            MsgBox, 16, Error, Color Mode %UserInput% not available! this icon only has %TotalColors% colors.
        }
    }
}

ExecuteAction(ActionType, IconData, SelectedColor) {
    if (ActionType == "Placement") {
        if (IconData.Type == "Path") {
            ChangePath(SelectedColor)
        } else {
            ChangePlacemark(IconData.X, IconData.Y, SelectedColor)
        }
    } else if (ActionType == "Folder") {
        ChangeFolder(IconData.X, IconData.Y, SelectedColor)
    }
}

ClickWait(PosX, PosY, ClickCount := 1) {
    global globalDelay
    Click, %PosX%, %PosY%, %ClickCount%
    Sleep, %globalDelay%
}

OpenProperties() {
    global globalDelay
    Send, !{Enter}
    Sleep, %globalDelay%
    Sleep, 200 ; Jeda ekstra untuk memastikan antarmuka jendela Properties selesai di-render sebelum kursor bergerak
}

; Fungsi baru khusus untuk objek Path (Cable)
ChangePath(color) {
    global globalDelay
    global colorClick
    OpenProperties()
    ClickWait(145, 127)
    ClickWait(112, 199)
    ClickWait(422, 421, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    Send, {Enter}
}

ChangePlacemark(iconx, icony, color) {
    global globalDelay
    global colorClick
    OpenProperties()
    ClickWait(521, 80, 3)
    ClickWait(iconx, icony)
    ClickWait(154, 59)
    ClickWait(435, 402, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    ;ClickWait(415, 435)

    Send, {Enter}
    ClickWait(482, 701)
    ClickWait(149, 245)
    ClickWait(115, 320)
    ClickWait(434, 423, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    ;Click, 398, 454
    Send, {Enter}
}

ChangeFolder(iconx, icony, color) {
    global globalDelay
    global colorClick
    OpenProperties()
    ClickWait(151, 183)
    ClickWait(469, 428)
    ClickWait(521, 80, 3)
    ClickWait(iconx, icony)
    ClickWait(154, 59)
    ClickWait(435, 402, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    ;ClickWait(415, 435)

    Send, {Enter}

    ClickWait(482, 701)
    ClickWait(149, 245)
    ClickWait(117, 250)
    ClickWait(434, 423, colorClick)
    Send, %color%
    Sleep, %globalDelay%
    ;Click, 398, 454
    Send, {Enter}
}

#IfWinActive ahk_exe googleearth.exe
!e::Send, !{Enter}
+Tab::Send, {Tab 5}
!s::Send, {Right}^{Left 2}^{Backspace}SLACK{Enter}
!a::Send, XXX.
!m::Send, MR.XXX.P
#IfWinActive
