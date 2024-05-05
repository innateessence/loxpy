class GenerateAST:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def define_visitor(self, file, base_name: str, types: dict):
        file.write("from abc import ABC, abstractmethod\n\n")
        file.write(f"class {base_name}Visitor(ABC):\n")
        for class_name in types:
            file.write(f"    @abstractmethod\n")
            file.write(f"    def visit_{class_name}(self, {base_name.lower()}):\n")
        file.write("\n")

    def define_type(self, file, base_name: str, class_name: str, fields: list):
        file.write(f"\n\nclass {class_name}({base_name}):\n")
        file.write(f"    def __init__(self, {', '.join(fields)}):\n")
        for field in fields:
            field_name = field.split(" ")[1]
            file.write(f"        self.{field_name} = {field_name}\n")
        file.write("\n")
        file.write("    def accept(self, visitor):\n")
        file.write(f"        return visitor.visit_{class_name}(self)\n")

    def define_ast(self, base_name: str, types: dict):
        path = f"{self.output_dir}/{base_name}.py"
        with open(path, "w") as file:
            file.write("from abc import ABC, abstractmethod\n\n")
            file.write(f"class {base_name}(ABC):\n")
            file.write("    @abstractmethod\n")
            file.write("    def accept(self, visitor):\n")
            for class_name, fields in types.items():
                self.define_type(file, base_name, class_name, fields)
