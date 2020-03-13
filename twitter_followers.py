import asyncio
import json
import urllib.request
import ssl
import iterm2

USER_KNOB_NAME = 'TWITTER_USER'
TOKEN_KNOB_NAME = 'BEARER_TOKEN'


async def main(connection):
    twitter_user = None

    component = iterm2.StatusBarComponent(
        short_description='Twitter followers',
        detailed_description='Shows count of Twitter followers',
        exemplar='🐦 3401',
        update_cadence=300,
        identifier='andypiper.iterm-twitter-info.user-count',
        knobs=[
            iterm2.StringKnob('Twitter user', 'username',
                              'twitterdev', USER_KNOB_NAME),
            iterm2.StringKnob(
                'Bearer token', 'bearer token value', '', TOKEN_KNOB_NAME)

        ],
    )

    @iterm2.StatusBarRPC
    async def twitter_user_count(knobs):
        twitter_user = knobs[USER_KNOB_NAME]
        token = knobs[TOKEN_KNOB_NAME]

        user_url = f'https://api.twitter.com/labs/2/users/by/username/{twitter_user}?user.fields=public_metrics'

        try:
            request = urllib.request.Request(
                user_url,
                headers={'Authorization': f'Bearer {token}'} if token else {},
            )
            followers = json.loads(
                urllib.request.urlopen(request).read().decode()
            )['data']['public_metrics']['followers_count']
            return f'🐦 {followers}'
        except Exception:
            raise
        else:
            return f'🐦 {followers}'

    @iterm2.RPC
    async def onclick(session_id):
        proc = await asyncio.create_subprocess_shell(
            f'open https://twitter.com/{twitter_user}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

    await component.async_register(connection, twitter_user_count, onclick=onclick)

iterm2.run_forever(main)
