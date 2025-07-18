import importlib

class FunctionRouter:
    """
    Dynamically imports and runs the correct function module from function_package/
    """
    def route(self, command, query):
        """
        command: string (e.g., 'search', 'rate', etc.)
        query: value or dict to pass to the function
        """
        module_name = f"function_package.{command}"
        try:
            module = importlib.import_module(module_name)
            # All function modules should have an 'execute' method
            if hasattr(module, "execute"):
                return module.execute(query)
            else:
                raise ImportError(f"Module '{module_name}' has no 'execute' function.")
        except Exception as e:
            raise RuntimeError(f"Function routing error for '{command}': {str(e)}")
