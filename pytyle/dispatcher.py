import time

import ptxcb
import tilers
from command import Command
from state import STATE
from window import Window
from tile import Tile

class Dispatcher(object):
    def __init__(self, event_data):
        self._event_data = event_data
        self._stop = False

        assert 'event' in self._event_data

        if hasattr(self, self._event_data['event']):
            getattr(self, self._event_data['event'])()
        else:
            print 'Unrecognized event: %s' % self._event_data['event']
            return

        ptxcb.Window.exec_queue()
        Tile.exec_queue()

        ptxcb.XCONN.push()

    def stop(self):
        return self._stop

    def KeyPressEvent(self):
        cmd = Command.lookup(self._event_data['keycode'], self._event_data['modifiers'])
        x = cmd.get_command()

        if x == 'quit':
            for tiler in Tile.iter_tilers():
                tiler.untile()

            self._stop = True
        elif x == 'debug':
            STATE.print_hierarchy(*STATE.get_active_wsid_and_mid())
        else:
            Tile.dispatch(tilers.Vertical, x)

    def ConfigureNotifyEvent(self):
        win = Window.deep_lookup(self._event_data['window'].wid)

        if win and win.lives():
            if win.pytyle_moved:
                win.pytyle_moved = False
            else:
                if STATE.pointer_grab and win.width == self._event_data['width'] and win.height == self._event_data['height']:
                    pointer = ptxcb.XROOT.query_pointer()

                    if ptxcb.XROOT.button_pressed():
                        STATE.moving = True

                win.set_geometry(
                    self._event_data['x'],
                    self._event_data['y'],
                    self._event_data['width'],
                    self._event_data['height']
                )

    def PropertyNotifyEvent(self):
        a = self._event_data['atom']

        if a == '_NET_ACTIVE_WINDOW':
            STATE.refresh_active()
        elif a == '_NET_CLIENT_LIST':
            old = ptxcb.XROOT.windows
            new = ptxcb.XROOT.get_window_ids()

            if old != new:
                added, removed = STATE.handle_window_add_or_remove(old, new)

                # Tile.sc_windows(added, removed)
        elif a == '_NET_WM_STATE':
            win = Window.lookup(self._event_data['window'].wid)

            if win and win.lives():
                win.update_property('_NET_WM_STATE')
                tiler = Tile.lookup(win.monitor.workspace.id, win.monitor.id)

                if tiler:
                    if win.tilable() and not win.container:
                        time.sleep(0.2)
                        tiler.add(win)
                    elif not win.tilable() and win.container:
                        time.sleep(0.2)
                        tiler.remove(win)
        else:
            win = Window.lookup(self._event_data['window'].wid)

            if win and win.lives():
                win.update_property(a)

    # Don't register new windows this way... Use _NET_CLIENT_LIST instead
    # You did it the first time for good reason!
    def CreateNotifyEvent(self):
        pass


    # Use the following to track window movement..? Hmmm
    # ConfigureNotify doesn't get reported when windows are moved (yes when resized)
    # It is reported for the ROOT window, however there is no way to know
    # which window is being moved... Check out XQueryTree!
    # http://xcb.freedesktop.org/manual/group__XCB____API.html#g4d0136b27bbab9642aa65d2a3edbc03c

    def FocusInEvent(self):
        if self._event_data['mode'] == 'Ungrab':
            STATE.pointer_grab = False

            if STATE.moving:
                pointer = ptxcb.XROOT.query_pointer()
                win = Window.deep_lookup(pointer.child)

                if win:
                    for tiler in Tile.iter_tilers(win.monitor.workspace.id):
                        if tiler:
                            tiler.needs_tiling()

                STATE.moving = False

    def FocusOutEvent(self):
        if self._event_data['mode'] == 'Grab':
            STATE.pointer_grab = True
