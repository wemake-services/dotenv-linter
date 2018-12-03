# -*- coding: utf-8 -*-


def normalize_text(text: str) -> str:
    """Removes trailing and leading spaces and quotes."""
    return text.strip().strip('\'"')
