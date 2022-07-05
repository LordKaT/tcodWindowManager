from __future__ import annotations
from tcod.console import Console
from tcod.event import KeyDown
import tcod.event as Event

class WindowManager:
  def __init__(self) -> None:
    self.window_list = []
    self.disable_input_focus = False

  def get_window(self, window_title: str) -> WindowObj:
    for window in self.window_list:
      if window.title == window_title:
        return window
    return None

  def create_window(self, window_obj: WindowObj) -> WindowObj:
    window_obj.open()
    self.window_list.append(window_obj)
    return window_obj

  def open(self, window_obj: WindowObj):
    window_obj.open()
    window_obj.got_focus()
    self.window_list.append(window_obj)
  
  def close(self, window_title: str="") -> None:
    if window_title == "":
      self.window_list[-1].close()
      self.window_list.pop()
      return

    for idx, window in enumerate(self.window_list):
      if window.title == window_title:
        window.lost_focus()
        window.close()
        del self.window_list[idx]
        return
    print("WindowManager close: window \"" + window_title + "\" not found!")

  def bring_to_front(self, window_title: str) -> None:
    if window_title == "":
      print("WindowManager bring_to_front: window_title cannot be blank!")
      return
    for idx, window in enumerate(self.window_list):
      if window.title == window_title:
        self.window_list.append(self.window_list.pop(idx))
        print(self.window_list[-1].title)
        return

  def has_focus(self, window_title: str="") -> bool:
    if window_title == "":
      print("WindowManager has_focus: window_title cannot be blank!")
      return
    return window_title == self.window_list[-1].title

  def input(self, event: KeyDown) -> bool:
    if len(self.window_list) == 0:
      return False
    if not self.disable_input_focus:
      match event.sym:
        case Event.K_TAB: # Cycle input focus
          self.window_list[-1].lost_focus()
          self.window_list.append(self.window_list.pop(0))
          self.window_list[-1].got_focus()
    return self.window_list[-1].input(event)

  def render(self, console: Console):
    for window in self.window_list:
      window.render(console)

class WindowObj():
  def __init__(self, window_manager: WindowManager=None, x: int=0, y: int=0, w: int=1, h:int=1,
              title: str="Window Title", content: str="",
              fg: tuple=(255, 255, 255), bg: tuple=(0, 0, 0)) -> None:
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.title = title
    self.content = content
    self.fg = fg
    self.bg = bg
    
    if window_manager == None:
      print("WindowObj: WindowManager cannot be None!")
      raise SystemExit()
    self.window_manager = window_manager

  def has_focus(self) -> bool: # do I have focus?
    return self.window_manager.has_focus(self.title)

  def got_focus(self) -> None:
    pass

  def lost_focus(self) -> None:
    pass

  def open(self):
    self.got_focus()

  def close(self):
    self.lost_focus()

  def input(self, event: KeyDown):
    return False

  def render(self, console: Console):
    console.draw_frame(self.x, self.y, self.w, self.h, title=self.title, fg=self.fg, bg=self.bg)
    console.print_box(self.x+1, self.y+1, self.w-2, self.h-2, self.content, fg=self.fg, bg=self.bg)
    if self.has_focus():
      console.print(self.x+self.w-2, self.y, '*')
