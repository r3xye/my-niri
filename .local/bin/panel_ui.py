#!/usr/bin/env python3

import html

import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")

from gi.repository import Gdk, Gtk, GtkLayerShell


CSS = b"""
window.quick-panel {
    background: #1d2021;
    border: 1px solid #665c54;
    border-radius: 18px;
}

window.quick-panel box.root {
    padding: 16px;
}

label.title {
    color: #fbf1c7;
    font: 700 16px "JetBrains Mono Nerd Font";
}

label.subtitle {
    color: #a89984;
    font: 12px "JetBrains Mono Nerd Font";
}

box.actions {
    margin-top: 12px;
    margin-bottom: 12px;
}

button.action {
    background: #282828;
    border: 1px solid #504945;
    border-radius: 12px;
    box-shadow: none;
    padding: 8px 10px;
}

button.action:hover,
button.action:focus {
    background: #3c3836;
    border-color: #d79921;
}

button.action label {
    color: #ebdbb2;
    font: 13px "JetBrains Mono Nerd Font";
}

scrolledwindow.list {
    background: transparent;
    border: none;
}

list {
    background: transparent;
}

list row {
    background: transparent;
    border-radius: 12px;
    margin-bottom: 6px;
    padding: 0;
}

list row:selected,
list row:hover {
    background: #3c3836;
}

list row box.item {
    padding: 10px 12px;
}

label.item-title {
    color: #ebdbb2;
    font: 13px "JetBrains Mono Nerd Font";
}

label.item-subtitle {
    color: #a89984;
    font: 11px "JetBrains Mono Nerd Font";
}
"""


def _apply_css():
    screen = Gdk.Screen.get_default()
    if screen is None:
        return
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_screen(
        screen,
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )


def _mnemonic_markup(label, mnemonic):
    if not mnemonic:
        return html.escape(label)
    idx = label.lower().find(mnemonic.lower())
    if idx < 0:
        return html.escape(label) + f"  [{html.escape(mnemonic.upper())}]"
    start = html.escape(label[:idx])
    mid = html.escape(label[idx])
    end = html.escape(label[idx + 1 :])
    return f"{start}<u>{mid}</u>{end}"


class QuickPanel:
    def __init__(self, title, subtitle, actions, items, width, height, xoffset, yoffset):
        _apply_css()
        self.actions = {a["mnemonic"].lower(): a for a in actions if a.get("mnemonic")}
        self.items = items
        self.result = None

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_name("quick-panel")
        self.window.get_style_context().add_class("quick-panel")
        self.window.set_default_size(width, height)
        self.window.set_resizable(False)
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.connect("destroy", self._quit)
        self.window.connect("key-press-event", self._on_key_press)

        GtkLayerShell.init_for_window(self.window)
        GtkLayerShell.set_layer(self.window, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_margin(self.window, GtkLayerShell.Edge.LEFT, xoffset)
        GtkLayerShell.set_margin(self.window, GtkLayerShell.Edge.TOP, yoffset)
        GtkLayerShell.set_keyboard_mode(self.window, GtkLayerShell.KeyboardMode.ON_DEMAND)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.get_style_context().add_class("root")
        self.window.add(root)

        title_label = Gtk.Label()
        title_label.set_markup(f'<span class="title">{html.escape(title)}</span>')
        title_label.set_xalign(0)
        root.pack_start(title_label, False, False, 0)

        if subtitle:
            subtitle_label = Gtk.Label()
            subtitle_label.set_markup(f'<span class="subtitle">{html.escape(subtitle)}</span>')
            subtitle_label.set_xalign(0)
            root.pack_start(subtitle_label, False, False, 4)

        if actions:
            actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            actions_box.get_style_context().add_class("actions")
            root.pack_start(actions_box, False, False, 0)
            for action in actions:
                button = Gtk.Button()
                button.get_style_context().add_class("action")
                label = Gtk.Label()
                label.set_use_markup(True)
                label.set_markup(_mnemonic_markup(action["label"], action.get("mnemonic")))
                button.add(label)
                button.connect("clicked", self._on_action_clicked, action["id"])
                actions_box.pack_start(button, False, False, 0)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self._on_row_activated)

        for item in items:
            row = Gtk.ListBoxRow()
            row.item_id = item["id"]

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            box.get_style_context().add_class("item")

            title_row = Gtk.Label()
            title_row.set_markup(f'<span class="item-title">{html.escape(item["title"])}</span>')
            title_row.set_xalign(0)
            box.pack_start(title_row, False, False, 0)

            subtitle_text = item.get("subtitle")
            if subtitle_text:
                subtitle_row = Gtk.Label()
                subtitle_row.set_markup(f'<span class="item-subtitle">{html.escape(subtitle_text)}</span>')
                subtitle_row.set_xalign(0)
                box.pack_start(subtitle_row, False, False, 0)

            row.add(box)
            self.listbox.add(row)

        if items:
            self.listbox.select_row(self.listbox.get_row_at_index(0))

        scroller = Gtk.ScrolledWindow()
        scroller.get_style_context().add_class("list")
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroller.add(self.listbox)
        root.pack_start(scroller, True, True, 0)

        self.window.show_all()

    def _set_result(self, kind, value):
        self.result = {"kind": kind, "value": value}
        self.window.close()

    def _on_action_clicked(self, _button, action_id):
        self._set_result("action", action_id)

    def _on_row_activated(self, _listbox, row):
        self._set_result("item", row.item_id)

    def _on_key_press(self, _widget, event):
        key = Gdk.keyval_name(event.keyval)
        if key == "Escape":
            self.window.close()
            return True
        if key in ("Return", "KP_Enter"):
            row = self.listbox.get_selected_row()
            if row is not None:
                self._set_result("item", row.item_id)
                return True
        if key in ("Up", "Down"):
            row = self.listbox.get_selected_row()
            index = row.get_index() if row is not None else 0
            if key == "Up":
                index = max(index - 1, 0)
            else:
                index = min(index + 1, len(self.items) - 1)
            next_row = self.listbox.get_row_at_index(index)
            if next_row is not None:
                self.listbox.select_row(next_row)
                next_row.grab_focus()
            return True
        char = Gdk.keyval_to_unicode(event.keyval)
        if char:
            action = self.actions.get(chr(char).lower())
            if action:
                self._set_result("action", action["id"])
                return True
        return False

    def _quit(self, *_args):
        Gtk.main_quit()

    def run(self):
        self.window.present()
        Gtk.main()
        return self.result


def run_panel(*, title, subtitle="", actions=None, items=None, width=480, height=420, xoffset=74, yoffset=58):
    panel = QuickPanel(
        title=title,
        subtitle=subtitle,
        actions=actions or [],
        items=items or [],
        width=width,
        height=height,
        xoffset=xoffset,
        yoffset=yoffset,
    )
    return panel.run()
