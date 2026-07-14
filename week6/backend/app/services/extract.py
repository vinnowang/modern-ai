import re


def extract_action_items(text: str) -> list[str]:
    """
    Parses note text to extract action items.
    Supports both legacy format (TODO: prefix / ! suffix) and standard Markdown checkboxes.
    """
    actions = []
    if not text:
        return actions

    # Pattern to match Markdown checkboxes: - [ ] task text
    checkbox_pattern = re.compile(r"^\s*-\s*\[\s*\]\s*(.+)$")

    for line in text.splitlines():
        cleaned_line = line.replace("\xa0", " ").strip()
        if not cleaned_line:
            continue

        # 1. Match standard Markdown checkbox items
        checkbox_match = checkbox_pattern.match(cleaned_line)
        if checkbox_match:
            actions.append(checkbox_match.group(1).strip())
            continue

        # 2. Match legacy rules (strip hyphen formatting first if present)
        legacy_line = cleaned_line.strip("- ")
        if legacy_line.lower().startswith("todo:") or legacy_line.endswith("!"):
            actions.append(legacy_line)

    return actions
