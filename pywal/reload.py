"""
Reload programs.
"""
import re
import shutil
import subprocess

from .settings import CACHE_DIR, HOME, MODULE_DIR
from . import util


def xrdb(xrdb_file=None):
    """Merge the colors into the X db so new terminals use them."""
    xrdb_file = xrdb_file or CACHE_DIR / "colors.Xresources"

    if shutil.which("xrdb"):
        subprocess.call(["xrdb", "-merge", xrdb_file],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)


def gtk():
    """Move gtkrc files to the correct location."""
    theme_path = HOME / ".themes" / "Flatabulous-wal"
    gtk2_file = CACHE_DIR / "colors-gtk2.rc"
    gtk3_file = __cache_dir__ / "colors-gtk3.css"

    if theme_path.is_dir():
        if gtk2_file.is_file():
            shutil.copy(gtk2_file, theme_path / "gtk-2.0")

        if gtk3_file.is_file():
            shutil.copy(gtk3_file, theme_path / "gtk-3.0")
            shutil.copy(gtk3_file, theme_path / "gtk-3.20")

        # Here we call a Python 2 script to reload the GTK themes.
        # This is done because the Python 3 GTK/Gdk libraries don't
        # provide a way of doing this.
        if shutil.which("python2"):
            util.disown("python2", MODULE_DIR / "scripts" / "gtk_reload.py")
        else:
            print("warning: GTK2 reload support requires Python 2.")


def i3():
    """Reload i3 colors."""
    if shutil.which("i3-msg"):
        util.disown("i3-msg", "reload")


def polybar():
    """Reload polybar colors."""
    if shutil.which("polybar"):
        util.disown("pkill", "-USR1", "polybar")


def env(xrdb_file=None):
    """Reload environment."""
    gtk()
    xrdb(xrdb_file)
    i3()
    polybar()
    print("reload: Reloaded environment.")


def colors(vte, cache_dir=CACHE_DIR):
    """Reload the current scheme."""
    sequence_file = cache_dir / "sequences"

    if sequence_file.is_file():
        sequences = "".join(util.read_file(sequence_file))

        # If vte mode was used, remove the unsupported sequence.
        if vte:
            sequences = re.sub(r"\]708;(\[.{0,3}\])?\#.{6}", "", sequences)

        print(sequences, end="")

    exit(0)
