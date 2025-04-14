import pandas as pd
from tqdm import tqdm
from mepgest.models import Delegate, schools, committees, assign_delegate_codes

def load_delegates(filepath, verbose=False):
    try:
        df = pd.read_excel(filepath)

        # Check required columns
        required_columns = {"Name", "Surname", "Gender", "Committee", "School"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Excel file is missing required columns: {required_columns - set(df.columns)}")

        print(f"📥 Loading {len(df)} participants from {filepath}...\n")
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Loading delegates"):
            Delegate(
                name=row["Name"],
                surname=row["Surname"],
                gender=row["Gender"],
                committee_name=row["Committee"],
                school_name=row["School"]
            )
        
        assign_delegate_codes()

        print("\n✅ Load complete.")

        if verbose:
            unique_committees = sorted(committees.keys())
            unique_schools = sorted(schools.keys())

            print("\n🧭 Unique Committees:")
            for c in unique_committees:
                print(f" - {c}: {len(c.delegates)} delegates")

            print("\n🏫 Unique Schools:")
            for s in unique_schools:
                print(f" - {s}: {c.delegates} delegates")

    except Exception as e:
        print(f"❌ Error loading participants: {e}")
