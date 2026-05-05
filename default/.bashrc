# ~/.bashrc

# Ha nem interaktív módban futunk, ne csináljon semmit
case $- in
    *i*) ;;
      *) return;;
esac
clear
fastfetch
sleep 2
clear
echo "#########################################################################
#                                                                       #
#     ██████╗ ██╗██╗     ██╗      ██████╗ ███╗   ██╗ █████╗ ███████╗    #
#     ██╔══██╗██║██║     ██║     ██╔═══██╗████╗  ██║██╔══██╗╚════██║    #
#     ██████╔╝██║██║     ██║     ██║   ██║██╔██╗ ██║╚██████║    ██╔╝    #
#     ██╔═══╝ ██║██║     ██║     ██║   ██║██║╚██╗██║ ╚═══██║   ██╔╝     #
#     ██║     ██║███████╗███████╗╚██████╔╝██║ ╚████║ █████╔╝   ██║      #
#     ╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚════╝    ╚═╝      #
#                                                                       #
#########################################################################"
echo "-------------------------------------------------------------------------"
echo "|                                                                       |"
echo "|                         Welcome, user!                                |"
echo "|                           $(date +'%Y.%m.%d')                                  |"
echo "|                                                                       |"
echo "-------------------------------------------------------------------------"
# Történetkezelés (History) beállításai
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000

# Ablakméret frissítése minden parancs után
shopt -s checkwinsize

# Színes terminál támogatás (ha a terminál képes rá)
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# Színes prompt beállítása (Debian stílus)
# user@host:~/mappa$ formátum
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

# Néhány hasznos alias (gyorsparancs)
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias del='find . -maxdepth 1 -type f -delete'
# Bash kiegészítések (auto-complete) betöltése
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
alias q='exit'
alias c='clear'
alias h='history'


export COMMON=$PILLON'/tools/SecLists/Discovery/Web-Content/common.txt'
export PILLON=$HOME'/Pillon_tool'
alias pil='cd $PILLON'

alias update='sudo apt update && sudo apt upgrade -y'
# Universal extract function
extract ()
{
    if [ -f "$1" ] ; then
        case "$1" in
            *.tar.bz2)   tar xvjf "$1"    ;;
            *.tar.gz)    tar xvzf "$1"    ;;
            *.bz2)       bunzip2 "$1"     ;;
            *.rar)       unrar x "$1"     ;;
            *.gz)        gunzip "$1"      ;;
            *.tar)       tar xvf "$1"     ;;
            *.tbz2)      tar xvjf "$1"    ;;
            *.tgz)       tar xvzf "$1"    ;;
            *.zip)       unzip "$1"       ;;
            *.Z)         uncompress "$1"  ;;
            *)           echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}s