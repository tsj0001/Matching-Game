import random
import tkinter as tk
from tkinter import ttk


class CoinFlipGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coin Flip Game: Runs and Proportions")
        self.root.geometry("980x700")
        self.root.resizable(False, False)

        self.total_flips = 0
        self.heads_count = 0
        self.tails_count = 0
        self.current_side = None
        self.current_streak = 0
        self.longest_streak = 0

        self.run_target = 10
        self.run_trials = 0
        self.run_total_flips = 0

        self.flip_history = []
        self.head_rate_history = []
        self.run_avg_history = []

        self.main = ttk.Frame(root, padding=16)
        self.main.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main, width=920, height=280, bg="#f6f2ea", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.status_var = tk.StringVar(value="Press Flip to start.")
        status = ttk.Label(self.main, textvariable=self.status_var, font=("Georgia", 11))
        status.grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 0))

        controls = ttk.Frame(self.main)
        controls.grid(row=2, column=0, sticky="w", pady=(14, 0))

        self.flip_btn = ttk.Button(controls, text="Flip (Animate)", command=self.start_flip)
        self.flip_btn.grid(row=0, column=0, padx=(0, 8))

        self.batch_entry_var = tk.StringVar(value="200")
        ttk.Label(controls, text="Batch flips:").grid(row=0, column=1, padx=(8, 4))
        self.batch_entry = ttk.Entry(controls, textvariable=self.batch_entry_var, width=8)
        self.batch_entry.grid(row=0, column=2, padx=(0, 8))

        self.batch_btn = ttk.Button(controls, text="Simulate", command=self.run_batch_flips)
        self.batch_btn.grid(row=0, column=3)

        self.run_entry_var = tk.StringVar(value="50")
        ttk.Label(controls, text="Run trials:").grid(row=0, column=4, padx=(12, 4))
        self.run_entry = ttk.Entry(controls, textvariable=self.run_entry_var, width=8)
        self.run_entry.grid(row=0, column=5, padx=(0, 8))

        self.run_btn = ttk.Button(
            controls,
            text=f"Simulate {self.run_target} in a row",
            command=self.run_run_trials,
        )
        self.run_btn.grid(row=0, column=6)

        self.show_ref_var = tk.BooleanVar(value=True)
        self.ref_line_btn = ttk.Checkbutton(
            controls,
            text="Show 0.5 line",
            variable=self.show_ref_var,
            command=self._draw_graph,
        )
        self.ref_line_btn.grid(row=0, column=7, padx=(12, 0))

        self.clear_btn = ttk.Button(controls, text="Clear", command=self.clear_all)
        self.clear_btn.grid(row=0, column=8, padx=(12, 0))

        stats = ttk.Frame(self.main, padding=(0, 10, 0, 0))
        stats.grid(row=3, column=0, columnspan=3, sticky="w")

        self.flips_var = tk.StringVar(value="Flips: 0")
        self.heads_var = tk.StringVar(value="Heads: 0")
        self.tails_var = tk.StringVar(value="Tails: 0")
        self.streak_var = tk.StringVar(value="Current streak: 0")
        self.longest_var = tk.StringVar(value="Longest streak: 0")
        self.run_trials_var = tk.StringVar(value=f"{self.run_target}-in-row trials: 0")
        self.run_avg_var = tk.StringVar(value="Avg flips to reach: 0.0")

        ttk.Label(stats, textvariable=self.flips_var, font=("Georgia", 12)).grid(row=0, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.heads_var, font=("Georgia", 12)).grid(row=1, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.tails_var, font=("Georgia", 12)).grid(row=2, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.streak_var, font=("Georgia", 12)).grid(row=3, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.longest_var, font=("Georgia", 12)).grid(row=4, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.run_trials_var, font=("Georgia", 12)).grid(row=5, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.run_avg_var, font=("Georgia", 12)).grid(row=6, column=0, sticky="e")

        self.graph_canvas = tk.Canvas(self.main, width=920, height=170, bg="#f6f2ea", highlightthickness=0)
        self.graph_canvas.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(16, 0))
        self.graph_rect = (70, 20, 870, 140)

        self._draw_static_layout()
        self._draw_graph()

    def _draw_static_layout(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            460,
            32,
            text="Flip a fair coin: track heads/tails and streaks.",
            font=("Georgia", 13, "italic"),
            fill="#6b5b4b",
        )
        self.coin_center = (460, 130)
        self._draw_coin(face="?", color="#c9c3bb")

        self.history_anchor = (100, 230)
        self.canvas.create_text(
            self.history_anchor[0],
            self.history_anchor[1] - 26,
            text="Last 20 flips:",
            font=("Georgia", 11),
            fill="#3b2e1f",
            anchor="w",
        )
        self._draw_flip_history()

    def _draw_coin(self, face, color):
        self.canvas.delete("coin")
        x, y = self.coin_center
        self.canvas.create_oval(
            x - 70,
            y - 70,
            x + 70,
            y + 70,
            outline="#6f5f4f",
            width=4,
            fill=color,
            tags="coin",
        )
        self.canvas.create_text(
            x,
            y,
            text=face,
            font=("Georgia", 36, "bold"),
            fill="#3b2e1f",
            tags="coin",
        )

    def _draw_flip_history(self):
        self.canvas.delete("history")
        start_x, y = self.history_anchor
        radius = 12
        gap = 8
        recent = self.flip_history[-20:]
        for i, face in enumerate(recent):
            x = start_x + i * (radius * 2 + gap)
            fill = "#d7c1a1" if face == "H" else "#cdd8df"
            self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                outline="#6f5f4f",
                width=2,
                fill=fill,
                tags="history",
            )
            self.canvas.create_text(
                x,
                y,
                text=face,
                font=("Georgia", 9, "bold"),
                fill="#3b2e1f",
                tags="history",
            )

    def _draw_graph(self):
        self.graph_canvas.delete("graph")
        x0, y0, x1, y1 = self.graph_rect
        axis_color = "#6f5f4f"
        line_color = "#0093e6"
        ref_color = "#3b2e1f"

        self.graph_canvas.create_line(x0, y0, x0, y1, fill=axis_color, width=2, tags="graph")
        self.graph_canvas.create_line(x0, y1, x1, y1, fill=axis_color, width=2, tags="graph")
        self.graph_canvas.create_text(x0 - 22, y0 - 6, text="P(H)", font=("Georgia", 10), fill=axis_color, tags="graph")
        self.graph_canvas.create_text(x1 + 12, y1 + 2, text="n", font=("Georgia", 10, "italic"), fill=axis_color, tags="graph")

        y_min = 0.0
        y_max = 1.0
        for value in (0.0, 0.5, 1.0):
            y = y1 - ((value - y_min) / (y_max - y_min)) * (y1 - y0)
            self.graph_canvas.create_line(x0 - 6, y, x0, y, fill=axis_color, width=1, tags="graph")
            self.graph_canvas.create_text(x0 - 28, y, text=f"{value:.1f}", font=("Georgia", 9), fill=axis_color, tags="graph")

        if self.show_ref_var.get():
            y = y1 - 0.5 * (y1 - y0)
            self.graph_canvas.create_line(x0, y, x1, y, fill=ref_color, width=1, tags="graph")

        n = len(self.head_rate_history)
        if n <= 1:
            tick_max = 1
        else:
            tick_max = n
        for t in range(5):
            value = int(round(t * tick_max / 4))
            x = x0 + (t / 4) * (x1 - x0)
            self.graph_canvas.create_line(x, y1, x, y1 + 6, fill=axis_color, width=1, tags="graph")
            self.graph_canvas.create_text(x, y1 + 16, text=str(value), font=("Georgia", 9), fill=axis_color, tags="graph")

        if not self.head_rate_history:
            return

        points = []
        denom = max(1, n - 1)
        for i, rate in enumerate(self.head_rate_history):
            x = x0 + (i / denom) * (x1 - x0)
            clamped = min(max(rate, y_min), y_max)
            y = y1 - ((clamped - y_min) / (y_max - y_min)) * (y1 - y0)
            points.extend([x, y])

        if n == 1:
            self.graph_canvas.create_oval(
                points[0] - 2,
                points[1] - 2,
                points[0] + 2,
                points[1] + 2,
                fill=line_color,
                outline="",
                tags="graph",
            )
        else:
            self.graph_canvas.create_line(*points, fill=line_color, width=2, tags="graph")

    def _update_stats(self):
        self.flips_var.set(f"Flips: {self.total_flips}")
        self.heads_var.set(f"Heads: {self.heads_count}")
        self.tails_var.set(f"Tails: {self.tails_count}")
        self.streak_var.set(f"Current streak: {self.current_streak}")
        self.longest_var.set(f"Longest streak: {self.longest_streak}")
        self.run_trials_var.set(f"{self.run_target}-in-row trials: {self.run_trials}")
        avg = self.run_total_flips / self.run_trials if self.run_trials else 0.0
        self.run_avg_var.set(f"Avg flips to reach: {avg:.1f}")

    def _record_flip(self, face):
        self.total_flips += 1
        if face == "H":
            self.heads_count += 1
        else:
            self.tails_count += 1

        if self.current_side == face:
            self.current_streak += 1
        else:
            self.current_side = face
            self.current_streak = 1

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.flip_history.append(face)
        if len(self.flip_history) > 200:
            self.flip_history = self.flip_history[-200:]

        rate = self.heads_count / self.total_flips if self.total_flips else 0.0
        self.head_rate_history.append(rate)

    def start_flip(self):
        self.flip_btn.config(state="disabled")
        self.batch_btn.config(state="disabled")
        self.run_btn.config(state="disabled")
        self.status_var.set("Flipping...")
        self._flip_steps = 0
        self._animate_flip()

    def _animate_flip(self):
        if self._flip_steps >= 10:
            face = random.choice(["H", "T"])
            self._apply_flip(face, update_graph=True)
            self.flip_btn.config(state="normal")
            self.batch_btn.config(state="normal")
            self.run_btn.config(state="normal")
            return

        face = random.choice(["H", "T"])
        color = "#d7c1a1" if face == "H" else "#cdd8df"
        self._draw_coin(face, color)
        self._flip_steps += 1
        self.root.after(120, self._animate_flip)

    def _apply_flip(self, face, update_graph=True):
        color = "#d7c1a1" if face == "H" else "#cdd8df"
        self._draw_coin(face, color)
        self._record_flip(face)
        self._draw_flip_history()
        self._update_stats()
        if update_graph:
            self._draw_graph()
        self.status_var.set(f"Last flip: {face}.")

    def run_batch_flips(self):
        try:
            n = int(self.batch_entry_var.get())
        except ValueError:
            self.status_var.set("Enter an integer for batch flips.")
            return
        if n <= 0:
            self.status_var.set("Batch flips must be positive.")
            return

        for _ in range(n):
            face = random.choice(["H", "T"])
            self._record_flip(face)

        last = self.flip_history[-1] if self.flip_history else "?"
        color = "#d7c1a1" if last == "H" else "#cdd8df"
        self._draw_coin(last, color)
        self._draw_flip_history()
        self._update_stats()
        self._draw_graph()
        self.status_var.set(f"Simulated {n} flips.")

    def run_run_trials(self):
        try:
            n = int(self.run_entry_var.get())
        except ValueError:
            self.status_var.set("Enter an integer for run trials.")
            return
        if n <= 0:
            self.status_var.set("Run trials must be positive.")
            return

        for _ in range(n):
            flips = self._simulate_run_to_target()
            self.run_trials += 1
            self.run_total_flips += flips
            avg = self.run_total_flips / self.run_trials
            self.run_avg_history.append(avg)

        self._update_stats()
        self.status_var.set(f"Simulated {n} run trials.")

    def _simulate_run_to_target(self):
        streak = 0
        last = None
        flips = 0
        while streak < self.run_target:
            face = random.choice(["H", "T"])
            flips += 1
            if face == last:
                streak += 1
            else:
                last = face
                streak = 1
        return flips

    def clear_all(self):
        self.total_flips = 0
        self.heads_count = 0
        self.tails_count = 0
        self.current_side = None
        self.current_streak = 0
        self.longest_streak = 0
        self.run_trials = 0
        self.run_total_flips = 0
        self.flip_history = []
        self.head_rate_history = []
        self.run_avg_history = []
        self._draw_coin("?", "#c9c3bb")
        self._draw_flip_history()
        self._update_stats()
        self._draw_graph()
        self.status_var.set("Cleared all simulations.")


def main():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TButton", font=("Georgia", 11))
    style.configure("TLabel", font=("Georgia", 11), background="#f6f2ea")
    style.configure("TFrame", background="#f6f2ea")
    app = CoinFlipGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
