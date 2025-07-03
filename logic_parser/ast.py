from dataclasses import dataclass
from typing import Optional
from logic_parser.token import Token
from collections import deque


@dataclass
class ASTNode:
    value: Token
    right: Optional["ASTNode"] = None
    left: Optional["ASTNode"] = None


class AST:
    def __init__(self) -> None:
        self.head: Optional[ASTNode] = None

    def add(self, value: Token):
        if not self.head:
            self.head = ASTNode(value)
            return self.head
        return self._add(self.head, value)

    def _add(self, node: Optional[ASTNode], value: Token):
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if not current:
                current = ASTNode(value)

            if not current.left:
                current.left = ASTNode(value)
                return current.left
            else:
                queue.append(current.left)
            if not current.right:
                current.right = ASTNode(value)
                return current.right
            else:
                queue.append(current.right)
