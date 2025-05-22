from typing import List, Optional, Dict
from pydantic import BaseModel
from model.person import Person


class NodeN(BaseModel):
    person: Person
    parent: Optional["NodeN"] = None


class TreeN(BaseModel):
    nodes: Dict[str, NodeN] = {}
    root_id: Optional[str] = None

    def create_person(self, person: Person, parent_id: Optional[str] = None) -> bool:
        """Create new person in the tree"""
        if person.id in self.nodes:
            return False  # Person already exists

        new_node = NodeN(person=person)

        # If no root exists, this becomes the root
        if self.root_id is None:
            self.root_id = person.id
            new_node.parent = None
        elif parent_id is None:
            # If no parent specified but root exists, make root the parent
            if self.root_id in self.nodes:
                new_node.parent = self.nodes[self.root_id]
        else:
            # Set specified parent
            if parent_id not in self.nodes:
                return False  # Parent doesn't exist
            new_node.parent = self.nodes[parent_id]

        self.nodes[person.id] = new_node
        return True

    def get_persons(self) -> List[Person]:
        """Get all persons in the tree"""
        return [node.person for node in self.nodes.values()]

    def get_person_by_id(self, person_id: str) -> Optional[Person]:
        """Get person by ID"""
        node = self.nodes.get(person_id)
        return node.person if node else None

    def get_parent(self, person_id: str) -> Optional[Person]:
        """Get parent of a person"""
        node = self.nodes.get(person_id)
        if node and node.parent:
            return node.parent.person
        return None

    def get_children(self, person_id: str) -> List[Person]:
        """Get all children of a person"""
        children = []
        for node in self.nodes.values():
            if node.parent and node.parent.person.id == person_id:
                children.append(node.person)
        return children

    def update_person(self, id: str, person: Person) -> bool:
        """Update person information (excluding ID and parent)"""
        if id not in self.nodes:
            return False

        # Keep the same parent and ID
        node = self.nodes[id]
        updated_person = Person(
            id=id,  # Keep original ID
            name=person.name,
            lastname=person.lastname,
            age=person.age,
            gender=person.gender,
            typedoc=person.typedoc,
            location=person.location
        )
        node.person = updated_person
        return True

    def delete_person(self, id: str) -> bool:
        """Delete person from the tree with proper orphan handling"""
        if id not in self.nodes:
            return False

        node_to_delete = self.nodes[id]
        children = self.get_children(id)

        # If deleting root
        if self.root_id == id:
            if not children:
                # No children, just remove root
                del self.nodes[id]
                self.root_id = None
                return True
            else:
                # Find oldest child to become new root
                oldest_child = max(children, key=lambda p: p.age)
                self.root_id = oldest_child.id
                self.nodes[oldest_child.id].parent = None

                # Reassign other children to new root
                for child in children:
                    if child.id != oldest_child.id:
                        self.nodes[child.id].parent = self.nodes[oldest_child.id]
        else:
            # Not root - reassign children to deleted node's parent
            deleted_parent = node_to_delete.parent
            for child in children:
                self.nodes[child.id].parent = deleted_parent

        # Remove the node
        del self.nodes[id]
        return True

    def get_persons_with_adult_child(self) -> List[Person]:
        """Get persons who have at least one adult child (18+)"""
        result = []
        for person_id in self.nodes:
            children = self.get_children(person_id)
            if any(child.age >= 18 for child in children):
                result.append(self.nodes[person_id].person)
        return result

    def filter_persons(self, location_code: Optional[str] = None,
                       typedoc_code: Optional[str] = None,
                       gender: Optional[str] = None) -> List[Person]:
        """Filter persons by criteria"""
        result = []
        for node in self.nodes.values():
            matches = True

            if location_code is not None and str(node.person.location.code) != location_code:
                matches = False
            if typedoc_code is not None and str(node.person.typedoc.code) != typedoc_code:
                matches = False
            if gender is not None and node.person.gender != gender:
                matches = False

            if matches:
                result.append(node.person)

        return result

    def get_persons_by_location(self, location_code: str) -> List[Person]:
        """Get persons by location code"""
        result = []
        for node in self.nodes.values():
            if str(node.person.location.code) == location_code:
                result.append(node.person)
        return result