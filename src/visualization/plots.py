from __future__ import annotations

from typing import Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pygame
from matplotlib.backends.backend_agg import FigureCanvasAgg


def draw_fitness_plot(
    screen: pygame.Surface,
    history: Sequence[float],
    rect: pygame.Rect,
    x_label: str = "Generation",
    y_label: str = "Fitness - Distance (pxls)",
) -> None:
    fig, ax = plt.subplots(figsize=(rect.width / 100, rect.height / 100), dpi=100)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.plot(list(range(1, len(history) + 1)), list(history), color="#2f5bea", linewidth=2.5)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.tick_params(axis="both", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.25)
    plt.tight_layout(pad=0.6)

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    size = canvas.get_width_height()
    raw_data = canvas.buffer_rgba()
    surface = pygame.image.frombuffer(raw_data, size, "RGBA")
    screen.blit(surface, rect.topleft)
    plt.close(fig)
