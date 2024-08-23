def convert_to_lua_table(python_dict):
    """
    Convert a Python dictionary to a Lua table representation.
    Does not support objects and does not support lists except list of strings.
    """
    def convert_value(value):
        if isinstance(value, dict):
            return convert_to_lua_table(value)
        elif isinstance(value, str):
            return f'[=[{value}]=]'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, list):
            return "{" + ", ".join(f'"{val}"' for val in value) + "}"
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            raise TypeError(f"Unsupported data type: {type(value)}")

    out = "{"
    for key, value in python_dict.items():
        lua_key = f'["{key}"]' if isinstance(key, str) else key
        lua_value = convert_value(value)
        out += f"{lua_key} = {lua_value}, "
    return out.rstrip(', ') + "}"

