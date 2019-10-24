#############################################################################
# Generated by PAGE version 4.14
# in conjunction with Tcl version 8.6
set vTcl(timestamp) ""


if {!$vTcl(borrow)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #d9d9d9
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #d8d8d8
set vTcl(active_menu_fg) #000000
}

#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top37
    global vTcl
    set base $vTcl(btop)
    if {$base == ""} {
        set base .top37
    }
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    set site_3_0 $base.tLa49
    set site_4_0 $site_3_0.scr50
    set site_3_0 $base.lab43
    set site_4_0 $site_3_0.scr44
    namespace eval ::widgets_bindings {
        set tagslist {}
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# GENERATED GUI PROCEDURES
#
    menu .pop38 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font TkMenuFont -foreground black -tearoff 1 
    vTcl:DefineAlias ".pop38" "Popupmenu1" vTcl:WidgetProc "" 1
    .pop38 add cascade \
        -menu .pop38.men47 -activebackground {#d9d9d9} \
        -activeforeground {#000000} -background {#d9d9d9} -command {{}} \
        -font TkMenuFont -foreground {#000000} -label File 
    set site_2_0 "."
    menu .pop38.men47 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font {-family {Segoe UI} -size 9} \
        -foreground black -tearoff 0 
    .pop38.men47 add command \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command NewFile -font TkMenuFont \
        -foreground {#000000} -label New 
    .pop38.men47 add command \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command OpenFile -font TkMenuFont \
        -foreground {#000000} -label Open 
    .pop38.men47 add command \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command SaveFile -font TkMenuFont \
        -foreground {#000000} -label Save 
    .pop38.men47 add separator \
        -background {#d9d9d9} 
    .pop38.men47 add command \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command Exit -font TkMenuFont \
        -foreground {#000000} -label Exit 
    .pop38 add cascade \
        -menu .pop38.men49 -activebackground {#d9d9d9} \
        -activeforeground {#000000} -background {#d9d9d9} -command {{}} \
        -font TkMenuFont -foreground {#000000} -label Import/Export \
        -state disabled 
    set site_2_0 "."
    menu .pop38.men49 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font {-family {Segoe UI} -size 9} \
        -foreground black -tearoff 0 
    .pop38 add command \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command Settings -font TkMenuFont \
        -foreground {#000000} -label Settings 
    .pop38 add command \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -command About -font TkMenuFont \
        -foreground {#000000} -label About 

proc vTclWindow.top37 {base} {
    if {$base == ""} {
        set base .top37
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background {#d9d9d9} -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 834x451+347+189
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1585 870
    wm minsize $top 116 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "New Toplevel"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    canvas $top.can42 \
        -background {#d9d9d9} -borderwidth 2 -closeenough 1.0 -height 191 \
        -highlightcolor black -insertbackground black -relief ridge \
        -selectbackground {#c4c4c4} -selectforeground black -width 271 
    vTcl:DefineAlias "$top.can42" "Canvas1" vTcl:WidgetProc "Toplevel1" 1
    canvas $top.can43 \
        -background {#d9d9d9} -borderwidth 2 -closeenough 1.0 -height 171 \
        -highlightcolor black -insertbackground black -relief ridge \
        -selectbackground {#c4c4c4} -selectforeground black -width 271 
    vTcl:DefineAlias "$top.can43" "Canvas2" vTcl:WidgetProc "Toplevel1" 1
    entry $top.ent44 \
        -background white -font TkFixedFont -foreground {#000000} \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black 
    vTcl:DefineAlias "$top.ent44" "Entry1" vTcl:WidgetProc "Toplevel1" 1
    button $top.but45 \
        -activebackground {#d9d9d9} -activeforeground black \
        -background {#d9d9d9} -command NowTime -foreground {#000000} \
        -highlightcolor black -pady 0 -text Now 
    vTcl:DefineAlias "$top.but45" "Button1" vTcl:WidgetProc "Toplevel1" 1
    ttk::style configure TLabelframe.Label -background #d9d9d9
    ttk::style configure TLabelframe.Label -foreground #000000
    ttk::style configure TLabelframe.Label -font TkDefaultFont
    ttk::style configure TLabelframe -background #d9d9d9
    ttk::labelframe $top.tLa49 \
        -text Objects -width 280 -height 435 
    vTcl:DefineAlias "$top.tLa49" "TLabelframe1" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.tLa49
    vTcl::widgets::ttk::scrolledlistbox::CreateCmd $site_3_0.scr50 \
        -background {#d9d9d9} -height 75 -highlightcolor black -width 125 
    vTcl:DefineAlias "$site_3_0.scr50" "Scrolledlistbox1" vTcl:WidgetProc "Toplevel1" 1

    $site_3_0.scr50.01 configure -background white \
        -font TkFixedFont \
        -foreground black \
        -height 3 \
        -highlightcolor #d9d9d9 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10 \
        -listvariable objs
    text $site_3_0.tex51 \
        -background white -font TkTextFont -foreground black -height 124 \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black -width 256 \
        -wrap word 
    .top37.tLa49.tex51 configure -font TkTextFont
    .top37.tLa49.tex51 insert end text
    vTcl:DefineAlias "$site_3_0.tex51" "Text1" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but52 \
        -activebackground {#d9d9d9} -activeforeground black \
        -background {#d9d9d9} -command EditObj -foreground {#000000} \
        -highlightcolor black -pady 0 -text Edit 
    vTcl:DefineAlias "$site_3_0.but52" "Button2" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but53 \
        -activebackground {#d9d9d9} -activeforeground black \
        -background {#d9d9d9} -command DelObj -foreground {#000000} \
        -highlightcolor black -pady 0 -text Delete 
    vTcl:DefineAlias "$site_3_0.but53" "Button3" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but54 \
        -activebackground {#d9d9d9} -activeforeground black \
        -background {#d9d9d9} -command AddObj -foreground {#000000} \
        -highlightcolor black -pady 0 -text Add 
    vTcl:DefineAlias "$site_3_0.but54" "Button3_2" vTcl:WidgetProc "Toplevel1" 1
    label $site_3_0.lab43 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -foreground {#000000} -highlightcolor black \
        -text Show 
    vTcl:DefineAlias "$site_3_0.lab43" "Label1" vTcl:WidgetProc "Toplevel1" 1
    ttk::combobox $site_3_0.tCo45 \
        -textvariable combobox -foreground {} -background {} -takefocus {} 
    vTcl:DefineAlias "$site_3_0.tCo45" "TCombobox1" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.scr50 \
        -in $site_3_0 -x 10 -y 50 -width 256 -relwidth 0 -height 218 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex51 \
        -in $site_3_0 -x 10 -y 270 -width 256 -height 124 -anchor nw \
        -bordermode ignore 
    place $site_3_0.but52 \
        -in $site_3_0 -x 100 -y 400 -width 47 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.but53 \
        -in $site_3_0 -x 180 -y 400 -width 47 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but54 \
        -in $site_3_0 -x 20 -y 400 -width 47 -height 24 -anchor nw \
        -bordermode ignore 
    place $site_3_0.lab43 \
        -in $site_3_0 -x 20 -y 20 -anchor nw -bordermode ignore 
    place $site_3_0.tCo45 \
        -in $site_3_0 -x 100 -y 20 -width 163 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    labelframe $top.lab43 \
        -foreground black -text Observations -background {#d9d9d9} \
        -height 435 -highlightcolor black -width 250 
    vTcl:DefineAlias "$top.lab43" "Labelframe1" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.lab43
    vTcl::widgets::ttk::scrolledlistbox::CreateCmd $site_3_0.scr44 \
        -background {#d9d9d9} -height 75 -highlightcolor black -width 125 
    vTcl:DefineAlias "$site_3_0.scr44" "Scrolledlistbox2" vTcl:WidgetProc "Toplevel1" 1

    $site_3_0.scr44.01 configure -background white \
        -font TkFixedFont \
        -foreground black \
        -height 3 \
        -highlightcolor #d9d9d9 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -width 10
    text $site_3_0.tex45 \
        -background white -font TkTextFont -foreground black -height 144 \
        -highlightcolor black -insertbackground black \
        -selectbackground {#c4c4c4} -selectforeground black -width 234 \
        -wrap word 
    .top37.lab43.tex45 configure -font TkTextFont
    .top37.lab43.tex45 insert end text
    vTcl:DefineAlias "$site_3_0.tex45" "Text2" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but46 \
        -activebackground {#d9d9d9} -background {#d9d9d9} -command AddObs \
        -foreground {#000000} -highlightcolor black -pady 0 -text Add 
    vTcl:DefineAlias "$site_3_0.but46" "Button4" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but47 \
        -activebackground {#d9d9d9} -background {#d9d9d9} -command EditObs \
        -foreground {#000000} -highlightcolor black -pady 0 -text Edit 
    vTcl:DefineAlias "$site_3_0.but47" "Button5" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but48 \
        -activebackground {#d9d9d9} -background {#d9d9d9} -command DelObs \
        -foreground {#000000} -highlightcolor black -pady 0 -text Delete 
    vTcl:DefineAlias "$site_3_0.but48" "Button6" vTcl:WidgetProc "Toplevel1" 1
    button $site_3_0.but49 \
        -activebackground {#d9d9d9} -background {#d9d9d9} -command ShowImg \
        -foreground {#000000} -highlightcolor black -pady 0 -state disabled \
        -text Image 
    vTcl:DefineAlias "$site_3_0.but49" "Button7" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.scr44 \
        -in $site_3_0 -x 10 -y 20 -width 231 -relwidth 0 -height 195 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tex45 \
        -in $site_3_0 -x 10 -y 220 -width 234 -relwidth 0 -height 144 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but46 \
        -in $site_3_0 -x 20 -y 400 -anchor nw -bordermode ignore 
    place $site_3_0.but47 \
        -in $site_3_0 -x 90 -y 400 -anchor nw -bordermode ignore 
    place $site_3_0.but48 \
        -in $site_3_0 -x 170 -y 400 -anchor nw -bordermode ignore 
    place $site_3_0.but49 \
        -in $site_3_0 -x 90 -y 370 -anchor nw -bordermode ignore 
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.can42 \
        -in $top -x 550 -y 240 -width 271 -relwidth 0 -height 191 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $top.can43 \
        -in $top -x 550 -y 60 -width 271 -relwidth 0 -height 171 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.ent44 \
        -in $top -x 570 -y 20 -anchor nw -bordermode ignore 
    place $top.but45 \
        -in $top -x 770 -y 20 -anchor nw -bordermode ignore 
    place $top.tLa49 \
        -in $top -x 10 -y 10 -width 280 -relwidth 0 -height 435 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab43 \
        -in $top -x 300 -y 10 -width 250 -relwidth 0 -height 435 -relheight 0 \
        -anchor nw -bordermode ignore 

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
Window show .top37 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}

