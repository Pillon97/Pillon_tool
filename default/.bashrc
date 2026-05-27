# ~/.bashrc: bash konfiguráció interaktív shellhez
# Kali alapokon, kibővítve

# ──────────────────────────────────────────────────────────
# Ha nem interaktív módban futunk, ne csináljon semmit
# ──────────────────────────────────────────────────────────
case $- in
    *i*) ;;
      *) return;;
esac

# ──────────────────────────────────────────────────────────
# Üdvözlő képernyő (csak interaktív shellnél fut)
# ──────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────
# Történet (History) kezelése
# ──────────────────────────────────────────────────────────
HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000

# Ablakméret frissítése minden parancs után
shopt -s checkwinsize

# ──────────────────────────────────────────────────────────
# Chroot detektálás (promptban való megjelenítéshez)
# ──────────────────────────────────────────────────────────
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# ──────────────────────────────────────────────────────────
# Színes prompt engedélyezése
# ──────────────────────────────────────────────────────────
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        color_prompt=yes
    else
        color_prompt=
    fi
fi

# Kali stílusú kétsoros prompt beállítása
PROMPT_ALTERNATIVE=twoline
NEWLINE_BEFORE_PROMPT=yes

if [ "$color_prompt" = yes ]; then
    VIRTUAL_ENV_DISABLE_PROMPT=1

    prompt_color='\[\033[;32m\]'
    info_color='\[\033[1;34m\]'
    prompt_symbol=㉿
    if [ "$EUID" -eq 0 ]; then # root esetén más színek
        prompt_color='\[\033[;94m\]'
        info_color='\[\033[1;31m\]'
    fi
    case "$PROMPT_ALTERNATIVE" in
        twoline)
            PS1=$prompt_color'┌──${debian_chroot:+($debian_chroot)──}${VIRTUAL_ENV:+(\[\033[0;1m\]$(basename $VIRTUAL_ENV)'$prompt_color')}('$info_color'\u'$prompt_symbol'\h'$prompt_color')-[\[\033[0;1m\]\w'$prompt_color']\n'$prompt_color'└─'$info_color'\$\[\033[0m\] ';;
        oneline)
            PS1='${VIRTUAL_ENV:+($(basename $VIRTUAL_ENV)) }${debian_chroot:+($debian_chroot)}'$info_color'\u@\h\[\033[00m\]:'$prompt_color'\[\033[01m\]\w\[\033[00m\]\$ ';;
    esac
    unset prompt_color
    unset info_color
    unset prompt_symbol
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# Xterm címsor beállítása
case "$TERM" in
xterm*|rxvt*|Eterm|aterm|kterm|gnome*|alacritty)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
esac

# Üres sor a prompt előtt
[ "$NEWLINE_BEFORE_PROMPT" = yes ] && PROMPT_COMMAND="PROMPT_COMMAND=echo"

# ──────────────────────────────────────────────────────────
# Színes ls, grep, less, man
# ──────────────────────────────────────────────────────────
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    export LS_COLORS="$LS_COLORS:ow=30;44:" # olvashatóbb 777-es mappák

    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
    alias diff='diff --color=auto'
    alias ip='ip --color=auto'

    export LESS_TERMCAP_mb=$'\E[1;31m'
    export LESS_TERMCAP_md=$'\E[1;36m'
    export LESS_TERMCAP_me=$'\E[0m'
    export LESS_TERMCAP_so=$'\E[01;33m'
    export LESS_TERMCAP_se=$'\E[0m'
    export LESS_TERMCAP_us=$'\E[1;32m'
    export LESS_TERMCAP_ue=$'\E[0m'
    export MANROFFOPT="-c"
fi

# ──────────────────────────────────────────────────────────
# Aliasok
# ──────────────────────────────────────────────────────────
# Listázás
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Navigáció
alias ..='cd ..'
alias ...='cd ../..'

# Rövid parancsok
alias q='exit'
alias c='clear'
alias h='history'

# Rendszer
alias update='sudo apt update && sudo apt upgrade -y'

# Veszélyes: töröl minden fájlt az aktuális mappából (almappákat nem)
alias delfiles='find . -maxdepth 1 -type f -delete'

# ──────────────────────────────────────────────────────────
# Környezeti változók (Pillon toolkit)
# Fontos: PILLON-t ELŐBB kell exportálni, mert a COMMON rá hivatkozik
# ──────────────────────────────────────────────────────────
export PILLON="$HOME/Pillon_tool"
export COMMON="$PILLON/tools/SecLists/Discovery/Web-Content/common.txt"
alias pil='cd $PILLON'

# ──────────────────────────────────────────────────────────
# extract() — univerzális kicsomagoló függvény
# ──────────────────────────────────────────────────────────
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
}

# ──────────────────────────────────────────────────────────
# Külső alias-fájl betöltése (ha létezik)
# ──────────────────────────────────────────────────────────
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# ──────────────────────────────────────────────────────────
# Bash tab-completion betöltése
# ──────────────────────────────────────────────────────────
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
