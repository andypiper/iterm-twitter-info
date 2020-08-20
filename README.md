# iTerm-Twitter-Info

[![v2](https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2)](https://developer.twitter.com/en/docs/twitter-api)

Some scripts and examples for bringing Twitter data to your [iTerm](https://iterm2.com)

iTerm2 has a configurable status bar which can include all kinds of additional information.

![iTerm2 window](/screenshot.png?raw=true "iTerm2 window")

This repository includes two ways to add a Twitter follower count to the status bar:

* `user_var.sh`: a script variable which can be set at session start, which uses [`twurl`](https://github.com/twitter/twurl) to call the Twitter API and [`jq`](https://stedolan.github.io/jq/) to extract the follower count. This method then uses an Interpolated String component to place the value of `user.twitterCount` into the status bar. The user to track is set in the script. This also assumes that `twurl` is installed, and configured with appropriate Twitter permissions.
* `twitter_followers.py`: a Python component, configurable in the status bar settings panel. The username and Twitter API bearer token must be configured in order for this to run. This component includes a Twitter icon, and will update every 10 minutes in the background while the iTerm session is running. Clicking on the component opens the user's Twitter profile on the web. Run `install.sh` to install this script to the iTerm scripts AutoLaunch directory, and enable it from the Scripts->AutoLaunch menu. This also requires the Python API setting to be enabled in iTerm Preferences (General->Magic->Enable Python API).

In the example shown in the screenshot, the script variable reflects the follower number at the start of the current session, while the Python component has updated in the meantime to reflect a lower current number.

Both of these approaches use the [Twitter v2](https://developer.twitter.com/en/products/twitter-api/early-access/guide) user API to retrieve the current user data. You will need a Twitter application and project with access to the v2 API to make use of these scripts.

## License

Copyright 2020 Andy Piper

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
