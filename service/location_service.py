import pandas as pd

class LocationService:
    def __init__(self, csv_path: str):
        self.locations_df = pd.read_csv(csv_path, encoding='latin1', sep=';')

    def get_states(self):
        # Get all states/departments
        states = self.locations_df[["Código Departamento", "Nombre Departamento"]].drop_duplicates()
        return [
            {"code": int(row["Código Departamento"]), "description": row["Nombre Departamento"]}
            for _, row in states.iterrows()
        ]

    def get_locations_by_state_code(self, state_code: int):
        #Get locations/cities by state/department code
        filtered = self.locations_df[self.locations_df["Código Departamento"] == state_code]
        return [
            {"code": int(row["Código Municipio"]), "description": row["Nombre Municipio"]}
            for _, row in filtered.iterrows()
        ]

    def get_location_by_code(self, location_code: int):
        # Get one location/city by code
        match = self.locations_df[self.locations_df["Código Municipio"] == location_code]
        if not match.empty:
            row = match.iloc[0]
            return {"code": int(row["Código Municipio"]), "description": row["Nombre Municipio"]}
        return None

    def get_capitals(self):
        # Get all states code
        capitals = self.locations_df[self.locations_df["Código Municipio"] % 100 == 1]
        return [
            {"code": int(row["Código Municipio"]), "description": row["Nombre Municipio"]}
            for _, row in capitals.iterrows()
        ]
