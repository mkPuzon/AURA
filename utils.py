'''utils.py

Contains general helpful functions for codebase.

Sep 2025
'''
def inspect_dictionary(d, indent=0):
    """ [Written by CLAUDE Sonnet 4]
    Neatly and clearly inspects a dictionary object, printing all key/value pairs
    at all levels and specifying the types of each element.

    Args:
        d (dict): The dictionary object to inspect.
        indent (int): The current indentation level for nested dictionaries (internal use).
    """
    if not isinstance(d, dict):
        print(f"{'  ' * indent}[ERROR] Expected dictionary, received {type(d).__name__}")
        return

    for key, value in d.items():
        key_type = type(key).__name__
        value_type = type(value).__name__
        
        # Print key with clear visual hierarchy
        print(f"{'  ' * indent}├─ {key} ({key_type})")

        # Handle nested dictionaries
        if isinstance(value, dict):
            print(f"{'  ' * indent}│  └─ {value_type} with {len(value)} key(s)")
            inspect_dictionary(value, indent + 1)
            if indent == 0:  # Add spacing after top-level nested dicts
                print()
        
        # Handle lists and tuples
        elif isinstance(value, (list, tuple)):
            print(f"{'  ' * indent}│  └─ {value} ({value_type}, length: {len(value)})")
            for i, item in enumerate(value):
                item_type = type(item).__name__
                print(f"{'  ' * (indent + 1)}   [{i}] {item} ({item_type})")
                # Recursively inspect dictionary items in lists
                if isinstance(item, dict):
                    inspect_dictionary(item, indent + 2)
        
        # Handle simple values
        else:
            print(f"{'  ' * indent}│  └─ {value} ({value_type})")
    
    # Add clean separation after top-level inspection
    if indent == 0:
        print("─" * 50)