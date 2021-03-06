import os
import subprocess
import random

from typing import List

from libqtile import hook, bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


###############################################################################
### Vars
###############################################################################
qtile_home = '~/.config/qtile'

# Keys
mod = 'mod4'
alt = 'mod1'
ctrl = 'control'
shift = 'shift'
space = 'space'
enter = 'Return'
tab = 'Tab'
esc = 'Escape'

# Fonts
font = 'CaskaydiaCove Nerd Font Medium'
font_bold = 'CaskaydiaCove Nerd Font Bold'
font_size = 13

# Applications
terminal = guess_terminal()
launcher = 'rofi -show drun'
browser = 'google-chrome-stable'
editor = 'emacsclient -c'

# System
lock_screen = 'betterlockscreen -l pixel'
suspend = 'systemctl suspend & ' + lock_screen

# Colors
colors = {
    'bg': '#1e232d',
    'bga': '#2E3440',
    'fg': '#d8dee9',
    'black0': '#2E3440',
    'black1': '#3B4252',
    'black2': '#434C5E',
    'black4': '#4C566A',
    'white0': '#D8DEE9',
    'white1': '#E5E9F0',
    'white2': '#ECEFF4',
    'red': '#bf616a',
    'orange': '#D08770',
    'yellow': '#EBCB8B',
    'green': '#A3BE8C',
    'pink': '#B48EAD',
    'blue0': '#8FBCBB',
    'blue1': '#88c0d0',
    'blue2': '#81A1C1',
    'blue3': '#5E81AC',
}

# Gradients
gradients = [
    ['#8FBCBB', '#88C0D0'],
    ['#8FBCBB', '#81A1C1'],
    ['#8FBCBB', '#5E81AC'],
    ['#88C0D0', '#81A1C1'],
    ['#81A1C1', '#5E81AC']
]

# Icons
icons = {
    'clock': '\uf017',
    'calendar': '\uf133',
    'volume': '\uf027',
    'chip': '\uf2db',
    'browser': '\ue743',
    'code': '\ue696',
    'terminal': '\uf120',
    'tools': '\uf7d9',
    'remote': '\ue066',
    'music': '\ue405',
    'cube': '\uf1b2',
    'network': '\uf6ff',
    'hdd': '\uf0a0',
    'python': '\ue606',
}

# Layout Theme
layout_theme = {
    'border_width': 3,
    'margin': 5,
    'border_focus': 'd3dee9',
    'border_normal': '3b4252',
    'font': font,
    'grow_amount': 2,
}

###############################################################################
### Functions
###############################################################################

volume_script = os.path.expanduser('~/.scripts/volume')

def volume_up(qtile):
    subprocess.call([volume_script, 'up'])

def volume_down(qtile):
    subprocess.call([volume_script, 'down'])

def volume_toggle(qtile):
    subprocess.call([volume_script, 'toggle'])

###############################################################################
### Autostart
###############################################################################
@hook.subscribe.startup
def autorestart():
    autorestart_script = os.path.expanduser(qtile_home + '/autorestart.sh')
    subprocess.call([autorestart_script])

@hook.subscribe.startup_once
def autostart():
    autostart_script = os.path.expanduser(qtile_home + '/autostart.sh')
    subprocess.call([autostart_script])

###############################################################################
### Keybindings
###############################################################################
keys = [
    # Switch between windows
    Key([mod], 'h', lazy.layout.left(), desc='Move focus to left'),
    Key([mod], 'l', lazy.layout.right(), desc='Move focus to right'),
    Key([mod], 'j', lazy.layout.down(), desc='Move focus down'),
    Key([mod], 'k', lazy.layout.up(), desc='Move focus up'),
    Key([mod], space, lazy.layout.next(),
        desc='Move window focus to other window'),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, shift], 'h', lazy.layout.shuffle_left(),
        desc='Move window to the left'),
    Key([mod, shift], 'l', lazy.layout.shuffle_right(),
        desc='Move window to the right'),
    Key([mod, shift], 'j', lazy.layout.shuffle_down(),
        desc='Move window down'),
    Key([mod, shift], 'k', lazy.layout.shuffle_up(),
        desc='Move window up'),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, ctrl], 'h', lazy.layout.grow_left(),
        desc='Grow window to the left'),
    Key([mod, ctrl], 'l', lazy.layout.grow_right(),
        desc='Grow window to the right'),
    Key([mod, ctrl], 'j', lazy.layout.grow_down(),
        desc='Grow window down'),
    Key([mod, ctrl], 'k', lazy.layout.grow_up(),
        desc='Grow window up'),
    Key([mod, ctrl], 'n', lazy.layout.normalize(),
        desc='Reset all window sizes'),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, shift], enter, lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'),

    # Launch Applications
    Key([mod], enter, lazy.spawn(terminal), desc='Launch terminal'),
    Key([mod], 'w', lazy.spawn(browser)),
    Key([mod], 'e', lazy.spawn(editor)),
    Key([mod], space, lazy.spawn(launcher)),

    # Toggle between different layouts as defined below
    Key([mod], tab, lazy.next_layout(), desc='Toggle between layouts'),
    Key([mod], 'q', lazy.window.kill(), desc='Kill focused window'),
    Key([alt], 'F4', lazy.window.kill(), desc='Kill focused window'),

    # System
    Key([mod, shift], esc, lazy.restart(), desc='Restart Qtile'),
    Key([mod, ctrl], esc, lazy.shutdown(), desc='Shutdown Qtile'),
    Key([mod], 'r', lazy.spawncmd(),
        desc='Spawn a command using a prompt widget'),
    Key([mod, ctrl], 'o', lazy.spawn(lock_screen), desc='Lock screen'),
    Key([mod, ctrl], 'p', lazy.spawn(suspend), desc='Lock and suspend system.'),

    # Media
    # Key([], 'XF86AudioRaizeVolume', lazy.spawn('amixer sset Master 5%+')),
    # Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer sset Master 5%-')),
    # Key([], 'XF86AudioMute', lazy.spawn('amixer sset Master toggle')),
    Key([mod], 'Up', lazy.spawn('amixer sset Master 5%+')),
    Key([mod], 'Down', lazy.spawn('amixer sset Master 5%-')),
]

###############################################################################
### Groups (workspaces)
###############################################################################

workspaces = [
    { 'label': icons['browser'], 'name': '1', 'key': '1', 'matches': [] },
    { 'label': icons['code'], 'name': '2', 'key': '2', 'matches': [] },
    { 'label': icons['remote'], 'name': '3', 'key': '3', 'matches': [] },
    { 'label': '4', 'name': '4', 'key': '4', 'matches': [] },
    { 'label': '5', 'name': '5', 'key': '5', 'matches': [] },
    { 'label': '6', 'name': '6', 'key': '6', 'matches': [] },
    { 'label': '7', 'name': '7', 'key': '7', 'matches': [] },
    { 'label': '8', 'name': '8', 'key': '8', 'matches': [] },
    { 'label': icons['music'], 'name': '9', 'key': '9', 'matches': [] },
]

groups = []

for ws in workspaces:
    matches = ws['matches'] if 'matches' in ws else None
    groups.append(Group(ws['name'], label=ws['label'], matches=matches))
    keys.extend([
        Key([mod], ws['key'], lazy.group[ws['name']].toscreen(),
            desc='Switch to group {}'.format(ws['label']) ),

        Key([mod, shift], ws['key'], lazy.window.togroup(ws['name'], switch_group=False),
            desc='Switch to & move focused window to group {}'.format(ws['label'])),
    ])

"""

groups = [Group(i) for i in '123456789']

for g in groups:
    keys.extend([
        Key([mod], g.name, lazy.group[g.name].toscreen(toggle=False),
            desc='Switch to group {}'.format(g.name)),
        Key([mod, shift], g.name, lazy.window.togroup(g.name, switch_group=False),
            desc='Switch focused window to group {}'.format(g.name))
    ])
"""

###############################################################################
### Layouts
###############################################################################
layouts = [
    layout.Bsp(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Matrix(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=font,
    fontsize=font_size,
    padding=16,
    foreground=colors['fg'],
    background=colors['bg']
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(padding=10, foreground=colors['bg']),
                widget.TextBox(text=icons['python'], foreground=colors['blue0']),
                widget.GroupBox(
                    highlight_color=gradients[0],
                    highlight_method='block',
                    block_highlight_text_color=colors['black0'],
                    this_current_screen_border=colors['blue1'],
                    # this_screen_border='',
                    other_current_screen_border=colors['green'],
                    # other_screen_border=colors['green'],
                    foreground=colors['fg'],
                    background=colors['bg'],
                    hide_unused=True,
                    padding=10,
                    rounded=True
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        'launch': ('#ff0000', '#ffffff'),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.CheckUpdates(
                    display_format=icons['cube'] + '  {updates}',
                    custom_command='checkupdates+aur',
                ),
                widget.DF(
                    fmt=icons['hdd'] + '  {}',
                    measure='G',
                    warn_space=43,
                    visible_on_warn=True,
                    warn_color=colors['fg'],
                ),
                widget.Net(
                    fmt=icons['network'] + '  {}',
                    foreground=colors['blue2']
                ),
                widget.Volume(
                    fmt=icons['volume'] + '  {}',
                    foreground=colors['blue0']
                ),
                widget.Clock(
                    fmt=icons['clock'] + '  {}',
                    format='%H:%M',
                    foreground=colors['pink']
                ),
                widget.Clock(
                    fmt=icons['calendar'] + '  {}',
                    format='%a %d/%m/%Y',
                    foreground=colors['green']
                ),
                widget.CurrentLayoutIcon(margin=10),
                widget.Systray(),
                # widget.QuickExit(),
                widget.Sep(padding=10, foreground=colors['bg']),
            ],
            28,
            background=colors['bg']
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = 'smart'

wmname = 'LG3D'
