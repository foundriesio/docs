get_fioctl () { 
  export fv=$(wget -q -O-  https://api.github.com/repos/foundriesio/fioctl/releases/latest | grep tag_name | sed -E 's/.*"([^"]+)".*/\1/')
  wget -q -O /usr/local/bin/fioctl https://github.com/foundriesio/fioctl/releases/download/${fv}/fioctl-linux-amd64
  chmod +x /usr/local/bin/fioctl
}

get_fioctl

export PS1="\$ "

su -s /bin/sh gavin
