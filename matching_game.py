import math
import random
import tkinter as tk
from tkinter import ttk


class MatchingGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matching Game: Die Rolls vs Positions")
        self.root.geometry("980x520")
        self.root.resizable(False, False)

        self.total_trials = 0
        self.total_successes = 0

        self.main = ttk.Frame(root, padding=16)
        self.main.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main, width=920, height=280, bg="#f6f2ea", highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.status_var = tk.StringVar(value="Press Roll 6 to play one trial.")
        status = ttk.Label(self.main, textvariable=self.status_var, font=("Georgia", 11))
        status.grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 0))

        controls = ttk.Frame(self.main)
        controls.grid(row=2, column=0, sticky="w", pady=(14, 0))

        self.roll_btn = ttk.Button(controls, text="Roll 6 (Animate)", command=self.start_roll)
        self.roll_btn.grid(row=0, column=0, padx=(0, 8))

        self.sim_entry_var = tk.StringVar(value="500")
        ttk.Label(controls, text="Batch trials:").grid(row=0, column=1, padx=(8, 4))
        self.sim_entry = ttk.Entry(controls, textvariable=self.sim_entry_var, width=8)
        self.sim_entry.grid(row=0, column=2, padx=(0, 8))

        self.sim_btn = ttk.Button(controls, text="Simulate", command=self.run_batch)
        self.sim_btn.grid(row=0, column=3)
        """
        self.auto_btn = ttk.Button(controls, text="Start Auto", command=self.toggle_auto)
        self.auto_btn.grid(row=0, column=4, padx=(12, 8))

        ttk.Label(controls, text="Speed (sec/game):").grid(row=0, column=5, padx=(0, 4))
        self.speed_var = tk.DoubleVar(value=3.0)
        self.speed_slider = ttk.Scale(
            controls,
            from_=0.5,
            to=5.0,
            variable=self.speed_var,
            orient="horizontal",
            length=160,
        )
        self.speed_slider.grid(row=0, column=6, padx=(0, 8))

        self.clear_btn = ttk.Button(controls, text="Clear", command=self.clear_history)
        self.clear_btn.grid(row=0, column=7) """

        stats = ttk.Frame(self.main, padding=(12, 0, 0, 0))
        stats.grid(row=2, column=1, columnspan=2, sticky="e")

        self.trials_var = tk.StringVar(value="Trials: 0")
        self.success_var = tk.StringVar(value="Successes: 0")
        self.rate_var = tk.StringVar(value="Success rate: 0.000")
        self.theory_var = tk.StringVar(
            value=f"Theoretical: {1 - (5 / 6) ** 6:.3f}"
        )

        ttk.Label(stats, textvariable=self.trials_var, font=("Georgia", 11)).grid(row=0, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.success_var, font=("Georgia", 11)).grid(row=1, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.rate_var, font=("Georgia", 11)).grid(row=2, column=0, sticky="e")
        ttk.Label(stats, textvariable=self.theory_var, font=("Georgia", 11)).grid(row=3, column=0, sticky="e")

        self.die_boxes = []
        self.auto_running = False
        self.auto_after_id = None
        self.recent_results = []
        self.hist_window = 50
        self._draw_static_layout()

    def _draw_static_layout(self):
        self.canvas.delete("all")
        base_x = 60
        gap = 135
        y = 70
        for i in range(6):
            x = base_x + i * gap
            label = f"position {i + 1}"
            self.canvas.create_text(x + 45, y - 30, text=label, font=("Georgia", 12), fill="#3b2e1f")
            self._draw_die_face(x, y, 0, tag=f"die{i}", outline="#b8a18a")
            self.die_boxes.append((x, y))

        self.canvas.create_text(
            460,
            245,
            text="Match if roll k equals position k (for k = 1..6).",
            font=("Georgia", 12, "italic"),
            fill="#6b5b4b",
        )
        self.bulb_center = (875, 120)
        # self.hist_rect = (660, 190, 910, 270)
        self._set_bulb_state("neutral")
        # self._draw_histogram()

    def _set_bulb_state(self, state):
        colors = {
            "neutral": "#c9c3bb",
            "success": "#39a24a",
            "failure": "#c44a3d",
        }
        fill = colors.get(state, colors["neutral"])
        self._draw_bulb(self.bulb_center[0], self.bulb_center[1], fill)

    def _draw_bulb(self, x, y, fill):
        self.canvas.delete("bulb")
        self.canvas.create_oval(
            x - 24,
            y - 24,
            x + 24,
            y + 24,
            outline="#6f5f4f",
            width=3,
            fill=fill,
            tags="bulb",
        )
        self.canvas.create_text(x, y + 58, text="Result", font=("Georgia", 11, "italic"), fill="#6b5b4b", tags="bulb")

    """ def _draw_histogram(self):
        self.canvas.delete("hist")
        x0, y0, x1, y1 = self.hist_rect
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#c8b9a8", width=2, tags="hist")
        self.canvas.create_text(
            (x0 + x1) / 2,
            y0 - 12,
            text=f"Rolling histogram (last {self.hist_window})",
            font=("Georgia", 10, "italic"),
            fill="#6b5b4b",
            tags="hist",
        )

        counts = [0] * 7
        for value in self.recent_results[-self.hist_window:]:
            counts[value] += 1
        max_count = max(counts) if counts else 1

        bar_gap = 6
        bar_width = (x1 - x0 - bar_gap * 8) / 7
        for i, count in enumerate(counts):
            bar_x0 = x0 + bar_gap + i * (bar_width + bar_gap)
            bar_x1 = bar_x0 + bar_width
            height = 0 if max_count == 0 else (count / max_count) * (y1 - y0 - 22)
            bar_y0 = y1 - height - 14
            bar_y1 = y1 - 14
            self.canvas.create_rectangle(
                bar_x0,
                bar_y0,
                bar_x1,
                bar_y1,
                fill="#9b7b5c",
                outline="",
                tags="hist",
            )
            self.canvas.create_text(
                (bar_x0 + bar_x1) / 2,
                y1 - 6,
                text=str(i),
                font=("Georgia", 9),
                fill="#6b5b4b",
                tags="hist",
            )
 """
    def _draw_die_face(self, x, y, value, tag, outline):
        self.canvas.delete(tag)
        size = 90
        self.canvas.create_rectangle(x, y, x + size, y + size, width=3, outline=outline, fill="#fffaf4", tags=tag)
        if value == 0:
            self.canvas.create_text(x + size / 2, y + size / 2, text="?", font=("Georgia", 22), fill="#8a7967", tags=tag)
            return

        cx = x + size / 2
        cy = y + size / 2
        offset = 22
        spots = {
            1: [(0, 0)],
            2: [(-1, -1), (1, 1)],
            3: [(-1, -1), (0, 0), (1, 1)],
            4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)],
            6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)],
        }
        for dx, dy in spots[value]:
            self.canvas.create_oval(
                cx + dx * offset - 7,
                cy + dy * offset - 7,
                cx + dx * offset + 7,
                cy + dy * offset + 7,
                fill="#3b2e1f",
                outline="",
                tags=tag,
            )

    def start_roll(self):
        self.roll_btn.config(state="disabled")
        self.sim_btn.config(state="disabled")
        # self.auto_btn.config(state="disabled")
        # self.clear_btn.config(state="disabled")
        self.status_var.set("Rolling...")
        self._set_bulb_state("neutral")
        self._roll_index = 0
        self._current_matches = 0
        self._roll_sequence()

    def _roll_sequence(self):
        if self._roll_index >= 6:
            self._finish_trial(animated=True)
            return

        idx = self._roll_index
        value = random.randint(1, 6)
        match = value == idx + 1
        outline = "#2f8f2f" if match else "#b8a18a"
        if match:
            self._current_matches += 1
        x, y = self.die_boxes[idx]
        self._draw_die_face(x, y, value, tag=f"die{idx}", outline=outline)
        self._roll_index += 1
        self.root.after(350, self._roll_sequence)

    def _finish_trial(self, animated=False):
        success = self._current_matches > 0
        self._record_result(self._current_matches)
        self.total_trials += 1
        if success:
            self.total_successes += 1
            self.status_var.set("Success! At least one match occurred.")
            self._set_bulb_state("success")
        else:
            self.status_var.set("Failure. No matches occurred.")
            self._set_bulb_state("failure")
        self._update_stats()
        self.roll_btn.config(state="normal")
        self.sim_btn.config(state="normal")
        if not animated:
            self._refresh_dice()

    def _refresh_dice(self):
        for i, (x, y) in enumerate(self.die_boxes):
            self._draw_die_face(x, y, 0, tag=f"die{i}", outline="#b8a18a")

    def _update_stats(self):
        rate = self.total_successes / self.total_trials if self.total_trials else 0.0
        self.trials_var.set(f"Trials: {self.total_trials}")
        self.success_var.set(f"Successes: {self.total_successes}")
        self.rate_var.set(f"Success rate: {rate:.3f}")

    def run_batch(self):
        try:
            n = int(self.sim_entry_var.get())
        except ValueError:
            self.status_var.set("Enter an integer for batch trials.")
            return
        if n <= 0:
            self.status_var.set("Batch trials must be positive.")
            return

        successes = 0
        for _ in range(n):
            matches = 0
            for k in range(1, 7):
                if random.randint(1, 6) == k:
                    matches += 1
            self._record_result(matches)
            if matches > 0:
                successes += 1

        self.total_trials += n
        self.total_successes += successes
        self._update_stats()
        self.status_var.set(f"Simulated {n} trials. Successes: {successes}.")
        if successes > 0:
            self._set_bulb_state("success")
        else:
            self._set_bulb_state("failure")
        self._refresh_dice()


    def _run_single_trial(self):
        matches = 0
        for k in range(1, 7):
            if random.randint(1, 6) == k:
                matches += 1
        self._current_matches = matches
        self._finish_trial(animated=False)


    def _record_result(self, matches):
        self.recent_results.append(matches)
        if len(self.recent_results) > self.hist_window:
            self.recent_results = self.recent_results[-self.hist_window:]
        # self._draw_histogram()


def main():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TButton", font=("Georgia", 11))
    style.configure("TLabel", font=("Georgia", 11), background="#f6f2ea")
    style.configure("TFrame", background="#f6f2ea")
    app = MatchingGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
