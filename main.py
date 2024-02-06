import ast
import configparser
import fileinput
import os
import pickle
import sys
import requests.auth
import json
from datetime import datetime
from requests import Response

config_file_parser = configparser.ConfigParser()
config_file_parser.read('main.py.ini')

general_config = config_file_parser['GENERAL']
login_config = config_file_parser['LOGIN']
search_endpoint = config_file_parser['SEARCH_ENDPOINT']
subreddit_endpoint = config_file_parser['SUBREDDIT_ENDPOINT']
comment_endpoint = config_file_parser['COMMENT_ENDPOINT']


def get_subreddits(query, sort, limit):
    url = f"{general_config['URL_BASE']}/{search_endpoint['URL']}"
    auth = get_authentication()
    params = {
        'q': query,
        'sort': sort,
        'limit': limit,
        'raw_json': 1
    }

    response = launch_request("subreddits_search", requests, url, auth, **params)

    path_subreddits = search_endpoint['PATH_SAVING']
    path_subreddits_urls = search_endpoint['PATH_SAVING_URLS']

    with open(path_subreddits, "w", encoding="utf-8") as file, \
            open(path_subreddits_urls, "w", encoding="utf-8") as file_urls:
        try:
            datetime_start = show_compilation_started()
            subreddits = response.json()['data']['children']
            for subreddit in subreddits:
                json.dump(subreddit, file, ensure_ascii=False, indent=None)
                file.write("\n")
                update_filesize_message(file.tell(), limit)

                url = subreddit["data"]["url"]
                file_urls.write(f"{url}\n")

            show_compilation_finished(datetime_start)
        except Exception as e:
            print(e)


def get_comment_ids_from_subreddits():
    path_subreddits_urls = search_endpoint['PATH_SAVING_URLS']
    with open(path_subreddits_urls, "r", encoding="utf-8") as file_urls:
        string = subreddit_endpoint['URL_FORMAT']
        datetime_start = show_compilation_started()
        for url in file_urls:
            url = string.format(subreddit=url).replace("\n", "")
            try:
                get_comment_ids_from_subreddit(url)
            except:
                print(f"The next URL was skipped because an error: {url}")
                continue
        show_compilation_finished(datetime_start)


def get_comment_ids_from_subreddit(url: str):
    name_subreddit = get_name_from_subreddit_url(url)

    url = f"{general_config['URL_BASE']}{url}"
    auth = get_authentication()
    params = {
        'raw_json': 1
    }

    response = launch_request(f"subreddits_comments/{name_subreddit}", requests, url, auth, **params)
    if response is None:
        return

    path_subreddit_comments = subreddit_endpoint["PATH_COMMENTS_ID"] \
        .format(subreddit=name_subreddit)

    with open(path_subreddit_comments, "w", encoding="utf-8") as file:
        try:
            comments = response.json()['data']['children']
            for comment in comments:
                comment_id = comment["data"]["id"]
                file.write(f"{name_subreddit, comment_id}\n")
        except Exception as e:
            print(e)


def get_comments_from_ids():
    path_comments = comment_endpoint['PATH_COMMENTS_ID']

    files = [os.path.join(path_comments, file_name) for file_name in os.listdir(path_comments) if
             os.path.isfile(os.path.join(path_comments, file_name))]

    with fileinput.input(files=files) as unique_file:
        datetime_start = show_compilation_started()
        for line in unique_file:
            subreddit, comment_id = ast.literal_eval(line)
            try:
                get_comments_info_from_subreddit(subreddit, comment_id)
            except:
                print(f"The next ID was skipped because an error: "
                      f"{subreddit}_{comment_id}")
                continue
        show_compilation_finished(datetime_start)


def get_comments_info_from_subreddit(subreddit: str, comment_id: str):
    url = f"{general_config['URL_BASE']}/" \
          f"{comment_endpoint['URL_FORMAT'].format(subreddit=subreddit, comment_id=comment_id)}"
    auth = get_authentication()
    params = {
        'raw_json': 1
    }

    response = launch_request(f"comments/{subreddit}_{comment_id}", requests, url, auth, **params)
    if response is None:
        return

    path_subreddit_comments = comment_endpoint["PATH_COMMENT_FORMAT"] \
        .format(subreddit=subreddit, comment_id=comment_id)
    with open(path_subreddit_comments, "w", encoding="utf-8") as file:
        try:
            comment_info = response.json()
            json.dump(comment_info, file, indent=2)
        except Exception as e:
            print(e)


def get_authentication():
    username = login_config['USERNAME']
    password = login_config['PASSWORD']
    return requests.auth.HTTPBasicAuth(username, password)


def launch_request(name: str, api: requests, url, auth, **params) -> Response:
    response_recover = None

    if general_config.getboolean("USE_RESTORABLE_REQUEST"):
        response_recover = recover_success_request(name)

    if response_recover is None:
        new_response = api.get(
            url,
            params=params,
            auth=auth
        )

        if new_response.status_code == 200:
            save_success_request(new_response, name)
            response_recover = new_response
        else:
            raise Exception("It was no possible to recover a useful request. "
                            "Reject because too many requests.")

    return response_recover


def show_compilation_started() -> datetime:
    datetime_start = datetime.now()
    print("-" * 60,
          f"\nProceso de recopilación iniciado: {datetime_start.strftime('%d/%m/%Y %H:%M:%S')}")
    return datetime_start


def show_compilation_finished(datetime_start: datetime):
    datetime_end = datetime.now()

    print(f"\nProceso terminado: {datetime_end.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Duración del proceso: {datetime_end - datetime_start} horas/minutos/segundos")
    print("-" * 60)


def update_filesize_message(filesize, limit):
    sys.stdout.write(
        f"\rTamaño actual del archivo: {filesize / 1000} kb | Cantidad de subreddits: {limit}"
    )


def save_success_request(response_request: Response, temp_filename: str):
    temporary_path = f"temp/{temp_filename}.pickle"
    with open(temporary_path, "wb") as file:
        pickle.dump(response_request, file)


def recover_success_request(temp_filename: str) -> Response:
    temporary_path = f"temp/{temp_filename}.pickle"
    if os.path.exists(temporary_path):
        with open(temporary_path, "rb") as file:
            return pickle.load(file)


def get_name_from_subreddit_url(url: str) -> str:
    url = url.removeprefix("/r/")
    url = url.removesuffix("/.json")
    return url


def create_directory_if_not_exists(relative_path: str):
    if not os.path.exists(relative_path):
        os.makedirs(relative_path, exist_ok=False)


def create_necessary_directories():
    create_directory_if_not_exists("temp")
    create_directory_if_not_exists("temp/subreddits_comments")
    create_directory_if_not_exists("temp/comments")

    create_directory_if_not_exists("data")
    create_directory_if_not_exists("data/subreddits_comments")
    create_directory_if_not_exists("data/comments")


if __name__ == "__main__":
    create_necessary_directories()

    get_subreddits(search_endpoint['QUERY'], search_endpoint['SORT'], search_endpoint['LIMIT'])
    get_comment_ids_from_subreddits()
    get_comments_from_ids()
