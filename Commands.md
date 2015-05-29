

# Global commands #

Global commands are layout agnostic. They can and ought to be available no matter what tiling layout is in place.

## tile ##

Picks the current tiler for the given monitor/workspace, and initiates its corresponding layout routine. The tile command works on a per monitor basis.

Also, "tile" can be appended with individual tiler names in order to avoid having to cycle to the layout you want. For example, "tile.Center" will invoke the Center layout algorithm. (Note: the tiling layout being called must be specified in the [tilers](Configuration#tilers.md) list.)

## untile ##

Untile.