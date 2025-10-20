import os
import sys
import json
import pandas as pd


def _load_lookup_data(lookup_dir):
    all_lookup_df = []
    for fname in os.listdir(lookup_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(lookup_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.json_normalize(data.get("data", []))

        holo = pd.to_numeric(df.get("tcgplayer.prices.holofoil.market"), errors="coerce")
        normal = pd.to_numeric(df.get("tcgplayer.prices.normal.market"), errors="coerce")
        df["card_market_value"] = holo.fillna(normal).fillna(0.0)

        df = df.rename(
            columns={
                "id": "card_id",
                "name": "card_name",
                "number": "card_number",
                "set.id": "set_id",
                "set.name": "set_name",
            }
        )

        required_cols = [
            "card_id",
            "card_name",
            "card_number",
            "set_id",
            "set_name",
            "card_market_value",
        ]
        df = df[[c for c in required_cols if c in df.columns]].copy()
        all_lookup_df.append(df)

    if not all_lookup_df:
        return pd.DataFrame(
            columns=[
                "card_id",
                "card_name",
                "card_number",
                "set_id",
                "set_name",
                "card_market_value",
            ]
        )

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values("card_market_value", ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first").reset_index(drop=True)
    return lookup_df


def _load_inventory_data(inventory_dir):
    inventory_data = []
    for fname in os.listdir(inventory_dir):
        if not fname.endswith(".csv"):
            continue
        path = os.path.join(inventory_dir, fname)
        inventory_data.append(pd.read_csv(path))

    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)
    inventory_df["card_id"] = (
        inventory_df["set_id"].astype(str) + "-" + inventory_df["card_number"].astype(str)
    )
    return inventory_df


def update_portfolio(inventory_dir, lookup_dir, output_file):
    import sys
    import pandas as pd

    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    final_cols = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "card_id",
        "card_name",
        "set_name",
        "card_market_value",
    ]

    if inventory_df.empty:
        print("Error: inventory is empty; writing empty portfolio.", file=sys.stderr)
        pd.DataFrame(columns=final_cols).to_csv(output_file, index=False)
        return

    
    lookup_cols = [c for c in ["card_id", "card_name", "set_name", "card_market_value"] if c in lookup_df.columns]
    lookup_needed = lookup_df[lookup_cols].copy()

    merged = pd.merge(inventory_df, lookup_needed, on="card_id", how="left")

    
    if "card_name" not in merged.columns:
        merged["card_name"] = pd.NA
    if "set_name" not in merged.columns:
        merged["set_name"] = pd.NA
    if "card_market_value" not in merged.columns:
        merged["card_market_value"] = pd.NA

    merged["card_market_value"] = merged["card_market_value"].fillna(0.0)
    merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")
    merged["card_name"] = merged["card_name"].fillna("UNKNOWN")

    merged["index"] = (
        merged["binder_name"].astype(str)
        + merged["page_number"].astype(str)
        + merged["slot_number"].astype(str)
    )

    merged[final_cols].to_csv(output_file, index=False)
    print(f"Success: wrote portfolio to {output_file}")



def main():
    update_portfolio(
        inventory_dir="./card_inventory/",
        lookup_dir="./card_set_lookup/",
        output_file="card_portfolio.csv",
    )


def test():
    update_portfolio(
        inventory_dir="./card_inventory_test/",
        lookup_dir="./card_set_lookup_test/",
        output_file="test_card_portfolio.csv",
    )


if __name__ == "__main__":
    print("Starting in Test Mode", file=sys.stderr)
    test()

#hopefully i did it right 

