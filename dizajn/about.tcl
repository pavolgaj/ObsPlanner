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

#############################################################################
# vTcl Code to Load User Fonts

vTcl:font:add_font \
    "-family {DejaVu Sans} -size 10 -weight normal -slant roman -underline 1 -overstrike 0" \
    user \
    vTcl:font10
vTcl:font:add_font \
    "-family {DejaVu Sans} -size 14 -weight bold -slant roman -underline 0 -overstrike 0" \
    user \
    vTcl:font9
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
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
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
        -background {#d9d9d9} 
    wm focusmodel $top passive
    wm geometry $top 300x240+542+240
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 1585 870
    wm minsize $top 1 1
    wm overrideredirect $top 0
    wm resizable $top 0 0
    wm deiconify $top
    wm title $top "About"
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    canvas $top.can38 \
        -background {#d9d9d9} -borderwidth 2 -closeenough 1.0 -height 71 \
        -insertbackground black -relief ridge -selectbackground {#c4c4c4} \
        -selectforeground black -width 81 
    vTcl:DefineAlias "$top.can38" "Canvas1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab39 \
        -background {#d9d9d9} -font $::vTcl(fonts,vTcl:font9,object) \
        -foreground {#000000} -text ObsPlaner 
    vTcl:DefineAlias "$top.lab39" "Label1" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab40 \
        -background {#d9d9d9} -foreground {#000000} \
        -text {(c) Pavol Gajdoš, 2019} 
    vTcl:DefineAlias "$top.lab40" "Label2" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab41 \
        -background {#d9d9d9} -foreground {#000000} -text {version 0.1} 
    vTcl:DefineAlias "$top.lab41" "Label3" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab42 \
        -background {#d9d9d9} -font $::vTcl(fonts,vTcl:font10,object) \
        -foreground {#0505f7} -highlightcolor {#0505f7} -text pavolg.6f.sk 
    vTcl:DefineAlias "$top.lab42" "Label4" vTcl:WidgetProc "Toplevel1" 1
    label $top.lab43 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#d9d9d9} -font $::vTcl(fonts,vTcl:font10,object) \
        -foreground {#0505f7} -highlightcolor {#0505f7} \
        -text github.com/pavolgaj/ObsPlanner 
    vTcl:DefineAlias "$top.lab43" "Label4_1" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.can38 \
        -in $top -x 111 -y 10 -width 81 -relwidth 0 -height 71 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab39 \
        -in $top -x 90 -y 90 -anchor nw -bordermode ignore 
    place $top.lab40 \
        -in $top -x 81 -y 210 -width 150 -height 21 -anchor nw \
        -bordermode ignore 
    place $top.lab41 \
        -in $top -x 110 -y 120 -anchor nw -bordermode ignore 
    place $top.lab42 \
        -in $top -x 100 -y 150 -anchor nw -bordermode ignore 
    place $top.lab43 \
        -in $top -x 30 -y 180 -width 250 -height 21 -anchor nw \
        -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

#############################################################################
## Binding tag:  _TopLevel

bind "_TopLevel" <<Create>> {
    if {![info exists _topcount]} {set _topcount 0}; incr _topcount
}
bind "_TopLevel" <<DeleteWindow>> {
    if {[set ::%W::_modal]} {
                vTcl:Toplevel:WidgetProc %W endmodal
            } else {
                destroy %W; if {$_topcount == 0} {exit}
            }
}
bind "_TopLevel" <Destroy> {
    if {[winfo toplevel %W] == "%W"} {incr _topcount -1}
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
