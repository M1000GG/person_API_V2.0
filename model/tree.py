from typing import List, Optional
from pydantic import BaseModel
from model.person import Person


class NodeN(BaseModel):
    person: Person
    children: List["NodeN"] = []
    parent: Optional["NodeN"] = None  # New parent reference

    def add_child(self, child: "NodeN") -> None:
        """Add child and set parent reference"""
        self.children.append(child)
        child.parent = self  # Set reverse relationship

    def remove_child_by_id(self, id: str) -> bool:
        """Remove child by ID and clean parent reference"""
        for i, child in enumerate(self.children):
            if child.person.id == id:
                removed_child = self.children.pop(i)
                removed_child.parent = None  # Clean reference
                return True

        # Search in grandchildren
        for child in self.children:
            if child.remove_child_by_id(id):
                return True

        return False


class TreeN(BaseModel):
    root: NodeN

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        """Create new person in the tree"""
        new_node = NodeN(person=person)

        if parent_id is None:
            self.root.add_child(new_node)
            return True

        # Find parent and add child
        parent_node = self._find_node(self.root, parent_id)
        if parent_node:
            parent_node.add_child(new_node)
            return True
        return False

    def _find_node(self, node: NodeN, id: str) -> Optional[NodeN]:
        """Find node by ID in the tree"""
        if node.person.id == id:
            return node

        for child in node.children:
            found = self._find_node(child, id)
            if found:
                return found
        return None

    def get_persons(self) -> List[Person]:
        """Get all persons in the tree"""
        result = []
        self._traverse(self.root, result)
        return result

    def _traverse(self, node: NodeN, result: List[Person]) -> None:
        """Traverse tree and collect persons"""
        result.append(node.person)
        for child in node.children:
            self._traverse(child, result)

    def update_person(self, id: str, person: Person) -> bool:
        """Update person information"""
        node = self._find_node(self.root, id)
        if node:
            node.person = person
            return True
        return False

    def delete_person(self, id: str) -> bool:
        """Delete person from the tree"""
        if self.root.person.id == id:
            if not self.root.children:
                self.root = None
                return True
            return False

        node = self._find_node(self.root, id)
        if node and node.parent:
            return node.parent.remove_child_by_id(id)
        return False

    def get_persons_with_adult_child(self) -> List[Person]:
        result = []
        self._find_persons_with_adult_child(self.root, result)
        return result

    def _find_persons_with_adult_child(self, node: NodeN, result: List[Person]) -> None:
        has_adult_child = any(child.person.age >= 18 for child in node.children)

        for child in node.children:
            self._find_persons_with_adult_child(child, result)

        if has_adult_child:
            result.append(node.person)

    def filter_persons(self, location_code: Optional[str] = None,
                       typedoc_code: Optional[str] = None,
                       gender: Optional[str] = None) -> List[Person]:
        result = []
        self._filter_recursive(self.root, location_code, typedoc_code, gender, result)
        return result

    def _filter_recursive(self, node: NodeN,
                          location_code: Optional[str],
                          typedoc_code: Optional[str],
                          gender: Optional[str],
                          result: List[Person]) -> None:
        matches = True

        if location_code is not None and str(node.person.location.code) != location_code:
            matches = False
        if typedoc_code is not None and str(node.person.typedoc.code) != typedoc_code:
            matches = False
        if gender is not None and node.person.gender != gender:
            matches = False

        if matches:
            result.append(node.person)

        for child in node.children:
            self._filter_recursive(child, location_code, typedoc_code, gender, result)

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        result = []
        self._get_by_location_recursively(self.root, location_code, result)
        return result

    def _get_by_location_recursively(self, node: NodeN, location_code: str, result: List[Person]) -> None:
        if str(node.person.location.code) == location_code:
            result.append(node.person)

        for child in node.children:
            self._get_by_location_recursively(child, location_code, result)