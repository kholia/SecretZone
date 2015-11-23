#!/bin/sh

# https://wiki.gentoo.org/wiki/QEMU/Windows_guest
# https://fedoraproject.org/wiki/Windows_Virtio_Drivers#Direct_download
# https://wiki.archlinux.org/index.php/QEMU#Enabling_KVM
# https://fedoraproject.org/wiki/How_to_use_qemu
#
# The default user-mode networking allows the guest to access the host OS at
# the IP address 10.0.2.2.
#
# From the QEMU monitor console, you can load / change ISO images.
# (qemu) info block
# ...
# (qemu) change ide1-cd0 win-virtio-drivers.iso


# exec qemu-system-x86_64 \
exec ~/QEMU/bin/qemu-system-x86_64 \
    -enable-kvm -localtime \
    -cpu host \
    -drive file=WindowsVM.img,if=virtio \
    -m 1600M -monitor stdio \
    -device usb-ehci \
    -name Windows \
    -netdev tap,id=net0,ifname=tap0,script=no,downscript=no -device rtl8139,netdev=net0,id=net0,mac=52:54:00:c9:18:27 \
    -usbdevice 'disk:format=qcow2:vid=04E8:pid=61B6:manufacturer=Samsung:product=Samsung M3 Portable:serial=324324:hdd.img' \
    "$@"
    # -usb \
    # -usbdevice disk:format=raw:usb.img \
    # -net nic,model=rtl8139 -net user,hostname=oldie \

# ./WindowsVM.sh -boot d -drive file=XP.iso,media=cdrom -drive file=virtio-win-0.1.105.iso,media=cdrom
