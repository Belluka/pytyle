## PyTyle 2 Development ##

This space is for the PyTyle project. PyTyle is an on-demand automatic (XMonad style) and manual (Musca style) tiling manager that works with existing EMWH compliant window managers. PyTyle was developed using Openbox, and so it will likely work best with that window manager.

The idea behind PyTyle is that tiling window managers have evolved an efficient means of organizing your windows, but can be overwhelming to some users (or if you're like me, you just want a traditional floating window manager from time to time). Thus, PyTyle slides unobtrusively into your window manager and allows one to tile on a per-workspace basis--only when you want it.

## NEW in PyTyle 2 ##

PyTyle is currently in the process of being re-written. In particular, the following are some of the new features:

  * The XCB library is used instead of Xlib, which ought to be faster. (It's also what all the cool kids are using nowadays.)
  * A [manual tiling](Manual_Tiling.md) mode, a la Musca. This allows one to construct your own layouts from scratch, and, as a result, have more control over the size and placement of your windows.
  * Automatic tiling layouts, a la Xmonad: Vertical(Rows), Horizontal(Rows), Cascade, Center, and Maximal. With automatic tiling, PyTyle decides how best to use your screen real estate.
  * Support for undecorated windows. This includes removing decorations from windows for you, and drawing smaller borders around each window (to indicate whether a window is active or not). Border sizes and colors are configurable.
  * Drag-and-drop windows to other positions in any tiling layout.
  * Automatic detection of panels (and anything that sets struts), even on multi-monitor setups.
  * A more versatile configuration system, with cascading options. (i.e., set options based on tiler, workspace, monitor, or any combination of the three).
  * Move any window from a tiling state to a floating state, even if the workspace its on is in a tiling state.

Still in the works:

  * A command line interface to interact with PyTyle (i.e., calling commands like "pytyle2 tile.Center --workspace=2 --monitor=1")
  * Better error checking mechanisms to prevent windows from getting resized to bad values.

Window managers tested:

  * Openbox
  * KWin

## Still in PyTyle 2 ##

  * Continuous tiling management on a per monitor per workspace basis. This means you can have the efficiency of tiling on one screen/workspace, and your regular floating window management on the other.
  * Multi-monitor support using Xinerama.
  * All the traditional tiling actions: untile, cycle layouts, cycle windows, move focus or windows between screens, resize windows, switch windows.
  * Dynamically reload the configuration file, which contains a plethora of options including modifiable keybindings and layout-specific options.
  * Allows for setting of margins or padding.
  * Set PyTyle to always ignore certain windows from tiling (like gmrun, krunner or gimp).
  * Change the order through which layouts can be cycled.
  * PyTyle can also automatically tile any monitor/workspace on startup.

## How to Install ##

First, you're going to need [xpyb](http://cgit.freedesktop.org/xcb/xpyb/). You should check your distribution for this package first. Alternatively, you can install [xpyb-ng](https://github.com/dequis/xpyb-ng), which is a fork of xpyb that is trying re-implement a large proportion of xpyb's C code to Python code. It currently works with PyTyle 2.

Secondly, you can grab PyTyle 2 from the [mercurial repository](http://code.google.com/p/pytyle/source/checkout), and install it with:

` sudo python setup.py install `

Or, if you're running both Python 2 and Python 3 side-by-side,

` sudo python2 setup.py install `

Finally, you can run PyTyle 2 like so,

` pytyle2 `