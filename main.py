import argparse
import textwrap

import qbittorrentapi


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bulk replace old tracker URL with new tracker URL",
    )

    parser.add_argument(
        "old_tracker_url",
        help=textwrap.dedent(
            """\
            The old tracker URL.
            """
        ),
    )

    parser.add_argument(
        "new_tracker_url",
        help=textwrap.dedent(
            """\
            The new tracker URL.
            """
        ),
    )

    parser.add_argument(
        "-U",
        "--url",
        help=textwrap.dedent(
            """\
            Qbittorent URL. Default: http://localhost:8080
            """
        ),
        default="http://localhost:8080",
    )
    parser.add_argument(
        "-u",
        "--username",
        help=textwrap.dedent(
            """\
            Qbittorent authentication username.
            Leave empty if "Bypass authentication for clients on localhost" is enabled in qBittorrent and the url is localhost or 127.0.0.1.
            """
        ),
    )

    parser.add_argument(
        "-p",
        "--password",
        help=textwrap.dedent(
            """\
            Qbittorent authentication password.
            Leave empty if "Bypass authentication for clients on localhost" is enabled in qBittorrent and the url is localhost or 127.0.0.1.
            """
        ),
    )

    args = parser.parse_args()

    old_tracker = args.old_tracker_url
    new_tracker = args.new_tracker_url
    url = args.url
    username = args.username
    password = args.password

    return old_tracker, new_tracker, url, username, password


def main():
    old_tracker, new_tracker, url, username, password = parse_args()

    conn_info = {
        "host": url,
        "username": username,
        "password": password,
    }

    matched_torrents = []
    with qbittorrentapi.Client(**conn_info) as qbt_client:
        # retrieve and show all torrents
        for torrent in qbt_client.torrents_info():
            if any(tracker.url for tracker in torrent.trackers if tracker.url == old_tracker):
                matched_torrents.append(torrent)
                print(f'Replacing tracker for: "{torrent.name}."')
                torrent.edit_tracker(old_tracker, new_tracker)
    if len(matched_torrents) > 0:
        print(f"Updated {len(matched_torrents)} torrents.")
    else:
        print(f'No torrents matched the tracker URL "{old_tracker}".')


if __name__ == "__main__":
    main()
