"""Tiny async wrapper around the Gofile.io upload API."""

import os

import aiohttp

from config import GOFILE_TOKEN

# Global upload endpoint — Gofile routes the file to the best store server.
UPLOAD_URL = "https://upload.gofile.io/uploadfile"


async def upload_to_gofile(file_path: str) -> dict:
    """Upload a local file to Gofile and return the API `data` payload.

    The returned dict contains (among others):
      - downloadPage : shareable download link (works on the free tier)
      - fileId       : Gofile content id
      - fileName     : stored file name

    Note: truly *direct* (hotlink) URLs require a Gofile premium token.
    On the free tier the `downloadPage` link is what you share.
    """
    form = aiohttp.FormData()
    form.add_field(
        "file",
        open(file_path, "rb"),
        filename=os.path.basename(file_path),
    )
    if GOFILE_TOKEN:
        form.add_field("token", GOFILE_TOKEN)

    timeout = aiohttp.ClientTimeout(total=60 * 60)  # allow big files
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(UPLOAD_URL, data=form) as resp:
            result = await resp.json()

    if result.get("status") != "ok":
        raise RuntimeError(f"Gofile upload failed: {result}")

    return result["data"]
