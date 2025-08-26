
class Message:
    def __init__(self, content: str, role: str = 'user') -> None:
        self.content = content
        self.role = role

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content
        }
