from pathlib import Path
import re


# Pasta onde estão os arquivos SEGYLOG
folder = Path(r"H:\VISTA_SEGY_LOGS")


def get_shot_range(file_path: Path):
    with file_path.open("r", encoding="latin-1") as file:
        for line in file:

            if "SHOT_POINT_NO" in line:

                match = re.search(r"=\s*(-?\d+)\s*-\s*(-?\d+)", line)

                if match:
                    first_sp = int(match.group(1))
                    last_sp = int(match.group(2))

                    return first_sp, last_sp

    return None, None


def get_line_name(file_path: Path):
    match = re.search(
        r"(\d+)-SW0*(\d+)",
        file_path.name,
        re.IGNORECASE
    )

    if match:
        project = match.group(1)
        swath = int(match.group(2))

        return f"{project}-sw{swath:03d}"

    return file_path.stem


print(f"{'Line':<15} {'First SP No':>12} {'Last SP No':>12}")
print("-" * 41)

for file_path in sorted(folder.glob("*.SEGYLOG")):

    first_sp, last_sp = get_shot_range(file_path)
    line_name = get_line_name(file_path)

    if first_sp is not None:
        print(
            f"{line_name:<15} "
            f"{first_sp:>12} "
            f"{last_sp:>12}"
        )
    else:
        print(f"{line_name:<15} SHOT_POINT_NO não encontrado")