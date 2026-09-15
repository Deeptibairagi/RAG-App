

# import requests

# from app.config import API_URL


# class APIClient:

#     def __init__(
#         self,
#         base_url: str,
#     ):

#         self.base_url = base_url.rstrip("/")

#     # ========================================================
#     # Check API
#     # ========================================================

#     def check_api(self):

#         try:

#             response = requests.get(
#                 f"{self.base_url}/health",
#                 timeout=5,
#             )

#             if response.status_code == 200:

#                 return (
#                     True,
#                     response.status_code,
#                     "API is running",
#                 )

#             return (
#                 False,
#                 response.status_code,
#                 "API returned an error.",
#             )

#         except requests.exceptions.ConnectionError:

#             return (
#                 False,
#                 None,
#                 "Could not connect to FastAPI.",
#             )

#         except requests.exceptions.Timeout:

#             return (
#                 False,
#                 None,
#                 "FastAPI request timed out.",
#             )

#         except Exception as exc:

#             return (
#                 False,
#                 None,
#                 str(exc),
#             )

#     # ========================================================
#     # Ask question
#     # ========================================================

#     def ask_question(
#         self,
#         question: str,
#         history: list,
#     ):

#         payload = {
#             "question": question,
#             "history": history,
#         }

#         try:

#             response = requests.post(
#                 f"{self.base_url}/api/chat/ask",
#                 json=payload,
#                 timeout=120,
#             )

#             # ------------------------------------------------
#             # HTTP error
#             # ------------------------------------------------

#             if response.status_code != 200:

#                 try:

#                     details = response.json()

#                 except Exception:

#                     details = response.text

#                 return {
#                     "success": False,
#                     "answer": "",
#                     "error": (
#                         f"API request failed "
#                         f"with status "
#                         f"{response.status_code}"
#                     ),
#                     "details": details,
#                     "status_code": response.status_code,
#                 }

#             # ------------------------------------------------
#             # Parse response
#             # ------------------------------------------------

#             data = response.json()

#             return {
#                 "success": data.get(
#                     "success",
#                     False,
#                 ),
#                 "answer": data.get(
#                     "answer",
#                     "",
#                 ),
#                 "error": data.get(
#                     "error",
#                     "",
#                 ),
#                 "details": data.get(
#                     "details",
#                 ),
#                 "status_code": response.status_code,
#             }

#         except requests.exceptions.ConnectionError:

#             return {
#                 "success": False,
#                 "answer": "",
#                 "error": "Could not connect to FastAPI.",
#                 "details": None,
#                 "status_code": None,
#             }

#         except requests.exceptions.Timeout:

#             return {
#                 "success": False,
#                 "answer": "",
#                 "error": "Request timed out.",
#                 "details": None,
#                 "status_code": None,
#             }

#         except Exception as exc:

#             return {
#                 "success": False,
#                 "answer": "",
#                 "error": str(exc),
#                 "details": None,
#                 "status_code": None,
#             }


# # ============================================================
# # Global API client
# # ============================================================

# api_client = APIClient(
#     API_URL
# )



import requests

from app.config import API_URL


class APIClient:
    """
    Client used by Streamlit to communicate with FastAPI.
    """

    def __init__(
        self,
        base_url: str,
    ):

        if not base_url:
            raise RuntimeError(
                "API_URL is not configured."
            )

        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    # ========================================================
    # Health check
    # ========================================================

    def check_api(self):

        try:

            response = self.session.get(
                f"{self.base_url}/health",
                timeout=(5, 15),
            )

            if response.status_code == 200:

                data = response.json()

                return (
                    True,
                    response.status_code,
                    data.get(
                        "status",
                        "API is running",
                    ),
                )

            return (
                False,
                response.status_code,
                (
                    f"FastAPI returned HTTP "
                    f"{response.status_code}"
                ),
            )

        except requests.exceptions.ConnectionError:

            return (
                False,
                None,
                "Could not connect to FastAPI.",
            )

        except requests.exceptions.Timeout:

            return (
                False,
                None,
                "FastAPI health check timed out.",
            )

        except requests.exceptions.RequestException as exc:

            return (
                False,
                None,
                f"FastAPI request failed: {exc}",
            )

        except Exception as exc:

            return (
                False,
                None,
                str(exc),
            )

    # ========================================================
    # Ask question
    # ========================================================

    def ask_question(
        self,
        question: str,
        history: list,
    ):

        question = (question or "").strip()

        if not question:

            return {
                "success": False,
                "answer": "",
                "error": "Question cannot be empty.",
                "details": None,
                "status_code": None,
            }

        payload = {
            "question": question,
            "history": history or [],
        }

        try:

            response = self.session.post(
                f"{self.base_url}/api/chat/ask",
                json=payload,
                timeout=(10, 180),
            )

            # ------------------------------------------------
            # HTTP error
            # ------------------------------------------------

            if not response.ok:

                try:
                    details = response.json()

                except ValueError:
                    details = response.text

                return {
                    "success": False,
                    "answer": "",
                    "error": (
                        f"API request failed "
                        f"with status "
                        f"{response.status_code}"
                    ),
                    "details": details,
                    "status_code": response.status_code,
                }

            # ------------------------------------------------
            # JSON response
            # ------------------------------------------------

            try:

                data = response.json()

            except ValueError:

                return {
                    "success": False,
                    "answer": "",
                    "error": (
                        "FastAPI returned an invalid "
                        "JSON response."
                    ),
                    "details": response.text,
                    "status_code": response.status_code,
                }

            return {
                "success": data.get(
                    "success",
                    False,
                ),
                "answer": data.get(
                    "answer",
                    "",
                ),
                "error": data.get(
                    "error",
                    "",
                ),
                "details": data.get(
                    "details",
                ),
                "status_code": response.status_code,
            }

        except requests.exceptions.ConnectionError:

            return {
                "success": False,
                "answer": "",
                "error": (
                    "Could not connect to FastAPI. "
                    "Please check whether the backend "
                    "is running."
                ),
                "details": None,
                "status_code": None,
            }

        except requests.exceptions.Timeout:

            return {
                "success": False,
                "answer": "",
                "error": (
                    "The RAG request timed out. "
                    "The backend may still be processing "
                    "the request."
                ),
                "details": None,
                "status_code": None,
            }

        except requests.exceptions.RequestException as exc:

            return {
                "success": False,
                "answer": "",
                "error": f"Request failed: {exc}",
                "details": None,
                "status_code": None,
            }

        except Exception as exc:

            return {
                "success": False,
                "answer": "",
                "error": str(exc),
                "details": None,
                "status_code": None,
            }


# ============================================================
# Global API client
# ============================================================

api_client = APIClient(
    API_URL
)