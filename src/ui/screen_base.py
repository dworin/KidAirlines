import curses


class ScreenBase:
    """Base class for all screens in the application"""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.setup_colors()

    def setup_colors(self):
        """Setup color pairs for the retro terminal look"""
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Main text
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlighted
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Headers
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)   # Selected
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)     # Error/Warning

    def clear(self):
        """Clear the screen"""
        self.stdscr.clear()

    def refresh(self):
        """Refresh the screen"""
        self.stdscr.refresh()

    def draw_header(self, title):
        """Draw application header"""
        self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
        header = "═" * self.width
        self.stdscr.addstr(0, 0, header[:self.width-1])

        title_text = f"  KIDAIRLINES - {title}  "
        title_x = (self.width - len(title_text)) // 2
        self.stdscr.addstr(1, title_x, title_text)

        self.stdscr.addstr(2, 0, header[:self.width-1])
        self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

    def draw_footer(self, instructions):
        """Draw footer with instructions"""
        self.stdscr.attron(curses.color_pair(2))
        footer_y = self.height - 2
        self.stdscr.addstr(footer_y, 2, instructions[:self.width-4])
        self.stdscr.attroff(curses.color_pair(2))

    def draw_box(self, y, x, height, width, title=None):
        """Draw a box with optional title"""
        # Draw corners and edges
        for i in range(height):
            if i == 0 or i == height - 1:
                self.stdscr.addstr(y + i, x, "+" + "-" * (width - 2) + "+")
            else:
                self.stdscr.addstr(y + i, x, "|" + " " * (width - 2) + "|")

        if title:
            title_str = f" {title} "
            title_x = x + (width - len(title_str)) // 2
            self.stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
            self.stdscr.addstr(y, title_x, title_str)
            self.stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)

    def show_message(self, message, error=False):
        """Show a message box and wait for keypress"""
        msg_height = 7
        msg_width = min(len(message) + 6, self.width - 10)
        msg_y = (self.height - msg_height) // 2
        msg_x = (self.width - msg_width) // 2

        self.draw_box(msg_y, msg_x, msg_height, msg_width, "MESSAGE")

        color = curses.color_pair(5) if error else curses.color_pair(1)
        self.stdscr.attron(color)

        # Word wrap message
        words = message.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) < msg_width - 4:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        for i, line in enumerate(lines[:3]):  # Max 3 lines
            text_x = msg_x + (msg_width - len(line)) // 2
            self.stdscr.addstr(msg_y + 2 + i, text_x, line)

        self.stdscr.attroff(color)

        self.stdscr.attron(curses.color_pair(2))
        prompt = "Press any key to continue..."
        prompt_x = msg_x + (msg_width - len(prompt)) // 2
        self.stdscr.addstr(msg_y + msg_height - 2, prompt_x, prompt)
        self.stdscr.attroff(curses.color_pair(2))

        self.refresh()
        self.stdscr.getch()

    def get_input(self, prompt, y, x, max_length=30):
        """Get text input from user. Returns None if ESC is pressed."""
        curses.curs_set(1)
        curses.noecho()  # We'll handle echo manually

        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.attroff(curses.color_pair(1))

        input_x = x + len(prompt) + 1

        # Draw input field
        self.stdscr.addstr(y, input_x, "_" * max_length)
        self.stdscr.move(y, input_x)
        self.refresh()

        input_str = ""
        cursor_pos = 0

        while True:
            key = self.stdscr.getch()

            # ESC key - cancel input
            if key == 27:
                curses.curs_set(0)
                return None

            # Enter key - submit input
            elif key in (curses.KEY_ENTER, 10, 13):
                break

            # Backspace - delete character
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if cursor_pos > 0:
                    input_str = input_str[:-1]
                    cursor_pos -= 1
                    # Redraw input field
                    self.stdscr.addstr(y, input_x, "_" * max_length)
                    self.stdscr.addstr(y, input_x, input_str)
                    self.stdscr.move(y, input_x + cursor_pos)
                    self.refresh()

            # Regular character
            elif 32 <= key <= 126 and cursor_pos < max_length:
                input_str += chr(key)
                cursor_pos += 1
                # Echo the character
                self.stdscr.addstr(y, input_x + cursor_pos - 1, chr(key))
                self.stdscr.move(y, input_x + cursor_pos)
                self.refresh()

        curses.curs_set(0)
        return input_str.strip()

    def display(self):
        """Override this method in subclasses"""
        raise NotImplementedError("Subclasses must implement display()")
