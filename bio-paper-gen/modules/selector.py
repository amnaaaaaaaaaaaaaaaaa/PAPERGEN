import pandas as pd

def select_questions(df: pd.DataFrame, chapters: list, distribution: dict, seed: int = 42) -> pd.DataFrame:
    """Selects questions from dataframe according to marks distribution."""
    selected = []

    df_chapters = df[df["chapter"].isin(chapters)].copy()

    for marks, count in distribution.items():
        subset = df_chapters[df_chapters["marks"] == marks]
        if subset.empty:
            continue
        chosen = subset.sample(
            n=min(count, len(subset)),
            random_state=seed
        )
        selected.append(chosen)

    if selected:
        return pd.concat(selected).reset_index(drop=True)
    else:
        return pd.DataFrame(columns=df.columns)

def derive_distribution(total_questions: int, total_marks: int) -> dict:
    """Derive a marks distribution if user only sets total questions/marks."""
    if total_questions == 0 and total_marks == 0:
        return {1:0, 2:0, 3:0, 5:0}

    # Simple fallback: assume equal distribution
    base = total_questions // 4 if total_questions else total_marks // (1+2+3+5)
    return {1: base, 2: base, 3: base, 5: base}
