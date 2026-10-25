from locust import HttpUser, task, between


class SecretaryUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def load_competitions(self):
        with self.client.post(
            "/showSummary",
            data={"email": "john@simplylift.co"},
            catch_response=True,
        ) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("Chargement des competitions > 5 s")

    @task(1)
    def update_points(self):
        with self.client.post(
            "/purchasePlaces",
            data={"club": "She Lifts", "competition": "Fall Classic", "places": "1"},
            catch_response=True,
        ) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("Mise a jour des points > 2 s")

    @task(1)
    def view_points_board(self):
        self.client.get("/points")
