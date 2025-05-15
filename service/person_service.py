from model.person import Person
from model.tree import TreeN, NodeN
from typing import List, Optional


class PersonService:
    def __init__(self):
        self.tree = None

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        """Create new person with optional parent"""
        if self.tree is None:
            root_node = NodeN(person=person)
            self.tree = TreeN(root=root_node)
            return True
        return self.tree.create_person(person, parent_id)

    def get_parent(self, person_id: str) -> Optional[Person]:
        """Get direct parent of a person"""
        if self.tree is None:
            return None

        node = self.tree._find_node(self.tree.root, person_id)
        return node.parent.person if (node and node.parent) else None

    def get_all_persons(self) -> List[Person]:
        """Get all persons in the system"""
        if self.tree is None:
            return []
        return self.tree.get_persons()

    def get_person_by_id(self, id: str) -> Optional[Person]:
        """Get person by ID"""
        if self.tree is None:
            return None
        node = self.tree._find_node(self.tree.root, id)
        return node.person if node else None

    def update_person(self, id: str, person: Person) -> bool:
        """Update person data"""
        if self.tree is None:
            return False
        return self.tree.update_person(id, person)

    def delete_person(self, id: str) -> bool:
        """Delete person by ID"""
        if self.tree is None:
            return False
        return self.tree.delete_person(id)

    def get_persons_with_adult_child(self) -> List[Person]:
        if self.tree is None:
            return []
        return self.tree.get_persons_with_adult_child()

    def filter_persons(self,
                      location_code: Optional[str] = None,
                      typedoc_code: Optional[str] = None,
                      gender: Optional[str] = None) -> List[Person]:
        if self.tree is None:
            return []
        return self.tree.filter_persons(location_code, typedoc_code, gender)

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        if self.tree is None:
            return []
        return self.tree.get_persons_by_location(location_code)