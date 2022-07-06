# tcodWindowManager
simple window manager for libtcod written in Python 3

this code assumes a screen width/height of 160x90 tiles. You'll have to modify it to fit your needs, unless I get around to making it more portable :)

How to use:

```
window_manager = WindowManager()

# you can also create this without assigning a local variable

main_window = window_manager.create_window(MainWindow(window_manager))
debug_window = window_manager.create_window(DebugWindow(window_manager))

# In game loop:
window_manager.render(console)

#In input loop:
if isinstance(event, tcod.event.KeyDown):
  window_manager.input(event)
```
