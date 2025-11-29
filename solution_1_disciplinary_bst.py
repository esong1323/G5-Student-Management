from dataclasses import dataclass
from typing import Optional, List


# ---------- Data type for one disciplinary record ----------

@dataclass
class StudentRecord:
    student_id: str
    name: str
    programme: str
    offence_type: str
    offence_date: str      # keep it simple: string "YYYY-MM-DD"
    penalty_level: str     # e.g. Warning / Probation / Suspension
    status: str            # e.g. Open / Closed


# ---------- BST node (internal structure) ----------

class BSTNode:
    """Node of a Binary Search Tree storing a StudentRecord."""
    def __init__(self, record: StudentRecord):
        self.key = record.student_id       # key used for searching
        self.record = record
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


# ---------- Abstract Data Type: DisciplinaryBST ----------

class DisciplinaryBST:
    """
    ADT that encapsulates all BST operations for disciplinary records.
    External code only uses this class; node pointers are hidden inside.
    """
    def __init__(self):
        self.root: Optional[BSTNode] = None

    # --- public methods (interface of the ADT) ---

    def insert(self, record: StudentRecord) -> None:
        """Insert a new record (or overwrite if student_id already exists)."""
        self.root = self._insert(self.root, record)

    def search(self, student_id: str) -> Optional[StudentRecord]:
        """Search by student ID. Return StudentRecord or None."""
        node = self._search(self.root, student_id)
        return node.record if node else None

    def update_penalty(self, student_id: str, new_penalty: str) -> bool:
        node = self._search(self.root, student_id)
        if node:
            node.record.penalty_level = new_penalty
            return True
        return False

    def update_status(self, student_id: str, new_status: str) -> bool:
        node = self._search(self.root, student_id)
        if node:
            node.record.status = new_status
            return True
        return False

    def delete(self, student_id: str) -> None:
        """Delete record with given ID (if exists)."""
        self.root = self._delete(self.root, student_id)

    def inorder_list(self) -> List[StudentRecord]:
        """Return all records sorted by student_id (inorder traversal)."""
        result: List[StudentRecord] = []
        self._inorder(self.root, result)
        return result

    # --- internal helper methods (hidden implementation) ---

    def _insert(self, node: Optional[BSTNode], record: StudentRecord) -> BSTNode:
        if node is None:
            return BSTNode(record)
        if record.student_id == node.key:
            node.record = record                # overwrite existing
        elif record.student_id < node.key:
            node.left = self._insert(node.left, record)
        else:
            node.right = self._insert(node.right, record)
        return node

    def _search(self, node: Optional[BSTNode], student_id: str) -> Optional[BSTNode]:
        if node is None:
            return None
        if student_id == node.key:
            return node
        if student_id < node.key:
            return self._search(node.left, student_id)
        else:
            return self._search(node.right, student_id)

    def _delete(self, node: Optional[BSTNode], student_id: str) -> Optional[BSTNode]:
        if node is None:
            return None

        if student_id < node.key:
            node.left = self._delete(node.left, student_id)
        elif student_id > node.key:
            node.right = self._delete(node.right, student_id)
        else:
            # found node to delete
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # two children: use inorder successor (smallest in right subtree)
            successor = self._min_value_node(node.right)
            node.key = successor.key
            node.record = successor.record
            node.right = self._delete(node.right, successor.key)
        return node

    def _min_value_node(self, node: BSTNode) -> BSTNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _inorder(self, node: Optional[BSTNode], result: List[StudentRecord]) -> None:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.record)
            self._inorder(node.right, result)


# ---------- Helper functions for UI / demo ----------

def print_record(record: StudentRecord) -> None:
    print(f"ID: {record.student_id}")
    print(f"Name: {record.name}")
    print(f"Programme: {record.programme}")
    print(f"Offence: {record.offence_type}")
    print(f"Date: {record.offence_date}")
    print(f"Penalty: {record.penalty_level}")
    print(f"Status: {record.status}")
    print("-" * 40)


def load_sample_data(tree: DisciplinaryBST) -> None:
    """Preload a few cases so your demo video has data immediately."""
    samples = [
        StudentRecord("A23001", "Alice Tan", "CS",
                      "Late submission", "2025-03-01", "Warning", "Open"),
        StudentRecord("A23015", "Ben Lee", "IT",
                      "Plagiarism", "2025-03-10", "Probation", "Open"),
        StudentRecord("A23007", "Chong Mei", "CS",
                      "Lab absence", "2025-03-12", "Warning", "Closed"),
    ]
    for r in samples:
        tree.insert(r)


# ---------- Simple console menu (for your video demo) ----------

def main():
    tree = DisciplinaryBST()
    load_sample_data(tree)

    menu = """
===== Student Disciplinary Record System (BST) =====
1. Add new disciplinary record
2. Search record by student ID
3. Update penalty level
4. Update case status
5. Delete record
6. Display all records (sorted by ID)
7. Exit
===================================================
"""
    while True:
        print(menu)
        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            sid = input("Student ID: ").strip()
            name = input("Name: ").strip()
            programme = input("Programme: ").strip()
            offence = input("Offence type: ").strip()
            date = input("Offence date (YYYY-MM-DD): ").strip()
            penalty = input("Penalty level: ").strip()
            status = input("Status (Open/Closed): ").strip()
            record = StudentRecord(sid, name, programme, offence, date, penalty, status)
            tree.insert(record)
            print("Record added/updated.\n")

        elif choice == "2":
            sid = input("Enter student ID to search: ").strip()
            record = tree.search(sid)
            if record:
                print("Record found:")
                print_record(record)
            else:
                print("No disciplinary record found for this student ID.\n")

        elif choice == "3":
            sid = input("Student ID to update penalty: ").strip()
            new_penalty = input("New penalty level: ").strip()
            if tree.update_penalty(sid, new_penalty):
                print("Penalty updated.\n")
            else:
                print("Student ID not found.\n")

        elif choice == "4":
            sid = input("Student ID to update status: ").strip()
            new_status = input("New status (Open/Closed): ").strip()
            if tree.update_status(sid, new_status):
                print("Status updated.\n")
            else:
                print("Student ID not found.\n")

        elif choice == "5":
            sid = input("Student ID to delete: ").strip()
            tree.delete(sid)
            print("If the record existed, it has been deleted.\n")

        elif choice == "6":
            records = tree.inorder_list()
            if not records:
                print("No disciplinary records in the system.\n")
            else:
                print("All disciplinary records (sorted by student ID):")
                for r in records:
                    print_record(r)

        elif choice == "7":
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 7.\n")


if __name__ == "__main__":
    main()
