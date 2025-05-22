from model.typedoc import Typedoc
from typing import List, Dict, Optional

class TypedocService:
    def __init__(self):
        # Initialize with Colombian identification document types
        self.typedocs: Dict[int, Typedoc] = {
            1: Typedoc(code=1, description="Cédula de Ciudadanía"),
            2: Typedoc(code=2, description="Tarjeta de Identidad"),
            3: Typedoc(code=3, description="Registro Civil"),
            4: Typedoc(code=4, description="Cédula de Extranjería"),
            5: Typedoc(code=5, description="Pasaporte"),
            6: Typedoc(code=6, description="Carné Diplomático"),
            7: Typedoc(code=7, description="Permiso Especial de Permanencia")
        }

    def get_all_typedocs(self) -> List[Typedoc]:
        # Get all available document types
        return list(self.typedocs.values())

    def get_typedoc_by_code(self, code: int) -> Optional[Typedoc]:
        # Get a specific document type by its code
        return self.typedocs.get(code)

    def create_typedoc(self, typedoc: Typedoc) -> bool:
        # Create a new document type if it doesn't exist
        if typedoc.code in self.typedocs:
            return False
        self.typedocs[typedoc.code] = typedoc
        return True

    def update_typedoc(self, code: int, typedoc: Typedoc) -> bool:
        # Update an existing document type
        if code not in self.typedocs:
            return False
        self.typedocs[code] = typedoc
        return True

    def delete_typedoc(self, code: int) -> bool:
        # Delete a document type by its code
        if code not in self.typedocs:
            return False
        del self.typedocs[code]
        return True