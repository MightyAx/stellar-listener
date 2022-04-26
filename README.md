# How to run on boot
Edit the service files for your user / install location
```
sudo cp services/*.service /etc/systemd/system
sudo systemctl enable sonicpi.service
sudo systemctl enable stellar.service

```
# Usefull Commands
```
sudo systemctl daemon-reload
systemctl status sonicpi.service
journalctl -xe
```