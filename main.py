from typing import Literal

from fastapi import FastAPI, Response
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field

app = FastAPI(title="napitki-playwright")


class RenderRequest(BaseModel):
    html: str
    format: Literal["png", "pdf"] = "png"
    width: int = Field(1200, ge=100, le=4000)
    height: int = Field(800, ge=100, le=4000)
    full_page: bool = True


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/render")
async def render(req: RenderRequest):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            page = await browser.new_page(viewport={"width": req.width, "height": req.height})
            await page.set_content(req.html, wait_until="networkidle")
            if req.format == "pdf":
                return Response(await page.pdf(print_background=True), media_type="application/pdf")
            return Response(await page.screenshot(full_page=req.full_page), media_type="image/png")
        finally:
            await browser.close()
