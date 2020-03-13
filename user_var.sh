test -e ${HOME}/.iterm2_shell_integration.zsh && source ${HOME}/.iterm2_shell_integration.zsh

export TWITTER_USER = "andypiper"

# sample for now
iterm2_print_user_vars() {
	iterm2_set_user_var twitterCount $(twurl -j "/labs/2/users/by/username/$TWITTER_USER?user.fields=public_metrics" | jq '.data.public_metrics.followers_count')
}
