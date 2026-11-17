from fastapi import Request, Response, status


class GlobalExceptionHandler:
    async def handle_unexpected(self, request: Request, exception: Exception) -> Response:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
