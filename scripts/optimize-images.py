from collections import deque
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"


def border_connected_mask(image: Image.Image, min_luma: int, max_chroma: int) -> Image.Image:
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def candidate(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        luma = (77 * red + 150 * green + 29 * blue) >> 8
        return luma >= min_luma and max(red, green, blue) - min(red, green, blue) <= max_chroma

    def add(x: int, y: int) -> None:
        offset = y * width + x
        if not visited[offset] and candidate(x, y):
            visited[offset] = 1
            queue.append((x, y))

    for x in range(width):
        add(x, 0)
        add(x, height - 1)
    for y in range(height):
        add(0, y)
        add(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x:
            add(x - 1, y)
        if x + 1 < width:
            add(x + 1, y)
        if y:
            add(x, y - 1)
        if y + 1 < height:
            add(x, y + 1)

    alpha = Image.new("L", (width, height), 255)
    alpha_pixels = alpha.load()
    for offset, is_background in enumerate(visited):
        if is_background:
            alpha_pixels[offset % width, offset // width] = 0

    return alpha.filter(ImageFilter.GaussianBlur(0.65))


def transparent_mockup(source: Path, output_stem: str, min_luma: int, max_chroma: int, widths: tuple[int, int], method: int = 6) -> None:
    source_image = Image.open(source).convert("RGBA")
    alpha = border_connected_mask(source_image, min_luma, max_chroma)
    source_image.putalpha(alpha)

    bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
    if not bbox:
        raise RuntimeError(f"No foreground found in {source}")
    left, top, right, bottom = bbox
    padding = 12
    crop = (
        max(0, left - padding),
        max(0, top - padding),
        min(source_image.width, right + padding),
        min(source_image.height, bottom + padding),
    )
    source_image = source_image.crop(crop)

    for width in widths:
        height = round(source_image.height * width / source_image.width)
        resized = source_image.resize((width, height), Image.Resampling.LANCZOS)
        output = IMAGES / f"{output_stem}-{width}.webp"
        resized.save(output, "WEBP", quality=82, method=method, exact=True)


def transparent_device_mockup(source: Path, output_stem: str, widths: tuple[int, int]) -> None:
    source_image = Image.open(source).convert("RGBA")
    image = cv2.cvtColor(np.array(source_image.convert("RGB")), cv2.COLOR_RGB2BGR)
    height, width = image.shape[:2]
    mask = np.full((height, width), cv2.GC_BGD, dtype=np.uint8)
    rectangle = (
        round(width * 0.018),
        round(height * 0.18),
        round(width * 0.965),
        round(height * 0.73),
    )
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(image, mask, rectangle, background_model, foreground_model, 7, cv2.GC_INIT_WITH_RECT)
    foreground = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        255,
        0,
    ).astype("uint8")
    foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    alpha = Image.fromarray(foreground, mode="L").filter(ImageFilter.GaussianBlur(0.65))
    source_image.putalpha(alpha)

    bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
    if not bbox:
        raise RuntimeError(f"No foreground found in {source}")
    left, top, right, bottom = bbox
    padding = 12
    source_image = source_image.crop((
        max(0, left - padding),
        max(0, top - padding),
        min(source_image.width, right + padding),
        min(source_image.height, bottom + padding),
    ))

    for target_width in widths:
        target_height = round(source_image.height * target_width / source_image.width)
        resized = source_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        resized.save(IMAGES / f"{output_stem}-{target_width}.webp", "WEBP", quality=82, method=6, exact=True)


def transparent_book_mockup(source: Path, output_stem: str, widths: tuple[int, int]) -> None:
    source_image = Image.open(source).convert("RGBA")
    image = cv2.cvtColor(np.array(source_image.convert("RGB")), cv2.COLOR_RGB2BGR)
    height, width = image.shape[:2]
    mask = np.full((height, width), cv2.GC_BGD, dtype=np.uint8)
    rectangle = (
        round(width * 0.035),
        round(height * 0.018),
        round(width * 0.93),
        round(height * 0.955),
    )
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(image, mask, rectangle, background_model, foreground_model, 8, cv2.GC_INIT_WITH_RECT)
    foreground = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        255,
        0,
    ).astype("uint8")
    foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    alpha = Image.fromarray(foreground, mode="L").filter(ImageFilter.GaussianBlur(0.7))
    source_image.putalpha(alpha)

    bbox = alpha.point(lambda value: 255 if value > 8 else 0).getbbox()
    if not bbox:
        raise RuntimeError(f"No foreground found in {source}")
    left, top, right, bottom = bbox
    padding = 10
    source_image = source_image.crop((
        max(0, left - padding),
        max(0, top - padding),
        min(source_image.width, right + padding),
        min(source_image.height, bottom + padding),
    ))

    for target_width in widths:
        target_height = round(source_image.height * target_width / source_image.width)
        resized = source_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        resized.save(IMAGES / f"{output_stem}-{target_width}.webp", "WEBP", quality=84, method=6, exact=True)


def optimize_pages() -> None:
    pages = IMAGES / "strony"
    for source in sorted(pages.glob("page-*.png")):
        image = Image.open(source).convert("RGB")
        image.save(source.with_suffix(".webp"), "WEBP", quality=82, method=6)


def optimize_social_preview() -> None:
    source = Image.open(IMAGES / "mockup-cyfrowy-pl.png").convert("RGB")
    target_ratio = 1200 / 630
    source_ratio = source.width / source.height
    if source_ratio > target_ratio:
        new_width = round(source.height * target_ratio)
        left = (source.width - new_width) // 2
        source = source.crop((left, 0, left + new_width, source.height))
    else:
        new_height = round(source.width / target_ratio)
        top = (source.height - new_height) // 2
        source = source.crop((0, top, source.width, top + new_height))
    source = source.resize((1200, 630), Image.Resampling.LANCZOS)
    source.save(ROOT / "public" / "og.jpg", "JPEG", quality=82, optimize=True, progressive=True)


transparent_device_mockup(
    IMAGES / "mockup-cyfrowy-pl.png",
    "mockup-cyfrowy-transparente",
    widths=(720, 1200),
)
transparent_mockup(
    IMAGES / "mockup-conteudo-pl.png",
    "mockup-conteudo-transparente",
    min_luma=242,
    max_chroma=22,
    widths=(700, 1100),
)
transparent_book_mockup(
    IMAGES / "mockup-livro-capa-pl-source.png",
    "mockup-livro-capa-pl-transparente",
    widths=(560, 900),
)
transparent_mockup(
    IMAGES / "hero-psychofarmakologia-pl-source.png",
    "hero-psychofarmakologia-pl-transparente",
    min_luma=235,
    max_chroma=18,
    widths=(720, 1200),
    method=4,
)
transparent_mockup(
    IMAGES / "hero-psychofarmakologia-mobile-pl-source.png",
    "hero-psychofarmakologia-mobile-pl-transparente",
    min_luma=235,
    max_chroma=18,
    widths=(700,),
    method=4,
)
optimize_pages()
optimize_social_preview()
