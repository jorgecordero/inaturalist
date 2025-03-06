import requests
import datetime

def get_inaturalist_observations(username, jwt_token, updated_since=None):
    """
    Fetches observations for a given iNaturalist username using the API.
    
    :param username: iNaturalist username.
    :param jwt_token: Your JWT token for authentication.
    :param updated_since: (Optional) ISO 8601 datetime string to filter observations updated after this time.
    :return: A tuple (observations, deleted_observations), where:
        - observations is a list of observations
        - deleted_observations is a list of deleted observation IDs (if provided by the server)
    """
    url = "https://api.inaturalist.org/v1/observations"
    
    headers = {
        "Authorization": jwt_token
    }

    params = {"user_login": username}
    if updated_since:
        params['updated_since'] = updated_since

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()

    observations = data.get('results', [])

    deleted_observations = []
    if 'X-Deleted-Observations' in response.headers:
        deleted_observations = response.headers['X-Deleted-Observations'].split(',')

    return observations, deleted_observations


if __name__ == "__main__":
    username = "iperezlorenzo"
    jwt_token = "Bearer YOUR_JWT_TOKEN"

    updated_since = (datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()

    observations, deleted_observations = get_inaturalist_observations(username, jwt_token, updated_since)

    print(f"Fetched {len(observations)} observations for {username}")
    if deleted_observations:
        print(f"Deleted observations: {', '.join(deleted_observations)}")

    for obs in observations:
        print(f"ID: {obs['id']}, Species: {obs.get('species_guess', 'Unknown')}, Observed On: {obs.get('observed_on', 'N/A')}")
