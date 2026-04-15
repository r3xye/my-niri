# my-niri

<p align="center">
  <img src="assets/screenshot.png" alt="my-niri desktop screenshot" width="100%">
</p>

<p align="center">
  <sub>Niri, Waybar, Wofi, Mako, Kitty, and Swaylock Effects in a Gruvbox-style desktop.</sub>
</p>

Personal Niri desktop dotfiles with a Gruvbox-style Wayland setup.

## Features

- Niri config split into small editable parts.
- Generated `~/.config/niri/config.kdl` is kept local and untracked.
- Waybar, Wofi, Mako, Kitty, and Swaylock configs.
- Swaylock Effects lock screen with screenshot blur, vignette, clock, and themed indicator.
- Helper scripts for workspace rules, app focus/spawn, keyboard layout status, Wi-Fi, and Bluetooth panels.

## Included

- `.config/niri/parts` - source files for the Niri config.
- `.config/niri/build.sh` - builds the local Niri `config.kdl` from local `~/.config/niri/parts`.
- `.config/niri/scripts` - Niri helper scripts.
- `.config/waybar` - Waybar config and style.
- `.config/wofi` - launcher and panel styles.
- `.config/mako` - notification style.
- `.config/kitty` - terminal config.
- `.config/swaylock` - Swaylock Effects theme.
- `.local/bin` - user scripts used by the desktop.

## Installation

Clone the repository and run commands from its root.

### Copy files

Copy the files you want into `$HOME`:

```sh
cp -r .config/kitty ~/.config/
cp -r .config/mako ~/.config/
cp -r .config/waybar ~/.config/
cp -r .config/wofi ~/.config/
cp -r .config/swaylock ~/.config/
cp -r .local/bin ~/.local/
```

For Niri, copy the local source files and build the generated config:

```sh
mkdir -p ~/.config/niri
cp -r .config/niri/parts ~/.config/niri/
cp -r .config/niri/scripts ~/.config/niri/
cp .config/niri/build.sh ~/.config/niri/
~/.config/niri/build.sh
```

### Symlink files

Create links from `$HOME` to this repository:

```sh
ln -sfn "$PWD/.config/kitty" ~/.config/kitty
ln -sfn "$PWD/.config/mako" ~/.config/mako
ln -sfn "$PWD/.config/waybar" ~/.config/waybar
ln -sfn "$PWD/.config/wofi" ~/.config/wofi
ln -sfn "$PWD/.config/swaylock" ~/.config/swaylock

mkdir -p ~/.local
ln -sfn "$PWD/.local/bin" ~/.local/bin
```

For Niri, symlink the editable parts and scripts, then build the local generated config:

```sh
mkdir -p ~/.config/niri
ln -sfn "$PWD/.config/niri/parts" ~/.config/niri/parts
ln -sfn "$PWD/.config/niri/scripts" ~/.config/niri/scripts
ln -sfn "$PWD/.config/niri/build.sh" ~/.config/niri/build.sh
~/.config/niri/build.sh
```

`~/.config/niri/config.kdl` is generated locally and is not tracked.
