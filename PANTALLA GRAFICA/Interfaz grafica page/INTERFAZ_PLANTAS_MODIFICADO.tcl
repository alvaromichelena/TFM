#############################################################################
# Generated by PAGE version 5.6
#  in conjunction with Tcl version 8.6
#  Oct 22, 2021 01:52:59 PM CEST  platform: Windows NT
set vTcl(timestamp) ""
if {![info exists vTcl(borrow)]} {
    tk_messageBox -title Error -message  "You must open project files from within PAGE."
    exit}


if {!$vTcl(borrow) && !$vTcl(template)} {

set vTcl(actual_gui_font_dft_desc)  TkDefaultFont
set vTcl(actual_gui_font_dft_name)  TkDefaultFont
set vTcl(actual_gui_font_text_desc)  TkTextFont
set vTcl(actual_gui_font_text_name)  TkTextFont
set vTcl(actual_gui_font_fixed_desc)  TkFixedFont
set vTcl(actual_gui_font_fixed_name)  TkFixedFont
set vTcl(actual_gui_font_menu_desc)  TkMenuFont
set vTcl(actual_gui_font_menu_name)  TkMenuFont
set vTcl(actual_gui_font_tooltip_desc)  TkDefaultFont
set vTcl(actual_gui_font_tooltip_name)  TkDefaultFont
set vTcl(actual_gui_font_treeview_desc)  TkDefaultFont
set vTcl(actual_gui_font_treeview_name)  TkDefaultFont
set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(actual_gui_menu_active_fg)  #000000
set vTcl(pr,autoalias) 1
set vTcl(pr,relative_placement) 1
set vTcl(mode) Relative
}




proc vTclWindow.top44 {base} {
    global vTcl
    if {$base == ""} {
        set base .top44
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -menu "$top.m62" -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 1130x667+2274+125
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1370 749
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "GUI"
    vTcl:DefineAlias "$top" "GUI" vTcl:Toplevel:WidgetProc "" 1
    set vTcl(real_top) {}
    vTcl:withBusyCursor {
    frame $top.fra45 \
        -borderwidth 2 -relief groove -background $vTcl(actual_gui_bg) \
        -height 417 -highlightbackground $vTcl(actual_gui_bg) \
        -highlightcolor black -width 560 
    vTcl:DefineAlias "$top.fra45" "Frame1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.fra45
    label $top.lab60 \
        -activebackground #f9f9f9 -activeforeground black -background #c0c0c0 \
        -borderwidth 9 -compound center -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {VISUALIZACIÓN DE LAS VARIABLES DEL PROCESO} 
    vTcl:DefineAlias "$top.lab60" "Label_visualizacion_var" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab60
    menu $top.m62 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(pr,menubgcolor) -font TkMenuFont \
        -foreground $vTcl(pr,menufgcolor) -tearoff 0 
    label $top.lab52 \
        -activebackground #f9f9f9 -activeforeground black -background #939393 \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.lab52" "Label_aux5" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab52
    label $top.lab55 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Selección de la planta} 
    vTcl:DefineAlias "$top.lab55" "Label_sel_planta" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab55
    ttk::combobox $top.tCo59 \
        -values {Planta 1, Planta 2, Planta 3, Planta 4, Planta 5} \
        -font {-family {Segoe UI} -size 13 -weight bold} \
        -textvariable combobox -foreground {} -background {} -takefocus {} 
    vTcl:DefineAlias "$top.tCo59" "Sel_planta" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tCo59
    label $top.lab45 \
        -activebackground #f9f9f9 -activeforeground black -background #939393 \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.lab45" "Label_aux4" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab45
    button $top.but46 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command BOTON_ON_OFF \
        -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text ON/OFF 
    vTcl:DefineAlias "$top.but46" "ButtonON_OFF" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.but46
    label $top.lab47 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Control on/off} 
    vTcl:DefineAlias "$top.lab47" "Label_marcha_paro" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab47
    label $top.lab48 \
        -activebackground #f9f9f9 -activeforeground black -background #939393 \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.lab48" "Label_aux3" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab48
    label $top.lab53 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Selección setpoint} 
    vTcl:DefineAlias "$top.lab53" "Label_set_point" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab53
    button $top.but54 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command BOTON_ACTUALIZAR \
        -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text ACTUALIZAR 
    vTcl:DefineAlias "$top.but54" "ButtonActualizar" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.but54
    label $top.lab56 \
        -activebackground #f9f9f9 -activeforeground black -background #939393 \
        -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Set Point} 
    vTcl:DefineAlias "$top.lab56" "Label_sp" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab56
    entry $top.ent57 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground blue \
        -selectforeground white -width 54 
    vTcl:DefineAlias "$top.ent57" "EntrySP" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.ent57
    frame $top.fra47 \
        -borderwidth 2 -relief groove -background $vTcl(actual_gui_bg) \
        -height 417 -highlightbackground $vTcl(actual_gui_bg) \
        -highlightcolor black -width 568 
    vTcl:DefineAlias "$top.fra47" "Frame2" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.fra47
    label $top.lab49 \
        -activebackground #f9f9f9 -activeforeground black -background #939393 \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.lab49" "Label_aux1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab49
    label $top.lab50 \
        -activebackground #f9f9f9 -activeforeground black -background #939393 \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.lab50" "Label_aux2" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab50
    text $top.tex51 \
        -background #000000 -font TkTextFont -foreground black -height 4 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief flat -selectbackground blue \
        -selectforeground white -width 45 -wrap word 
    $top.tex51 configure -font "TkTextFont"
    $top.tex51 insert end text
    vTcl:DefineAlias "$top.tex51" "Text1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tex51
    text $top.tex52 \
        -background #0000ff -font TkTextFont -foreground black -height 4 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief flat -selectbackground blue \
        -selectforeground white -width 45 -wrap word 
    $top.tex52 configure -font "TkTextFont"
    $top.tex52 insert end text
    vTcl:DefineAlias "$top.tex52" "Text1_1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tex52
    text $top.tex53 \
        -background #00e800 -font TkTextFont -foreground black -height 4 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief flat -selectbackground blue \
        -selectforeground white -width 45 -wrap word 
    $top.tex53 configure -font "TkTextFont"
    $top.tex53 insert end text
    vTcl:DefineAlias "$top.tex53" "Text1_3" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tex53
    text $top.tex54 \
        -background #ff0000 -font TkTextFont -foreground black -height 6 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief flat -selectbackground blue \
        -selectforeground white -width 34 -wrap word 
    $top.tex54 configure -font "TkTextFont"
    $top.tex54 insert end text
    vTcl:DefineAlias "$top.tex54" "Text1_2" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tex54
    checkbutton $top.che55 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #939393 -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text SP -variable checkSP 
    vTcl:DefineAlias "$top.che55" "CheckbuttonSP" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.che55
    checkbutton $top.che56 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #939393 -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text PV -variable checkPV 
    vTcl:DefineAlias "$top.che56" "CheckbuttonPV" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.che56
    checkbutton $top.che57 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #939393 -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text ERR -variable checkERR 
    vTcl:DefineAlias "$top.che57" "CheckbuttonERR" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.che57
    checkbutton $top.che58 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #939393 -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text CP -variable checkCP 
    vTcl:DefineAlias "$top.che58" "CheckbuttonCP" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.che58
    label $top.lab59 \
        -activebackground #f9f9f9 -activeforeground black -background #c0c0c0 \
        -borderwidth 9 -compound center -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {VISUALIZACIÓN DE LOS PARÁMETROS DE IDENTIFICACIÓN} 
    vTcl:DefineAlias "$top.lab59" "Label_visualizacion_pesos" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab59
    checkbutton $top.che62 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #939393 -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text a0 -variable checkSP 
    vTcl:DefineAlias "$top.che62" "CheckbuttonSP_1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.che62
    text $top.tex63 \
        -background #008000 -font TkTextFont -foreground black -height 4 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief flat -selectbackground blue \
        -selectforeground white -width 45 -wrap word 
    $top.tex63 configure -font "TkTextFont"
    $top.tex63 insert end text
    vTcl:DefineAlias "$top.tex63" "Text1_4" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tex63
    text $top.tex64 \
        -background #0000ff -font TkTextFont -foreground black -height 4 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief flat -selectbackground blue \
        -selectforeground white -width 45 -wrap word 
    $top.tex64 configure -font "TkTextFont"
    $top.tex64 insert end text
    vTcl:DefineAlias "$top.tex64" "Text1_1_1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tex64
    text $top.tex65 \
        -background #ff0000 -font TkTextFont -foreground black -height 6 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief flat -selectbackground blue \
        -selectforeground white -width 34 -wrap word 
    $top.tex65 configure -font "TkTextFont"
    $top.tex65 insert end text
    vTcl:DefineAlias "$top.tex65" "Text1_2_1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.tex65
    checkbutton $top.che66 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #939393 -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text b0 -variable checkSP 
    vTcl:DefineAlias "$top.che66" "CheckbuttonSP_1_1" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.che66
    checkbutton $top.che67 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background #939393 -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 9 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text b1 -variable checkSP 
    vTcl:DefineAlias "$top.che67" "CheckbuttonSP_1_2" vTcl:WidgetProc "GUI" 1
    label $top.lab71 \
        -activebackground #f9f9f9 -activeforeground black -background #939393 \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.lab71" "Label_aux6" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab71
    label $top.lab74 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font {-family {Segoe UI} -size 12 -weight bold -slant roman -underline 0 -overstrike 0} \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Función de transferencia} 
    vTcl:DefineAlias "$top.lab74" "Label_vis_ft" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab74
    label $top.lab75 \
        -activebackground #f9f9f9 -activeforeground black -background #ffffff \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -relief ridge -state active -text Label 
    vTcl:DefineAlias "$top.lab75" "Label_ft" vTcl:WidgetProc "GUI" 1
    vTcl:copy_lock $top.lab75
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.fra45 \
        -in $top -x 0 -relx 0.009 -y 0 -rely 0.075 -width 0 -relwidth 0.487 \
        -height 0 -relheight 0.625 -anchor nw -bordermode ignore 
    place $top.lab60 \
        -in $top -x 0 -relx 0.062 -y 0 -rely 0.015 -width 0 -relwidth 0.382 \
        -height 0 -relheight 0.048 -anchor nw -bordermode ignore 
    place $top.lab52 \
        -in $top -x 0 -relx 0.394 -y 0 -rely 0.78 -width 0 -relwidth 0.212 \
        -height 0 -relheight 0.16 -anchor nw -bordermode ignore 
    place $top.lab55 \
        -in $top -x 0 -relx 0.414 -y 0 -rely 0.795 -width 0 -relwidth 0.173 \
        -height 0 -relheight 0.048 -anchor nw -bordermode ignore 
    place $top.tCo59 \
        -in $top -x 0 -relx 0.434 -y 0 -rely 0.87 -width 0 -relwidth 0.136 \
        -height 0 -relheight 0.037 -anchor nw -bordermode ignore 
    place $top.lab45 \
        -in $top -x 0 -relx 0.23 -y 0 -rely 0.78 -width 0 -relwidth 0.142 \
        -height 0 -relheight 0.19 -anchor nw -bordermode ignore 
    place $top.but46 \
        -in $top -x 0 -relx 0.257 -y 0 -rely 0.87 -width 97 -relwidth 0 \
        -height 44 -relheight 0 -anchor nw -bordermode ignore 
    place $top.lab47 \
        -in $top -x 0 -relx 0.239 -y 0 -rely 0.795 -width 0 -relwidth 0.121 \
        -height 0 -relheight 0.048 -anchor nw -bordermode ignore 
    place $top.lab48 \
        -in $top -x 0 -relx 0.018 -y 0 -rely 0.78 -width 0 -relwidth 0.188 \
        -height 0 -relheight 0.19 -anchor nw -bordermode ignore 
    place $top.lab53 \
        -in $top -x 0 -relx 0.035 -y 0 -rely 0.795 -width 0 -relwidth 0.151 \
        -height 0 -relheight 0.048 -anchor nw -bordermode ignore 
    place $top.but54 \
        -in $top -x 0 -relx 0.063 -y 0 -rely 0.916 -width 107 -relwidth 0 \
        -height 24 -relheight 0 -anchor nw -bordermode ignore 
    place $top.lab56 \
        -in $top -x 0 -relx 0.044 -y 0 -rely 0.855 -width 0 -relwidth 0.074 \
        -height 0 -relheight 0.048 -anchor nw -bordermode ignore 
    place $top.ent57 \
        -in $top -x 0 -relx 0.124 -y 0 -rely 0.864 -width 54 -relwidth 0 \
        -height 20 -relheight 0 -anchor nw -bordermode ignore 
    place $top.fra47 \
        -in $top -x 0 -relx 0.504 -y 0 -rely 0.075 -width 0 -relwidth 0.487 \
        -height 0 -relheight 0.625 -anchor nw -bordermode ignore 
    place $top.lab49 \
        -in $top -x 0 -relx 0.018 -y 0 -rely 0.705 -width 0 -relwidth 0.469 \
        -height 0 -relheight 0.055 -anchor nw -bordermode ignore 
    place $top.lab50 \
        -in $top -x 0 -relx 0.513 -y 0 -rely 0.705 -width 0 -relwidth 0.469 \
        -height 0 -relheight 0.055 -anchor nw -bordermode ignore 
    place $top.tex51 \
        -in $top -x 0 -relx 0.035 -y 0 -rely 0.727 -width 0 -relwidth 0.027 \
        -height 0 -relheight 0.009 -anchor nw -bordermode ignore 
    place $top.tex52 \
        -in $top -x 0 -relx 0.152 -y 0 -rely 0.727 -width 0 -relwidth 0.027 \
        -height 0 -relheight 0.009 -anchor nw -bordermode ignore 
    place $top.tex53 \
        -in $top -x 0 -relx 0.278 -y 0 -rely 0.727 -width 0 -relwidth 0.027 \
        -height 0 -relheight 0.009 -anchor nw -bordermode ignore 
    place $top.tex54 \
        -in $top -x 0 -relx 0.395 -y 0 -rely 0.727 -width 0 -relwidth 0.027 \
        -height 0 -relheight 0.009 -anchor nw -bordermode ignore 
    place $top.che55 \
        -in $top -x 0 -relx 0.062 -y 0 -rely 0.712 -width 0 -relwidth 0.042 \
        -height 0 -relheight 0.04 -anchor nw -bordermode ignore 
    place $top.che56 \
        -in $top -x 0 -relx 0.181 -y 0 -rely 0.72 -width 0 -relwidth 0.042 \
        -height 0 -relheight 0.025 -anchor nw -bordermode ignore 
    place $top.che57 \
        -in $top -x 0 -relx 0.425 -y 0 -rely 0.72 -width 0 -relwidth 0.044 \
        -height 0 -relheight 0.025 -anchor nw -bordermode ignore 
    place $top.che58 \
        -in $top -x 0 -relx 0.31 -y 0 -rely 0.718 -width 0 -relwidth 0.035 \
        -height 0 -relheight 0.028 -anchor nw -bordermode ignore 
    place $top.lab59 \
        -in $top -x 0 -relx 0.541 -y 0 -rely 0.015 -width 0 -relwidth 0.408 \
        -height 0 -relheight 0.048 -anchor nw -bordermode ignore 
    place $top.che62 \
        -in $top -x 0 -relx 0.602 -y 0 -rely 0.712 -width 0 -relwidth 0.042 \
        -height 0 -relheight 0.04 -anchor nw -bordermode ignore 
    place $top.tex63 \
        -in $top -x 0 -relx 0.575 -y 0 -rely 0.727 -width 0 -relwidth 0.027 \
        -height 0 -relheight 0.009 -anchor nw -bordermode ignore 
    place $top.tex64 \
        -in $top -x 0 -relx 0.732 -y 0 -rely 0.727 -width 0 -relwidth 0.027 \
        -height 0 -relheight 0.009 -anchor nw -bordermode ignore 
    place $top.tex65 \
        -in $top -x 0 -relx 0.867 -y 0 -rely 0.727 -width 0 -relwidth 0.027 \
        -height 0 -relheight 0.009 -anchor nw -bordermode ignore 
    place $top.che66 \
        -in $top -x 0 -relx 0.759 -y 0 -rely 0.712 -width 0 -relwidth 0.042 \
        -height 0 -relheight 0.04 -anchor nw -bordermode ignore 
    place $top.che67 \
        -in $top -x 0 -relx 0.894 -y 0 -rely 0.712 -width 0 -relwidth 0.042 \
        -height 0 -relheight 0.04 -anchor nw -bordermode ignore 
    place $top.lab71 \
        -in $top -x 0 -relx 0.655 -y 0 -rely 0.78 -width 0 -relwidth 0.294 \
        -height 0 -relheight 0.205 -anchor nw -bordermode ignore 
    place $top.lab74 \
        -in $top -x 0 -relx 0.708 -y 0 -rely 0.795 -width 0 -relwidth 0.191 \
        -height 0 -relheight 0.033 -anchor nw -bordermode ignore 
    place $top.lab75 \
        -in $top -x 0 -relx 0.673 -y 0 -rely 0.837 -width 0 -relwidth 0.26 \
        -height 0 -relheight 0.139 -anchor nw -bordermode ignore 
    } ;# end vTcl:withBusyCursor 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top44 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}
