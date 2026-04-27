#!/usr/bin/python3
"""Función Main"""
import asyncio

import pygame  # noqa: F401  (necesario para que pygbag detecte la dependencia)
import esper  # noqa: F401  (necesario para que pygbag detecte la dependencia)

from src.engine.game_engine import GameEngine

# Crear el engine FUERA de la coroutine para evitar
# "The video driver did not add any displays" en pygbag/wasm.
engine = GameEngine()


async def main() -> None:
    await engine.run()


asyncio.run(main())



