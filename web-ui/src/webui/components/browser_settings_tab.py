import os
from distutils.util import strtobool
import gradio as gr
import logging
from gradio.components import Component
import urllib.request
import urllib.error
import json as pyjson

from src.webui.webui_manager import WebuiManager
from src.utils import config

logger = logging.getLogger(__name__)

async def close_browser(webui_manager: WebuiManager):
    """
    Close browser
    """
    if webui_manager.bu_current_task and not webui_manager.bu_current_task.done():
        webui_manager.bu_current_task.cancel()
        webui_manager.bu_current_task = None

    if webui_manager.bu_browser_context:
        logger.info("⚠️ Closing browser context when changing browser config.")
        await webui_manager.bu_browser_context.close()
        webui_manager.bu_browser_context = None

    if webui_manager.bu_browser:
        logger.info("⚠️ Closing browser when changing browser config.")
        await webui_manager.bu_browser.close()
        webui_manager.bu_browser = None

def create_browser_settings_tab(webui_manager: WebuiManager):
    """
    Creates a browser settings tab.
    """
    input_components = set(webui_manager.get_components())
    tab_components = {}

    with gr.Group():
        with gr.Row():
            browser_binary_path = gr.Textbox(
                label="Browser Binary Path",
                lines=1,
                interactive=True,
                placeholder="e.g. '/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome'"
            )
            browser_user_data_dir = gr.Textbox(
                label="Browser User Data Dir",
                lines=1,
                interactive=True,
                placeholder="Leave it empty if you use your default user data",
            )
    with gr.Group():
        with gr.Row():
            use_own_browser = gr.Checkbox(
                label="Use Own Browser",
                value=bool(strtobool(os.getenv("USE_OWN_BROWSER", "false"))),
                info="Use your existing browser instance",
                interactive=True
            )
            keep_browser_open = gr.Checkbox(
                label="Keep Browser Open",
                value=bool(strtobool(os.getenv("KEEP_BROWSER_OPEN", "true"))),
                info="Keep Browser Open between Tasks",
                interactive=True
            )
            headless = gr.Checkbox(
                label="Headless Mode",
                value=False,
                info="Run browser without GUI",
                interactive=True
            )
            disable_security = gr.Checkbox(
                label="Disable Security",
                value=False,
                info="Disable browser security",
                interactive=True
            )

    with gr.Group():
        with gr.Row():
            window_w = gr.Number(
                label="Window Width",
                value=1280,
                info="Browser window width",
                interactive=True
            )
            window_h = gr.Number(
                label="Window Height",
                value=1100,
                info="Browser window height",
                interactive=True
            )
    with gr.Group():
        with gr.Row():
            cdp_url = gr.Textbox(
                label="CDP URL",
                value=os.getenv("BROWSER_CDP", None),
                info="CDP URL for browser remote debugging",
                interactive=True,
            )
            wss_url = gr.Textbox(
                label="WSS URL",
                info="WSS URL for browser remote debugging",
                interactive=True,
            )
    with gr.Group():
        gr.Markdown("Select an existing Chrome tab to operate in the same window.")
        with gr.Row():
            refresh_tabs_btn = gr.Button("🔄 Refresh Tabs")
            existing_tab = gr.Dropdown(
                label="Existing Tabs (CDP)",
                choices=[],
                value=None,
                interactive=True,
                allow_custom_value=False,
                info="Pick a tab; this sets WSS URL to attach to that tab"
            )
    with gr.Group():
        with gr.Row():
            save_recording_path = gr.Textbox(
                label="Recording Path",
                placeholder="e.g. ./tmp/record_videos",
                info="Path to save browser recordings",
                interactive=True,
            )

            save_trace_path = gr.Textbox(
                label="Trace Path",
                placeholder="e.g. ./tmp/traces",
                info="Path to save Agent traces",
                interactive=True,
            )

        with gr.Row():
            save_agent_history_path = gr.Textbox(
                label="Agent History Save Path",
                value="./tmp/agent_history",
                info="Specify the directory where agent history should be saved.",
                interactive=True,
            )
            save_download_path = gr.Textbox(
                label="Save Directory for browser downloads",
                value="./tmp/downloads",
                info="Specify the directory where downloaded files should be saved.",
                interactive=True,
            )
    tab_components.update(
        dict(
            browser_binary_path=browser_binary_path,
            browser_user_data_dir=browser_user_data_dir,
            use_own_browser=use_own_browser,
            keep_browser_open=keep_browser_open,
            headless=headless,
            disable_security=disable_security,
            save_recording_path=save_recording_path,
            save_trace_path=save_trace_path,
            save_agent_history_path=save_agent_history_path,
            save_download_path=save_download_path,
            cdp_url=cdp_url,
            wss_url=wss_url,
            refresh_tabs_btn=refresh_tabs_btn,
            existing_tab=existing_tab,
            window_h=window_h,
            window_w=window_w,
        )
    )
    webui_manager.add_components("browser_settings", tab_components)

    async def close_wrapper():
        """Wrapper for handle_clear."""
        await close_browser(webui_manager)

    headless.change(close_wrapper)
    keep_browser_open.change(close_wrapper)
    disable_security.change(close_wrapper)
    use_own_browser.change(close_wrapper)

    def _fetch_cdp_targets(cdp: str):
        if not cdp:
            return [], None, gr.update()
        # Normalize URL (Playwright accepts http://host:port)
        cdp_root = cdp.rstrip("/")
        url = f"{cdp_root}/json"
        try:
            with urllib.request.urlopen(url, timeout=3) as resp:
                data = resp.read().decode("utf-8", errors="ignore")
                targets = pyjson.loads(data)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
            logger.warning(f"Failed to fetch CDP targets from {url}: {e}")
            return [], None, gr.update()

        # Filter to pages having webSocketDebuggerUrl
        items = []
        for t in targets or []:
            if t.get("type") != "page":
                continue
            ws = t.get("webSocketDebuggerUrl")
            title = t.get("title") or "(no title)"
            page_url = t.get("url") or ""
            if ws:
                label = f"{title} — {page_url}"[:180]
                items.append((label, ws))

        # Return list of labels and select first
        if not items:
            return [], None, gr.update()
        labels = [label for label, _ in items]
        first_ws = items[0][1]
        return labels, first_ws, gr.update(value=first_ws)

    def on_refresh_tabs(curr_cdp: str):
        labels, ws, ws_update = _fetch_cdp_targets(curr_cdp)
        return gr.update(choices=labels, value=(labels[0] if labels else None)), ws_update

    def on_pick_tab(label: str, curr_cdp: str):
        # Re-fetch to map label->ws (avoid storing global state)
        labels, first_ws, _ = _fetch_cdp_targets(curr_cdp)
        if not labels:
            return gr.update()
        # Try to map back by index
        try:
            idx = labels.index(label)
        except ValueError:
            return gr.update()
        # Fetch all again to get same ordering
        cdp_root = (curr_cdp or "").rstrip("/")
        try:
            with urllib.request.urlopen(f"{cdp_root}/json", timeout=3) as resp:
                targets = pyjson.loads(resp.read().decode("utf-8", errors="ignore"))
        except Exception:
            return gr.update()
        pages = [t for t in targets if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
        if idx < 0 or idx >= len(pages):
            return gr.update()
        return gr.update(value=pages[idx]["webSocketDebuggerUrl"])

    refresh_tabs_btn.click(
        fn=on_refresh_tabs,
        inputs=[cdp_url],
        outputs=[existing_tab, wss_url]
    )
    existing_tab.change(
        fn=on_pick_tab,
        inputs=[existing_tab, cdp_url],
        outputs=[wss_url]
    )
