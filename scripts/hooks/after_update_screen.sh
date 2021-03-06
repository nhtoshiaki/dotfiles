#!/bin/bash
# A script executed after screen is changed.

#PRIMARY=
#SECONDARY=

echo "PRIMARY: $PRIMARY"
echo "SECONDARY: $SECONDARY"

function setWallpaper {
    nitrogen --restore
}

function launch_polybar {
    MONITOR1="$1"
    MONITOR2="$2" 
    . "$HOME/.config/polybar/launch.sh"
}

function launch_conky {
    . "$HOME/.config/conky/launch.sh"
}

function set_bspwm_desktops {
    if [[ -n "$1" ]]; then
        if [[ -n "$2" ]]; then
            bspc monitor "$1" -d I II III IV V VI VII
            bspc monitor "$2" -d VIII IX X
        else
            bspc monitor "$1" -d I II III IV V VI VII VIII IX X
        fi
    fi
}

case "$CURRENT_DESKTOP" in
    "i3")
        launch_polybar "$PRIMARY" "$SECONDARY"
        launch_conky
        ;;
    "bspwm")
        set_bspwm_desktops "$PRIMARY" "$SECONDARY"
        launch_polybar "$PRIMARY" "$SECONDARY"
        launch_conky
        ;;
    *)
        ;;
esac

setWallpaper

