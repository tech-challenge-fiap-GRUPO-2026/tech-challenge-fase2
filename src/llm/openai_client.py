from __future__ import annotations

import os
from collections.abc import Callable, Sequence
from typing import Any

from src.llm.prompts import ChatMessage


class OpenAIChatClient:
    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        client_factory: Callable[..., Any] | None = None,
    ) -> None:
        self.model = model
        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_api_key:
            raise ValueError("OPENAI_API_KEY nao configurada.")

        if client_factory is None:
            try:
                from openai import OpenAI
            except ModuleNotFoundError as exc:
                raise RuntimeError("Pacote openai nao instalado. Instale com `.venv/bin/pip install openai`.") from exc

            client_factory = OpenAI

        self.client = client_factory(api_key=resolved_api_key)

    def complete(self, messages: Sequence[ChatMessage]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": message.role, "content": message.content} for message in messages],
        )
        content = response.choices[0].message.content
        return "" if content is None else str(content).strip()


def load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        return

    load_dotenv()
