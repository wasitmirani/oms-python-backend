import grpc

import user_pb2
import user_pb2_grpc


def create_user(stub):
    request = user_pb2.CreateUserRequest(
        name="Alice",
        email="alice@example.com"
    )
    response = stub.CreateUser(request)
    print("Created user:", response)

def get_user(stub, user_id):
    request = user_pb2.GetUserRequest(id=user_id)
    response = stub.GetUser(request)
    print("Fetched user:", response)

def update_user(stub, user_id):
    request = user_pb2.UpdateUserRequest(
        id=user_id,
        name="Alice Smith",
        email="alice.smith@example.com"
    )
    response = stub.UpdateUser(request)
    print("Updated user:", response)

def delete_user(stub, user_id):
    request = user_pb2.DeleteUserRequest(id=user_id)
    response = stub.DeleteUser(request)
    print("Deleted user:", response.success)


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = user_pb2_grpc.UserServiceStub(channel)

    create_user(stub)

    # Assuming the user_id is 1
    user_id = 1
    get_user(stub, user_id)
    update_user(stub, user_id)
    get_user(stub, user_id)
    delete_user(stub, user_id)
    get_user(stub, user_id)


if __name__ == "__main__":
    run()
