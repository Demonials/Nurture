import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import traceback

from nurture_lang.runtime import Runtime, RuntimeErrorNurture
from nurture_lang.registry import registry, root_suggestions, member_suggestions

TITLE = "Nurture IDE 0.1.0"

class Autocomplete:
    def __init__(self, editor):
        self.editor = editor
        self.popup = None
        self.listbox = None
        self.items = []
        self.active = False

    def current_prefix(self):
        line = self.editor.get("insert linestart", "insert")
        if not line:
            return ""
        # Prefix is the current identifier/member expression.
        token = line.split()[-1] if line.split() else ""
        return token

    def hide(self):
        if self.popup:
            self.popup.destroy()
        self.popup = None
        self.listbox = None
        self.items = []
        self.active = False

    def show(self):
        prefix = self.current_prefix()
        if not prefix:
            self.hide()
            return

        items = member_suggestions(prefix) if "." in prefix else root_suggestions(prefix)
        if not items:
            self.hide()
            return

        self.items = items[:20]

        if self.popup:
            self.popup.destroy()

        self.popup = tk.Toplevel(self.editor)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        frame = tk.Frame(self.popup, bg="#181818", bd=1, relief="solid")
        frame.pack()

        self.listbox = tk.Listbox(
            frame, width=42, height=min(12, len(self.items)),
            bg="#181818", fg="#eeeeee",
            selectbackground="#3a3a3a", selectforeground="white",
            borderwidth=0, highlightthickness=0,
            font=("Consolas", 10)
        )
        self.listbox.pack()
        self.listbox.bind("<Double-Button-1>", self.accept)
        self.listbox.bind("<Return>", self.accept)

        for item in self.items:
            self.listbox.insert("end", item)

        self.listbox.selection_set(0)
        self.listbox.activate(0)

        box = self.editor.bbox("insert")
        if box:
            x, y, w, h = box
            px = self.editor.winfo_rootx() + x
            py = self.editor.winfo_rooty() + y + h + 2
            self.popup.geometry(f"+{px}+{py}")

        self.active = True

    def accept(self, event=None):
        if not self.active or not self.listbox:
            return
        selection = self.listbox.curselection()
        if not selection:
            return
        value = self.items[selection[0]]
        prefix = self.current_prefix()
        self.editor.delete(f"insert-{len(prefix)}c", "insert")
        self.editor.insert("insert", value)
        self.hide()
        return "break"

    def key(self, event):
        if not self.active:
            return False
        if event.keysym in ("Up", "Down"):
            index = self.listbox.curselection()[0] if self.listbox.curselection() else 0
            index += -1 if event.keysym == "Up" else 1
            index %= len(self.items)
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            return True
        if event.keysym in ("Return", "Tab"):
            self.accept()
            return True
        if event.keysym == "Escape":
            self.hide()
            return True
        return False

class IDE:
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE)
        self.root.geometry("1180x720")
        self.root.minsize(900, 560)

        self.current_file = None
        self.output_box = None
        self.editor = None
        self.runtime = Runtime(self.output, self.input_dialog)

        self.build()
        self.autocomplete = Autocomplete(self.editor)

        self.editor.bind("<KeyRelease>", self.on_key)
        self.editor.bind("<KeyPress>", self.on_keypress)
        self.editor.bind("<Control-space>", self.complete)
        self.editor.bind("<F5>", self.run)

        self.editor.insert("1.0",
            'name = "Udit"\\n'
            'write("Hello " + name)\\n\\n'
            'loop i in 1..5:\\n'
            '    write(i)\\n\\n'
            'function add(a, b):\\n'
            '    return a + b\\n\\n'
            'write(add(10, 20))\\n'
        )

        self.output("Nurture 0.1.0")
        self.output("Autocomplete: type w or web.")
        self.output("F5 = execute | Ctrl+Space = force autocomplete")

    def build(self):
        bar = tk.Frame(self.root, bg="#101010")
        bar.pack(fill="x")

        for label, fn in [
            ("▶ EXECUTE", self.run),
            ("RUN LINE", self.run_line),
            ("OPEN .USD", self.open),
            ("SAVE", self.save),
            ("CLEAR", self.clear),
            ("HELP", self.help),
        ]:
            tk.Button(bar, text=label, command=fn, bg="#222", fg="white",
                      activebackground="#333", activeforeground="white",
                      relief="flat", padx=12, pady=7).pack(side="left", padx=3, pady=4)

        tk.Label(bar, text="Nurture | F5 | Ctrl+Space",
                 bg="#101010", fg="#999").pack(side="right", padx=12)

        pane = tk.PanedWindow(self.root, orient="vertical", bg="#101010")
        pane.pack(fill="both", expand=True)

        ef = tk.Frame(pane, bg="#0d0d0d")
        of = tk.Frame(pane, bg="#0d0d0d")
        pane.add(ef, minsize=320)
        pane.add(of, minsize=150)

        self.editor = tk.Text(ef, wrap="none", bg="#0d0d0d", fg="#eee",
                              insertbackground="white", selectbackground="#333",
                              font=("Consolas", 12), undo=True)
        self.editor.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(ef, command=self.editor.yview)
        sb.pack(side="right", fill="y")
        self.editor.configure(yscrollcommand=sb.set)

        self.output_box = tk.Text(of, wrap="word", bg="#101010", fg="#ddd",
                                  font=("Consolas", 10), state="disabled")
        self.output_box.pack(fill="both", expand=True)

    def input_dialog(self, prompt=""):
        from tkinter import simpledialog
        value = simpledialog.askstring("Nurture Input", str(prompt), parent=self.root)
        return "" if value is None else value

    def output(self, value=""):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", str(value) + "\n")
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def on_keypress(self, event):
        if self.autocomplete.key(event):
            return "break"

    def on_key(self, event):
        if event.keysym not in ("Up", "Down", "Return", "Tab", "Escape"):
            self.autocomplete.show()

    def complete(self, event=None):
        self.autocomplete.show()
        return "break"

    def run(self, event=None):
        self.autocomplete.hide()
        self.clear()
        code = self.editor.get("1.0", "end-1c")
        try:
            self.runtime.execute(code)
            self.output(">>> done")
        except Exception as exc:
            self.output("ERROR: " + str(exc))
            if not isinstance(exc, RuntimeErrorNurture):
                self.output(traceback.format_exc())

    def run_line(self):
        line = self.editor.get("insert linestart", "insert lineend").strip()
        if not line:
            return
        try:
            self.runtime.execute(line)
        except Exception as exc:
            self.output("ERROR: " + str(exc))

    def clear(self):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

    def open(self):
        path = filedialog.askopenfilename(filetypes=[("Nurture source", "*.usd"), ("All files", "*.*")])
        if path:
            self.current_file = Path(path)
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", self.current_file.read_text(encoding="utf-8"))
            self.root.title(self.current_file.name + " - " + TITLE)

    def save(self):
        if not self.current_file:
            path = filedialog.asksaveasfilename(defaultextension=".usd",
                                                filetypes=[("Nurture source", "*.usd")])
            if not path:
                return
            self.current_file = Path(path)
        self.current_file.write_text(self.editor.get("1.0", "end-1c"), encoding="utf-8")
        self.output("Saved: " + str(self.current_file))

    def help(self):
        win = tk.Toplevel(self.root)
        win.title("Nurture Documentation")
        win.geometry("820x580")
        box = tk.Text(win, wrap="word", font=("Consolas", 10))
        box.pack(fill="both", expand=True)
        box.insert("1.0", registry.documentation())
        box.configure(state="disabled")

def main():
    root = tk.Tk()
    IDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
