# CarlBotTranslateV2
This is a helper API that generates images with [Google Translate](https://translate.google.com) translations.

This is a faster but more basic version of the original: https://github.com/imptype/CarlBotTranslate.

For comparison, the old one takes a few seconds to respond, this takes under a second.

## Running

This is a newbie guide to run your own instance, incase mine gets overcrowded.

You can use [Google Cloud Shell](shell.cloud.google.com) if you can't do stuff like installing the CLI.

1. Login to [Google Cloud Shell](shell.cloud.google.com) (requires [Gmail](https://mail.google.com) account).
2. Select Home Workspace (or some other place if you know what you're doing).
3. In terminal, run `git clone https://github.com/imptype/CarlBotTranslateV2` to clone this repo.
4. Run `curl -fsSL https://get.deta.dev/space-cli.sh | sh` to install the [Space CLI](https://deta.space/docs/en/reference/cli).
5. Run `space login` and enter your access token when prompted.
    - Access tokens can be generated from https://deta.space -> Settings (signup/login first).
6. Run `cd CarlBotTranslateV2` to go into the folder in terminal.
    - Make sure you're in this folder, or you might push the wrong files.
7. Run `space new` and enter a name for your app.
8. Run `space push` to build the app in Deta Space.
9. Go to https://deta.space and click on your app to run it.
    - This opens a URL that looks like this `https://{app_name}-1-a1234567.deta.space`.
    - Custom domains are available and custom subdomains are coming in the future.

Then you can access routes with that base url, e.g. `https://{app_name}-1-a1234567.deta.space/translate?sl=en&tl=es&text=hello`.

Also, you can run this anywhere that offers free hosting/serverless functions, not just on Deta.

## Examples

Request | Response
--- | ---
`GET /translate?hl=en&sl=en&tl=es&text=item` | !c
--- | ---
`GET /translate?hl=en&sl=en&tl=es&text=item` | b
--- | ---
`GET /translate?hl=en&sl=en&tl=es&text=item` | a

## Links
🔗 Source: X

🔗 Github: https://github.com/imptype/CarlBotTranslateV2
