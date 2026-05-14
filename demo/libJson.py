import json
import os


class JsonHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_json(self):
        """Read JSON file and return parsed data."""
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File {self.file_path} not found")

            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.file_path}")
            return None
        except Exception as e:
            print(f"Error: Failed to read JSON file: {str(e)}")
            return None

    def write_json(self, data):
        """Write data to JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error: Failed to write JSON file: {str(e)}")
            return False


# Example usage:
# if __name__ == "__main__":
#     # Initialize with file path
#     json_handler = JsonHandler("example.json")

#     # Example data to write
#     sample_data = {
#         "name": "John",
#         "age": 30,
#         "city": "New York"
#     }

#     # Write JSON
#     if json_handler.write_json(sample_data):
#         print("Successfully wrote to JSON file")

#     # Read JSON
#     data = json_handler.read_json()
#     if data:
#         print("Read data:", data)

# Example usage:
# data = read_json_file("data/hailuoai.json")
# print(data['list'][0]['key'])
