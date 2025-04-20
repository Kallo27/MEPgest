import pandas as pd
from tqdm import tqdm
from mepgest.models import Delegate, schools, committees, assign_delegate_codes
import re

def load_delegates(filepath, verbose=False):
    delegates = []  # List to collect Delegate objects

    try:
        df = pd.read_excel(filepath)

        # Check required columns
        required_columns = {"Name", "Surname", "Gender", "Committee", "School"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Excel file is missing required columns: {required_columns - set(df.columns)}")

        print(f"📥 Loading {len(df)} participants from {filepath}...\n")
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Loading delegates"):
            name = str(row["Name"]).strip().title()
            surname = str(row["Surname"]).strip().title()
            gender = str(row["Gender"]).strip()
            committee = str(row["Committee"]).strip()
            
            # Extract school name from quotes, if present
            raw_school = str(row["School"]).strip()
            match = re.search(r'"(.*?)"', raw_school)
            school = match.group(1).strip() if match else raw_school.title()

            # Create the delegate and append it to the list
            delegate = Delegate(
                name=name,
                surname=surname,
                gender=gender,
                committee_name=committee,
                school_name=school
            )
            delegates.append(delegate)  # Add the delegate to the list
        
        # Call the function to assign codes (if needed)
        assign_delegate_codes()

        print("\n✅ Load complete.")

        if verbose:
            unique_committees = sorted(committees.items())
            unique_schools = sorted(schools.items())

            print("\n🧭 Unique Committees:")
            for name, committee in unique_committees:
                print(f" - {name}: {len(committee.delegates)} delegates")

            print("\n🏫 Unique Schools:")
            for name, school in unique_schools:
                print(f" - {name}: {len(school.delegates)} delegates")

        return delegates  # Return the list of delegates

    except Exception as e:
        print(f"❌ Error loading participants: {e}")
        return []  # Return an empty list if there was an error
