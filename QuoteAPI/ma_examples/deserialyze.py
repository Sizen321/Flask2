from author import Author
from schema import AuthorSchema
import json


json_data = """
{
    "id": "123",
    "name": "Ivan",
    "email": "ivan@mail.ru"
}
"""

schema = AuthorSchema()
json_data_as_dict = json.loads(json_data)

# dict -> validated dict
result = schema.load(json_data_as_dict)
print(result)
print(Author(**result))

# json -> validated dict
result = schema.loads(json_data)
print(result)