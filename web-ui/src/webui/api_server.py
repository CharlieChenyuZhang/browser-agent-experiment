from __future__ import annotations

import asyncio
import json
import uuid
from typing import Dict

import gradio as gr
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from src.webui.webui_manager import WebuiManager
from src.webui.components.browser_use_agent_tab import (
    run_agent_task,
    handle_pause_resume,
    handle_stop,
)


class AgentApi:
  def __init__(self, ui_manager: WebuiManager):
    self.ui = ui_manager
    self.app = FastAPI()
    # Allow calls from chrome extensions and local dev
    self.app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=False,
      allow_methods=["*"],
      allow_headers=["*"],
      expose_headers=["*"],
    )
    self._streams: Dict[str, asyncio.Queue[str]] = {}

    @self.app.post("/api/agent/start")
    async def start(payload: Dict[str, str]):
      task = (payload or {}).get("task", "").strip()
      if not task:
        raise HTTPException(400, "task is required")

      if "browser_use_agent.user_input" not in self.ui.id_to_component:
        raise HTTPException(500, "WebUI components not initialized")

      components: Dict[gr.components.Component, object] = {}
      user_input_comp = self.ui.get_component_by_id("browser_use_agent.user_input")
      components[user_input_comp] = task

      run_id = str(uuid.uuid4())
      q: asyncio.Queue[str] = asyncio.Queue()
      self._streams[run_id] = q

      async def pump():
        try:
          last_len = 0
          async for _ in run_agent_task(self.ui, components):
            # Stream only when there are new chat messages available
            history = getattr(self.ui, "bu_chat_history", []) or []
            if isinstance(history, list) and len(history) > last_len:
              # Send the newest message as a JSON payload
              msg = history[-1]
              await q.put(json.dumps({
                "type": "chat",
                "message": msg
              }))
              last_len = len(history)
        except Exception as e:
          await q.put(f"error: {e}")
        finally:
          await q.put("[DONE]")

      asyncio.create_task(pump())
      return {"runId": run_id}

    @self.app.post("/api/agent/pause")
    async def pause(_: Dict[str, str]):
      await handle_pause_resume(self.ui)
      return {"ok": True}

    @self.app.post("/api/agent/resume")
    async def resume(_: Dict[str, str]):
      await handle_pause_resume(self.ui)
      return {"ok": True}

    @self.app.post("/api/agent/stop")
    async def stop(_: Dict[str, str]):
      await handle_stop(self.ui)
      return {"ok": True}

    @self.app.get("/api/agent/stream")
    async def stream(runId: str):
      q = self._streams.get(runId)
      if q is None:
        q = asyncio.Queue()
        self._streams[runId] = q

      async def event_generator():
        while True:
          msg = await q.get()
          if msg == "[DONE]":
            yield {"event": "status", "data": json.dumps({"state": "done"})}
            break
          # If it's a JSON payload already, forward as-is; otherwise wrap as log
          try:
            data_obj = json.loads(msg)
            yield {"data": json.dumps(data_obj)}
          except Exception:
            yield {"data": json.dumps({"type": "log", "message": str(msg)})}

      return EventSourceResponse(event_generator())

    @self.app.get("/api/debug/components")
    async def debug_components():
      try:
        keys = sorted(list(self.ui.id_to_component.keys()))
      except Exception as e:
        raise HTTPException(500, f"Error reading components: {e}")
      return {"count": len(keys), "keys": keys}


def create_api_app(ui_manager: WebuiManager) -> FastAPI:
  return AgentApi(ui_manager).app


