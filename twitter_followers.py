import asyncio
import json
import urllib.request
import ssl
import iterm2

USER_KNOB_NAME = 'TWITTER_USER'
TOKEN_KNOB_NAME = 'BEARER_TOKEN'

# Twitter logo as 32*34 and 16*17 base64-encoded PNGs (Retina and non-Retina)
ICON2X = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAiCAYAAAA+stv/AAAAmmVYSWZNTQAqAAAACAAGARIAAwAAAAEAAQAAARoABQAAAAEAAABWARsABQAAAAEAAABeASgAAwAAAAEAAgAAATEAAgAAABUAAABmh2kABAAAAAEAAAB8AAAAAAAAAEgAAAABAAAASAAAAAFQaXhlbG1hdG9yIFBybyAxLjUuNQAAAAKgAgAEAAAAAQAAACCgAwAEAAAAAQAAACIAAAAAhkubXQAAAAlwSFlzAAALEwAACxMBAJqcGAAAA2dpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIgogICAgICAgICAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iPgogICAgICAgICA8dGlmZjpYUmVzb2x1dGlvbj43MjAwMDAvMTAwMDA8L3RpZmY6WFJlc29sdXRpb24+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx0aWZmOllSZXNvbHV0aW9uPjcyMDAwMC8xMDAwMDwvdGlmZjpZUmVzb2x1dGlvbj4KICAgICAgICAgPHRpZmY6UmVzb2x1dGlvblVuaXQ+MjwvdGlmZjpSZXNvbHV0aW9uVW5pdD4KICAgICAgICAgPGV4aWY6UGl4ZWxZRGltZW5zaW9uPjM0PC9leGlmOlBpeGVsWURpbWVuc2lvbj4KICAgICAgICAgPGV4aWY6UGl4ZWxYRGltZW5zaW9uPjMyPC9leGlmOlBpeGVsWERpbWVuc2lvbj4KICAgICAgICAgPHhtcDpDcmVhdG9yVG9vbD5QaXhlbG1hdG9yIFBybyAxLjUuNTwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8eG1wOk1ldGFkYXRhRGF0ZT4yMDIwLTAzLTE2VDEyOjQzOjI1WjwveG1wOk1ldGFkYXRhRGF0ZT4KICAgICAgPC9yZGY6RGVzY3JpcHRpb24+CiAgIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+Ctth+BAAAANwSURBVFiF7ZZNaFxVFMd/575pM3UyM0EzljaZJi2tIUI3VqUKRitVceNK7Qe0k+ii6ELEroXBD3DhQhdFKxY7U5dqEURRlFQxCzVF0YJaCJNknhNJTNvMSzVl8u5xMUmYJDPTvGGCLnp2597/Pb8/93HOfXAj/uOQplVKq9ma9HY5DimEPkQ2ofYXteY0kdbv3Cfln0p5+6mp6F9PJ7wFAyqdmcu73dTNPzcKT24vfgLyaNV9ZcrfyO2Fw9HpPScJTbXMPqPoS/n+WJsAdGS8fQ76sQ93/pGKXQzKT2aLgygP1NMI6ikyDZoAuUnRvW4q/r0BcOB+hahRvtl6qtgTCJ6ZefF6cABFokA3SAT0FTcXG+7Mzhw25U12Ldjc7IT4dltmdv/aLZhjQQwDE6jsTnZ7BaM6aQBE0ApBu2I/TWaLx/ec1A31KnVlvV7QjoAGtiA8pqJvj6favizfgPL7CtEGlNcnw97FrjNX7kDVVKuklvsCwgHmBXnZTcXTAOXCtnSuhrjbWnM+mfWmOjLevu73cmFUl1rXQrgBA2PjqWh6MSkXS6tJbveGgL11jwqzKDMCn1nRQSztIvJmML6O5FPxncsNqEr3aa/HF35CaAlWMCAefnNTsd7F3AAks967viPPgbxV1qxfiOpoZR4qr3IZ1eNNHMy1DYicq8wXukC/Wn80IKgPZ1cZcHOxz4GRdTegXFk56sttmBZrcJ5YfwOSW7m0NGDGUpEfMfQhy5/NpvINr9Y0AJAfiQ45vuxQJA3MNpdOwT3Senblcqgy6dxRvMtX+UKUlmbPAxV5B5FVLb688VRlW9YbUrinmXDQfP5orKuageWPjIjO+6UDSFOv36qY56vBVxsACk/dkjdy7TaUS83h6wfu0ehHtXarPrNjRxITjkY7RM1+EfkQmGiQPqybYv31BPWHr6p0nrl6SNSeANoCwi84du6h0YFb/wxuYFBDybGrDyL+CyCPBAQDDDl27vHrwQGkK+v1zvs27jgSUqEdpQ/lILClAXBJIJOYiz57/piU1nIgFC61un+HvNdUeRht6A8HwCKM4uvB8YH4D+MBDi59gp3va+zavPcGwkBA+K9qzQG3P3KhVqutycBiJE5MtoYjGzdD6G5E70XpEbEJRULAJSCnRoYR+doaO1E4FJ1uBHwj/jfxL251R/5qcBGOAAAAAElFTkSuQmCC"
ICON = "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"


async def main(connection):
    app = await iterm2.async_get_app(connection)
    icon = iterm2.StatusBarComponent.Icon(1, ICON)
    icon2x = iterm2.StatusBarComponent.Icon(2, ICON2X)

    # Register the status bar component
    # The username and bearer token are configurable values
    component = iterm2.StatusBarComponent(
        short_description='Twitter followers',
        detailed_description='Shows count of Twitter followers',
        exemplar='3401',
        update_cadence=600,
        identifier='andypiper.iterm-twitter-info.user-count',
        knobs=[
            iterm2.StringKnob('Twitter user', 'username',
                              'twitterdev', USER_KNOB_NAME),
            iterm2.StringKnob(
                'Bearer token', 'bearer token value', 'xxxxxx', TOKEN_KNOB_NAME)
        ],
        icons=[icon, icon2x]
    )

    @iterm2.StatusBarRPC
    async def twitter_user_count(knobs):
        twitter_user = knobs[USER_KNOB_NAME]
        token = knobs[TOKEN_KNOB_NAME]

        # we need to put the username into a session variable to pass to the click handler
        try:
            session = app.current_terminal_window.current_tab.current_session
        except Exception:
            return

        await session.async_set_variable("user.twitter_user", twitter_user)

        # this is the API endpoint to get user data, with metrics requested
        user_url = f'https://api.twitter.com/labs/2/users/by/username/{twitter_user}?user.fields=public_metrics'

        try:
            request = urllib.request.Request(
                user_url,
                headers={'Authorization': f'Bearer {token}'} if token else {},
            )
            followers = json.loads(
                urllib.request.urlopen(request).read().decode()
            )['data']['public_metrics']['followers_count']
            return f'{followers}'
        except Exception:
            raise
        else:
            return f'{followers}'

    @iterm2.RPC
    async def onclick(session_id):
        try:
            session = app.current_terminal_window.current_tab.current_session
        except Exception:
            return

        # grab the username from the session user variable
        twitter_user = await session.async_get_variable("user.twitter_user")

        # open a browser window to the Twitter user profile
        proc = await asyncio.create_subprocess_shell(
            f'open https://twitter.com/{twitter_user}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

    await component.async_register(connection, twitter_user_count, onclick=onclick)

iterm2.run_forever(main)
