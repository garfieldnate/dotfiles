 # Nathan's dotfiles

![Screenshot of my shell prompt](https://i.imgur.com/EkEtphC.png)

## Installation

**Warning:** These are my personal dotfiles, forked from [Mathias Bynens' dotfiles](https://github.com/mathiasbynens/dotfiles.git). He is much more of a poweruser than I am, and is more likely to update his file often. Please fork from his repo, not mine. Do not simply download and run the contents of these repositories; review the contents first, editing or (more likely) deleting lines for your use. Then run the contents.

### Steps for Setting Up a New Computer

1. Install [Homebrew](https://brew.sh)
2. `brew install git`
3. `git clone https://github.com/garfieldnate/dotfiles.git && cd dotfiles && source bootstrap.sh`
4. (Mac) `./brew.sh`
5. `./install_tools.sh`
6. Install/setup pCloud and Audacity manually
7. (Mac) `./casks.sh`
8. (Mac) `./.macos`
9. Copy ssh keys, then do `chmod 400 ~/.ssh/id_rsa`
10. Check that multi-language input works (.macos file doesn't seem to work :(); check that ^F12 switches to previous input method.
11. Check that fonts are readable everywhere
12. Set iTerm2 to use ~/.config/iterm2 for configuration
13. Copy personal files
14. Customize Finder sidebar: @Drafts, workspaces, Dropbox, pCloud, home, Downloads, Recents, Applications.
15. sudo cp crontab.txt /usr/lib/cron/tabs/nglenn (TODO: unite that with cron/ folder)


### Using Git and the bootstrap script

You can clone the repository wherever you want. (I like to keep it in `~/Projects/dotfiles`, with `~/dotfiles` as a symlink.) The bootstrapper script will pull in the latest version and copy the files to your home folder.

```bash
git clone https://github.com/garfieldnate/dotfiles.git && cd dotfiles && source bootstrap.sh
```

To update, `cd` into your local `dotfiles` repository and then:

```bash
source bootstrap.sh
```

Alternatively, to update while avoiding the confirmation prompt:

```bash
set -- -f; source bootstrap.sh
```

### Specify the `$PATH`

If `~/.path` exists, it will be sourced along with the other files, before any feature testing (such as [detecting which version of `ls` is being used](https://github.com/mathiasbynens/dotfiles/blob/aff769fd75225d8f2e481185a71d5e05b76002dc/.aliases#L21-26)) takes place.

Here’s an example `~/.path` file that adds `/usr/local/bin` to the `$PATH`:

```bash
export PATH="/usr/local/bin:$PATH"
```

### Add custom commands without creating a new fork

If `~/.extra` exists, it will be sourced along with the other files. You can use this to add a few custom commands without the need to fork this entire repository, or to add commands you don’t want to commit to a public repository.
