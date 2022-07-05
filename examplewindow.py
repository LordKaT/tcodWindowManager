import tcod.event as Event
from tcod.console import Console
from tcod.event import KeyDown
from windowmanager import WindowManager, WindowObj

'''
this code assumes a screen width/height of 160x90 tiles.

how to use:

window_manager = WindowManager()

# you can also create this without assigning a local variable
main_window = window_manager.create_window(MainWindow(window_manager))
debug_window = window_manager.create_window(DebugWindow(window_manager))

In game loop:

window_manager.render(console)

In input loop:

if isinstance(event, tcod.event.KeyDown):
  window_manager.input(event)
'''

class ConfirmQuitWindow(WindowObj):
  def __init__(self, window_manager: WindowManager = None,
      x: int = 65, y: int = 41, w: int = 30, h: int = 4,
      title: str = "Confirm Quit?", content: str = "Y to Quit\nN to Cancel",
      fg: tuple = (255, 0, 0), bg: tuple = (0, 0, 0)) -> None:
    super().__init__(window_manager, x, y, w, h, title, content, fg, bg)

  def got_focus(self) -> None:
    self.window_manager.disable_input_focus = True

  def lost_focus(self) -> None:
    self.window_manager.disable_input_focus = False

  def input(self, event: KeyDown) -> bool:
    key = event.sym
    match key:
      case Event.K_n:
        self.window_manager.close(self.title)
      case Event.K_y:
        raise SystemExit()
    return False

  def render(self, console: Console) -> None:
    console.draw_frame(self.x, self.y, self.w, self.h, fg=self.fg, bg=self.bg, decoration="╔═╗║ ║╚═╝")
    console.print_box(self.x, self.y, self.w, 1, self.title, alignment=tcod.constants.CENTER)
    console.print_box(self.x+1, self.y+1, self.w-1, self.h-1, self.content, fg=(255, 255, 255), bg=self.bg)
    if self.has_focus():
      console.print(self.x+self.w-2, self.y, '*', fg=(255, 255, 255))
    return

class EscapeWindow(WindowObj):
  def __init__(self, window_manager: WindowManager = None,
    x: int = 50, y: int = 39, w: int = 30, h: int = 8,
    title: str = "Main Menu",
    content: str = (
      "Q) Quit\n"
      "\n"
      "This is a test"
    ),
    fg: tuple = (255, 255, 255), bg: tuple = (0, 0, 0)) -> None:
    super().__init__(window_manager, x, y, w, h, title, content, fg, bg)

  def got_focus(self) -> None:
    self.window_manager.disable_input_focus = True

  def lost_focus(self) -> None:
    self.window_manager.disable_input_focus = False

  def input(self, event: KeyDown):
    key = event.sym
    match key:
      case Event.K_ESCAPE:
        self.window_manager.close(self.title)
      case Event.K_q:
        self.window_manager.create_window(ConfirmQuitWindow(window_manager=self.window_manager))

class MainWindow(WindowObj):
  def __init__(self, window_manager: WindowManager = None,
      x: int = 0, y: int = 0, w: int = 120, h: int = 90,
      title: str = "Main Window", content: str = "",
      fg: tuple = (255, 255, 255), bg: tuple = (0, 0, 0)) -> None:
    super().__init__(window_manager, x, y, w, h, title, content, fg, bg)

  def input(self, event: KeyDown) -> bool:
    key = event.sym
    match key:
      case Event.K_BACKQUOTE:
        if self.window_manager.get_window("Debug Window") == None:
          debug_window = DebugWindow(self.window_manager)
          self.window_manager.create_window(debug_window)
        else:
          self.window_manager.bring_to_front("Debug Window")
      case _:
        return super().input(event)
    return False
        
class DebugWindow(WindowObj):
  def __init__(self, window_manager: WindowManager = None,
      x: int = 120, y: int = 0, w: int = 40, h: int = 90,
      title: str = "Debug Window", content: str = "",
      fg: tuple = (255, 255, 255), bg: tuple = (0, 0, 0)) -> None:
    content = (
      "Debug window activated\n"
      "ESC) ConfirmQuitMenu\n"
      "A) Test Multi-Level Menu\n"
      "B) Close MLW\n"
      "C) Bring Main Window to front\n"
      "I) Inventory Test\n"
    )
    super().__init__(window_manager, x, y, w, h, title, content, fg, bg)

  def input(self, event: KeyDown) -> bool:
    key = event.sym
    match key:
      case Event.K_ESCAPE:
        self.window_manager.create_window(EscapeWindow(window_manager=self.window_manager))
      case Event.K_a: # multi-level window test
        mlw = DebugWindow(self.window_manager, self.x, self.y, self.w, self.h, self.title, self.content)
        mlw.title = "Debug Window " + str(len(self.window_manager.window_list))
        self.window_manager.create_window(mlw)
      case Event.K_b:
        self.window_manager.close(self.title)
      case Event.K_c:
        self.window_manager.bring_to_front("Main Window")
      case Event.K_i:
        self.window_manager.create_window(DebugTestInventoryWindow(window_manager=self.window_manager))
    return False

class DebugTestInventoryWindow(WindowObj):
  def __init__(self, window_manager: WindowManager = None,
      x: int = 50, y: int = 10, w: int = 60, h: int = 70,
      title: str = "Inventory Test", content: str = "",
      fg: tuple = (255, 255, 255), bg: tuple = (0, 0, 0)) -> None:
    super().__init__(window_manager, x, y, w, h, title, content, fg, bg)
    self.inventory = []
    for i in range(1, 37):
      if i < 10:
        self.inventory.append((str(i), chr(i + 47), "Test Item " + str(i)))
      else:
        self.inventory.append((str(i + 88), chr(i + 86), "Test Item " + str(i)))
    for item in self.inventory:
      self.content += item[1] + ") " + item[2] + "\n"

  def got_focus(self) -> None:
    self.window_manager.disable_input_focus = True

  def lost_focus(self) -> None:
    self.window_manager.disable_input_focus = False

  def input(self, event: KeyDown) -> bool:
    key = event.sym
    match key:
      case Event.K_ESCAPE:
        self.window_manager.close(self.title)
      case _:
        keyinput = -1
        if (key >= 48 and key <= 57):
          keyinput = key - 48
        elif (key >= 97 and key <= 122):
          keyinput = key - 87
        print("Inventory input: " + str(keyinput) + " " + self.inventory[keyinput][1] + " " + self.inventory[keyinput][2])
        if keyinput > -1:
          self.window_manager.create_window(DebugTestInventoryInfoWindow(
            window_manager=self.window_manager,
            title=self.inventory[keyinput][2],
            content="This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description This is a test description hi mom"
          ))
    return False

class DebugTestInventoryInfoWindow(WindowObj):
  def __init__(self, window_manager: WindowManager = None,
      x: int = 30, y: int = 30, w: int = 100, h: int = 30,
      title: str = "Item", content: str = "",
      fg: tuple = (255, 255, 255), bg: tuple = (0, 0, 0)) -> None:
    super().__init__(window_manager, x, y, w, h, title, content, fg, bg)
  
  def input(self, event: KeyDown):
    key = event.sym
    match key:
      case Event.K_ESCAPE:
        self.window_manager.close(self.title)
    return False
