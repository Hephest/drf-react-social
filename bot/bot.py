import configparser
import datetime
import json
import time
from random import randrange

import click
import requests
from faker import Faker

API_URL = 'http://0.0.0.0:8000/api/v1/'
API_POSTS = API_URL + 'posts/'
USER_SIGNUP_URL = API_URL + 'users/register/'
TOKEN_OBTAIN_URL = API_URL + 'token/obtain/'
TOKEN_REFRESH_URL = API_URL + 'token/refresh/'


def api_refresh_token(refresh_token):
    """Refresh expired access token by longer-lived refresh token."""

    payload = {
        'refresh': refresh_token,
    }

    response = requests.post(TOKEN_REFRESH_URL, json=payload)

    response_json = json.loads(response.text)
    new_access_token = response_json['access']

    return new_access_token


def signup_users(users_count, storage_path):
    """Generate and sign up all fake users."""

    fake = Faker()
    data = {}
    total_users = 0

    with click.progressbar(
            range(users_count),
            label='Generating and signing up users',
            show_eta=True,
            fill_char=click.style('#', fg='green'),
            bar_template='[ ] %(label)s [%(bar)s] %(info)s'
    ) as bar:
        for user in bar:
            fake_username = fake.profile(fields=['username'])['username']
            fake_email = fake.profile(fields=['mail'])['mail']
            fake_password = fake.password(length=12, special_chars=False, upper_case=False)

            payload = {
                'username': fake_username,
                'email': fake_email,
                'password': fake_password,
            }

            response = requests.post(USER_SIGNUP_URL, json=payload)

            if response.status_code == 201:
                data[user] = {
                    'id': user,
                    'username': fake_username,
                    'password': fake_password,
                    'email': fake_email,
                    'access_token': '',
                    'refresh_token': ''
                }

                total_users += 1

    with open(storage_path, 'w') as storage:
        json.dump(data, storage, indent=4)

    click.echo(
        ' └─[' + click.style('❢', fg='blue') + '] ' + click.style(str(total_users), fg='green')
        + ' fake users created in ' + click.style(storage_path, fg='green')
    )

    click.echo('\r[{}] Generating and signing up users'.format(click.style('✓', fg='green')))


def update_users(storage_path):
    """Update access and refresh tokens for fake users in JSON."""

    with open(storage_path, 'r') as database:
        data = json.load(database)

    with click.progressbar(
            data,
            label='Retrieving tokens',
            show_eta=True,
            fill_char=click.style('#', fg='green'),
            bar_template='[ ] %(label)s [%(bar)s] %(info)s'
    ) as bar:
        for user in bar:
            payload = {
                'username': data[user]['username'],
                'password': data[user]['password'],
            }
            response = requests.post(TOKEN_OBTAIN_URL, json=payload)
            response_json = json.loads(response.text)
            data[user]['access_token'] = response_json['access']
            data[user]['refresh_token'] = response_json['refresh']

    with open(storage_path, 'w') as output:
        json.dump(data, output, indent=4)

    click.echo('\r[{}] Retrieving tokens'.format(click.style('✓', fg='green')))


def create_posts(storage_path, max_posts):
    """Create randrange(0, max_posts) posts by user."""

    fake = Faker()
    total_posts = 0

    with open(storage_path, 'r') as database:
        data = json.load(database)

    with click.progressbar(
            data,
            label='Creating posts',
            show_eta=True,
            fill_char=click.style('#', fg='green'),
            bar_template='[ ] %(label)s [%(bar)s] %(info)s'
    ) as bar:
        for user in bar:
            posts_count = randrange(0, max_posts)
            for post in range(0, posts_count):
                header = {
                    'Authorization': 'JWT {}'.format(data[user]['access_token'])
                }
                payload = {
                    'title': fake.sentence(nb_words=6, variable_nb_words=True),
                    'content': fake.text(max_nb_chars=350),
                }

                response = requests.post(API_POSTS, headers=header, json=payload)

                if response.status_code == 401:
                    header = {
                        'Authorization': 'JWT {}'.format(api_refresh_token(data[user]['refresh_token']))
                    }
                    payload = {
                        'title': fake.sentence(nb_words=6, variable_nb_words=True),
                        'content': fake.text(max_nb_chars=350),
                    }
                    response = requests.post(API_POSTS, headers=header, json=payload)
                elif response.status_code == 201:
                    total_posts += 1

    click.echo('\r[{}] Creating posts'.format(click.style('✓', fg='green')))
    click.echo(
        ' └─[' + click.style('❢', fg='blue') + '] ' + click.style(str(total_posts), fg='green')
        + ' posts was created by fake users.'
    )

    return total_posts


def like_posts(storage_path, max_likes, total_posts):
    """Like randrange(0, max_likes) posts per user."""

    total_likes = 0

    with open(storage_path, 'r') as database:
        data = json.load(database)

    with click.progressbar(
            data,
            label='Like posts',
            show_eta=True,
            fill_char=click.style('#', fg='green'),
            bar_template='[ ] %(label)s [%(bar)s] %(info)s'
    ) as bar:
        for user in bar:
            liked_posts = randrange(0, max_likes)
            for post in range(0, liked_posts):
                post_id = randrange(0, total_posts)
                header = {
                    'Authorization': 'JWT {}'.format(data[user]['access_token'])
                }

                url = API_POSTS + '{}/like/'.format(post_id)
                response = requests.post(url, headers=header)

                if response.status_code == 200:
                    total_likes += 1

    click.echo('\r[{}] Like posts'.format(click.style('✓', fg='green')))
    click.echo(
        ' └─[' + click.style('❢', fg='blue') + '] ' + click.style(str(total_likes), fg='green')
        + ' likes was created by fake users.'
    )


@click.command()
def cli():
    """Automation bot script for testing purposes."""
    click.clear()
    click.secho('[Automation Bot]', fg='red')
    click.secho('v0.1.0', fg='green')
    click.echo(
        """
        
        Options:
                
            c) Run bot from configuration file
            i) Run bot in interactive mode (default)
        
        """
    )

    option = click.prompt(click.style('Select your option:', fg='green'), default='i', type=str)
    if option == 'c':
        run()
    elif option == 'i':
        run_interactive()
    else:
        click.secho('Error: option not valid.', fg='red')


def run():
    """Run automation bot by provided configuration file."""
    click.clear()
    click.secho('[Automation Bot] Manual mode', fg='red')
    click.secho('v0.1.0', fg='green')
    click.echo()

    config = configparser.ConfigParser()
    config.read('config.ini')

    users_count = 10
    max_posts = 3
    max_likes = 4
    storage_filename = 'users.json'

    try:
        users_count = int(config['constants']['number_of_users'])
        click.echo('Number of users: ' + click.style(str(users_count), fg='green'))
    except KeyError:
        click.secho('Error: `number_of_users` missed in config.ini!', fg='red')
        click.secho('\t Will be used default value of {}'.format(str(users_count)), fg='red')

    try:
        max_posts = int(config['constants']['max_posts_per_user'])
        click.echo('Max posts per user: ' + click.style(str(max_posts), fg='green'))
    except KeyError:
        click.secho('Error: `max_posts_per_user` missed in config.ini!', fg='red')
        click.secho('\t Will be used default value of {}'.format(str(max_posts)), fg='red')

    try:
        max_likes = int(config['constants']['max_likes_per_user'])
        click.echo('Max likes per user: ' + click.style(str(max_likes), fg='green'))
    except KeyError:
        click.secho('Error: `max_likes_per_user` missed in config.ini!', fg='red')
        click.secho('\t Will be used default value of {}'.format(str(max_likes)), fg='red')

    try:
        storage_filename = str(config['storage']['filename'])
        click.echo('Storage file name (JSON): ' + click.style(storage_filename, fg='green'))
    except KeyError:
        click.secho('Error: `filename` missed in config.ini!', fg='red')
        click.secho('\t Will be used default filename of {}'.format(storage_filename), fg='red')

    click.echo()

    t1_start = time.perf_counter()

    signup_users(users_count, storage_filename)
    update_users(storage_filename)
    total_posts = create_posts(storage_filename, max_posts)
    like_posts(storage_filename, max_likes, total_posts)

    t1_stop = time.perf_counter()

    total_elapsed_time = datetime.timedelta(seconds=(t1_stop - t1_start))
    click.echo('Total elapsed time: ' + str(total_elapsed_time))


def run_interactive():
    """Run automation bot in interactive mode."""
    click.clear()
    click.secho('[Automation Bot] Interactive mode', fg='red')
    click.secho('v0.1.0', fg='green')
    click.echo()

    users_count = click.prompt(click.style('Number of users', fg='green'), type=int)
    max_posts = click.prompt(click.style('Max posts per user', fg='green'), type=int)
    max_likes = click.prompt(click.style('Max likes per user', fg='green'), type=int)
    storage_path = click.prompt(click.style('Storage file name (JSON)', fg='green'), type=str)
    click.echo()

    t1_start = time.perf_counter()

    signup_users(users_count, storage_path)
    update_users(storage_path)
    total_posts = create_posts(storage_path, max_posts)
    like_posts(storage_path, max_likes, total_posts)
    click.echo()

    t1_stop = time.perf_counter()

    total_elapsed_time = datetime.timedelta(seconds=(t1_stop - t1_start))
    click.echo('Total elapsed time: ' + str(total_elapsed_time))


if __name__ == '__main__':
    cli()
