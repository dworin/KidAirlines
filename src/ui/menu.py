import curses
from .screen_base import ScreenBase


class Menu(ScreenBase):
    """Generic menu class for navigation"""

    def __init__(self, stdscr, title, options):
        """
        Initialize menu
        options: list of tuples (display_text, callback_function)
        """
        super().__init__(stdscr)
        self.title = title
        self.options = options
        self.current_selection = 0

    def display(self):
        """Display the menu and handle selection"""
        while True:
            self.clear()
            self.draw_header(self.title)
            self.draw_menu_items()
            self.draw_footer("↑/↓: Navigate | 1-9: Select | ENTER: Select | Q: Quit")
            self.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.current_selection = (self.current_selection - 1) % len(self.options)
            elif key == curses.KEY_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.options)
            elif key == ord('\n') or key == curses.KEY_ENTER:
                # Execute selected option
                result = self.options[self.current_selection][1]()
                if result == "EXIT":
                    return "EXIT"
            elif key in [ord('q'), ord('Q')]:
                return "EXIT"
            elif ord('1') <= key <= ord('9'):
                # Handle number key selection
                option_index = key - ord('1')  # Convert to 0-based index
                if option_index < len(self.options):
                    result = self.options[option_index][1]()
                    if result == "EXIT":
                        return "EXIT"

    def draw_menu_items(self):
        """Draw menu items"""
        start_y = 5
        menu_width = 60
        menu_x = (self.width - menu_width) // 2

        for idx, (text, _) in enumerate(self.options):
            y_pos = start_y + idx * 2

            # Add number prefix (1-9)
            number_prefix = f"{idx + 1}. " if idx < 9 else "   "

            if idx == self.current_selection:
                self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
                display_text = f"> {number_prefix}{text} <"
            else:
                self.stdscr.attron(curses.color_pair(1))
                display_text = f"  {number_prefix}{text}  "

            # Center the text
            text_x = menu_x + (menu_width - len(display_text)) // 2
            self.stdscr.addstr(y_pos, text_x, display_text)

            if idx == self.current_selection:
                self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            else:
                self.stdscr.attroff(curses.color_pair(1))


class ListSelector(ScreenBase):
    """Generic list selector for choosing from items"""

    def __init__(self, stdscr, title, items, display_func=None):
        """
        Initialize list selector
        items: list of items to select from
        display_func: function to convert item to display string (default: str)
        """
        super().__init__(stdscr)
        self.title = title
        self.items = items
        self.display_func = display_func or str
        self.current_selection = 0
        self.scroll_offset = 0

    def display(self):
        """Display the list and return selected item or None"""
        if not self.items:
            self.show_message("No items available")
            return None

        max_visible = self.height - 10  # Leave room for header/footer

        while True:
            self.clear()
            self.draw_header(self.title)
            self.draw_list_items(max_visible)
            self.draw_footer("↑/↓: Navigate | ENTER: Select | ESC: Cancel")
            self.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                if self.current_selection > 0:
                    self.current_selection -= 1
                    if self.current_selection < self.scroll_offset:
                        self.scroll_offset = self.current_selection
            elif key == curses.KEY_DOWN:
                if self.current_selection < len(self.items) - 1:
                    self.current_selection += 1
                    if self.current_selection >= self.scroll_offset + max_visible:
                        self.scroll_offset = self.current_selection - max_visible + 1
            elif key == ord('\n') or key == curses.KEY_ENTER:
                return self.items[self.current_selection]
            elif key == 27:  # ESC
                return None

    def draw_list_items(self, max_visible):
        """Draw list items with scrolling"""
        start_y = 4

        visible_items = self.items[self.scroll_offset:self.scroll_offset + max_visible]

        for idx, item in enumerate(visible_items):
            actual_idx = self.scroll_offset + idx
            y_pos = start_y + idx

            display_text = self.display_func(item)
            # Truncate if too long
            if len(display_text) > self.width - 10:
                display_text = display_text[:self.width-13] + "..."

            if actual_idx == self.current_selection:
                self.stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
                self.stdscr.addstr(y_pos, 5, f"> {display_text}")
                self.stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            else:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y_pos, 5, f"  {display_text}")
                self.stdscr.attroff(curses.color_pair(1))

        # Show scroll indicators
        if self.scroll_offset > 0:
            self.stdscr.attron(curses.color_pair(2))
            self.stdscr.addstr(start_y - 1, self.width // 2, "^^^ MORE ^^^")
            self.stdscr.attroff(curses.color_pair(2))

        if self.scroll_offset + max_visible < len(self.items):
            self.stdscr.attron(curses.color_pair(2))
            self.stdscr.addstr(start_y + max_visible, self.width // 2, "vvv MORE vvv")
            self.stdscr.attroff(curses.color_pair(2))
