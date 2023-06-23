import grpc
import psycopg2

import user_pb2
import user_pb2_grpc


# Database connection configuration
conn = psycopg2.connect(
    host="localhost",
    database="your_database_name",
    user="your_username",
    password="your_password"
)


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (request.id,))
            result = cursor.fetchone()
            if result:
                user = user_pb2.User(
                    id=result[0],
                    name=result[1],
                    email=result[2]
                )
                return user
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found.")
                return None

    def CreateUser(self, request, context):
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                (request.name, request.email)
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            user = user_pb2.User(
                id=user_id,
                name=request.name,
                email=request.email
            )
            return user

    def UpdateUser(self, request, context):
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id",
                (request.name, request.email, request.id)
            )
            if cursor.rowcount > 0:
                conn.commit()
                user = user_pb2.User(
                    id=request.id,
                    name=request.name,
                    email=request.email
                )
                return user
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found.")
                return None

    def DeleteUser(self, request, context):
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (request.id,))
            if cursor.rowcount > 0:
                conn.commit()
                response = user_pb2.DeleteUserResponse(success=True)
                return response
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found.")
                return None


def serve():
    server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)
        conn.close()


if __name__ == "__main__":
    serve()
