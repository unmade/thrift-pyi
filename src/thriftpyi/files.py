from pathlib import Path


def save(data: str, to: str) -> None:
    Path.mkdir(Path(to).parent, exist_ok=True)
    with open(to, "w+") as f:
        f.write(data)
