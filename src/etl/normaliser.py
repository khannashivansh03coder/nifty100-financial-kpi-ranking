def normalise_financials(df):
    """
    Cleans and normalises financial columns
    """

    df = df.copy()

    # Standardise column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Drop completely empty rows
    df = df.dropna(how="all")

    # Convert numeric columns safely
    for col in df.columns:
        if col not in ["company", "symbol", "sector"]:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.replace("%", "")
            )
            df[col] = df[col].apply(
                lambda x: float(x) if x.replace(".", "", 1).isdigit() else None
            )

    return df