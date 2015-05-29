## Manual Tiling ##

Manual tiling in PyTyle is a complex issue. The amount of trickery it puts the window manager through is substantive, and for this reason, manual tiling should be considered nothing short of experimental.

One of the biggest contributors to why there is so much trickery is the notion of a container that represents an empty space. To a traditional floating window manager, this notion doesn't really exist, and so, PyTyle must work around this fact.

It is currently doing this by creating so-called "place holder" windows. These are windows created inside the PyTyle program (and therefore, if PyTyle is stopped, these windows will disappear). They are purposefully created so that the running window manager will recognize them (unlike the windows used to draw borders around each window, i.e., the bordered windows have the [override redirect](http://tronche.com/gui/x/xlib/window/attributes/override-redirect.html) flag set), and treat them as normal windows.

But, irrevocably, they aren't normal windows. They must be destroyed and re-created whenever tiling layouts change, or if a new frame is created/destroyed, and there are fewer windows than frames. This is the complication and is one of the things that makes maintaining a manual layout a bit complex.

For example, manual layouts should not be started automatically when PyTyle starts (i.e., "tile\_on\_startup" should be false for all manual layouts). This is because a place holder window may be created when a manual layout is invoked, and it could end up on the wrong workspace if invoked on a workspace other than the one it is supposed to be tiling.

Finally, the data structure representing the manual layout is that of a tree. Each node is either a HorizontalFrame, a VerticalFrame, or a LeafFrame. Only LeafFrames can contain windows directly, and no frame may have a direct child like itself. So for example, a HorizontalFrame's parent cannot be a HorizontalFrame, but a HorizontalFrame's parent's parent could be a HorizontalFrame. Also, either HorizontalFrame or VerticalFrame can contain any number of children except 1. That is, if a HorizontalFrame or a VerticalFrame has only one child, then it ought to be removed and have its only child assigned as a child to its parent.

Layout changes are made to the data structure in a hierarchical fashion, and window positions are determined by a window's ratio with respect to its direct parent. There is a configuration option, shallow\_resize, that affects how this tree is traversed when resizing windows. In particular, if shallow\_resize is set to true, it will only resize windows and its corresponding siblings. However, if it is set to false, it will look to resize siblings of any of its ancestors.