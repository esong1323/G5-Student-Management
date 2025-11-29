# ============================================
# Student Management System using BST (Python)
# Task 2 – MECS1023 Advanced Data Structures
# ============================================

from dataclasses import dataclass


# -------------------------------
# 1. Student Data Type (ADT)
# -------------------------------
@dataclass
class Student:
    student_id: str   # will be used as BST key
    name: str
    program: str
    cgpa: float

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Program: {self.program}, CGPA: {self.cgpa:.2f}"


# -------------------------------
# 2. BST Node (ADT)
# -------------------------------
class BSTNode:
    def __init__(self, key: str, value: Student):
        self.key = key          # student_id
        self.value = value      # Student object
        self.left = None        # left child
        self.right = None       # right child


# -------------------------------
# 3. StudentBST (BST ADT)
# -------------------------------
class StudentBST:
    def __init__(self):
        self.root = None

    # --------- Insert ----------
    def insert(self, student: Student):
        """Insert a student into the BST using student_id as key."""
        if self.root is None:
            self.root = BSTNode(student.student_id, student)
        else:
            self._insert_recursive(self.root, student)

    def _insert_recursive(self, node: BSTNode, student: Student):
        if student.student_id == node.key:
            # already exists -> ignore or update
            print(f"[WARN] Student with ID {student.student_id} already exists. Skipping insert.")
            return
        elif student.student_id < node.key:
            if node.left is None:
                node.left = BSTNode(student.student_id, student)
            else:
                self._insert_recursive(node.left, student)
        else:  # student.student_id > node.key
            if node.right is None:
                node.right = BSTNode(student.student_id, student)
            else:
                self._insert_recursive(node.right, student)

    # --------- Search ----------
    def search(self, student_id: str) -> Student | None:
        """Search for a student by ID. Return Student or None."""
        node = self._search_recursive(self.root, student_id)
        return node.value if node else None

    def _search_recursive(self, node: BSTNode | None, key: str) -> BSTNode | None:
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    # --------- Update ----------
    def update(self, student_id: str, new_name: str | None = None,
               new_program: str | None = None, new_cgpa: float | None = None) -> bool:
        """Update fields of a student. Return True if updated, False if not found."""
        node = self._search_recursive(self.root, student_id)
        if not node:
            return False

        if new_name is not None:
            node.value.name = new_name
        if new_program is not None:
            node.value.program = new_program
        if new_cgpa is not None:
            node.value.cgpa = new_cgpa
        return True

    # --------- Delete ----------
    def delete(self, student_id: str):
        """Delete a student by ID from the BST."""
        self.root = self._delete_recursive(self.root, student_id)

    def _delete_recursive(self, node: BSTNode | None, key: str) -> BSTNode | None:
        if node is None:
            return None

        # Search for node
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node found
            # Case 1: No child
            if node.left is None and node.right is None:
                return None
            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: Two children -> Find inorder successor (smallest in right subtree)
            successor = self._min_value_node(node.right)
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.key)

        return node

    def _min_value_node(self, node: BSTNode) -> BSTNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    # --------- Traversal ----------
    def inorder(self):
        """Return list of students in sorted order of student_id."""
        result: list[Student] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node: BSTNode | None, result: list):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)


# -------------------------------
# 4. Menu-driven Interface
# -------------------------------
def print_menu():
    print("\n===== Student Management System (BST) =====")
    print("1. Add new student")
    print("2. Search student by ID")
    print("3. Update student")
    print("4. Delete student")
    print("5. Display all students (sorted by ID)")
    print("6. Exit")


def main():
    tree = StudentBST()

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            # Add student
            sid = input("Enter Student ID: ").strip()
            name = input("Enter Name: ").strip()
            program = input("Enter Program: ").strip()
            try:
                cgpa = float(input("Enter CGPA: ").strip())
            except ValueError:
                print("[ERROR] Invalid CGPA. Setting to 0.0")
                cgpa = 0.0

            student = Student(student_id=sid, name=name, program=program, cgpa=cgpa)
            tree.insert(student)
            print("[INFO] Student added (if ID was unique).")

        elif choice == "2":
            # Search student
            sid = input("Enter Student ID to search: ").strip()
            student = tree.search(sid)
            if student:
                print("[FOUND] ", student)
            else:
                print("[NOT FOUND] Student with that ID.")

        elif choice == "3":
            # Update student
            sid = input("Enter Student ID to update: ").strip()
            student = tree.search(sid)
            if not student:
                print("[NOT FOUND] Cannot update. Student does not exist.")
                continue

            print("Leave field empty if you don't want to change it.")
            new_name = input(f"New Name (current: {student.name}): ").strip()
            new_program = input(f"New Program (current: {student.program}): ").strip()
            new_cgpa_str = input(f"New CGPA (current: {student.cgpa}): ").strip()

            kwargs = {}
            if new_name:
                kwargs["new_name"] = new_name
            if new_program:
                kwargs["new_program"] = new_program
            if new_cgpa_str:
                try:
                    kwargs["new_cgpa"] = float(new_cgpa_str)
                except ValueError:
                    print("[WARN] Invalid CGPA. Keeping old value.")

            if tree.update(sid, **kwargs):
                print("[INFO] Student updated successfully.")
            else:
                print("[ERROR] Update failed.")

        elif choice == "4":
            # Delete student
            sid = input("Enter Student ID to delete: ").strip()
            student = tree.search(sid)
            if not student:
                print("[NOT FOUND] Student does not exist.")
            else:
                tree.delete(sid)
                print("[INFO] Student deleted.")

        elif choice == "5":
            # Display all
            students = tree.inorder()
            if not students:
                print("[INFO] No students in the system.")
            else:
                print("\n--- All Students (sorted by ID) ---")
                for s in students:
                    print(s)

        elif choice == "6":
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
th