#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/KAIROS || exit 1
source venv/bin/activate

case "$1" in
  status|health)
    python main.py "$1"
    ;;
  *)
    echo "Allowed commands: status, health"
    exit 1
    ;;
esac
