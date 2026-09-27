import tkinter as tk
from tkinter import ttk


def calculate(salary, needs):
    """
    W-N-I allocation rule.

    N = min(S, N0)
    R = max(0, S - N)
    W = R * N / (S + N)
    I = R * S / (S + N)

    Returns:
        wants, needs, investment
    """

    if salary < 0 or needs < 0:
        raise ValueError("Salary and needs cannot be negative.")

    # Actual needs cannot exceed available salary.
    n = min(salary, needs)

    # Money left after necessities.
    remaining = max(0.0, salary - n)

    # Avoid division by zero when S = N = 0.
    denominator = salary + n

    if denominator == 0:
        wants = 0.0
        investment = 0.0
    else:
        wants = remaining * n / denominator
        investment = remaining * salary / denominator

    return wants, n, investment


def marginal_values(salary, needs):
    """
    Derivatives for the S > N region:

        dW/dS = 2N² / (S+N)²
        dI/dS = 1 - 2N² / (S+N)²

    When S <= N, an extra rupee simply increases N.
    """

    if salary <= needs:
        return 0.0, 0.0, 1.0

    denominator = (salary + needs) ** 2

    dw = 2 * needs ** 2 / denominator
    di = 1 - dw

    return dw, 0.0, di


class WNIApp:
    def __init__(self, root):
        self.root = root

        root.title("W-N-I Rule")
        root.geometry("560x650")
        root.minsize(500, 580)

        self.salary = tk.DoubleVar(value=8000)
        self.needs = tk.DoubleVar(value=7000)

        self.setup_style()
        self.build_ui()

        self.update()


    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("TkDefaultFont", 22, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("TkDefaultFont", 10)
        )

        style.configure(
            "Output.TLabel",
            font=("TkDefaultFont", 13)
        )

        style.configure(
            "Big.TLabel",
            font=("TkDefaultFont", 18, "bold")
        )


    def build_ui(self):
        main = ttk.Frame(self.root, padding=24)
        main.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        ttk.Label(
            main,
            text="W-N-I Rule",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Adaptive Wants • Needs • Investments",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(0, 20))


        # ---------------------------------------------------------
        # Inputs
        # ---------------------------------------------------------

        input_frame = ttk.LabelFrame(
            main,
            text="Parameters",
            padding=15
        )

        input_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            input_frame,
            text="Salary (S)"
        ).grid(row=0, column=0, sticky="w")

        salary_entry = ttk.Entry(
            input_frame,
            textvariable=self.salary,
            width=18
        )

        salary_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(15, 0)
        )

        ttk.Label(
            input_frame,
            text="Needs baseline (N₀)"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(12, 0)
        )

        needs_entry = ttk.Entry(
            input_frame,
            textvariable=self.needs,
            width=18
        )

        needs_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(15, 0),
            pady=(12, 0)
        )

        input_frame.columnconfigure(1, weight=1)


        salary_entry.bind("<Return>", lambda _: self.update())
        needs_entry.bind("<Return>", lambda _: self.update())


        # ---------------------------------------------------------
        # Salary slider
        # ---------------------------------------------------------

        ttk.Label(
            main,
            text="Salary slider"
        ).pack(anchor="w")

        self.slider = ttk.Scale(
            main,
            from_=0,
            to=100000,
            variable=self.salary,
            command=lambda _: self.update()
        )

        self.slider.pack(fill="x", pady=(5, 15))


        # ---------------------------------------------------------
        # Outputs
        # ---------------------------------------------------------

        output_frame = ttk.LabelFrame(
            main,
            text="Allocation",
            padding=15
        )

        output_frame.pack(fill="x", pady=(0, 15))


        self.needs_label = self.output_row(
            output_frame,
            "Needs (N)",
            0
        )

        self.wants_label = self.output_row(
            output_frame,
            "Wants (W)",
            1
        )

        self.invest_label = self.output_row(
            output_frame,
            "Investment (I)",
            2
        )

        self.total_label = self.output_row(
            output_frame,
            "Total",
            3
        )


        # ---------------------------------------------------------
        # Ratio
        # ---------------------------------------------------------

        self.ratio_label = ttk.Label(
            output_frame,
            text="I / W = —",
            style="Output.TLabel"
        )

        self.ratio_label.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(12, 0)
        )


        # ---------------------------------------------------------
        # Marginal allocation
        # ---------------------------------------------------------

        marginal_frame = ttk.LabelFrame(
            main,
            text="Marginal allocation",
            padding=15
        )

        marginal_frame.pack(fill="x", pady=(0, 15))


        self.dw_label = ttk.Label(
            marginal_frame,
            text="dW/dS = —",
            style="Output.TLabel"
        )

        self.dw_label.pack(anchor="w")


        self.di_label = ttk.Label(
            marginal_frame,
            text="dI/dS = —",
            style="Output.TLabel"
        )

        self.di_label.pack(anchor="w", pady=(6, 0))


        # ---------------------------------------------------------
        # Formula
        # ---------------------------------------------------------

        formula_frame = ttk.LabelFrame(
            main,
            text="Rule",
            padding=15
        )

        formula_frame.pack(fill="x")


        formula = (
            "N = min(S, N₀)\n"
            "R = max(0, S − N)\n"
            "W = R × N / (S + N)\n"
            "I = R × S / (S + N)"
        )

        ttk.Label(
            formula_frame,
            text=formula,
            font=("TkFixedFont", 10)
        ).pack(anchor="w")


    def output_row(self, parent, name, row):
        ttk.Label(
            parent,
            text=name,
            style="Output.TLabel"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=4
        )

        label = ttk.Label(
            parent,
            text="₹0.00",
            style="Big.TLabel"
        )

        label.grid(
            row=row,
            column=1,
            sticky="e",
            pady=4
        )

        parent.columnconfigure(1, weight=1)

        return label


    def update(self):
        try:
            salary = max(0.0, float(self.salary.get()))
            needs = max(0.0, float(self.needs.get()))

            wants, actual_needs, investment = calculate(
                salary,
                needs
            )

            dw, _, di = marginal_values(
                salary,
                actual_needs
            )

        except (ValueError, tk.TclError):
            return


        # ---------------------------------------------------------
        # Outputs
        # ---------------------------------------------------------

        self.needs_label.config(
            text=f"₹{actual_needs:,.2f}"
        )

        self.wants_label.config(
            text=f"₹{wants:,.2f}"
        )

        self.invest_label.config(
            text=f"₹{investment:,.2f}"
        )

        self.total_label.config(
            text=f"₹{wants + actual_needs + investment:,.2f}"
        )


        # ---------------------------------------------------------
        # Investment / Wants ratio
        # ---------------------------------------------------------

        if wants > 0:
            ratio = investment / wants
            self.ratio_label.config(
                text=f"I / W = {ratio:.3f}"
            )
        else:
            self.ratio_label.config(
                text="I / W = —"
            )


        # ---------------------------------------------------------
        # Marginal allocation
        # ---------------------------------------------------------

        self.dw_label.config(
            text=f"dW/dS = {dw:.4f}"
        )

        self.di_label.config(
            text=f"dI/dS = {di:.4f}"
        )


if __name__ == "__main__":
    root = tk.Tk()

    app = WNIApp(root)

    root.mainloop()
