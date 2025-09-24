from dotenv import load_dotenv
load_dotenv()
import argparse
import gradio as gr
from src.webui.interface import theme_map, create_ui
from src.webui.webui_manager import WebuiManager
from src.webui.api_server import create_api_app
from fastapi import FastAPI
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="Gradio WebUI for Browser Agent")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=7788, help="Port to listen on")
    parser.add_argument("--theme", type=str, default="Ocean", choices=theme_map.keys(), help="Theme to use for the UI")
    args = parser.parse_args()

    # Create shared WebuiManager, Gradio UI and FastAPI app
    ui_manager = WebuiManager()
    demo = create_ui(ui_manager=ui_manager, theme_name=args.theme)
    app = create_api_app(ui_manager)
    # Mount Gradio UI onto the same FastAPI app so API routes remain available
    gr.mount_gradio_app(app, demo, path="/")

    uvicorn.run(app, host=args.ip, port=args.port)


if __name__ == '__main__':
    main()
