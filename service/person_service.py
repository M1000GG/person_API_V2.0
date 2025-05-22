from model.person import Person, PersonCreate, PersonUpdate
from model.tree import TreeN
from typing import List, Optional

class PersonService:
    def __init__(self):
        self.tree = TreeN()

    def create_person_from_codes(self, person_create: PersonCreate, parent_id: Optional[str] = None) -> bool:
        """Create person using location and typedoc services to auto-complete data"""
        # This method will be called from the controller with auto-completed data
        pass

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        """Create new person with optional parent"""
        return self.tree.create_person(person, parent_id)

    def get_parent(self, person_id: str) -> Optional[Person]:
        """Get direct parent of a person"""
        return self.tree.get_parent(person_id)

    def get_children(self, person_id: str) -> List[Person]:
        """Get all children of a person"""
        return self.tree.get_children(person_id)

    def get_all_persons(self) -> List[Person]:
        """Get all persons in the system"""
        return self.tree.get_persons()

    def get_person_by_id(self, id: str) -> Optional[Person]:
        """Get person by ID"""
        return self.tree.get_person_by_id(id)

    def update_person(self, id: str, person: Person) -> bool:
        """Update person data (excluding ID and parent)"""
        return self.tree.update_person(id, person)

    def delete_person(self, id: str) -> bool:
        """Delete person by ID"""
        return self.tree.delete_person(id)

    def get_persons_with_adult_child(self) -> List[Person]:
        """Get persons with adult children"""
        return self.tree.get_persons_with_adult_child()

    def filter_persons(self,
                      location_code: Optional[str] = None,
                      typedoc_code: Optional[str] = None,
                      gender: Optional[str] = None) -> List[Person]:
        """Filter persons by criteria"""
        return self.tree.filter_persons(location_code, typedoc_code, gender)

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        """Get persons by location"""
        return self.tree.get_persons_by_location(location_code)