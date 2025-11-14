import pandas as pd

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "invoice no": "invoiceno",
        "invoice number": "invoiceno",
        "inv no": "invoiceno",
        "inv_num": "invoiceno",
        "invoice": "invoiceno",
        "invoice #": "invoiceno",
        "reference": "referenceno",
        "reference no": "referenceno",
        "reference number": "referenceno",
        "business name": "businessname",
        "business": "businessname",
        "client name": "clientname",
        "customer name": "clientname",
        "client": "clientname",
        "customer": "clientname",
        "amount": "amount",
        "payment amount": "amount",
        "paid": "amount",
        "total amount": "amount",
    }

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[\s\-\#_]+", " ", regex=True)
        .str.replace(r"[^a-z0-9 ]", "", regex=True)
    )
    df.rename(columns=lambda c: rename_map.get(c, c.replace(" ", "")), inplace=True)
    return df