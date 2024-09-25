from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

groups = []
students = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
        {"id": 4, "name": "David"},
        {"id": 5, "name": "Eve"},
    ]
group_id_counter = 0

def find_student_by_id(sid):
    for student in students:
        if student["id"] == int(sid):
            return student
    return None

def find_student_by_name(sname):
    for student in students:
        if student["name"] == sname:
            return student
    return None

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    return jsonify(groups)

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    return jsonify(students)

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    group_member_ids = []
    for name in group_members:
        stripped_name = name.strip()
        student = find_student_by_name(stripped_name)
        if student is None:
            return "Student " + stripped_name + " not found", 400
        group_member_ids.append(student["id"])

    global group_id_counter
    group_id_counter += 1
    group_id = group_id_counter

    group_obj = {
        "id": group_id,
        "groupName": group_name,
        "members": group_member_ids,
    }

    groups.append(group_obj)
    return jsonify(group_obj), 201

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    for group in groups:
        if group["id"] == group_id:
            groups.remove(group)
            return '', 204

    return "Group id " + group_id + " is not found", 400

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # TODO: (sample response below)
    for group in groups:
        if group["id"] == group_id:
            return jsonify({
                    "id": group["id"],
                    "groupName": group["groupName"],
                    "members": list(map(find_student_by_id, group["members"])),
                })
    abort(404, "Group not found")

if __name__ == '__main__':
    app.run(port=3902, debug=True)
