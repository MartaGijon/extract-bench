import os
import json

def infer_string_config(key, values):
    if not values:
        return "string_exact"
    
    avg_len = sum(len(str(v)) for v in values if v is not None) / len([v for v in values if v is not None] or [1])
    key_lower = key.lower()
    
    semantic_keywords = ["name", "title", "description", "abstract", "summary", "review", "comment", "reason", "date", "time", "content", "text"]
    exact_keywords = ["id", "identifier", "code", "email", "url", "link", "type", "status", "category", "currency", "gender", "country", "state", "city", "position"]
    
    if avg_len > 30:
        return "string_semantic"
    
    for kw in semantic_keywords:
        if kw in key_lower:
            return "string_semantic"
            
    for kw in exact_keywords:
        if kw in key_lower:
            return "string_exact"
            
    # Default for short strings that don't match heuristics
    return "string_exact"

def infer_type_and_config(key, values):
    non_null_values = [v for v in values if v is not None]
    if not non_null_values:
        return {"anyOf": [{"type": "string"}, {"type": "null"}]}, "string_exact"
        
    has_null = len(non_null_values) < len(values)
    
    if all(isinstance(v, bool) for v in non_null_values):
        json_type = "boolean"
        config = "boolean_exact"
    elif all(isinstance(v, int) for v in non_null_values) and not all(isinstance(v, bool) for v in non_null_values):
        json_type = "integer"
        config = "integer_exact"
    elif all(isinstance(v, (int, float)) for v in non_null_values) and not all(isinstance(v, bool) for v in non_null_values):
        json_type = "number"
        config = "number_exact"
    elif all(isinstance(v, str) for v in non_null_values):
        json_type = "string"
        config = infer_string_config(key, non_null_values)
    elif all(isinstance(v, list) for v in non_null_values):
        json_type = "array"
        config = "array_llm"
    elif all(isinstance(v, dict) for v in non_null_values):
        json_type = "object"
        config = None
    else:
        # mixed types, default to string
        json_type = "string"
        config = "string_exact"
        
    if has_null:
        schema_type = {"anyOf": [{"type": json_type}, {"type": "null"}]}
    else:
        schema_type = {"type": json_type}
        
    return schema_type, config

def generate_object_schema(items):
    properties = {}
    
    if not items:
        return {"type": "object", "properties": {}}
        
    all_keys = set()
    for item in items:
        all_keys.update(item.keys())
        
    required = list(all_keys.copy())
    for item in items:
        required = [k for k in required if k in item]
        
    for key in all_keys:
        values = [item.get(key) for item in items]
        schema_type, config = infer_type_and_config(key, values)
        
        prop_schema = {}
        prop_schema.update(schema_type)
        if config:
            prop_schema["evaluation_config"] = config
            
        properties[key] = prop_schema
        
    schema = {
        "type": "object",
        "properties": properties,
        "required": required
    }
    return schema

def main():
    input_dir = "ground_truth"
    output_dir = "ground_truth_schema"
    
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if not filename.endswith(".json"):
            continue
            
        filepath = os.path.join(input_dir, filename)
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
            
        if isinstance(data, dict):
            properties = {}
            required = []
            
            for key, val in data.items():
                if isinstance(val, list) and all(isinstance(item, dict) for item in val):
                    item_schema = generate_object_schema(val)
                    properties[key] = {
                        "type": "array",
                        "items": item_schema,
                        "evaluation_config": "array_llm"
                    }
                    required.append(key)
                elif isinstance(val, list):
                    # Array of primitives
                    properties[key] = {
                        "type": "array",
                        "items": {"type": "string"},
                        "evaluation_config": "array_llm"
                    }
                    required.append(key)
                else:
                    schema_type, config = infer_type_and_config(key, [val])
                    prop_schema = {}
                    prop_schema.update(schema_type)
                    if config:
                        prop_schema["evaluation_config"] = config
                    properties[key] = prop_schema
                    required.append(key)
                    
            schema = {
                "type": "object",
                "properties": properties,
                "required": required
            }
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # The root is a list of objects
            item_schema = generate_object_schema(data)
            schema = {
                "type": "array",
                "items": item_schema,
                "evaluation_config": "array_llm"
            }
        else:
            schema = {"type": "object"}
            
        out_filename = filename.replace(".json", "-schema.json")
        out_filepath = os.path.join(output_dir, out_filename)
        
        with open(out_filepath, 'w') as f:
            json.dump(schema, f, indent=4)
            
if __name__ == "__main__":
    main()
